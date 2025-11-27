<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/usr/bin/env python3
"""
SHENRON v4.0 Orchestrator - Importable Module
For use by Flask API server
"""

import requests
import json
import time
from typing import List, Dict, Any, Tuple, Optional, Callable
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor, as_completed
import chromadb
from chromadb.utils import embedding_functions
import paramiko
import re
import os
import logging

# Setup basic logging for critical errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

RISK_KEYWORDS = {
    "delete", "remove", "rm", "drop", "destroy",
    "invest", "trade", "buy", "sell", "money",
    "deploy", "restart", "reboot", "shutdown",
    "password", "key", "secret", "token",
    "critical", "production", "live", "ssh", "sudo"
}

CRITICAL_LENGTH_THRESHOLD = 220  # characters
LOW_CONFIDENCE_PHRASES = {
    "i'm not sure", "cannot", "can't", "unsure",
    "might not", "uncertain", "possibly", "maybe", "no guarantee",
    "would need more information", "not enough information",
    "should consult", "recommend checking", "double-check"
}

# Configuration
LM_STUDIO_API = os.environ.get("LM_STUDIO_API", "http://<VM100_IP>:1234/v1")
CHROMA_DB_PATH = os.environ.get("CHROMA_DB_PATH", r"C:\GOKU-AI\chroma_db")
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# SSH Configuration (for agent mode)
def get_ssh_hosts() -> Dict[str, Dict[str, Any]]:
    """
    Retrieve SSH host configurations from environment or secure config.
    WARNING: Storing credentials in code is insecure. Use environment variables or vault in production!
    """
    # Example: You can load from ENV or a secure vault/service.
    # For now, fallback to the previous hardcoded values if not set.
    hosts = {
        "vm150": {
            "host": os.environ.get("SSH_VM150_HOST", "<VM150_IP>"),
            "user": os.environ.get("SSH_VM150_USER", "wp1"),
            "port": int(os.environ.get("SSH_VM150_PORT", "22")),
        },
        "vm120": {
            "host": os.environ.get("SSH_VM120_HOST", "<VM120_IP>"),
            "user": os.environ.get("SSH_VM120_USER", "truenas"),
            "port": int(os.environ.get("SSH_VM120_PORT", "22")),
        },
    }
    return hosts

@dataclass
class Fighter:
    """DBZ-Warrior configuration"""
    name: str
    emoji: str
    role: str
    model: str
    temperature: float
    persona: str
    context_length: int = 32768
    max_tokens: int = 2048

# Custom exception used to signal an external cancellation request
class WishCancelled(Exception):
    pass

# The 6 DBZ-Warriors
FIGHTERS = [
    Fighter(
        "GOKU",
        "🥋",
        "Adaptive Warrior & Growth Catalyst",
        "Goku-deepseek-coder-v2-lite-instruct",
        0.7,
        persona="Energetic Saiyan hero who speaks with upbeat encouragement, references training and growth, keeps things simple and motivational while still giving concrete guidance."
    ),
    Fighter(
        "VEGETA",
        "👑",
        "Technical Authority",
        "Vegeta-llama-3.2-3b-instruct",
        0.3,
        persona="Proud Saiyan prince with sharp sarcasm; delivers precise technical insights, battle metaphors, and confident critiques without losing professionalism."
    ),
    Fighter(
        "PICCOLO",
        "🧠",
        "Strategic Sage",
        "Piccolo-qwen2.5-coder-7b-instruct",
        0.5,
        persona="Calm Namekian tactician who analyzes situations methodically, balances offense/defense, and offers stepwise strategies with disciplined tone."
    ),
    Fighter(
        "GOHAN",
        "⚠️",
        "Risk Sentinel",
        "Gohan-mistral-7b-instruct-v0.3",
        0.4,
        persona="Thoughtful scholar-warrior focused on risk, safeguards, and preparedness; careful tone, highlights edge cases and mitigation paths."
    ),
    Fighter(
        "KRILLIN",
        "🔧",
        "Practical Engineer",
        "Krillin-phi-3-mini-128k-instruct",
        0.6,
        persona="Down-to-earth human engineer with hands-on tips, light humor, and actionable checklists aimed at quick wins and reliability."
    ),
    Fighter(
        "FRIEZA",
        "😈",
        "Chaos Tyrant",
        "Frieza-phi-3-mini-128k-instruct",
        0.9,
        persona="Elegant villain who relishes controlled chaos; offers cunning insights, hints at domination, yet remains begrudgingly helpful."
    ),
]

# Safety Guardrails for Agent Mode
SAFE_COMMANDS = [
    r"^df\s+(-h)?",  # Disk space
    r"^uptime",  # System uptime
    r"^free\s+(-h)?",  # Memory usage
    r"^systemctl\s+status",  # Service status
    r"^ls\s+",  # List files
    r"^cat\s+",  # View files (read-only)
    r"^head\s+",  # View file start
    r"^tail\s+",  # View file end
    r"^ps\s+",  # Process list
    r"^netstat",  # Network stats
]

MODERATE_COMMANDS = [
    r"^systemctl\s+(restart|reload)",  # Service restart
    r"^apt\s+update",  # Package update
    r"^apt\s+upgrade",  # Package upgrade
    r"^mkdir\s+",  # Create directory
    r"^touch\s+",  # Create file
]

DANGEROUS_COMMANDS = [
    r"rm\s+-rf",  # Recursive force delete
    r"^dd\s+",  # Disk destruction
    r"^shutdown",  # System shutdown
    r"^reboot",  # System reboot
    r"^halt",  # System halt
    r"^mkfs",  # Format filesystem
    r"chmod\s+777",  # Insecure permissions
]

# ============================================================================
# PARALLEL EXECUTION FUNCTION (ProcessPoolExecutor compatible)
# ============================================================================

def build_persona_prompt(fighter_source) -> str:
    """Create persona instructions for a fighter."""
    if isinstance(fighter_source, dict):
        name = fighter_source.get("name")
        emoji = fighter_source.get("emoji")
        role = fighter_source.get("role")
        persona = fighter_source.get("persona", "")
    else:
        name = getattr(fighter_source, "name")
        emoji = getattr(fighter_source, "emoji")
        role = getattr(fighter_source, "role")
        persona = getattr(fighter_source, "persona", "")

    return f"""You are {name} {emoji}, {role}.

Personality Profile:
{persona}

Communication Guidelines:
- Stay fully in-character with Dragon Ball tone and references.
- Speak in first person, weaving brief character flavor before diving into advice.
- Deliver concise, actionable guidance with clear steps or bullet lists when helpful.
- Avoid generic AI disclaimers; focus on decisive insight tailored to the user's question.
- Keep the main response under 350 words while remaining informative and practical.

MCP Directive Protocol:
- Whenever you need to run automation (read/write files, run commands, inspect repos, etc.), emit a JSON directive inside a fenced code block exactly like: