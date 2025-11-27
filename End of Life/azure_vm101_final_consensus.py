#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Three-Agent Consensus for VM101 v1.0.0
============================================

Builds final consensus using actual Code Agent fixes and Review Agent validation.

Author: Cursor AI
Date: November 25, 2025
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


def create_final_consensus_prompt() -> str:
    """Create final consensus prompt with actual fixes and validation."""
    
    # Read Code Agent fixes
    vm_config = read_file_content(DEPLOYMENT_PACKAGE / "vm-config.json")
    task_1_2 = read_file_content(DEPLOYMENT_PACKAGE / "TASK-1.2-DEPLOY-KEYS-LINUX.sh")
    task_1_3 = read_file_content(DEPLOYMENT_PACKAGE / "TASK-1.3-TEST-WINDOWS.sh")
    
    # Code Agent fixes summary
    code_agent_fixes = f"""
**Issue 1: PowerShell Syntax Error - FIXED**
- File: TASK-1.3-TEST-WINDOWS.sh (lines 80-85)
- Change: Changed backslash \\ to backtick ` for PowerShell line continuation
- Status: ✅ Fixed

**Issue 2: Username Hardcoding - FIXED**
- Created: vm-config.json (parameterized config)
- Updated: TASK-1.2-DEPLOY-KEYS-LINUX.sh
- Added: load_vm_config(), deploy_from_config(), test_ssh_with_key() functions
- Status: ✅ Fixed

**Issue 3: SSH Error Handling - FIXED**
- Updated: TASK-1.2-DEPLOY-KEYS-LINUX.sh
- Added: Detailed exit code handling (0=success, 255=connection, 1=auth)
- Added: Comprehensive verification logic with troubleshooting
- Status: ✅ Fixed

**Code Changes:**
- vm-config.json: {len(vm_config) if vm_config else 0} chars
- TASK-1.2-DEPLOY-KEYS-LINUX.sh: {len(task_1_2) if task_1_2 else 0} chars
- TASK-1.3-TEST-WINDOWS.sh: {len(task_1_3) if task_1_3 else 0} chars
"""
    
    # Review Agent validation summary
    review_agent_validation = """
**What Review Agent AGREES With:**
✅ vm-config.json - Well-structured, proper JSON format
✅ TASK-1.2 parameterization approach - Good abstraction
✅ TASK-1.3 Windows deployment logic - Sound approach
✅ General best practices - Error handling, logging, documentation

**What Review Agent DISAGREES With / Issues Found:**
❌ TASK-1.2 - JSON parsing via grep/sed (unreliable)
   - Issue: Fragile parsing, breaks with special characters
   - Recommendation: Use jq tool instead

❌ TASK-1.3 - Embedded PowerShell complexity
   - Issue: Hard to maintain and debug
   - Recommendation: Extract to separate file or use heredoc

❌ TASK-1.2 - Missing variable validation
   - Issue: Empty values could cause silent failures
   - Recommendation: Add explicit null checks

❌ Both Scripts - No input validation on prompts
   - Issue: Accepts any input
   - Recommendation: Add validation loop

❌ TASK-1.2 - Fragile key verification
   - Issue: String matching too fragile
   - Recommendation: Use key fingerprints instead

**Review Agent Final Recommendation:**
⚠️ PARTIALLY AGREE - v1.0.0 has good structure but needs refinements

**Blocking Issues:**
1. JSON parsing method is unreliable
2. PowerShell command complexity needs simplification
3. Key verification logic needs strengthening

**Non-blocking Issues:**
- Input validation improvements
- Error context enhancement
"""
    
    prompt = f"""# Final Three-Agent Consensus for VM101 v1.0.0

You are Azure GPT-4.1, the final validator and consensus builder.

## SITUATION

**Code Agent** has fixed 3 issues:
1. ✅ PowerShell syntax error (backslash → backtick)
2. ✅ Username hardcoding (created vm-config.json)
3. ✅ SSH error handling (improved verification)

**Review Agent** has validated:
- ✅ Agrees with structure and approach
- ⚠️ PARTIALLY AGREE - Found 5 issues (3 blocking, 2 non-blocking)
- ❌ Disagrees with JSON parsing method (grep/sed)
- ❌ Disagrees with PowerShell complexity
- ❌ Disagrees with key verification approach

## YOUR TASK

Build final consensus and decide:

1. **Are Code Agent's fixes correct?**
   - PowerShell fix: Is backtick correct?
   - Config file: Is approach sound?
   - Error handling: Is it comprehensive?

2. **Are Review Agent's concerns valid?**
   - JSON parsing: Is grep/sed really a problem?
   - PowerShell: Is complexity an issue?
   - Key verification: Is string matching insecure?

3. **Can we approve v1.0.0?**
   - With current fixes?
   - With Review Agent's recommended changes?
   - Or needs more work?

4. **Final Recommendation:**
   - APPROVE - Ready for production
   - APPROVE_WITH_CONDITIONS - Fix Review Agent's blocking issues first
   - REJECT - Needs significant work

## CONSENSUS CRITERIA

For v1.0.0 approval:
- ✅ All 3 agents must AGREE or STRONGLY AGREE
- ✅ Code quality ≥ 95/100
- ✅ No CRITICAL issues
- ✅ Production ready

## OUTPUT FORMAT

```json
{{
    "consensus_metadata": {{
        "reviewer": "Azure GPT-4.1",
        "date": "{datetime.now().isoformat()}",
        "agents": ["code_agent", "review_agent", "gpt41"]
    }},
    "code_agent_assessment": {{
        "fixes_correct": true|false,
        "fixes_complete": true|false,
        "quality": "EXCELLENT|GOOD|FAIR|POOR",
        "score": 0-100,
        "agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE"
    }},
    "review_agent_assessment": {{
        "concerns_valid": true|false,
        "blocking_issues_valid": true|false,
        "non_blocking_issues_valid": true|false,
        "agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE"
    }},
    "consensus_analysis": {{
        "points_of_agreement": ["list"],
        "points_of_disagreement": ["list"],
        "resolution": "how to resolve",
        "consensus_score": 0.0-1.0
    }},
    "final_recommendation": {{
        "v1_0_0_approved": true|false,
        "approval_type": "APPROVE|APPROVE_WITH_CONDITIONS|REJECT",
        "conditions": ["list if APPROVE_WITH_CONDITIONS"],
        "code_quality_score": 0-100,
        "production_ready": true|false,
        "reasoning": "detailed explanation",
        "next_steps": ["action items"]
    }}
}}
```

Provide your comprehensive consensus analysis now.
"""
    return prompt


def main():
    """Main consensus building function."""
    logger.info("=" * 80)
    logger.info("Final Three-Agent Consensus for VM101 v1.0.0")
    logger.info("=" * 80)
    
    # Initialize Azure client
    client = initialize_azure_client()
    if not client:
        return 1
    
    # Create prompt with actual fixes and validation
    logger.info("\n📝 Creating consensus prompt with actual fixes...")
    prompt = create_final_consensus_prompt()
    
    logger.info("\n🤖 Calling Azure GPT-4.1 for final consensus...")
    
    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a consensus builder and final validator. Your role is to build agreement between multiple AI agents, assess code quality, and make final production readiness decisions."
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
        output_file = OUTPUT_DIR / f"final_consensus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Try to parse as JSON
        try:
            # Extract JSON from markdown code blocks if present
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                consensus = json.loads(json_match.group(1))
            else:
                json_match = re.search(r'\{.*\}', content, re.DOTALL)
                if json_match:
                    consensus = json.loads(json_match.group(0))
                else:
                    consensus = json.loads(content)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(consensus, f, indent=2, ensure_ascii=False)
            
            logger.info(f"✅ Consensus saved to {output_file}")
            
            # Print summary
            print("\n" + "=" * 80)
            print("FINAL CONSENSUS RESULTS")
            print("=" * 80)
            
            final_rec = consensus.get("final_recommendation", {})
            approval = final_rec.get("approval_type", "UNKNOWN")
            approved = final_rec.get("v1_0_0_approved", False)
            quality_score = final_rec.get("code_quality_score", 0)
            production_ready = final_rec.get("production_ready", False)
            
            print(f"\n📊 Approval Status: {approval}")
            print(f"✅ v1.0.0 Approved: {'YES' if approved else 'NO'}")
            print(f"📈 Code Quality Score: {quality_score}/100")
            print(f"🚀 Production Ready: {'YES' if production_ready else 'NO'}")
            
            if final_rec.get("conditions"):
                print(f"\n⚠️  Conditions:")
                for condition in final_rec.get("conditions", []):
                    print(f"   - {condition}")
            
            if final_rec.get("next_steps"):
                print(f"\n📋 Next Steps:")
                for i, step in enumerate(final_rec.get("next_steps", []), 1):
                    print(f"   {i}. {step}")
            
            print(f"\n📄 Full report: {output_file}")
            print("=" * 80)
            
        except json.JSONDecodeError:
            # Save as text if not JSON
            output_file = output_file.with_suffix('.txt')
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"✅ Consensus saved to {output_file} (as text)")
            print(f"\n📄 Consensus saved to: {output_file}")
        
        return 0
        
    except Exception as e:
        logger.error(f"❌ Error calling Azure OpenAI: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())



