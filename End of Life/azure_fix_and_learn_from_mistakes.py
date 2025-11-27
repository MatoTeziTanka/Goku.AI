#!/usr/bin/env python3
"""
Azure API: Fix All Issues and Learn From Mistakes

This script asks Azure GPT-4.1 to:
1. Fix all issues identified by Zencoder (14 issues + 4 additional)
2. Explain why the original script had these problems
3. Provide recommendations for better prompting in the future
4. Generate a corrected, production-ready script

All with comprehensive logging, security-first approach, and QC framework adherence.
"""

import os
import sys
import json
import io
from pathlib import Path
from datetime import datetime
from openai import AzureOpenAI

# Windows Unicode fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Base directory
BASE_DIR = Path(r"C:\Users\sethp\Documents\Github")

# Azure OpenAI Configuration
AZURE_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
AZURE_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1")

# If not in environment, try reading from config files
if not AZURE_ENDPOINT or not AZURE_API_KEY:
    config_file = BASE_DIR / "api_keys_config.json"
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                azure_config = config.get("azure", {})
                if not AZURE_ENDPOINT:
                    endpoint = azure_config.get("endpoint", "")
                    if endpoint:
                        if "cognitiveservices.azure.com" in endpoint:
                            endpoint = endpoint.replace("cognitiveservices.azure.com", "openai.azure.com")
                        if not endpoint.startswith("http"):
                            AZURE_ENDPOINT = f"https://{endpoint}/"
                        else:
                            AZURE_ENDPOINT = endpoint
                if not AZURE_API_KEY:
                    AZURE_API_KEY = azure_config.get("api_key", "")
        except Exception as e:
            print(f"Warning: Could not read config file: {e}")

# Validate Azure configuration
if not AZURE_ENDPOINT or not AZURE_API_KEY:
    print("ERROR: Azure OpenAI configuration not found.")
    print("Please set AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY environment variables,")
    print("or configure them in api_keys_config.json")
    sys.exit(1)

# Initialize Azure OpenAI client
try:
    client = AzureOpenAI(
        api_key=AZURE_API_KEY,
        api_version=AZURE_API_VERSION,
        azure_endpoint=AZURE_ENDPOINT
    )
except Exception as e:
    print(f"ERROR: Failed to initialize Azure OpenAI client: {e}")
    sys.exit(1)

# Repositories
REPOSITORIES = [
    "BitPhoenix", "Dell-Server-Roadmap", "Dino-Cloud", "DinoCloud",
    "FamilyFork", "GSMG.IO", "Goku.AI", "Keyhound", "Scalpstorm",
    "Server-Roadmap", "StreamForge"
]

# QC Framework
QC_FRAMEWORK = """
## QC Control Framework (100/10 Mindset)

### Scoring Categories (Total: 100 points)

1. **Functional QA** (20 pts)
   - All code executes without errors
   - All scripts are functional and tested
   - All deliverables are complete and usable
   - Comprehensive testing coverage

2. **Documentation & Comment Quality** (20 pts)
   - Comprehensive documentation
   - Clear explanations of why, not what
   - Proper logging and audit trails
   - All decisions documented
   - Inline comments, docstrings, block comments

3. **Security & Safety** (15 pts)
   - Zero security issues
   - No secrets or credentials exposed
   - Security best practices followed
   - Proper access controls
   - Dependency vulnerability scanning

4. **Efficiency / Optimization** (15 pts)
   - Batch automation, not manual work
   - Efficient execution
   - Proper resource usage
   - Scalable solutions
   - Pre-commit hooks, CI/CD optimization

5. **AI Learning & Adaptation** (15 pts)
   - Learning from execution
   - Adaptive improvements
   - Knowledge capture
   - Continuous improvement
   - Self-updating documentation

6. **Innovation & Impact** (15 pts)
   - Innovative solutions
   - World-class impact
   - Exceeds expectations
   - Strategic thinking
   - Transformative improvements
"""


def read_file_content(file_path, max_chars=15000):
    """Read file content, return None if file doesn't exist"""
    full_path = BASE_DIR / file_path
    if full_path.exists():
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if len(content) > max_chars:
                    return content[:max_chars] + f"\n\n[File truncated - showing first {max_chars} characters of {len(content)} total]"
                return content
        except Exception as e:
            return f"Error reading file: {e}"
    return None


def build_fix_and_learn_prompt():
    """Build comprehensive prompt for fixing issues and learning"""
    
    # Read all relevant files
    original_script = read_file_content("azure_100_percent_qc_improvement.py", 20000)
    zencoder_findings = read_file_content("AZURE_REVIEW_ZENCODER_FINDINGS_20251126_011753.md", 10000)
    original_generator = read_file_content("azure_generate_100_percent_improvement_script.py", 10000)
    azure_review = read_file_content("AZURE_REVIEW_COMPLETE_PROJECT_20251126_010222.md", 5000)
    
    prompt = f"""You are an expert Python developer and quality assurance specialist. You previously generated a script (`azure_100_percent_qc_improvement.py`) that had 18 issues identified by Zencoder (14 original + 4 additional).

## CONTEXT: WHAT WENT WRONG

### Original Generation Process
1. **Input Script:** `azure_generate_100_percent_improvement_script.py` - This script called Azure API to generate the improvement script
2. **Output Script:** `azure_100_percent_qc_improvement.py` - The generated script with issues
3. **Review:** Zencoder reviewed the output and found 18 issues
4. **Validation:** Azure API reviewed Zencoder's findings and FULLY AGREED with all 18 issues

### Issues Found (18 total)

**Critical (4):**
1. Incomplete Implementation - Functions called but not defined
2. Dangerous File Operations - shutil.rmtree() without verification
3. Repository Path Issue - Hard-coded path assumption
4. Security Scanning Incomplete - Missing function, weak regex

**Major (5):**
5. Unhandled Edge Cases - Path handling issues
6. Logging Performance Issue - O(n) complexity per log
7. Assumed Test Execution - Tests not actually run
8. No Error Recovery - Processes all repos even if one fails
9. Missing Implementations in Verification - Checks for files that don't exist

**Code Quality (5):**
10. Duplicate File Header
11. Missing Type Hints
12. Hard-coded Values
13. No Unit Tests
14. Insufficient Error Handling

**Additional (4):**
15. No Dependency Pinning
16. No Dry-run Coverage for All Operations
17. No Atomic File Writes
18. No Output Validation

### Original Generated Script

{original_script[:10000] if original_script else "[Script not found]"}

### Zencoder's Review

{zencoder_findings[:8000] if zencoder_findings else "[Review not found]"}

### Original Generator Script (What We Asked For)

{original_generator[:8000] if original_generator else "[Generator not found]"}

---

## YOUR TASK: THREE PARTS

### PART 1: EXPLAIN WHAT WENT WRONG

Analyze why the original generation created these problems:

1. **What was wrong with the original prompt?**
   - What specific aspects of the prompt led to incomplete implementations?
   - Why were security checks incomplete?
   - Why were dangerous operations not properly guarded?
   - What assumptions were made that shouldn't have been?

2. **What was missing from the requirements?**
   - What should have been explicitly stated but wasn't?
   - What implicit requirements were not communicated?
   - What validation steps should have been requested?

3. **What could have been better in the prompt structure?**
   - How should the prompt have been organized?
   - What examples should have been provided?
   - What constraints should have been emphasized?

### PART 2: PROVIDE BETTER PROMPTING RECOMMENDATIONS

Based on the mistakes, provide specific recommendations for future prompts:

1. **Prompt Structure Recommendations**
   - How to structure prompts for code generation
   - What sections to include
   - What order to present information

2. **Specific Phrasing Recommendations**
   - How to word requirements to avoid incomplete implementations
   - How to emphasize security requirements
   - How to request comprehensive error handling
   - How to ensure all functions are implemented

3. **Validation Requirements**
   - What validation steps to request
   - How to ensure completeness
   - How to verify security

4. **Example Improved Prompt Sections**
   - Show before/after examples
   - Demonstrate better phrasing
   - Provide templates for future use

### PART 3: GENERATE FIXED SCRIPT

Create a COMPLETE, PRODUCTION-READY script that:

1. **Fixes ALL 18 Issues**
   - Implements all missing functions
   - Adds security validation
   - Fixes path handling
   - Implements proper error recovery
   - Adds comprehensive logging
   - Includes all type hints
   - Removes duplicate headers
   - Makes paths configurable
   - Adds dependency pinning
   - Implements atomic writes
   - Adds output validation
   - Actually runs tests

2. **Comprehensive Logging (WHO/WHAT/WHERE/WHEN/WHY)**
   - Every action logged with:
     - WHO: Function/agent name
     - WHAT: Action performed
     - WHERE: File path
     - WHEN: Timestamp
     - WHY: Reason for action (which QC category, which recommendation)
   - Structured logging (JSON format)
   - Performance-optimized (buffer and batch writes)
   - Complete audit trail

3. **Security-First Approach**
   - Scan all content for secrets before writing
   - Validate .env.example files use only placeholders
   - Use robust secret scanning (not just regex)
   - Add path validation and whitelisting
   - Require confirmation for destructive operations
   - Security audit after all changes

4. **Covers All 11 Repositories**
   - BitPhoenix, Dell-Server-Roadmap, Dino-Cloud, DinoCloud, FamilyFork, GSMG.IO, Goku.AI, Keyhound, Scalpstorm, Server-Roadmap, StreamForge
   - Configurable paths (CLI arguments or config file)
   - Validates repository existence
   - Handles consolidation (Server-Roadmap→Dell-Server-Roadmap, DinoCloud→Dino-Cloud)

5. **QC Framework Adherence**
   - Functional QA: All code tested, all functions implemented
   - Documentation: Comprehensive docstrings, inline comments explaining WHY
   - Security: Zero vulnerabilities, proper validation
   - Efficiency: Optimized logging, batch operations
   - AI Learning: Complete audit trail, learning documentation
   - Innovation: Best practices, transformative improvements

6. **Production-Ready Features**
   - Dry-run mode
   - Rollback capability
   - Error recovery
   - Atomic file writes
   - Output validation
   - Dependency pinning
   - Comprehensive error handling
   - Type hints throughout
   - Unit test structure
   - Cross-platform compatibility (pathlib.Path)

## OUTPUT FORMAT

Provide your response in this structure:

### 1. WHAT WENT WRONG ANALYSIS

[Detailed analysis of why the original generation had problems]

### 2. PROMPTING RECOMMENDATIONS

[Specific recommendations for better prompts in the future]

### 3. FIXED SCRIPT

[Complete, production-ready Python script with all fixes]

---

## REQUIREMENTS FOR FIXED SCRIPT

- File name: `azure_100_percent_qc_improvement_FIXED.py`
- All 18 issues fixed
- Comprehensive logging (who/what/where/when/why)
- Security-first approach
- Covers all 11 repositories
- QC framework adherence
- Production-ready
- Well-documented
- Type hints
- Error handling
- Testing structure

---

## QC FRAMEWORK

{QC_FRAMEWORK}

---

Generate the complete analysis, recommendations, and fixed script.
"""

    return prompt


def call_azure_api(prompt, max_retries=3):
    """Call Azure OpenAI API with retry logic"""
    for attempt in range(max_retries):
        try:
            print(f"  Attempt {attempt + 1}/{max_retries}...")
            sys.stdout.flush()
            
            response = client.chat.completions.create(
                model=AZURE_DEPLOYMENT,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert Python developer, quality assurance specialist, and prompt engineering expert. You analyze mistakes, learn from them, and create production-ready solutions. You always prioritize security, comprehensive logging, and QC framework adherence. You provide detailed explanations and actionable recommendations."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=16000
            )
            return response.choices[0].message.content
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 60
                print(f"Error calling Azure API (attempt {attempt + 1}/{max_retries}): {e}")
                print(f"Waiting {wait_time} seconds before retry...")
                sys.stdout.flush()
                import time
                time.sleep(wait_time)
            else:
                raise


def extract_script_from_response(response):
    """Extract Python script from response (handle markdown code blocks)"""
    if "```python" in response:
        start = response.find("```python") + 9
        end = response.find("```", start)
        if end > start:
            return response[start:end].strip()
    elif "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        if end > start:
            return response[start:end].strip()
    return None


def main():
    """Main execution function"""
    print("="*70)
    print("AZURE API: FIX ALL ISSUES AND LEARN FROM MISTAKES")
    print("="*70)
    print(f"\nExecution Date: {datetime.now().isoformat()}")
    print(f"Task: Fix 18 issues, explain mistakes, provide better prompting")
    print(f"Scope: All 11 repositories, comprehensive logging, security-first")
    print("\nBuilding comprehensive prompt...")
    
    # Check Azure configuration
    print(f"\nAzure Configuration:")
    print(f"  Endpoint: {AZURE_ENDPOINT[:50]}..." if AZURE_ENDPOINT else "  Endpoint: NOT SET")
    print(f"  API Key: {'SET' if AZURE_API_KEY else 'NOT SET'}")
    print(f"  Deployment: {AZURE_DEPLOYMENT}")
    
    if not AZURE_ENDPOINT or not AZURE_API_KEY:
        print("\nERROR: Azure configuration incomplete!")
        sys.exit(1)
    
    # Build prompt
    print("\nReading all relevant files...")
    print("  - Original generated script...")
    print("  - Zencoder's findings...")
    print("  - Original generator script...")
    print("  - Azure review...")
    
    prompt = build_fix_and_learn_prompt()
    print(f"Prompt built ({len(prompt)} characters)")
    
    print("\nCalling Azure GPT-4.1 API...")
    print("(This may take 5-8 minutes for comprehensive response...)\n")
    sys.stdout.flush()
    
    try:
        # Call Azure API
        print("Sending fix and learn request to Azure API...")
        sys.stdout.flush()
        response = call_azure_api(prompt)
        print(f"\nReceived response ({len(response)} characters)")
        sys.stdout.flush()
        
        # Extract script if present
        extracted_script = extract_script_from_response(response)
        
        # Create comprehensive document
        doc_file = BASE_DIR / f"AZURE_FIX_AND_LEARN_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        document = f"""# Azure API: Fix All Issues and Learn From Mistakes

**Generated:** {datetime.now().isoformat()}  
**Generator:** Azure GPT-4.1  
**Purpose:** Fix all 18 issues, explain mistakes, provide better prompting recommendations  
**Status:** Complete

---

## Review Metadata

- **WHO Generated:** Azure GPT-4.1 API
- **WHAT Generated:** Fixed script + mistake analysis + prompting recommendations
- **WHEN Generated:** {datetime.now().isoformat()}
- **WHERE Generated:** Azure OpenAI API endpoint
- **WHY Generated:** To fix all issues, learn from mistakes, and improve future prompts

---

## Issues Being Fixed

- **Total Issues:** 18 (14 original + 4 additional)
- **Critical Issues:** 4 (must fix)
- **Major Issues:** 5 (should fix)
- **Code Quality Issues:** 5 (nice to have)
- **Additional Issues:** 4 (Azure identified)

---

## Azure GPT-4.1 Response

{response}

---

## Extracted Script

"""
        
        if extracted_script:
            document += f"```python\n{extracted_script}\n```\n\n"
            document += "**Note:** Script extracted from response above. Save as `azure_100_percent_qc_improvement_FIXED.py`\n\n"
        else:
            document += "**Note:** Script may be embedded in the response above. Review and extract manually.\n\n"
        
        document += f"""---

## Next Steps

1. Review the "WHAT WENT WRONG" analysis
2. Review the "PROMPTING RECOMMENDATIONS"
3. Extract and save the fixed script
4. Review the fixed script thoroughly
5. Test in dry-run mode
6. Execute after approval

---

**Generated:** {datetime.now().isoformat()}  
**Status:** ✅ Complete
"""
        
        # Write document
        with open(doc_file, 'w', encoding='utf-8') as f:
            f.write(document)
        
        # If script was extracted, save it separately
        if extracted_script:
            script_file = BASE_DIR / "azure_100_percent_qc_improvement_FIXED.py"
            with open(script_file, 'w', encoding='utf-8') as f:
                f.write(extracted_script)
            print(f"\n✅ Fixed script saved to: {script_file.name}")
        
        print("="*70)
        print("FIX AND LEARN COMPLETE")
        print("="*70)
        print(f"\nDocument saved to: {doc_file.name}")
        print(f"\nResponse Preview:")
        print("-" * 70)
        print(response[:1000] + "..." if len(response) > 1000 else response)
        print("-" * 70)
        print(f"\nFull response available in: {doc_file.name}")
        
        return doc_file
        
    except Exception as e:
        print(f"\nERROR: Failed to complete fix and learn: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

