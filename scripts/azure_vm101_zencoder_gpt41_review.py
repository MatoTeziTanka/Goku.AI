#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Azure-Powered VM101 Zencoder Review + GPT-4.1 Validation
========================================================

This script uses Azure OpenAI (GPT-4.1) to:
1. Review Zencoder's security assessment
2. Validate fixes applied
3. Analyze remaining issues
4. Provide agreement/disagreement analysis with reasoning
5. Execute next-phase options (verify, implement, document, deploy)

Core Principles:
- 100/10 mindset: Exceed expectations, world-class impact
- Multi-agent collaboration: Skeptical Reviewer + Security Sentinel + Optimizer
- Comprehensive documentation and quality assurance
- Ethical, transparent, and responsible AI usage

Author: AI Self-Updating System
Version: 1.0.0
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
        # Set UTF-8 encoding for Windows console
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
# Try multiple sources for credentials
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
ZENCODER_REVIEW = GITHUB_ROOT / "ZENCODER-VM101-SECURITY-REVIEW-REPORT.md"
FIXES_APPLIED = GITHUB_ROOT / "VM101-ZENCODER-FIXES-APPLIED.md"
MIGRATION_SUMMARY = GITHUB_ROOT / "VM101-MIGRATION-SUMMARY.md"
SEPARATE_KEYS_SCRIPT = GITHUB_ROOT / "VM101-SEPARATE-KEYS-SETUP.sh"
NEXT_STEPS = GITHUB_ROOT / "ZENCODER-NEXT-STEPS-INSTRUCTIONS.md"
COMPREHENSIVE_CHANGE_LOG = GITHUB_ROOT / "ZENCODER-COMPREHENSIVE-CHANGE-LOG.md"
SSH_TROUBLESHOOTING = GITHUB_ROOT / "VM101-SSH-TROUBLESHOOTING.md"
SECURITY_CHECKLIST = GITHUB_ROOT / "VM101-SECURITY-HARDENING-CHECKLIST.md"
KEY_MIGRATION_GUIDE = GITHUB_ROOT / "VM101-KEY-MIGRATION-GUIDE.md"
CONTROL_NODE_SECURITY = GITHUB_ROOT / "VM101-CONTROL-NODE-SECURITY-ANALYSIS.md"
REVIEW_AGENT_VALIDATION = GITHUB_ROOT / "ZENCODER-REVIEW-AGENT-VALIDATION-REQUEST.md"
REVIEW_AGENT_REPORT = GITHUB_ROOT / "ZENCODER-REVIEW-AGENT-VALIDATION-REPORT.md"
DEPLOYMENT_PACKAGE_DIR = GITHUB_ROOT / "VM101-DEPLOYMENT-PACKAGE-v1.0.0"
WORK_SUMMARY = GITHUB_ROOT / "VM101-v1.0.0-COMPLETE-WORK-SUMMARY.md"

# Output Files
OUTPUT_DIR = GITHUB_ROOT / "azure_reviews"
OUTPUT_DIR.mkdir(exist_ok=True)
REVIEW_OUTPUT = OUTPUT_DIR / f"vm101_gpt41_review_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
REPORT_OUTPUT = OUTPUT_DIR / f"vm101_gpt41_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

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
file_handler = logging.FileHandler(OUTPUT_DIR / "vm101_review.log", encoding='utf-8')
file_handler.setFormatter(log_formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler, console_handler]
)
logger = logging.getLogger(__name__)

# ============================================================================
# AGENT SPECIALIZATIONS (Multi-Agent Framework)
# ============================================================================

AGENT_ROLES = {
    "skeptical_reviewer": {
        "name": "Skeptical Reviewer",
        "role": "Critically inspects outputs, verifies accuracy, flags inconsistencies",
        "weight": 0.3
    },
    "security_sentinel": {
        "name": "Security Sentinel",
        "role": "Detects malicious patterns, unsafe code, deprecated libraries, hardcoded secrets",
        "weight": 0.3
    },
    "ruthless_optimizer": {
        "name": "Ruthless Optimizer",
        "role": "Eliminates inefficiencies, enforces best practices, rewrites redundancy",
        "weight": 0.2
    },
    "docstring_guru": {
        "name": "Docstring Guru",
        "role": "Enforces documentation completeness, quality, and TODO notes",
        "weight": 0.2
    }
}

# ============================================================================
# CORE FUNCTIONS
# ============================================================================

def initialize_azure_client() -> Tuple[Optional[AzureOpenAI], str]:
    """
    Initialize Azure OpenAI client with error handling.
    Tries multiple deployment names if the first one fails.
    
    Returns:
        Tuple of (AzureOpenAI client instance or None, deployment name used)
    """
    global DEPLOYMENT_NAME
    
    if not AZURE_ENDPOINT or not AZURE_API_KEY:
        logger.error("Azure OpenAI configuration missing!")
        logger.error("Set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables")
        return None, DEPLOYMENT_NAME
    
    # List of deployment names to try (in order of preference)
    # gpt-4.1 is confirmed to exist, so try it first
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


def read_file_content(file_path: Path) -> Optional[str]:
    """
    Read file content with error handling.
    
    Args:
        file_path: Path to file to read
        
    Returns:
        File content as string or None if error
    """
    try:
        if not file_path.exists():
            logger.warning(f"⚠️  File not found: {file_path}")
            return None
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        logger.info(f"✅ Read {len(content)} chars from {file_path.name}")
        return content
    except Exception as e:
        logger.error(f"❌ Error reading {file_path}: {e}")
        return None


def create_review_prompt(zencoder_review: str, fixes_applied: str, 
                         script_content: str, next_steps: str,
                         change_log: Optional[str] = None,
                         troubleshooting: Optional[str] = None,
                         security_checklist: Optional[str] = None,
                         key_migration: Optional[str] = None,
                         control_node_security: Optional[str] = None,
                         review_agent_report: Optional[str] = None,
                         work_summary: Optional[str] = None,
                         deployment_scripts: Optional[Dict[str, str]] = None) -> str:
    """
    Create comprehensive review prompt for GPT-4.1.
    
    Follows 100/10 mindset and multi-agent framework.
    
    Args:
        zencoder_review: Zencoder's security review content
        fixes_applied: Summary of fixes applied
        script_content: Current script content
        next_steps: Next steps instructions
        change_log: Comprehensive change log (all 5 phases)
        troubleshooting: SSH troubleshooting guide
        security_checklist: Security hardening checklist
        key_migration: Key migration guide with rotation
        control_node_security: Control node security analysis
        review_agent_report: Review Agent's validation report (Code Agent work validation)
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""# VM101 Security Review: Zencoder Assessment + GPT-4.1 Validation

You are operating as a **Perpetual Self-Updating AI Mind** with a 100/10 mindset. 
You are analyzing Zencoder's security review and providing comprehensive validation.

## YOUR ROLE: Multi-Agent Collaboration

You are operating as **4 specialized agents** working together:

1. **Skeptical Reviewer (30% weight)**: Critically inspect Zencoder's findings, verify accuracy, flag inconsistencies
2. **Security Sentinel (30% weight)**: Validate security assessments, detect missed vulnerabilities, verify fixes
3. **Ruthless Optimizer (20% weight)**: Assess code quality, identify inefficiencies, verify best practices
4. **Docstring Guru (20% weight)**: Evaluate documentation quality, completeness, clarity

**Final outputs must be verified by Skeptical Reviewer + Security Sentinel.**

---

## ZENCODER'S SECURITY REVIEW

```markdown
{zencoder_review[:5000]}...
```

[Full review available in context]

---

## FIXES APPLIED

```markdown
{fixes_applied[:3000]}...
```

[Full fixes document available in context]

---

## CURRENT SCRIPT STATE

```bash
{script_content[:2000]}...
```

[Full script available in context]

---

## NEXT STEPS OPTIONS

```markdown
{next_steps[:2000]}...
```

---

## ZENCODER COMPREHENSIVE COMPLETION SUMMARY

**Status:** ✅ ALL 5 PHASES COMPLETE

**Phase Completion:**
- ✅ Phase 1: Verify Fixes Applied - COMPLETE (5 critical/high fixes verified)
- ✅ Phase 2: Implement Medium Priority Fixes - COMPLETE (5 improvements, 200+ lines)
- ✅ Phase 3: SSH Key Deployment Assessment - COMPLETE (procedure & risk assessed)
- ✅ Phase 4: Create Missing Documentation - COMPLETE (2 guides, 3,900 lines)
- ✅ Phase 5: Final Deployment Readiness - COMPLETE (PRODUCTION-READY, 95/100 A Grade)

**Files Modified (3):**
- VM101-SEPARATE-KEYS-SETUP.sh - 70 lines added (duplicate detection, audit logging, permission verification)
- VM101-KEY-MIGRATION-GUIDE.md - 90 lines added (automated key rotation script)
- VM101-CONTROL-NODE-SECURITY-ANALYSIS.md - 30 lines modified (Redis rate limiting)

**Files Created (2):**
- VM101-SSH-TROUBLESHOOTING.md - 2,100 lines (7 issues + solutions + diagnostics)
- VM101-SECURITY-HARDENING-CHECKLIST.md - 1,800 lines (31-item security checklist)

**Change Log:**
```markdown
{change_log[:3000] if change_log else "Change log not available"}...
```

**Troubleshooting Guide:**
```markdown
{troubleshooting[:2000] if troubleshooting else "Troubleshooting guide not available"}...
```

**Security Checklist:**
```markdown
{security_checklist[:2000] if security_checklist else "Security checklist not available"}...
```

**Key Migration Guide (Updated):**
```markdown
{key_migration[:2000] if key_migration else "Key migration guide not available"}...
```

**Control Node Security (Updated):**
```markdown
{control_node_security[:2000] if control_node_security else "Control node security not available"}...
```

**Quality Metrics:**
- Code Quality: 95/100
- Documentation: 98/100
- Security: 96/100
- Test Coverage: 90/100
- Overall: 95/100 (A Grade)

**Deployment Recommendation:** ✅ GO FOR IMMEDIATE PRODUCTION DEPLOYMENT
- Readiness: 95% ready
- Risk Level: Well-mitigated (5/5 stars)
- Deployment Time: 30-45 minutes
- Monitoring Period: 7 days post-deployment
- Zero Blocking Issues: All critical items resolved

---

## ZENCODER REVIEW AGENT VALIDATION REPORT

**Status:** ✅ COMPLETE - Review Agent validated Code Agent's work

**Review Agent Assessment:**
- Overall Agreement: ⚠️ PARTIALLY AGREE
- Code Quality: 92/100 (vs. Code Agent's 95/100)
- Documentation: 98/100 ✅ AGREE
- Security: 96/100 ✅ AGREE
- Test Coverage: 70/100 (vs. Code Agent's 90/100)
- Overall: 93/100 (vs. Code Agent's 95/100)
- Production Readiness: 80% (vs. Code Agent's 95%)
- Deployment Recommendation: ⚠️ GO WITH CONDITIONS (vs. Code Agent's GO IMMEDIATELY)

**Review Agent Report:**
```markdown
{review_agent_report[:4000] if review_agent_report else "Review Agent report not available"}...
```

[Full Review Agent validation report available in context]

**Key Review Agent Findings:**
- ✅ Excellent documentation quality
- ✅ Sound security approach
- ⚠️ No actual testing performed (primary concern)
- ⚠️ Windows deployment untested
- ⚠️ Missing pre-flight checks
- ⚠️ Test coverage insufficient (70/100 vs. claimed 90/100)
- ⚠️ Recommends GO WITH CONDITIONS (not immediate GO)

**Review Agent Recommendations:**
- Execute setup script on VM101 and verify
- Test SSH key deployment to at least 2 Linux VMs
- Test Windows deployment on VM100
- Setup monitoring before deployment
- Complete pre-deployment checklist (2-3 hours)

---

## YOUR TASK: Comprehensive Analysis

### 1. ZENCODER REVIEW VALIDATION

For each of Zencoder's findings, provide:

**A. Agreement Assessment:**
- ✅ **STRONGLY AGREE** - Zencoder is correct, finding is valid
- ✅ **AGREE** - Zencoder is mostly correct, minor nuances
- ⚠️ **PARTIALLY AGREE** - Zencoder is partially correct, but missing context
- ❌ **DISAGREE** - Zencoder's finding is incorrect or overstated
- ❓ **NEEDS MORE INFO** - Cannot determine without additional context

**B. Reasoning:**
- Why you agree/disagree
- What Zencoder got right/wrong
- What context might be missing
- What additional considerations exist

**C. Security Impact:**
- Actual risk level (Critical/High/Medium/Low)
- Real-world exploitability
- Impact if not fixed

### 2. FIXES VALIDATION

For each fix applied, assess:

**A. Fix Correctness:**
- ✅ **CORRECT** - Fix addresses the issue properly
- ⚠️ **PARTIALLY CORRECT** - Fix helps but incomplete
- ❌ **INCORRECT** - Fix doesn't address issue or introduces new problems

**B. Code Quality:**
- Follows best practices?
- Proper error handling?
- Security implications?
- Edge cases covered?

**C. Production Readiness:**
- Ready for deployment?
- Needs testing?
- Additional improvements needed?

### 3. REMAINING ISSUES ANALYSIS

For remaining medium/low priority issues:

**A. Priority Assessment:**
- Should priority be higher/lower?
- Actual business impact?
- Risk if deferred?

**B. Implementation Recommendations:**
- Best approach to fix?
- Dependencies?
- Testing requirements?

### 4. NEXT STEPS RECOMMENDATIONS

Evaluate the 5 next-step options:

**A. Option 1 (Verify Fixes):**
- Is this the right first step?
- What should be verified?
- Additional verification needed?

**B. Option 2 (Implement Medium Fixes):**
- Which fixes should be prioritized?
- Implementation order?
- Risk assessment?

**C. Option 3 (Deploy Keys):**
- Is deployment ready?
- Prerequisites?
- Risk mitigation?

**D. Option 4 (Documentation):**
- What documentation is critical?
- Missing documentation?
- Quality standards?

**E. Option 5 (Comprehensive):**
- Is this approach recommended?
- Timeline realistic?
- Resource requirements?

---

## OUTPUT FORMAT

Provide your analysis in structured JSON format:

```json
{{
    "review_metadata": {{
        "reviewer": "GPT-4.1 Multi-Agent System",
        "review_date": "{datetime.now().isoformat()}",
        "zencoder_review_date": "2025-11-24",
        "agents_used": ["skeptical_reviewer", "security_sentinel", "ruthless_optimizer", "docstring_guru"],
        "overall_agreement_score": 0.0-1.0
    }},
    "zencoder_findings_validation": [
        {{
            "finding_id": "CRITICAL-1",
            "finding_title": "Windows SSH Key Deployment",
            "zencoder_severity": "CRITICAL",
            "gpt41_agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE|NEEDS_MORE_INFO",
            "agreement_score": 0.0-1.0,
            "reasoning": "Detailed explanation",
            "security_impact": "CRITICAL|HIGH|MEDIUM|LOW",
            "exploitability": "High|Medium|Low",
            "agent_consensus": {{
                "skeptical_reviewer": "AGREE|DISAGREE",
                "security_sentinel": "AGREE|DISAGREE",
                "ruthless_optimizer": "AGREE|DISAGREE",
                "docstring_guru": "AGREE|DISAGREE"
            }},
            "additional_considerations": "Any additional context or concerns"
        }}
    ],
    "fixes_validation": [
        {{
            "fix_id": "FIX-1",
            "fix_title": "Windows SSH Command Fix",
            "fix_correctness": "CORRECT|PARTIALLY_CORRECT|INCORRECT",
            "code_quality": "EXCELLENT|GOOD|FAIR|POOR",
            "production_ready": true|false,
            "testing_required": true|false,
            "additional_improvements": "Suggestions",
            "agent_consensus": {{...}}
        }}
    ],
    "remaining_issues_analysis": [
        {{
            "issue_id": "MEDIUM-1",
            "issue_title": "Key Rotation Schedule",
            "current_priority": "MEDIUM",
            "recommended_priority": "HIGH|MEDIUM|LOW",
            "business_impact": "High|Medium|Low",
            "implementation_recommendations": "Detailed approach",
            "dependencies": ["list"],
            "testing_requirements": "What needs testing"
        }}
    ],
    "review_agent_comparison": {{
        "review_agent_agreement": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE",
        "review_agent_concerns_valid": true|false,
        "score_discrepancies_analysis": {{
            "code_quality": {{
                "code_agent_score": 95,
                "review_agent_score": 92,
                "gpt41_assessment": "Which is more accurate?",
                "reasoning": "Why"
            }},
            "test_coverage": {{
                "code_agent_score": 90,
                "review_agent_score": 70,
                "gpt41_assessment": "Which is more accurate?",
                "reasoning": "Why"
            }},
            "overall_score": {{
                "code_agent_score": 95,
                "review_agent_score": 93,
                "gpt41_assessment": "Which is more accurate?",
                "reasoning": "Why"
            }},
            "readiness": {{
                "code_agent_percentage": 95,
                "review_agent_percentage": 80,
                "gpt41_assessment": "Which is more accurate?",
                "reasoning": "Why"
            }}
        }},
        "deployment_recommendation_comparison": {{
            "code_agent_recommendation": "GO FOR IMMEDIATE PRODUCTION DEPLOYMENT",
            "review_agent_recommendation": "GO WITH CONDITIONS",
            "gpt41_recommendation": "GO|NO-GO|GO_WITH_CONDITIONS",
            "gpt41_reasoning": "Why",
            "which_agent_correct": "CODE_AGENT|REVIEW_AGENT|BOTH|NEITHER",
            "final_recommendation": "GO|NO-GO|GO_WITH_CONDITIONS"
        }},
        "critical_issues_validation": {{
            "no_actual_testing": {{
                "review_agent_concern": "No actual testing performed",
                "gpt41_assessment": "VALID|INVALID|PARTIALLY_VALID",
                "should_block_deployment": true|false,
                "reasoning": "Why"
            }},
            "windows_deployment_untested": {{
                "review_agent_concern": "Windows deployment untested",
                "gpt41_assessment": "VALID|INVALID|PARTIALLY_VALID",
                "should_block_deployment": true|false,
                "reasoning": "Why"
            }},
            "missing_preflight_checks": {{
                "review_agent_concern": "Missing pre-flight checks",
                "gpt41_assessment": "VALID|INVALID|PARTIALLY_VALID",
                "should_block_deployment": true|false,
                "reasoning": "Why"
            }}
        }}
    }},
    "comprehensive_completion_validation": {{
        "phase_completion_assessment": {{
            "phase_1_status": "COMPLETE|INCOMPLETE|NEEDS_REVIEW",
            "phase_2_status": "COMPLETE|INCOMPLETE|NEEDS_REVIEW",
            "phase_3_status": "COMPLETE|INCOMPLETE|NEEDS_REVIEW",
            "phase_4_status": "COMPLETE|INCOMPLETE|NEEDS_REVIEW",
            "phase_5_status": "COMPLETE|INCOMPLETE|NEEDS_REVIEW",
            "overall_completion": true|false,
            "missing_components": ["list of any missing items"]
        }},
        "changes_validation": {{
            "modified_files_quality": "EXCELLENT|GOOD|FAIR|POOR",
            "new_files_quality": "EXCELLENT|GOOD|FAIR|POOR",
            "code_additions_quality": "EXCELLENT|GOOD|FAIR|POOR",
            "documentation_quality": "EXCELLENT|GOOD|FAIR|POOR",
            "issues_found": ["list of any issues"]
        }},
        "quality_metrics_validation": {{
            "code_quality_score_accurate": true|false,
            "documentation_score_accurate": true|false,
            "security_score_accurate": true|false,
            "test_coverage_accurate": true|false,
            "overall_score_accurate": true|false,
            "recommended_adjustments": {{"metric": "adjusted_score"}}
        }},
        "deployment_readiness_validation": {{
            "readiness_percentage_accurate": true|false,
            "risk_assessment_accurate": true|false,
            "go_for_deployment_recommendation": "STRONGLY_AGREE|AGREE|PARTIALLY_AGREE|DISAGREE",
            "blocking_issues_remaining": ["list"],
            "deployment_timeline_realistic": true|false,
            "monitoring_period_appropriate": true|false
        }},
        "documentation_validation": {{
            "troubleshooting_guide_quality": "EXCELLENT|GOOD|FAIR|POOR",
            "security_checklist_quality": "EXCELLENT|GOOD|FAIR|POOR",
            "completeness": "COMPLETE|MOSTLY_COMPLETE|INCOMPLETE",
            "missing_sections": ["list"]
        }}
    }},
    "next_steps_recommendations": {{
        "recommended_sequence": ["Option 1", "Option 2", ...],
        "option_1_analysis": {{
            "recommended": true|false,
            "reasoning": "...",
            "additional_verification": ["list"]
        }},
        "option_2_analysis": {{...}},
        "option_3_analysis": {{...}},
        "option_4_analysis": {{...}},
        "option_5_analysis": {{...}},
        "post_completion_recommendations": {{
            "immediate_actions": ["list"],
            "pre_deployment_checks": ["list"],
            "deployment_sequence": ["step 1", "step 2", ...],
            "post_deployment_monitoring": ["list"]
        }}
    }},
    "overall_assessment": {{
        "zencoder_review_quality": "EXCELLENT|GOOD|FAIR|POOR",
        "fixes_quality": "EXCELLENT|GOOD|FAIR|POOR",
        "production_readiness": "READY|NEEDS_WORK|NOT_READY",
        "recommended_actions": ["Prioritized list"],
        "risk_assessment": "LOW|MEDIUM|HIGH|CRITICAL",
        "timeline_recommendation": "X weeks"
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

- **Functional QA**: 20 pts - Verify all findings are accurate
- **Documentation**: 20 pts - Comprehensive, clear analysis
- **Security & Safety**: 15 pts - Identify all security implications
- **Efficiency**: 15 pts - Prioritize effectively
- **AI Learning**: 15 pts - Learn from Zencoder's approach
- **Innovation**: 15 pts - Suggest improvements beyond fixes

**Strive to exceed expectations and provide world-class analysis.**

---

Provide your comprehensive analysis now.
"""
    return prompt


def call_azure_openai(client: AzureOpenAI, prompt: str, max_tokens: int = 8000) -> Optional[str]:
    """
    Call Azure OpenAI API with comprehensive error handling.
    
    Args:
        client: Azure OpenAI client instance
        prompt: Prompt to send
        max_tokens: Maximum tokens in response
        
    Returns:
        Response content or None if error
    """
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
            temperature=0.3,  # Lower temperature for more consistent, analytical responses
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
    """
    Parse JSON response from GPT-4.1, handling markdown code blocks.
    
    Args:
        response: Raw response string
        
    Returns:
        Parsed JSON dict or None if error
    """
    try:
        # Remove markdown code blocks if present
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            response = response[start:end].strip()
        elif "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            response = response[start:end].strip()
        
        return json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parsing error: {e}")
        logger.error(f"   Response preview: {response[:500]}")
        return None


def generate_markdown_report(analysis: Dict) -> str:
    """
    Generate comprehensive markdown report from analysis.
    
    Args:
        analysis: Parsed JSON analysis from GPT-4.1
        
    Returns:
        Formatted markdown report
    """
    report = f"""# GPT-4.1 VM101 Security Review Validation

**Review Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
**Reviewer:** GPT-4.1 Multi-Agent System  
**Zencoder Review Date:** 2025-11-24  
**Status:** ✅ Complete

---

## 📊 EXECUTIVE SUMMARY

**Overall Agreement Score:** {analysis.get('review_metadata', {}).get('overall_agreement_score', 'N/A')}/1.0

**Zencoder Review Quality:** {analysis.get('overall_assessment', {}).get('zencoder_review_quality', 'N/A')}  
**Fixes Quality:** {analysis.get('overall_assessment', {}).get('fixes_quality', 'N/A')}  
**Production Readiness:** {analysis.get('overall_assessment', {}).get('production_readiness', 'N/A')}  
**Risk Assessment:** {analysis.get('overall_assessment', {}).get('risk_assessment', 'N/A')}

---

## 🔍 ZENCODER FINDINGS VALIDATION

"""
    
    # Add findings validation
    for finding in analysis.get('zencoder_findings_validation', []):
        agreement = finding.get('gpt41_agreement', 'UNKNOWN')
        emoji = "✅" if "AGREE" in agreement else "⚠️" if "PARTIALLY" in agreement else "❌"
        
        report += f"""### {emoji} {finding.get('finding_title', 'Unknown')}

**Finding ID:** {finding.get('finding_id', 'N/A')}  
**Zencoder Severity:** {finding.get('zencoder_severity', 'N/A')}  
**GPT-4.1 Agreement:** **{agreement}** (Score: {finding.get('agreement_score', 'N/A')})  
**Security Impact:** {finding.get('security_impact', 'N/A')}  
**Exploitability:** {finding.get('exploitability', 'N/A')}

**Reasoning:**
{finding.get('reasoning', 'No reasoning provided')}

**Agent Consensus:**
- Skeptical Reviewer: {finding.get('agent_consensus', {}).get('skeptical_reviewer', 'N/A')}
- Security Sentinel: {finding.get('agent_consensus', {}).get('security_sentinel', 'N/A')}
- Ruthless Optimizer: {finding.get('agent_consensus', {}).get('ruthless_optimizer', 'N/A')}
- Docstring Guru: {finding.get('agent_consensus', {}).get('docstring_guru', 'N/A')}

**Additional Considerations:**
{finding.get('additional_considerations', 'None')}

---

"""
    
    # Add fixes validation
    report += """## ✅ FIXES VALIDATION

"""
    
    for fix in analysis.get('fixes_validation', []):
        correctness = fix.get('fix_correctness', 'UNKNOWN')
        emoji = "✅" if correctness == "CORRECT" else "⚠️" if "PARTIALLY" in correctness else "❌"
        
        report += f"""### {emoji} {fix.get('fix_title', 'Unknown')}

**Fix ID:** {fix.get('fix_id', 'N/A')}  
**Correctness:** **{correctness}**  
**Code Quality:** {fix.get('code_quality', 'N/A')}  
**Production Ready:** {'✅ Yes' if fix.get('production_ready') else '❌ No'}  
**Testing Required:** {'⚠️ Yes' if fix.get('testing_required') else '✅ No'}

**Additional Improvements:**
{fix.get('additional_improvements', 'None')}

---

"""
    
    # Add remaining issues
    report += """## ⏳ REMAINING ISSUES ANALYSIS

"""
    
    for issue in analysis.get('remaining_issues_analysis', []):
        current_prio = issue.get('current_priority', 'N/A')
        recommended_prio = issue.get('recommended_priority', 'N/A')
        priority_change = "⬆️" if recommended_prio > current_prio else "⬇️" if recommended_prio < current_prio else "➡️"
        
        report += f"""### {priority_change} {issue.get('issue_title', 'Unknown')}

**Current Priority:** {current_prio}  
**Recommended Priority:** {recommended_prio}  
**Business Impact:** {issue.get('business_impact', 'N/A')}

**Implementation Recommendations:**
{issue.get('implementation_recommendations', 'None')}

**Dependencies:** {', '.join(issue.get('dependencies', [])) or 'None'}

---

"""
    
    # Add next steps
    report += f"""## 🚀 NEXT STEPS RECOMMENDATIONS

**Recommended Sequence:** {' → '.join(analysis.get('next_steps_recommendations', {}).get('recommended_sequence', []))}

"""
    
    for option_num in range(1, 6):
        option_key = f"option_{option_num}_analysis"
        option_data = analysis.get('next_steps_recommendations', {}).get(option_key, {})
        if option_data:
            recommended = "✅ RECOMMENDED" if option_data.get('recommended') else "❌ NOT RECOMMENDED"
            report += f"""### Option {option_num}: {recommended}

**Reasoning:**
{option_data.get('reasoning', 'No reasoning provided')}

**Additional Verification:**
{', '.join(option_data.get('additional_verification', [])) or 'None'}

---

"""
    
    # Add Review Agent comparison
    review_agent_comp = analysis.get('review_agent_comparison', {})
    if review_agent_comp:
        report += """## 🔍 REVIEW AGENT vs CODE AGENT COMPARISON

"""
        
        deployment_comp = review_agent_comp.get('deployment_recommendation_comparison', {})
        report += f"""### Deployment Recommendation Comparison

**Code Agent:** GO FOR IMMEDIATE PRODUCTION DEPLOYMENT  
**Review Agent:** GO WITH CONDITIONS (after 2-3 hours testing)  
**GPT-4.1 Recommendation:** **{deployment_comp.get('gpt41_recommendation', 'N/A')}**

**Which Agent is Correct:** {deployment_comp.get('which_agent_correct', 'N/A')}

**GPT-4.1 Reasoning:**
{deployment_comp.get('gpt41_reasoning', 'No reasoning provided')}

---

"""
        
        score_analysis = review_agent_comp.get('score_discrepancies_analysis', {})
        if score_analysis:
            report += """### Score Discrepancies Analysis

"""
            
            for metric, data in score_analysis.items():
                code_score = data.get('code_agent_score', 'N/A')
                review_score = data.get('review_agent_score', 'N/A')
                gpt41_assessment = data.get('gpt41_assessment', 'N/A')
                
                report += f"""**{metric.replace('_', ' ').title()}:**
- Code Agent: {code_score}
- Review Agent: {review_score}
- GPT-4.1 Assessment: {gpt41_assessment}
- Reasoning: {data.get('reasoning', 'No reasoning provided')}

"""
        
        critical_issues = review_agent_comp.get('critical_issues_validation', {})
        if critical_issues:
            report += """### Critical Issues Validation

"""
            
            for issue_name, issue_data in critical_issues.items():
                concern = issue_data.get('review_agent_concern', 'N/A')
                assessment = issue_data.get('gpt41_assessment', 'N/A')
                blocks = '✅ YES' if issue_data.get('should_block_deployment') else '❌ NO'
                
                report += f"""**{issue_name.replace('_', ' ').title()}:**
- Review Agent Concern: {concern}
- GPT-4.1 Assessment: {assessment}
- Should Block Deployment: {blocks}
- Reasoning: {issue_data.get('reasoning', 'No reasoning provided')}

"""
        
        report += "---\n\n"
    
    # Add comprehensive completion validation
    completion_validation = analysis.get('comprehensive_completion_validation', {})
    if completion_validation:
        report += """## ✅ COMPREHENSIVE COMPLETION VALIDATION

"""
        
        # Phase completion assessment
        phase_assessment = completion_validation.get('phase_completion_assessment', {})
        report += f"""### Phase Completion Assessment

**All Phases Complete:** {'✅ Yes' if phase_assessment.get('overall_completion') else '❌ No'}

**Phase Status:**
- Phase 1 (Verify Fixes): {phase_assessment.get('phase_1_status', 'N/A')}
- Phase 2 (Implement Medium Fixes): {phase_assessment.get('phase_2_status', 'N/A')}
- Phase 3 (SSH Deployment Assessment): {phase_assessment.get('phase_3_status', 'N/A')}
- Phase 4 (Create Documentation): {phase_assessment.get('phase_4_status', 'N/A')}
- Phase 5 (Deployment Readiness): {phase_assessment.get('phase_5_status', 'N/A')}

**Missing Components:**
{', '.join(phase_assessment.get('missing_components', [])) or 'None'}

---

"""
        
        # Changes validation
        changes_validation = completion_validation.get('changes_validation', {})
        report += f"""### Changes Validation

**Modified Files Quality:** {changes_validation.get('modified_files_quality', 'N/A')}  
**New Files Quality:** {changes_validation.get('new_files_quality', 'N/A')}  
**Code Additions Quality:** {changes_validation.get('code_additions_quality', 'N/A')}  
**Documentation Quality:** {changes_validation.get('documentation_quality', 'N/A')}

**Issues Found:**
{', '.join(changes_validation.get('issues_found', [])) or 'None'}

---

"""
        
        # Quality metrics validation
        quality_metrics = completion_validation.get('quality_metrics_validation', {})
        report += f"""### Quality Metrics Validation

**Code Quality Score Accurate:** {'✅ Yes' if quality_metrics.get('code_quality_score_accurate') else '❌ No'}  
**Documentation Score Accurate:** {'✅ Yes' if quality_metrics.get('documentation_score_accurate') else '❌ No'}  
**Security Score Accurate:** {'✅ Yes' if quality_metrics.get('security_score_accurate') else '❌ No'}  
**Test Coverage Accurate:** {'✅ Yes' if quality_metrics.get('test_coverage_accurate') else '❌ No'}  
**Overall Score Accurate:** {'✅ Yes' if quality_metrics.get('overall_score_accurate') else '❌ No'}

**Recommended Adjustments:**
{json.dumps(quality_metrics.get('recommended_adjustments', {}), indent=2) if quality_metrics.get('recommended_adjustments') else 'None'}

---

"""
        
        # Deployment readiness validation
        deployment_validation = completion_validation.get('deployment_readiness_validation', {})
        report += f"""### Deployment Readiness Validation

**Readiness Percentage Accurate:** {'✅ Yes' if deployment_validation.get('readiness_percentage_accurate') else '❌ No'}  
**Risk Assessment Accurate:** {'✅ Yes' if deployment_validation.get('risk_assessment_accurate') else '❌ No'}  
**Go for Deployment Recommendation:** **{deployment_validation.get('go_for_deployment_recommendation', 'N/A')}**  
**Deployment Timeline Realistic:** {'✅ Yes' if deployment_validation.get('deployment_timeline_realistic') else '❌ No'}  
**Monitoring Period Appropriate:** {'✅ Yes' if deployment_validation.get('monitoring_period_appropriate') else '❌ No'}

**Blocking Issues Remaining:**
{', '.join(deployment_validation.get('blocking_issues_remaining', [])) or 'None'}

---

"""
        
        # Documentation validation
        doc_validation = completion_validation.get('documentation_validation', {})
        report += f"""### Documentation Validation

**Troubleshooting Guide Quality:** {doc_validation.get('troubleshooting_guide_quality', 'N/A')}  
**Security Checklist Quality:** {doc_validation.get('security_checklist_quality', 'N/A')}  
**Completeness:** {doc_validation.get('completeness', 'N/A')}

**Missing Sections:**
{', '.join(doc_validation.get('missing_sections', [])) or 'None'}

---

"""
    
    # Add overall assessment
    overall = analysis.get('overall_assessment', {})
    report += f"""## 📋 OVERALL ASSESSMENT

**Zencoder Review Quality:** {overall.get('zencoder_review_quality', 'N/A')}  
**Fixes Quality:** {overall.get('fixes_quality', 'N/A')}  
**Production Readiness:** {overall.get('production_readiness', 'N/A')}  
**Risk Assessment:** {overall.get('risk_assessment', 'N/A')}  
**Timeline Recommendation:** {overall.get('timeline_recommendation', 'N/A')}

**Recommended Actions:**
"""
    
    for i, action in enumerate(overall.get('recommended_actions', []), 1):
        report += f"{i}. {action}\n"
    
    # Add post-completion recommendations if available
    post_completion = analysis.get('next_steps_recommendations', {}).get('post_completion_recommendations', {})
    if post_completion:
        report += "\n---\n\n"
        report += """## 🚀 POST-COMPLETION RECOMMENDATIONS

**Immediate Actions:**
"""
        for i, action in enumerate(post_completion.get('immediate_actions', []), 1):
            report += f"{i}. {action}\n"
        
        report += "\n**Pre-Deployment Checks:**\n"
        for i, check in enumerate(post_completion.get('pre_deployment_checks', []), 1):
            report += f"{i}. {check}\n"
        
        report += "\n**Deployment Sequence:**\n"
        for i, step in enumerate(post_completion.get('deployment_sequence', []), 1):
            report += f"{i}. {step}\n"
        
        report += "\n**Post-Deployment Monitoring:**\n"
        for i, monitor in enumerate(post_completion.get('post_deployment_monitoring', []), 1):
            report += f"{i}. {monitor}\n"
    
    report += "\n---\n\n"
    
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
**Quality Score:** TBD (100/10 mindset)
"""
    
    return report


def main():
    """
    Main execution function.
    
    Orchestrates the complete review process:
    1. Initialize Azure OpenAI client
    2. Read all relevant files
    3. Create comprehensive prompt
    4. Call GPT-4.1 for analysis
    5. Parse and validate response
    6. Generate markdown report
    7. Save outputs
    """
    logger.info("=" * 80)
    logger.info("VM101 Zencoder Review + GPT-4.1 Validation")
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
    
    # Read files
    logger.info("\n📖 Reading files...")
    zencoder_review = read_file_content(ZENCODER_REVIEW)
    fixes_applied = read_file_content(FIXES_APPLIED)
    script_content = read_file_content(SEPARATE_KEYS_SCRIPT)
    next_steps = read_file_content(NEXT_STEPS)
    
    # Read comprehensive completion files (optional but recommended)
    change_log = read_file_content(COMPREHENSIVE_CHANGE_LOG)
    troubleshooting = read_file_content(SSH_TROUBLESHOOTING)
    security_checklist = read_file_content(SECURITY_CHECKLIST)
    key_migration = read_file_content(KEY_MIGRATION_GUIDE)
    control_node_security = read_file_content(CONTROL_NODE_SECURITY)
    review_agent_report = read_file_content(REVIEW_AGENT_REPORT)
    
    if not all([zencoder_review, fixes_applied, script_content]):
        logger.error("❌ Missing required files!")
        return 1
    
    # Warn if comprehensive files missing
    if not change_log:
        logger.warning("⚠️  Comprehensive change log not found - review will be limited")
    if not troubleshooting:
        logger.warning("⚠️  Troubleshooting guide not found")
    if not security_checklist:
        logger.warning("⚠️  Security checklist not found")
    if not review_agent_report:
        logger.warning("⚠️  Review Agent validation report not found - will miss Review Agent vs Code Agent comparison")
    
    # Create prompt
    logger.info("\n📝 Creating review prompt...")
    prompt = create_review_prompt(
        zencoder_review or "",
        fixes_applied or "",
        script_content or "",
        next_steps or "",
        change_log=change_log,
        troubleshooting=troubleshooting,
        security_checklist=security_checklist,
        key_migration=key_migration,
        control_node_security=control_node_security,
        review_agent_report=review_agent_report
    )
    
    # Call Azure OpenAI
    logger.info("\n🤖 Calling GPT-4.1 for analysis...")
    response = call_azure_openai(client, prompt, max_tokens=8000)
    
    if not response:
        logger.error("❌ No response from Azure OpenAI")
        return 1
    
    # Parse response
    logger.info("\n🔍 Parsing response...")
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
    logger.info("\n📄 Generating markdown report...")
    report = generate_markdown_report(analysis)
    
    # Save report
    logger.info(f"\n[SAVE] Saving report to {REPORT_OUTPUT}")
    with open(REPORT_OUTPUT, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Summary
    logger.info("\n" + "=" * 80)
    logger.info("✅ REVIEW COMPLETE")
    logger.info("=" * 80)
    logger.info(f"📊 JSON Analysis: {REVIEW_OUTPUT}")
    logger.info(f"📄 Markdown Report: {REPORT_OUTPUT}")
    logger.info(f"📝 Log File: {OUTPUT_DIR / 'vm101_review.log'}")
    
    # Print key findings
    overall = analysis.get('overall_assessment', {})
    completion_validation = analysis.get('comprehensive_completion_validation', {})
    
    logger.info(f"\n🎯 Key Findings:")
    logger.info(f"   Agreement Score: {analysis.get('review_metadata', {}).get('overall_agreement_score', 'N/A')}")
    logger.info(f"   Production Ready: {overall.get('production_readiness', 'N/A')}")
    logger.info(f"   Risk Level: {overall.get('risk_assessment', 'N/A')}")
    
    # Print completion validation
    if completion_validation:
        phase_assessment = completion_validation.get('phase_completion_assessment', {})
        deployment_validation = completion_validation.get('deployment_readiness_validation', {})
        
        logger.info(f"\n✅ Comprehensive Completion Validation:")
        logger.info(f"   All Phases Complete: {phase_assessment.get('overall_completion', 'N/A')}")
        logger.info(f"   Deployment Recommendation: {deployment_validation.get('go_for_deployment_recommendation', 'N/A')}")
        logger.info(f"   Readiness Accurate: {deployment_validation.get('readiness_percentage_accurate', 'N/A')}")
        
        quality_metrics = completion_validation.get('quality_metrics_validation', {})
        logger.info(f"   Quality Metrics Accurate: {quality_metrics.get('overall_score_accurate', 'N/A')}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

