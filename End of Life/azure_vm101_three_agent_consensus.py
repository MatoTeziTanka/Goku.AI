#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Three-Agent Consensus Builder for VM101 v1.0.0
==============================================

Uses Azure GPT-4.1 to build consensus between:
1. Zencoder Code Agent (code creator)
2. Zencoder Review Agent (code reviewer)
3. Azure GPT-4.1 (final validator)

Creates an agreed-upon v1.0.0 that all agents approve.

Author: Cursor AI
Date: November 24, 2025
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

try:
    from openai import AzureOpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: pip install openai")
    sys.exit(1)

# Configuration
GITHUB_ROOT = Path(__file__).parent
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")

# Load from config if not in environment
if not AZURE_ENDPOINT or not AZURE_API_KEY:
    config_file = GITHUB_ROOT / "api_keys_config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                azure_config = config.get("azure", {})
                if not AZURE_ENDPOINT:
                    endpoint = azure_config.get("endpoint", "")
                    if endpoint and "cognitiveservices.azure.com" in endpoint:
                        endpoint = endpoint.replace("cognitiveservices.azure.com", "openai.azure.com")
                    AZURE_ENDPOINT = f"https://{endpoint}/" if endpoint and not endpoint.startswith("http") else endpoint
                if not AZURE_API_KEY:
                    AZURE_API_KEY = azure_config.get("api_key", "")
                if not DEPLOYMENT_NAME or DEPLOYMENT_NAME == "gpt-4":
                    DEPLOYMENT_NAME = azure_config.get("model", "gpt-4.1")
        except Exception:
            pass

# File paths
DEPLOYMENT_PACKAGE = GITHUB_ROOT / "VM101-DEPLOYMENT-PACKAGE-v1.0.0"
CONSENSUS_PROCESS = GITHUB_ROOT / "VM101-v1.0.0-THREE-AGENT-CONSENSUS-PROCESS.md"
OUTPUT_DIR = GITHUB_ROOT / "azure_reviews"
OUTPUT_DIR.mkdir(exist_ok=True)

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_file_content(file_path: Path) -> Optional[str]:
    """Read file content."""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None


def initialize_azure_client() -> Optional[AzureOpenAI]:
    """Initialize Azure OpenAI client."""
    if not AZURE_ENDPOINT or not AZURE_API_KEY:
        logger.error("Azure OpenAI configuration missing!")
        return None
    
    try:
        client = AzureOpenAI(
            api_key=AZURE_API_KEY,
            api_version=AZURE_API_VERSION,
            azure_endpoint=AZURE_ENDPOINT
        )
        logger.info(f"✅ Azure OpenAI client initialized (Deployment: {DEPLOYMENT_NAME})")
        return client
    except Exception as e:
        logger.error(f"❌ Failed to initialize Azure OpenAI: {e}")
        return None


def create_consensus_prompt(code_agent_fixes: str, review_agent_validation: str, 
                           current_issues: List[Dict]) -> str:
    """Create consensus-building prompt."""
    
    issues_list = "\n".join([
        f"- {issue['issue']} (Severity: {issue['severity']})"
        for issue in current_issues
    ])
    
    prompt = f"""# Three-Agent Consensus Building for VM101 v1.0.0

You are Azure GPT-4.1, the final validator and consensus builder.

## YOUR ROLE

Build consensus between 3 AI agents:
1. **Zencoder Code Agent** - Created fixes for v1.0.0 issues
2. **Zencoder Review Agent** - Validated the fixes
3. **You (Azure GPT-4.1)** - Final validator and consensus builder

## CURRENT SITUATION

**Issues Identified:**
{issues_list}

**Code Agent's Fixes:**
{code_agent_fixes[:5000] if code_agent_fixes else "Not yet provided"}

**Review Agent's Validation:**
{review_agent_validation[:5000] if review_agent_validation else "Not yet provided"}

## YOUR TASK

1. **Review Code Agent's Fixes:**
   - Are the fixes correct?
   - Do they address all issues?
   - Is code quality acceptable?

2. **Review Review Agent's Validation:**
   - Is the validation accurate?
   - Are concerns valid?
   - Is the assessment fair?

3. **Build Consensus:**
   - What do all 3 agents agree on?
   - What are the disagreements?
   - How to resolve disagreements?

4. **Final v1.0.0 Approval:**
   - Can we approve v1.0.0?
   - What conditions must be met?
   - What's the final recommendation?

## CONSENSUS CRITERIA

For v1.0.0 to be approved, ALL 3 agents must:
- ✅ AGREE or STRONGLY AGREE on code quality
- ✅ AGREE on security improvements
- ✅ AGREE on production readiness
- ❌ NO CRITICAL issues remaining
- ✅ Code quality score ≥ 95/100

## OUTPUT FORMAT

Provide your analysis in JSON:

```json
{{
    "consensus_metadata": {{
        "reviewer": "Azure GPT-4.1",
        "date": "{datetime.now().isoformat()}",
        "agents_involved": ["code_agent", "review_agent", "gpt41"]
    }},
    "code_agent_assessment": {{
        "fixes_quality": "EXCELLENT|GOOD|FAIR|POOR",
        "fixes_complete": true|false,
        "issues_addressed": ["list"],
        "remaining_issues": ["list"],
        "agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE"
    }},
    "review_agent_assessment": {{
        "validation_accurate": true|false,
        "concerns_valid": true|false,
        "assessment_fair": true|false,
        "agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE"
    }},
    "consensus_analysis": {{
        "points_of_agreement": ["list"],
        "points_of_disagreement": ["list"],
        "resolution_strategy": "how to resolve disagreements",
        "consensus_score": 0.0-1.0
    }},
    "final_recommendation": {{
        "v1_0_0_approved": true|false,
        "conditions": ["list of conditions"],
        "code_quality_score": 0-100,
        "production_ready": true|false,
        "recommendation": "APPROVE|APPROVE_WITH_CONDITIONS|REJECT",
        "reasoning": "detailed explanation"
    }},
    "next_steps": [
        "action items for final v1.0.0"
    ]
}}
```

Provide your comprehensive consensus analysis now.
"""
    return prompt


def main():
    """Main consensus building function."""
    logger.info("=" * 80)
    logger.info("Three-Agent Consensus Builder for VM101 v1.0.0")
    logger.info("=" * 80)
    
    # Initialize Azure client
    client = initialize_azure_client()
    if not client:
        return 1
    
    # Read consensus process document
    process_doc = read_file_content(CONSENSUS_PROCESS)
    
    # Current issues (from Azure review)
    current_issues = [
        {
            "issue": "Task 1.3 PowerShell syntax error",
            "severity": "HIGH",
            "fix_needed": "Use backtick ` instead of backslash \\"
        },
        {
            "issue": "Task 1.2 username hardcoding",
            "severity": "MEDIUM",
            "fix_needed": "Parameterize usernames via config file"
        },
        {
            "issue": "Task 1.2 verification logic",
            "severity": "MEDIUM",
            "fix_needed": "Improve verification to handle SSH errors"
        }
    ]
    
    # For now, we'll create a prompt that asks GPT-4.1 to:
    # 1. Review what needs to be fixed
    # 2. Provide instructions for Code Agent
    # 3. Provide validation criteria for Review Agent
    # 4. Build consensus on final v1.0.0
    
    logger.info("\n📝 Creating consensus prompt...")
    
    # This will be populated when Code Agent and Review Agent provide their inputs
    code_agent_fixes = "Code Agent fixes will be provided here"
    review_agent_validation = "Review Agent validation will be provided here"
    
    prompt = create_consensus_prompt(code_agent_fixes, review_agent_validation, current_issues)
    
    logger.info("\n🤖 Calling Azure GPT-4.1 for consensus...")
    
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a consensus builder and final validator. Your role is to build agreement between multiple AI agents and ensure quality standards are met."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=8000
        )
        
        content = response.choices[0].message.content
        logger.info(f"✅ Received {len(content)} chars from Azure OpenAI")
        
        # Save response
        output_file = OUTPUT_DIR / f"three_agent_consensus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Try to parse as JSON
        try:
            consensus = json.loads(content)
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(consensus, f, indent=2, ensure_ascii=False)
            logger.info(f"✅ Consensus saved to {output_file}")
        except json.JSONDecodeError:
            # Save as text if not JSON
            output_file = output_file.with_suffix('.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Consensus saved to {output_file}")
        
        print("\n" + "=" * 80)
        print("CONSENSUS BUILDING COMPLETE")
        print("=" * 80)
        print(f"\n📄 Output saved to: {output_file}")
        print("\nNext steps:")
        print("1. Code Agent should fix the issues identified")
        print("2. Review Agent should validate the fixes")
        print("3. Run this script again with their inputs to build final consensus")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error calling Azure OpenAI: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())



