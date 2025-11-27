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
LM_STUDIO_API = "http://<VM100_IP>:1234/v1"
CHROMA_DB_PATH = r"C:\GOKU-AI\chroma_db"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# SSH Configuration (for agent mode)
SSH_HOSTS = {
    "vm150": {"host": "<VM150_IP>", "user": "wp1", "port": 22},
    "vm120": {"host": "<VM120_IP>", "user": "truenas", "port": 22},
}

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
```json
{
  "status": "planning|pending|solved|blocked",
  "summary": "Short recap of current progress or need.",
  "directives": [
    {
      "tool": "run_command|read_file|write_file|search_files|list_directory|get_system_info",
      "vm": "<VM150_IP>",
      "path": "/var/www/shenron.lightspeedup.com/script-fixed.js",
      "command": "git pull",
      "content": "<file contents when using write_file>",
      "reason": "Why this action is required",
      "expect": "What evidence will confirm success",
      "timeout": 120
    }
  ],
  "artifacts": [
    {
      "type": "log|file|evidence",
      "path": "/tmp/output.txt",
      "value": "optional inline content or hash",
      "description": "What this artifact proves"
    }
  ]
}
```
- `directives` may contain up to 5 actions per response. Omit unused fields. Every directive MUST include `tool`, `vm`, and either `command` or `path` depending on the tool.
- Use VM IPs already documented (e.g., <VM150_IP> for web server, <VM100_IP> for orchestrator).
- If you have enough information to produce verified results (private keys, proofs), set `"status": "solved"` and describe the artifacts under `"artifacts"`.
- If a previous attempt failed, return `"status": "blocked"` and suggest alternative hypotheses in `"summary"`.
- Always keep your narrative explanation separate from the JSON block so humans can read the plan AND machines can parse the directives.
"""


def query_fighter_parallel(fighter_data: dict, user_query: str, context: str) -> dict:
    """
    Standalone function for parallel execution (ProcessPoolExecutor compatible)
    
    This function is designed to work with ProcessPoolExecutor by being:
    1. A module-level function (not a class method)
    2. Using only picklable arguments
    3. Self-contained with all necessary imports
    
    Args:
        fighter_data: Dict with fighter attributes
        user_query: User's question
        context: RAG context
    
    Returns:
        Dict with fighter response
    """
    import requests
    import time
    
    start_time = time.time()
    
    # Build prompt
    persona_prompt = build_persona_prompt(fighter_data)

    if context:
        prompt = f"""{persona_prompt}

KNOWLEDGE BASE INTEL:
{context}

USER QUESTION:
{user_query}

Provide your expert analysis:"""
    else:
        prompt = f"""{persona_prompt}
USER QUESTION:
{user_query}

Provide your expert analysis:"""
    
    try:
        response = requests.post(
            "http://<VM100_IP>:1234/v1/chat/completions",  # Hardcoded for subprocess compatibility
            json={
                "model": fighter_data['model'],
                "messages": [{"role": "user", "content": prompt}],
                "temperature": fighter_data['temperature'],
                "max_tokens": fighter_data.get('max_tokens', 2048)
            },
            timeout=300
        )
        
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            data = response.json()
            answer = data['choices'][0]['message']['content']
            return {
                "fighter": fighter_data['name'],
                "emoji": fighter_data['emoji'],
                "role": fighter_data['role'],
                "answer": answer,
                "success": True,
                "response_time": elapsed_time
            }
        else:
            return {
                "fighter": fighter_data['name'],
                "emoji": fighter_data['emoji'],
                "role": fighter_data['role'],
                "answer": f"Error: HTTP {response.status_code}",
                "success": False,
                "response_time": elapsed_time
            }
    
    except Exception as e:
        return {
            "fighter": fighter_data['name'],
            "emoji": fighter_data['emoji'],
            "role": fighter_data['role'],
            "answer": f"Error: {str(e)}",
            "success": False,
            "response_time": time.time() - start_time
        }


class ShenronOrchestrator:
    """The Eternal Dragon that grants wishes through AI consensus + TRUE synthesis + Agent mode"""

    def __init__(self):
        """Initialize SHENRON with RAG and SSH capabilities"""
        # Initialize ChromaDB client
        try:
            self.chroma_client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
            self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=EMBEDDING_MODEL
            )
            self.collection = self.chroma_client.get_collection(
                name="knowledge_base",
                embedding_function=self.embedding_function
            )
        except Exception as e:
            self.collection = None

        # Initialize SSH connections (lazy loading)
        self.ssh_connections = {}

    def get_fighter(self, name: str) -> Fighter:
        for fighter in FIGHTERS:
            if fighter.name == name:
                return fighter
        raise ValueError(f"Unknown fighter requested: {name}")

    @staticmethod
    def contains_risk_keywords(text: str) -> Tuple[bool, List[str]]:
        lowered = text.lower()
        matched = sorted({kw for kw in RISK_KEYWORDS if kw in lowered})
        return (len(matched) > 0, matched)

    @staticmethod
    def looks_low_confidence(answer: str) -> Tuple[bool, List[str]]:
        lowered = answer.lower()
        matched = sorted({phrase for phrase in LOW_CONFIDENCE_PHRASES if phrase in lowered})
        return (len(matched) > 0, matched)

    @staticmethod
    def is_long_query(user_query: str) -> bool:
        return len(user_query.strip()) > CRITICAL_LENGTH_THRESHOLD

    def search_knowledge_base(self, query: str, n_results: int = 3) -> str:
        """Search the knowledge base for relevant context."""
        if not self.collection:
            return ""

        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results
            )

            if not results['documents'] or not results['documents'][0]:
                return ""

            context_parts = []
            for i, doc in enumerate(results['documents'][0]):
                source = results['metadatas'][0][i]['source']
                context_parts.append(f"[{source}] {doc}")

            context = "\n\n".join(context_parts)
            return f"**KNOWLEDGE BASE CONTEXT:**\n{context}\n\n"

        except Exception as e:
            return ""

    def query_fighter(self, fighter: Fighter, user_query: str, context: str = "") -> Dict[str, Any]:
        """Query a single DBZ-Warrior."""
        start_time = time.time()

        if context:
            prompt = (
                f"{build_persona_prompt(fighter)}\n"
                f"KNOWLEDGE BASE INTEL:\n{context}\n\n"
                f"USER QUESTION:\n{user_query}\n\n"
                f"Provide your expert analysis:"
            )
        else:
            prompt = (
                f"{build_persona_prompt(fighter)}\n"
                f"USER QUESTION:\n{user_query}\n\n"
                f"Provide your expert analysis:"
            )

        try:
            response = requests.post(
                f"{LM_STUDIO_API}/chat/completions",
                json={
                    "model": fighter.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": fighter.temperature,
                    "max_tokens": fighter.max_tokens
                },
                timeout=900
            )

            elapsed_time = time.time() - start_time

            if response.status_code == 200:
                data = response.json()
                answer = data['choices'][0]['message']['content']

                return {
                    "fighter": fighter.name,
                    "emoji": fighter.emoji,
                    "role": fighter.role,
                    "answer": answer,
                    "success": True,
                    "response_time": elapsed_time,
                    "temperature": fighter.temperature,
                    "model": fighter.model
                }
            else:
                return {
                    "fighter": fighter.name,
                    "emoji": fighter.emoji,
                    "role": fighter.role,
                    "answer": f"Error: HTTP {response.status_code}",
                    "success": False,
                    "response_time": elapsed_time
                }

        except Exception as e:
            return {
                "fighter": fighter.name,
                "emoji": fighter.emoji,
                "role": fighter.role,
                "answer": f"Error: {str(e)}",
                "success": False,
                "response_time": time.time() - start_time
            }

    def synthesize_responses(self, user_query: str, responses: List[Dict[str, Any]]) -> str:
        """
        NEW v4.0: TRUE SYNTHESIS - 7th AI call to create unified response
        Uses GOKU as synthesis engine
        """
        successful = [r for r in responses if r["success"]]
        
        if len(successful) == 0:
            return "The council was unable to provide guidance on this matter."

        # Build synthesis prompt
        synthesis_prompt = f"""You are SHENRON, the Eternal Dragon and orchestrator of the AI Council.

USER'S QUESTION:
{user_query}

The 6 DBZ-Warriors have provided their insights:

"""
        
        for resp in successful:
            synthesis_prompt += f"---\n{resp['emoji']} {resp['fighter']} ({resp['role']}):\n{resp['answer']}\n\n"

        synthesis_prompt += """---

YOUR TASK:
Read ALL warrior responses above and synthesize them into ONE unified, coherent answer that:
1. Combines the best insights from each warrior
2. Eliminates redundancy
3. Resolves any contradictions
4. Provides actionable recommendations
5. Speaks with SHENRON's authoritative voice

Do NOT just repeat one warrior's response. Create a TRUE synthesis.

SHENRON's Unified Response:"""

        # Call GOKU for synthesis
        try:
            response = requests.post(
                f"{LM_STUDIO_API}/chat/completions",
                json={
                    "model": "deepseek-coder-v2-lite-instruct",  # GOKU's model
                    "messages": [{"role": "user", "content": synthesis_prompt}],
                    "temperature": 0.6,  # Balanced for synthesis
                    "max_tokens": 4096  # Allow longer synthesis
                },
                timeout=900
            )

            if response.status_code == 200:
                data = response.json()
                synthesized = data['choices'][0]['message']['content']
                return synthesized
            else:
                return self._fallback_synthesis(successful)

        except Exception as e:
            return self._fallback_synthesis(successful)

    def _fallback_synthesis(self, responses: List[Dict[str, Any]]) -> str:
        """Fallback synthesis if 7th call fails"""
        if len(responses) == 1:
            return responses[0]['answer']
        
        # Simple concatenation with headers
        parts = []
        for r in responses:
            parts.append(f"**{r['emoji']} {r['fighter']}**: {r['answer'][:500]}...")
        
        return "The council provides these insights:\n\n" + "\n\n".join(parts)

    def consult_council(self, user_query: str, use_rag: bool = True,
                        cancel_checker: Optional[Callable[[], bool]] = None) -> Dict[str, Any]:
        """
        Consult all 6 DBZ-Warriors in PARALLEL using ProcessPoolExecutor.
        
        v4.1 PERFORMANCE FIX:
        - Changed from ThreadPoolExecutor to ProcessPoolExecutor
        - TRUE parallel execution (6 separate Python processes)
        - Bypasses Python GIL (Global Interpreter Lock)
        - Expected: 4-6x faster (60s → 10-30s)
        """
        def cancelled() -> bool:
            return bool(cancel_checker and cancel_checker())

        if cancelled():
            raise WishCancelled()

        # Step 1: RAG Search
        context = ""
        if use_rag:
            context = self.search_knowledge_base(user_query, n_results=3)

        # Step 2: Prepare fighter data for parallel execution
        # Convert Fighter objects to dicts (picklable)
        fighter_data_list = [
            {
                "name": f.name,
                "emoji": f.emoji,
                "role": f.role,
                "model": f.model,
                "temperature": f.temperature,
                "persona": f.persona,
                "max_tokens": f.max_tokens,
            }
            for f in FIGHTERS
        ]

        # Step 3: Query all warriors in parallel (TRUE parallelism!)
        responses = []

        executor = ProcessPoolExecutor(max_workers=6)
        futures = {
            executor.submit(query_fighter_parallel, fighter_data, user_query, context): fighter_data
            for fighter_data in fighter_data_list
        }

        try:
            for future in as_completed(futures):
                if cancelled():
                    for f in futures:
                        f.cancel()
                    executor.shutdown(wait=False, cancel_futures=True)
                    raise WishCancelled()

                fighter_data = futures[future]
                try:
                    result = future.result()
                    responses.append(result)
                except Exception as e:
                    responses.append({
                        "fighter": fighter_data['name'],
                        "emoji": fighter_data['emoji'],
                        "role": fighter_data['role'],
                        "answer": f"Error: {str(e)}",
                        "success": False,
                        "response_time": 0
                    })
        finally:
            try:
                executor.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                executor.shutdown(wait=False)

        # Sort by original order
        response_order = {f.name: i for i, f in enumerate(FIGHTERS)}
        responses.sort(key=lambda r: response_order.get(r['fighter'], 999))

        return {
            "query": user_query,
            "rag_context_used": bool(context),
            "responses": responses,
            "success_count": sum(1 for r in responses if r["success"]),
            "total_fighters": len(FIGHTERS)
        }

    def consult_subset(self, user_query: str, fighters: List[Fighter], context: str,
                       cancel_checker: Optional[Callable[[], bool]] = None) -> List[Dict[str, Any]]:
        if not fighters:
            return []

        if cancel_checker and cancel_checker():
            raise WishCancelled()

        fighter_data_list = [
            {
                "name": f.name,
                "emoji": f.emoji,
                "role": f.role,
                "model": f.model,
                "temperature": f.temperature,
                "persona": f.persona,
                "max_tokens": f.max_tokens,
            }
            for f in fighters
        ]

        responses = []
        executor = ProcessPoolExecutor(max_workers=len(fighter_data_list))
        futures = {
            executor.submit(query_fighter_parallel, fighter_data, user_query, context): fighter_data
            for fighter_data in fighter_data_list
        }

        try:
            for future in as_completed(futures):
                if cancel_checker and cancel_checker():
                    for f in futures:
                        f.cancel()
                    executor.shutdown(wait=False, cancel_futures=True)
                    raise WishCancelled()

                fighter_data = futures[future]
                try:
                    responses.append(future.result())
                except Exception as exc:
                    responses.append({
                        "fighter": fighter_data['name'],
                        "emoji": fighter_data['emoji'],
                        "role": fighter_data['role'],
                        "answer": f"Error: {exc}",
                        "success": False,
                        "response_time": 0
                    })
        finally:
            try:
                executor.shutdown(wait=False, cancel_futures=True)
            except TypeError:
                executor.shutdown(wait=False)

        response_order = {f.name: i for i, f in enumerate(fighters)}
        responses.sort(key=lambda r: response_order.get(r['fighter'], 999))
        return responses


    def cascading_consult(self, user_query: str, use_rag: bool = True,
                          cancel_checker: Optional[Callable[[], bool]] = None) -> Dict[str, Any]:
        context = ""
        if use_rag:
            context = self.search_knowledge_base(user_query, n_results=3)

        validation_reasons: List[str] = []

        if cancel_checker and cancel_checker():
            raise WishCancelled()

        goku = self.query_fighter(self.get_fighter("GOKU"), user_query, context)

        if not goku["success"]:
            validation_reasons.append("Primary warrior failed to answer.")

        risk_hit, risks = self.contains_risk_keywords(user_query)
        if risk_hit:
            validation_reasons.append(f"Risk keywords detected: {', '.join(risks)}")

        if self.is_long_query(user_query):
            validation_reasons.append("Query length exceeds safe threshold.")

        low_confidence = []
        if goku["success"]:
            low_confidence_flag, low_confidence = self.looks_low_confidence(goku["answer"])
            if low_confidence_flag:
                validation_reasons.append(f"Low confidence language: {', '.join(low_confidence)}")

        requires_validation = len(validation_reasons) > 0

        responses = [goku]
        consulted = ["GOKU"]

        if requires_validation:
            secondary_fighters = [f for f in FIGHTERS if f.name != "GOKU"]
            secondary_responses = self.consult_subset(user_query, secondary_fighters, context, cancel_checker=cancel_checker)
            responses.extend(secondary_responses)
            consulted.extend([resp["fighter"] for resp in secondary_responses])

        response_order = {f.name: i for i, f in enumerate(FIGHTERS)}
        responses.sort(key=lambda r: response_order.get(r['fighter'], 999))

        return {
            "responses": responses,
            "validation_required": requires_validation,
            "validation_reasons": validation_reasons,
            "consulted_fighters": consulted,
            "rag_context_used": bool(context)
        }


    def analyze_consensus(self, responses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze responses to detect consensus."""
        successful_responses = [r for r in responses if r["success"]]

        if not successful_responses:
            return {
                "type": "failure",
                "message": "No warriors were able to respond.",
                "consensus_level": 0
            }

        success_rate = len(successful_responses) / len(responses)

        if success_rate == 1.0:
            consensus_type = "unanimous"
            message = f"All {len(responses)} warriors agree."
        elif success_rate >= 0.75:
            consensus_type = "strong"
            message = f"{len(successful_responses)}/{len(responses)} warriors provided answers."
        elif success_rate >= 0.5:
            consensus_type = "majority"
            message = f"{len(successful_responses)}/{len(responses)} warriors responded."
        else:
            consensus_type = "weak"
            message = f"Only {len(successful_responses)}/{len(responses)} warriors responded."

        return {
            "type": consensus_type,
            "message": message,
            "consensus_level": success_rate,
            "successful_fighters": [r['fighter'] for r in successful_responses],
            "failed_fighters": [r['fighter'] for r in responses if not r['success']]
        }

    def grant_wish(self, user_query: str, use_rag: bool = True,
                   cancel_checker: Optional[Callable[[], bool]] = None) -> Dict[str, Any]:
        """
        Main entry point: Grant the user's wish
        v4.0: Now with TRUE synthesis!
        """
        start_time = time.time()

        cascade_result = self.cascading_consult(user_query, use_rag=use_rag, cancel_checker=cancel_checker)
        responses = cascade_result["responses"]

        consensus = self.analyze_consensus(responses)

        if cascade_result["validation_required"] and responses:
            synthesized_answer = self.synthesize_responses(user_query, responses)
            synthesis_method = "true_ai"
        else:
            synthesized_answer = responses[0]["answer"] if responses else "No response from GOKU."
            synthesis_method = "single_pass"
 
        elapsed_time = time.time() - start_time

        result = {
            "query": user_query,
            "rag_used": cascade_result["rag_context_used"],
            "consensus": consensus,
            "synthesized_answer": synthesized_answer,
            "warrior_responses": responses,
            "total_time": elapsed_time,
            "wish_granted": consensus["consensus_level"] > 0,
            "synthesis_method": synthesis_method,
            "validation": {
                "required": cascade_result["validation_required"],
                "reasons": cascade_result["validation_reasons"],
                "consulted_fighters": cascade_result["consulted_fighters"]
            }
        }

        return self.post_process_result(result)

    # ========================================================================
    # AGENT MODE - SSH Command Execution
    # ========================================================================

    def classify_command(self, command: str) -> Tuple[str, str]:
        """
        Classify command safety level
        Returns: (classification, reason)
        """
        # Check dangerous commands first
        for pattern in DANGEROUS_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                return ("dangerous", f"Matches dangerous pattern: {pattern}")

        # Check moderate commands
        for pattern in MODERATE_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                return ("moderate", f"Matches moderate pattern: {pattern}")

        # Check safe commands
        for pattern in SAFE_COMMANDS:
            if re.search(pattern, command, re.IGNORECASE):
                return ("safe", f"Matches safe pattern: {pattern}")

        # Unknown command - require approval
        return ("unknown", "Command not in whitelist")

    def execute_command(self, host_key: str, command: str, require_approval: bool = True) -> Dict[str, Any]:
        """
        Execute SSH command on remote host
        
        Args:
            host_key: Key from SSH_HOSTS dict (e.g., "vm150")
            command: Command to execute
            require_approval: If True, return command for approval instead of executing
        
        Returns:
            Dict with execution results
        """
        # Classify command
        classification, reason = self.classify_command(command)

        # Check if dangerous
        if classification == "dangerous":
            return {
                "success": False,
                "error": "DANGEROUS COMMAND BLOCKED",
                "reason": reason,
                "command": command,
                "executed": False
            }

        # Check if approval needed
        if classification in ["moderate", "unknown"] and require_approval:
            return {
                "success": False,
                "approval_required": True,
                "classification": classification,
                "reason": reason,
                "command": command,
                "host": host_key,
                "message": f"Command requires approval: {command}"
            }

        # Safe command - execute
        if host_key not in SSH_HOSTS:
            return {
                "success": False,
                "error": f"Unknown host: {host_key}",
                "executed": False
            }

        host_config = SSH_HOSTS[host_key]

        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            ssh.connect(
                hostname=host_config["host"],
                username=host_config["user"],
                port=host_config["port"],
                timeout=30
            )

            stdin, stdout, stderr = ssh.exec_command(command, timeout=30)
            
            exit_code = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            ssh.close()

            return {
                "success": exit_code == 0,
                "exit_code": exit_code,
                "output": output,
                "error": error if error else None,
                "command": command,
                "host": host_key,
                "classification": classification,
                "executed": True
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command": command,
                "host": host_key,
                "executed": False
            }

    # ---------------------------------------------------------------------
    # Result post-processing & directive analysis
    # ---------------------------------------------------------------------

    def _extract_json_directives(self, text: str) -> List[Dict[str, Any]]:
        """Extract JSON directives embedded in a model response."""
        if not text:
            return []

        directives: List[Dict[str, Any]] = []

        try:
            matches = re.findall(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL | re.IGNORECASE)
        except re.error:
            matches = []

        for block in matches:
            try:
                directives.append(json.loads(block))
            except json.JSONDecodeError:
                continue

        return directives

    def post_process_result(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Inspect warrior outputs for tool directives, capture artifacts,
        and flag unresolved actions that require MCP follow-up.
        """
        artifacts: List[Dict[str, Any]] = []
        pending_actions: List[Dict[str, Any]] = []
        collected_directives: List[Dict[str, Any]] = []

        def collect_from_source(source: str, payload: str):
            directives = self._extract_json_directives(payload)
            for directive in directives:
                collected_directives.append({"source": source, "directive": directive})

        # Gather directives from each warrior response
        for response in result.get("warrior_responses", []):
            collect_from_source(response.get("fighter", "unknown"), response.get("answer", ""))

        # Also scan the synthesized answer for directives
        collect_from_source("SYNTHESIS", result.get("synthesized_answer", ""))

        for item in collected_directives:
            directive = item["directive"]
            source = item["source"]
            status = str(directive.get("status", "")).lower()
            private_key = directive.get("private_key")
            artifacts_payload = directive.get("artifacts")
            directive_list = directive.get("directives") or directive.get("actions")

            if private_key:
                placeholder = "your_private_key" in str(private_key).lower()
                if not placeholder:
                    artifacts.append({
                        "source": source,
                        "type": "private_key",
                        "value": private_key,
                        "verification": directive.get("verification_artifacts", [])
                    })
                    if status == "solved":
                        continue

            if artifacts_payload:
                entries = artifacts_payload if isinstance(artifacts_payload, list) else [artifacts_payload]
                for entry in entries:
                    if isinstance(entry, dict):
                        artifacts.append({
                            "source": source,
                            "type": entry.get("type", "artifact"),
                            "value": entry.get("value") or entry.get("path") or entry,
                            "details": entry
                        })
                    else:
                        artifacts.append({
                            "source": source,
                            "type": "artifact",
                            "value": entry,
                            "details": {"value": entry}
                        })
                if status == "solved":
                    continue

            if directive_list and isinstance(directive_list, list):
                for action in directive_list:
                    summary = (
                        action.get("summary")
                        or action.get("reason")
                        or action.get("description")
                        or f"Execute {action.get('tool', 'action')}"
                    )
                    pending_actions.append({
                        "source": source,
                        "status": action.get("status") or status or "pending",
                        "summary": summary,
                        "directive": action,
                        "root_directive": directive
                    })
                continue

            pending_actions.append({
                "source": source,
                "status": directive.get("status") or status or "pending",
                "summary": directive.get("summary")
                           or directive.get("description")
                           or directive.get("message")
                           or directive.get("status")
                           or "Follow-up action required",
                "directive": directive
            })

        result["artifacts"] = artifacts
        result["pending_actions"] = pending_actions
        result["tool_directives"] = collected_directives

        # Override wish_granted if artifacts are missing
        if artifacts:
            result["wish_granted"] = True
        elif pending_actions:
            result["wish_granted"] = False
        else:
            # No artifacts and no actionable directives – treat as unresolved
            result["wish_granted"] = False

        return result



