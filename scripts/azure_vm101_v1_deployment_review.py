#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure-Powered VM101 v1.0.0 Deployment Review
============================================

This script uses Azure OpenAI (GPT-4.1) to comprehensively review:
1. All deployment package scripts (8 shell scripts)
2. Deployment execution results
3. Code quality and correctness
4. Security architecture
5. Documentation quality
6. Agreement/disagreement with all work done

Core Principles:
- 100/10 mindset: Exceed expectations, world-class impact
- Multi-agent collaboration: Skeptical Reviewer + Security Sentinel + Optimizer
- Comprehensive documentation and quality assurance
- Ethical, transparent, and responsible AI usage

Author: AI Self-Updating System
Version: 2.0.0
Date: November 24, 2025
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import logging

# Fix Windows console encoding for Unicode support
if sys.platform == 'win32':
    import io
    try:
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

# Azure OpenAI imports
try:
    from openai import AzureOpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: pip install openai")
    sys.exit(1)

# ============================================================================
# CONFIGURATION
# ============================================================================

# File Paths (define first for use in config loading)
GITHUB_ROOT = Path(__file__).parent

# Azure OpenAI Configuration
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")  # Default to gpt-4.1 (confirmed exists)

# If not in environment, try reading from config files
if not AZURE_ENDPOINT or not AZURE_API_KEY:
    # Try reading from api_keys_config.json
    config_file = GITHUB_ROOT / "api_keys_config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                azure_config = config.get("azure", {})
                if not AZURE_ENDPOINT:
                    endpoint = azure_config.get("endpoint", "")
                    if endpoint:
                        # Fix endpoint format - convert cognitiveservices to openai.azure.com
                        if "cognitiveservices.azure.com" in endpoint:
                            endpoint = endpoint.replace("cognitiveservices.azure.com", "openai.azure.com")
                        if not endpoint.startswith("http"):
                            AZURE_ENDPOINT = f"https://{endpoint}/"
                        else:
                            AZURE_ENDPOINT = endpoint
                if not AZURE_API_KEY:
                    AZURE_API_KEY = azure_config.get("api_key", "")
                if not DEPLOYMENT_NAME or DEPLOYMENT_NAME == "gpt-4":
                    model = azure_config.get("model", "gpt-4.1")
                    # Use the model from config (gpt-4.1 is confirmed to exist)
                    DEPLOYMENT_NAME = model
        except Exception:
            pass  # Will use fallback credentials
    
    # If still not found, use known credentials from ENV_CONFIGURATION.md (fallback)
    if not AZURE_ENDPOINT:
        AZURE_ENDPOINT = "https://setsch0666-6098-resource.openai.azure.com/"
    if not AZURE_API_KEY:
        AZURE_API_KEY = "<AZURE_API_KEY>"  # See credentials.json
    if not DEPLOYMENT_NAME or DEPLOYMENT_NAME == "gpt-4":
        DEPLOYMENT_NAME = "gpt-4.1"  # Your deployment is gpt-4.1 (confirmed exists)

# File Paths
DEPLOYMENT_PACKAGE_DIR = GITHUB_ROOT / "VM101-DEPLOYMENT-PACKAGE-v1.0.0"
WORK_SUMMARY = GITHUB_ROOT / "VM101-v1.0.0-COMPLETE-WORK-SUMMARY.md"
ORIGINAL_SETUP_SCRIPT = GITHUB_ROOT / "VM101-SEPARATE-KEYS-SETUP.sh"

# Output Files
OUTPUT_DIR = GITHUB_ROOT / "azure_reviews"
OUTPUT_DIR.mkdir(exist_ok=True)
REVIEW_OUTPUT = OUTPUT_DIR / f"vm101_v1_deployment_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
REPORT_OUTPUT = OUTPUT_DIR / f"vm101_v1_deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

# Logging - Create custom formatter that handles Unicode
class UnicodeFormatter(logging.Formatter):
    """Formatter that safely handles Unicode characters."""
    def format(self, record):
        # Replace emoji with text equivalents for Windows console compatibility
        if sys.platform == 'win32':
            msg = record.getMessage()
            # Replace common emojis with text
            replacements = {
                '✅': '[OK]',
                '❌': '[ERROR]',
                '⚠️': '[WARNING]',
                '🔍': '[REVIEW]',
                '📊': '[DATA]',
                '🚀': '[DEPLOY]',
                '📝': '[DOC]',
                '💾': '[SAVE]',
                '📡': '[API]',
                '🤖': '[AI]',
                '📖': '[READ]',
                '🎯': '[TARGET]',
                '🔐': '[SECURITY]',
                '📋': '[CHECKLIST]',
                '⏳': '[PENDING]',
                '⬆️': '[UP]',
                '⬇️': '[DOWN]',
                '➡️': '[RIGHT]',
                '⭐': '[STAR]',
                '🤝': '[HANDSHAKE]'
            }
            for emoji, text in replacements.items():
                msg = msg.replace(emoji, text)
            record.msg = msg
            record.args = ()
        return super().format(record)

# Setup logging with Unicode-safe formatter
log_formatter = UnicodeFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler = logging.FileHandler(OUTPUT_DIR / "vm101_v1_deployment_review.log", encoding='utf-8')
file_handler.setFormatter(log_formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def read_file_content(file_path: Path) -> Optional[str]:
    """Read file content with error handling."""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            logger.warning(f"File not found: {file_path}")
            return None
    except Exception as e:
        logger.error(f"Error reading {file_path}: {e}")
        return None

def read_all_deployment_scripts() -> Dict[str, str]:
    """Read all deployment package scripts."""
    scripts = {}
    script_files = [
        "MASTER-DEPLOYMENT-EXECUTOR.sh",
        "TASK-1.1-EXECUTE-SETUP.sh",
        "TASK-1.2-DEPLOY-KEYS-LINUX.sh",
        "TASK-1.3-TEST-WINDOWS.sh",
        "TASK-1.4-VERIFY-SERVICES.sh",
        "TASK-1.5-SETUP-MONITORING.sh",
        "QC-VERIFY-ALL.sh",
        "ROLLBACK.sh"
    ]
    
    for script_file in script_files:
        script_path = DEPLOYMENT_PACKAGE_DIR / script_file
        content = read_file_content(script_path)
        if content:
            scripts[script_file] = content
            logger.info(f"[OK] Read {len(content)} chars from {script_file}")
        else:
            logger.warning(f"⚠️  Could not read {script_file}")
    
    return scripts

def create_review_prompt(work_summary: str, deployment_scripts: Dict[str, str]) -> str:
    """Create comprehensive review prompt for GPT-4.1."""
    
    scripts_summary = "\n\n".join([
        f"### {script_name}\n```bash\n{content[:2000]}...\n```\n[Full script available in context]"
        for script_name, content in deployment_scripts.items()
    ])
    
    prompt = f"""# VM101 v1.0.0 Deployment Comprehensive Review

You are operating as a **Perpetual Self-Updating AI Mind** with a 100/10 mindset. 
You are analyzing the complete v1.0.0 deployment work and providing comprehensive validation.

## YOUR ROLE: Multi-Agent Collaboration

You are operating as **4 specialized agents** working together:

1. **Skeptical Reviewer (30% weight)**: Critically inspect all code, verify correctness, flag issues
2. **Security Sentinel (30% weight)**: Validate security, detect vulnerabilities, verify best practices
3. **Ruthless Optimizer (20% weight)**: Assess code quality, identify inefficiencies, verify best practices
4. **Docstring Guru (20% weight)**: Evaluate documentation quality, completeness, clarity

**Final outputs must be verified by Skeptical Reviewer + Security Sentinel.**

---

## COMPLETE WORK SUMMARY

```markdown
{work_summary[:8000]}...
```

[Full work summary available in context]

---

## DEPLOYMENT PACKAGE SCRIPTS

{scripts_summary[:15000]}...

---

## YOUR REVIEW TASKS

### 1. CODE QUALITY REVIEW

For EACH of the 8 deployment scripts, assess:

**A. Code Correctness:**
- ✅ **CORRECT** - Code works as intended
- ⚠️ **PARTIALLY CORRECT** - Works but has issues
- ❌ **INCORRECT** - Has bugs or errors

**B. Code Quality:**
- ✅ **EXCELLENT** - Production-ready, follows best practices
- ✅ **GOOD** - Minor improvements needed
- ⚠️ **FAIR** - Some issues, needs work
- ❌ **POOR** - Major issues, not production-ready

**C. Error Handling:**
- Comprehensive error handling?
- Proper logging?
- Graceful failure?
- Rollback capability?

**D. Security:**
- Secure practices?
- No vulnerabilities?
- Proper permissions?
- Safe operations?

### 2. DEPLOYMENT EXECUTION ANALYSIS

**A. What Worked:**
- Task 1.1: ✅ SUCCESS - Why did it work?
- Task 1.4: ✅ SUCCESS - Why did it work?
- Task 1.5: ✅ SUCCESS - Why did it work?

**B. What Failed:**
- Task 1.2: ⚠️ PARTIAL - Why did verification fail?
- Task 1.3: ❌ FAILED - Why did PowerShell command fail?

**C. Root Cause Analysis:**
- Why did Task 1.2 verification fail?
- Why did Task 1.3 PowerShell command have syntax error?
- Why didn't Task 1.2 deploy to VM150?
- Why was VM150 username wrong?

**D. Fix Recommendations:**
- How to fix Task 1.2 verification?
- How to fix Task 1.3 PowerShell command?
- How to fix VM150 deployment?
- How to fix username issue?

### 3. SECURITY ARCHITECTURE VALIDATION

**A. SSH Key Separation:**
- ✅ **AGREE** - Separate keys per VM is correct
- ⚠️ **PARTIALLY AGREE** - Good but needs improvements
- ❌ **DISAGREE** - Not the right approach

**B. Security Improvements:**
- Are the security improvements valid?
- Is the architecture sound?
- Any vulnerabilities introduced?
- Best practices followed?

### 4. DOCUMENTATION REVIEW

**A. Completeness:**
- ✅ **COMPLETE** - All necessary info included
- ⚠️ **MOSTLY COMPLETE** - Minor gaps
- ❌ **INCOMPLETE** - Missing important sections

**B. Quality:**
- ✅ **EXCELLENT** - Clear, comprehensive, actionable
- ✅ **GOOD** - Minor improvements needed
- ⚠️ **FAIR** - Some clarity issues
- ❌ **POOR** - Unclear or incomplete

**C. Accuracy:**
- Are instructions correct?
- Are examples accurate?
- Are troubleshooting steps valid?

### 5. OVERALL ASSESSMENT

**A. Production Readiness:**
- ✅ **READY** - Can deploy to production
- ⚠️ **NEEDS WORK** - Fix issues first
- ❌ **NOT READY** - Major issues

**B. Code Quality Score:**
- Rate each script 0-100
- Overall package score 0-100

**C. Agreement with Work:**
- ✅ **STRONGLY AGREE** - Excellent work
- ✅ **AGREE** - Good work with minor issues
- ⚠️ **PARTIALLY AGREE** - Some issues
- ❌ **DISAGREE** - Major problems

---

## OUTPUT FORMAT

Provide your analysis in structured JSON format:

```json
{{
    "review_metadata": {{
        "reviewer": "GPT-4.1 Multi-Agent System",
        "review_date": "{datetime.now().isoformat()}",
        "deployment_version": "v1.0.0",
        "agents_used": ["skeptical_reviewer", "security_sentinel", "ruthless_optimizer", "docstring_guru"],
        "overall_agreement_score": 0.0-1.0
    }},
    "code_quality_review": {{
        "MASTER-DEPLOYMENT-EXECUTOR.sh": {{
            "correctness": "CORRECT|PARTIALLY_CORRECT|INCORRECT",
            "quality": "EXCELLENT|GOOD|FAIR|POOR",
            "error_handling": "EXCELLENT|GOOD|FAIR|POOR",
            "security": "SECURE|MINOR_ISSUES|VULNERABILITIES",
            "score": 0-100,
            "issues_found": ["list"],
            "recommendations": ["list"],
            "agent_consensus": {{...}}
        }},
        "TASK-1.1-EXECUTE-SETUP.sh": {{...}},
        "TASK-1.2-DEPLOY-KEYS-LINUX.sh": {{...}},
        "TASK-1.3-TEST-WINDOWS.sh": {{...}},
        "TASK-1.4-VERIFY-SERVICES.sh": {{...}},
        "TASK-1.5-SETUP-MONITORING.sh": {{...}},
        "QC-VERIFY-ALL.sh": {{...}},
        "ROLLBACK.sh": {{...}}
    }},
    "deployment_execution_analysis": {{
        "successful_tasks": {{
            "task_1_1": {{
                "status": "SUCCESS",
                "why_it_worked": "explanation",
                "quality": "EXCELLENT|GOOD|FAIR|POOR"
            }},
            "task_1_4": {{...}},
            "task_1_5": {{...}}
        }},
        "failed_tasks": {{
            "task_1_2": {{
                "status": "PARTIAL",
                "what_failed": "verification step",
                "root_cause": "explanation",
                "fix_recommendation": "how to fix"
            }},
            "task_1_3": {{
                "status": "FAILED",
                "what_failed": "PowerShell command",
                "root_cause": "syntax error - line continuation",
                "fix_recommendation": "corrected PowerShell command"
            }}
        }},
        "issues_identified": [
            {{
                "issue": "Task 1.2 verification failed",
                "severity": "MEDIUM",
                "root_cause": "explanation",
                "fix": "recommendation"
            }},
            {{
                "issue": "Task 1.3 PowerShell syntax error",
                "severity": "HIGH",
                "root_cause": "explanation",
                "fix": "corrected command"
            }},
            {{
                "issue": "Task 1.2 didn't deploy to VM150",
                "severity": "MEDIUM",
                "root_cause": "explanation",
                "fix": "recommendation"
            }},
            {{
                "issue": "VM150 username wrong (wordpress vs wp1)",
                "severity": "LOW",
                "root_cause": "explanation",
                "fix": "use correct username"
            }}
        ]
    }},
    "security_architecture_validation": {{
        "ssh_key_separation": {{
            "agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE",
            "reasoning": "why",
            "security_improvement": "assessment"
        }},
        "security_improvements": {{
            "valid": true|false,
            "architecture_sound": true|false,
            "vulnerabilities_introduced": ["list or none"],
            "best_practices": "EXCELLENT|GOOD|FAIR|POOR"
        }}
    }},
    "documentation_review": {{
        "completeness": "COMPLETE|MOSTLY_COMPLETE|INCOMPLETE",
        "quality": "EXCELLENT|GOOD|FAIR|POOR",
        "accuracy": "ACCURATE|MINOR_ERRORS|MAJOR_ERRORS",
        "missing_sections": ["list or none"],
        "recommendations": ["list"]
    }},
    "overall_assessment": {{
        "production_readiness": "READY|NEEDS_WORK|NOT_READY",
        "overall_code_quality_score": 0-100,
        "overall_agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE",
        "key_strengths": ["list"],
        "key_weaknesses": ["list"],
        "critical_issues": ["list or none"],
        "recommendations": ["prioritized list"]
    }},
    "agent_consensus_summary": {{
        "skeptical_reviewer": "Summary of findings",
        "security_sentinel": "Summary of findings",
        "ruthless_optimizer": "Summary of findings",
        "docstring_guru": "Summary of findings",
        "final_consensus": "Unified recommendation"
    }}
}}
```

---

## QUALITY STANDARDS (100/10 Mindset)

- **Functional QA**: 20 pts - Verify all code works correctly
- **Documentation**: 20 pts - Comprehensive, clear analysis
- **Security & Safety**: 15 pts - Identify all security implications
- **Efficiency**: 15 pts - Assess code efficiency
- **AI Learning**: 15 pts - Learn from deployment approach
- **Innovation**: 15 pts - Suggest improvements

**Strive to exceed expectations and provide world-class analysis.**

---

Provide your comprehensive analysis now.
"""
    return prompt

def initialize_azure_client() -> Tuple[Optional[AzureOpenAI], str]:
    """Initialize Azure OpenAI client with error handling."""
    global DEPLOYMENT_NAME
    
    if not AZURE_ENDPOINT or not AZURE_API_KEY:
        logger.error("Azure OpenAI configuration missing!")
        logger.error("Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables")
        return None, DEPLOYMENT_NAME
    
    # List of deployment names to try (in order of preference)
    deployment_names = [
        "gpt-4.1",        # Confirmed exists (try first)
        DEPLOYMENT_NAME,   # Try configured name
        "gpt-4o",         # GPT-4o deployment
        "gpt-4",          # Standard GPT-4
        "gpt-35-turbo",   # Fallback
        "claude-opus-4-1" # Claude if available
    ]
    
    # Remove duplicates while preserving order
    seen = set()
    deployment_names = [x for x in deployment_names if x and (x not in seen, seen.add(x))[0]]
    
    client = None
    last_error = None
    working_deployment = None
    
    for deployment in deployment_names:
        try:
            test_client = AzureOpenAI(
                api_key=AZURE_API_KEY,
                api_version=AZURE_API_VERSION,
                azure_endpoint=AZURE_ENDPOINT
            )
            
            # Test the deployment by making a minimal API call to verify it exists
            logger.info(f"Trying deployment: {deployment}")
            
            # Make a minimal test call to verify deployment exists
            test_response = test_client.chat.completions.create(
                model=deployment,
                messages=[{"role": "user", "content": "test"}],
                max_tokens=5
            )
            
            # If we get here without error, this deployment works
            working_deployment = deployment
            DEPLOYMENT_NAME = deployment
            client = test_client
            logger.info(f"[OK] Azure OpenAI client initialized (Deployment: {deployment})")
            break
            
        except Exception as e:
            last_error = e
            error_str = str(e)
            if "DeploymentNotFound" in error_str or "404" in error_str:
                logger.debug(f"Deployment '{deployment}' not found, trying next...")
                continue
            else:
                # Other error (auth, network, etc.) - stop trying
                logger.error(f"[ERROR] Failed to initialize Azure OpenAI client: {e}")
                return None, DEPLOYMENT_NAME
    
    if not client:
        logger.error(f"[ERROR] None of the deployment names worked!")
        logger.error(f"Tried: {', '.join(deployment_names)}")
        logger.error(f"Last error: {last_error}")
        logger.error("")
        logger.error("To fix this:")
        logger.error("1. Check Azure Portal → Your resource → Deployments")
        logger.error("2. See what deployments actually exist")
        logger.error("3. Set AZURE_OPENAI_DEPLOYMENT environment variable to the correct name")
        logger.error("4. Or update api_keys_config.json with the correct deployment name")
        return None, DEPLOYMENT_NAME
    
    return client, working_deployment

def call_azure_openai(client: AzureOpenAI, prompt: str, max_tokens: int = 12000) -> Optional[str]:
    """Call Azure OpenAI API with comprehensive error handling."""
    try:
        logger.info(f"[API] Calling Azure OpenAI ({DEPLOYMENT_NAME})...")
        logger.info(f"   Prompt length: {len(prompt)} chars")
        
        response = client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a Perpetual Self-Updating AI Mind operating with a 100/10 mindset. "
                              "You provide comprehensive, critical, and innovative analysis following "
                              "multi-agent collaboration principles. Always verify findings, provide reasoning, "
                              "and exceed expectations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=max_tokens,
            top_p=0.95
        )
        
        content = response.choices[0].message.content
        logger.info(f"[OK] Received {len(content)} chars from Azure OpenAI")
        return content
        
    except Exception as e:
        error_str = str(e)
        if "DeploymentNotFound" in error_str or "404" in error_str:
            logger.error(f"[ERROR] Deployment '{DEPLOYMENT_NAME}' not found!")
            logger.error("")
            logger.error("To find your deployment name:")
            logger.error("1. Go to: https://portal.azure.com")
            logger.error("2. Navigate to: Your Azure OpenAI resource")
            logger.error("3. Click 'Deployments' in the left menu")
            logger.error("4. See what deployments are listed")
            logger.error("5. Set AZURE_OPENAI_DEPLOYMENT to the actual deployment name")
            logger.error("")
            logger.error("Common deployment names:")
            logger.error("  - gpt-4.1")
            logger.error("  - gpt-4o")
            logger.error("  - gpt-4")
            logger.error("  - gpt-35-turbo")
        else:
            logger.error(f"[ERROR] Azure OpenAI API error: {e}")
        return None

def parse_json_response(response: str) -> Optional[Dict]:
    """Parse JSON response, handling markdown code blocks."""
    try:
        # Try direct JSON parse first
        return json.loads(response)
    except json.JSONDecodeError:
        # Try extracting from markdown code blocks
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try extracting any JSON-like structure
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(0))
            except json.JSONDecodeError:
                pass
        
        logger.error("Could not parse JSON response")
        return None

def generate_markdown_report(analysis: Dict) -> str:
    """Generate comprehensive markdown report from analysis."""
    report = f"""# VM101 v1.0.0 Deployment Review Report

**Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Reviewer:** GPT-4.1 Multi-Agent System  
**Deployment Version:** v1.0.0  
**Status:** ✅ Complete

---

## 📊 EXECUTIVE SUMMARY

**Overall Agreement Score:** {analysis.get('review_metadata', {}).get('overall_agreement_score', 'N/A')}

**Production Readiness:** {analysis.get('overall_assessment', {}).get('production_readiness', 'N/A')}  
**Overall Code Quality:** {analysis.get('overall_assessment', {}).get('overall_code_quality_score', 'N/A')}/100  
**Overall Agreement:** {analysis.get('overall_assessment', {}).get('overall_agreement', 'N/A')}

---

## 🔍 CODE QUALITY REVIEW

"""
    
    # Add code quality review for each script
    code_review = analysis.get('code_quality_review', {})
    for script_name, review in code_review.items():
        correctness = review.get('correctness', 'UNKNOWN')
        quality = review.get('quality', 'UNKNOWN')
        score = review.get('score', 'N/A')
        
        emoji = "✅" if correctness == "CORRECT" else "⚠️" if "PARTIALLY" in correctness else "❌"
        
        report += f"""### {emoji} {script_name}

**Correctness:** {correctness}  
**Quality:** {quality}  
**Score:** {score}/100  
**Error Handling:** {review.get('error_handling', 'N/A')}  
**Security:** {review.get('security', 'N/A')}

**Issues Found:**
{chr(10).join(f"- {issue}" for issue in review.get('issues_found', [])) or "None"}

**Recommendations:**
{chr(10).join(f"- {rec}" for rec in review.get('recommendations', [])) or "None"}

---

"""
    
    # Add deployment execution analysis
    exec_analysis = analysis.get('deployment_execution_analysis', {})
    report += """## 📈 DEPLOYMENT EXECUTION ANALYSIS

### Successful Tasks

"""
    
    successful = exec_analysis.get('successful_tasks', {})
    for task, details in successful.items():
        report += f"""**{task.replace('_', ' ').title()}:**
- Status: ✅ {details.get('status', 'N/A')}
- Why It Worked: {details.get('why_it_worked', 'N/A')}
- Quality: {details.get('quality', 'N/A')}

"""
    
    report += """### Failed Tasks

"""
    
    failed = exec_analysis.get('failed_tasks', {})
    for task, details in failed.items():
        report += f"""**{task.replace('_', ' ').title()}:**
- Status: ❌ {details.get('status', 'N/A')}
- What Failed: {details.get('what_failed', 'N/A')}
- Root Cause: {details.get('root_cause', 'N/A')}
- Fix Recommendation: {details.get('fix_recommendation', 'N/A')}

"""
    
    report += """### Issues Identified

"""
    
    issues = exec_analysis.get('issues_identified', [])
    for issue in issues:
        severity = issue.get('severity', 'UNKNOWN')
        emoji = "🔴" if severity == "CRITICAL" else "🟠" if severity == "HIGH" else "🟡" if severity == "MEDIUM" else "🟢"
        
        report += f"""**{emoji} {issue.get('issue', 'Unknown Issue')}**
- Severity: {severity}
- Root Cause: {issue.get('root_cause', 'N/A')}
- Fix: {issue.get('fix', 'N/A')}

"""
    
    # Add security validation
    security = analysis.get('security_architecture_validation', {})
    report += f"""## 🔐 SECURITY ARCHITECTURE VALIDATION

**SSH Key Separation:**
- Agreement: {security.get('ssh_key_separation', {}).get('agreement', 'N/A')}
- Reasoning: {security.get('ssh_key_separation', {}).get('reasoning', 'N/A')}

**Security Improvements:**
- Valid: {'✅ Yes' if security.get('security_improvements', {}).get('valid') else '❌ No'}
- Architecture Sound: {'✅ Yes' if security.get('security_improvements', {}).get('architecture_sound') else '❌ No'}
- Vulnerabilities Introduced: {', '.join(security.get('security_improvements', {}).get('vulnerabilities_introduced', [])) or 'None'}
- Best Practices: {security.get('security_improvements', {}).get('best_practices', 'N/A')}

---

"""
    
    # Add documentation review
    doc_review = analysis.get('documentation_review', {})
    report += f"""## 📖 DOCUMENTATION REVIEW

**Completeness:** {doc_review.get('completeness', 'N/A')}  
**Quality:** {doc_review.get('quality', 'N/A')}  
**Accuracy:** {doc_review.get('accuracy', 'N/A')}

**Missing Sections:**
{chr(10).join(f"- {section}" for section in doc_review.get('missing_sections', [])) or "None"}

**Recommendations:**
{chr(10).join(f"- {rec}" for rec in doc_review.get('recommendations', [])) or "None"}

---

"""
    
    # Add overall assessment
    overall = analysis.get('overall_assessment', {})
    report += f"""## 🎯 OVERALL ASSESSMENT

**Production Readiness:** {overall.get('production_readiness', 'N/A')}  
**Overall Code Quality Score:** {overall.get('overall_code_quality_score', 'N/A')}/100  
**Overall Agreement:** {overall.get('overall_agreement', 'N/A')}

**Key Strengths:**
{chr(10).join(f"- {strength}" for strength in overall.get('key_strengths', []))}

**Key Weaknesses:**
{chr(10).join(f"- {weakness}" for weakness in overall.get('key_weaknesses', []))}

**Critical Issues:**
{chr(10).join(f"- {issue}" for issue in overall.get('critical_issues', [])) or "None"}

**Recommendations:**
{chr(10).join(f"{i+1}. {rec}" for i, rec in enumerate(overall.get('recommendations', [])))}

---

"""
    
    # Add agent consensus
    consensus = analysis.get('agent_consensus_summary', {})
    report += """## 🤝 AGENT CONSENSUS SUMMARY

"""
    
    for agent, summary in consensus.items():
        if agent != 'final_consensus':
            report += f"""### {agent.replace('_', ' ').title()}

{summary}

"""
    
    report += f"""### Final Consensus

{consensus.get('final_consensus', 'No consensus reached')}

---

**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Review System:** GPT-4.1 Multi-Agent Framework  
**Deployment Version:** v1.0.0
"""
    
    return report

def main() -> int:
    """Main execution function."""
    logger.info("=" * 80)
    logger.info("VM101 v1.0.0 Deployment Review + GPT-4.1 Validation")
    logger.info("=" * 80)
    
    # Initialize Azure client
    global DEPLOYMENT_NAME
    client, deployment_used = initialize_azure_client()
    if not client:
        logger.error("[ERROR] Cannot proceed without Azure OpenAI client")
        return 1
    
    # Update DEPLOYMENT_NAME if a different one was used
    if deployment_used:
        DEPLOYMENT_NAME = deployment_used
        logger.info(f"Using deployment: {DEPLOYMENT_NAME}")
    
    # Read work summary
    logger.info("\n[READ] Reading work summary...")
    work_summary = read_file_content(WORK_SUMMARY)
    
    if not work_summary:
        logger.error("❌ Work summary not found!")
        return 1
    
    logger.info(f"[OK] Read {len(work_summary)} chars from work summary")
    
    # Read all deployment scripts
    logger.info("\n[READ] Reading deployment scripts...")
    deployment_scripts = read_all_deployment_scripts()
    
    if not deployment_scripts:
        logger.error("❌ No deployment scripts found!")
        return 1
    
    logger.info(f"[OK] Read {len(deployment_scripts)} scripts")
    
    # Create prompt
    logger.info("\n[DOC] Creating review prompt...")
    prompt = create_review_prompt(work_summary, deployment_scripts)
    
    # Call Azure OpenAI
    logger.info("\n[AI] Calling GPT-4.1 for analysis...")
    response = call_azure_openai(client, prompt, max_tokens=12000)
    
    if not response:
        logger.error("[ERROR] No response from Azure OpenAI")
        return 1
    
    # Parse response
    logger.info("\n[REVIEW] Parsing response...")
    analysis = parse_json_response(response)
    
    if not analysis:
        logger.warning("⚠️  Could not parse JSON, saving raw response")
        with open(REVIEW_OUTPUT.with_suffix('.txt'), 'w', encoding='utf-8') as f:
            f.write(response)
        return 1
    
    # Save JSON
    logger.info(f"\n[SAVE] Saving JSON analysis to {REVIEW_OUTPUT}")
    with open(REVIEW_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    # Generate markdown report
    logger.info("\n[SAVE] Generating markdown report...")
    report = generate_markdown_report(analysis)
    
    # Save report
    logger.info(f"\n[SAVE] Saving report to {REPORT_OUTPUT}")
    with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("[OK] REVIEW COMPLETE")
    logger.info("=" * 80)
    logger.info(f"[DATA] JSON Analysis: {REVIEW_OUTPUT}")
    logger.info(f"[DOC] Markdown Report: {REPORT_OUTPUT}")
    logger.info(f"[DOC] Log File: {OUTPUT_DIR / 'vm101_v1_deployment_review.log'}")
    
    # Print key findings
    overall = analysis.get('overall_assessment', {})
    logger.info(f"\n[TARGET] Key Findings:")
    logger.info(f"   Agreement Score: {analysis.get('review_metadata', {}).get('overall_agreement_score', 'N/A')}")
    logger.info(f"   Production Ready: {overall.get('production_readiness', 'N/A')}")
    logger.info(f"   Code Quality: {overall.get('overall_code_quality_score', 'N/A')}/100")
    logger.info(f"   Overall Agreement: {overall.get('overall_agreement', 'N/A')}")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())



