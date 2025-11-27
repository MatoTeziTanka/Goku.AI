#!/usr/bin/env python3
"""
Azure API: Generate 100/100 QC Improvement Script

This script uses Azure GPT-4.1 to generate a comprehensive Python script that will:
1. Address all Azure review recommendations
2. Achieve 100/100 QC score across all 11 repositories
3. Include comprehensive logging (who/what/where/when/why)
4. Double-check everything before completion
5. Maintain security and QC audit standards

The generated script will then be reviewed before execution.
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


def read_file_content(file_path, max_chars=5000):
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


def build_generation_prompt():
    """Build prompt for Azure to generate the improvement script"""
    
    # Read Azure review recommendations
    azure_review = read_file_content("AZURE_REVIEW_COMPLETE_PROJECT_20251126_010222.md", 10000)
    
    # Read current QC improvements
    qc_improvements = read_file_content("QC_SCORE_IMPROVEMENTS.md", 5000)
    
    # Read security audit
    security_audit = read_file_content("SECURITY_AUDIT_REPORT.md", 5000)
    
    prompt = f"""You are an expert Python developer and quality assurance specialist. Your task is to create a comprehensive Python script that will improve all 11 GitHub repositories to achieve 100/100 QC score.

## CONTEXT

### Current Status
- **Current QC Score:** 86/100 (Excellent)
- **Target QC Score:** 100/100 (100/10 Mindset)
- **Repositories:** 11 total
- **Current Issues:** See Azure review recommendations below

### Azure Review Recommendations

{azure_review}

### QC Framework

{QC_FRAMEWORK}

## REQUIREMENTS FOR THE GENERATED SCRIPT

### 1. Comprehensive Logging (MANDATORY)
The script MUST log EVERY action with:
- **WHO:** Which agent/function performed the action
- **WHAT:** What action was performed (file created, modified, deleted, etc.)
- **WHERE:** Full file path where action occurred
- **WHEN:** Timestamp of action
- **WHY:** Reason for the action (which recommendation, which QC category)

### 2. Double-Check Before Completion (MANDATORY)
- Verify all files were created/modified correctly
- Verify all security checks pass
- Verify all tests pass
- Verify all documentation is complete
- Verify all QC improvements are applied
- Generate final verification report

### 3. Security Requirements (MANDATORY)
- Scan all files for secrets before writing
- Verify .env.example files use only placeholders
- Run security scans after all changes
- Never commit secrets or credentials
- Validate all security policies

### 4. QC Improvements Required

#### Functional QA (20 pts) - Current: 17/20
- Fix encoding issue in BitPhoenix/.gitignore
- Ensure all linting tools are available/installed
- Add comprehensive test coverage
- Verify all scripts execute without errors

#### Documentation (20 pts) - Current: 18/20
- Deepen documentation (onboarding, technical guides)
- Add comprehensive docstrings to all functions
- Add inline comments explaining WHY, not WHAT
- Create detailed technical documentation
- Add AI collaboration guides

#### Security (15 pts) - Current: 15/15
- Maintain perfect security score
- Add dependency vulnerability scanning
- Add pre-commit hooks for security
- Enhance security policies

#### Efficiency (15 pts) - Current: 13/15
- Add pre-commit hooks to all repos
- Automate all testing and validation
- Optimize CI/CD workflows
- Add code coverage reporting

#### AI Learning (15 pts) - Current: 12/15
- Document learning cycles explicitly
- Create knowledge base updates
- Add adaptive improvement tracking
- Enhance AI collaboration documentation

#### Innovation (15 pts) - Current: 11/15
- Implement self-healing CI/CD
- Add advanced automation
- Create transformative improvements
- Implement world-class best practices

### 5. Repository-Specific Improvements

For each of the 11 repositories:
- BitPhoenix: Fix encoding, add coverage, enhance docs
- Dell-Server-Roadmap: Add coverage, dependency scanning
- Dino-Cloud: Enhance onboarding, add tests
- FamilyFork: Deepen technical docs, add coverage
- GSMG.IO: Add dependency scanning, enhance security
- Goku.AI: Add tests, deepen documentation
- Keyhound: Add coverage, pre-commit hooks
- Scalpstorm: Enhance depth, add tests
- Server-Roadmap: Continue improvements
- StreamForge: Add substantive code, tests
- DinoCloud: (consolidated, but verify)

### 6. Script Structure Requirements

The generated script MUST include:

```python
#!/usr/bin/env python3
\"\"\"
[Comprehensive docstring explaining the script]
\"\"\"

# 1. IMPORTS AND CONFIGURATION
# 2. LOGGING SETUP (comprehensive logging class)
# 3. SECURITY CHECKS (scan for secrets, validate files)
# 4. REPOSITORY PROCESSING (for each repo)
# 5. QC IMPROVEMENTS (by category)
# 6. VERIFICATION (double-check everything)
# 7. FINAL REPORT (comprehensive summary)
```

### 7. Logging Class Requirements

Create a comprehensive logging class that logs:
- All file operations (create, modify, delete)
- All security checks
- All QC improvements
- All verification steps
- All errors and warnings
- Final summary with statistics

Format: JSON or structured text with timestamps

### 8. Security Validation

Before ANY file write:
- Scan content for secrets/credentials
- Validate .env.example uses placeholders only
- Check file paths for security issues
- Verify no hardcoded credentials

After ALL changes:
- Run security scan
- Verify no secrets exposed
- Validate all security policies

### 9. Verification Steps

Before completion, verify:
- [ ] All files created/modified successfully
- [ ] All security checks passed
- [ ] All tests pass
- [ ] All documentation complete
- [ ] All QC improvements applied
- [ ] All repositories processed
- [ ] No errors or warnings
- [ ] Final QC score calculated

### 10. Output Requirements

Generate:
1. **Execution Log** - Detailed log of all actions
2. **Security Report** - Security validation results
3. **QC Improvement Report** - QC score improvements by category
4. **Verification Report** - Final verification results
5. **Summary Report** - Overall project status

## SCRIPT REQUIREMENTS

1. **File Name:** `azure_100_percent_qc_improvement.py`
2. **Comprehensive Error Handling:** Try/except for all operations
3. **Windows Compatibility:** Handle Windows paths correctly
4. **Unicode Support:** Proper encoding handling
5. **Modular Design:** Functions for each QC category
6. **Dry-Run Mode:** Optional dry-run to preview changes
7. **Rollback Capability:** Ability to rollback changes if needed
8. **Progress Reporting:** Show progress for each repository
9. **Validation:** Validate all inputs and outputs
10. **Documentation:** Comprehensive docstrings and comments

## CODE QUALITY REQUIREMENTS

- Follow PEP 8 style guide
- Use type hints where appropriate
- Add comprehensive docstrings
- Add inline comments explaining WHY
- Use meaningful variable names
- Handle all edge cases
- Include error recovery

## FINAL REQUIREMENTS

The script must:
- Be production-ready
- Be well-documented
- Be secure
- Be efficient
- Be maintainable
- Achieve 100/100 QC score
- Follow 100/10 mindset

---

Generate the complete Python script that meets all these requirements. The script should be ready to review and execute.
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
                        "content": "You are an expert Python developer and quality assurance specialist. You create production-ready, secure, well-documented Python scripts that follow best practices and achieve 100/100 QC scores. You always include comprehensive logging, security checks, and verification steps."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=8000
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


def main():
    """Main execution function"""
    print("="*70)
    print("AZURE API: GENERATE 100/100 QC IMPROVEMENT SCRIPT")
    print("="*70)
    print(f"\nGeneration Date: {datetime.now().isoformat()}")
    print(f"Target: 100/100 QC Score across all 11 repositories")
    print(f"Current: 86/100 QC Score")
    print("\nBuilding generation prompt...")
    
    # Check Azure configuration
    print(f"\nAzure Configuration:")
    print(f"  Endpoint: {AZURE_ENDPOINT[:50]}..." if AZURE_ENDPOINT else "  Endpoint: NOT SET")
    print(f"  API Key: {'SET' if AZURE_API_KEY else 'NOT SET'}")
    print(f"  Deployment: {AZURE_DEPLOYMENT}")
    
    if not AZURE_ENDPOINT or not AZURE_API_KEY:
        print("\nERROR: Azure configuration incomplete!")
        sys.exit(1)
    
    # Build prompt
    print("\nReading Azure review and recommendations...")
    prompt = build_generation_prompt()
    print(f"Prompt built ({len(prompt)} characters)")
    
    print("\nCalling Azure GPT-4.1 API to generate improvement script...")
    print("(This may take 3-5 minutes...)\n")
    sys.stdout.flush()
    
    try:
        # Call Azure API
        print("Sending generation request to Azure API...")
        sys.stdout.flush()
        generated_script = call_azure_api(prompt)
        print(f"\nReceived generated script ({len(generated_script)} characters)")
        sys.stdout.flush()
        
        # Extract Python code from response (handle markdown code blocks)
        if "```python" in generated_script:
            # Extract code from markdown code block
            start = generated_script.find("```python") + 9
            end = generated_script.find("```", start)
            if end > start:
                generated_script = generated_script[start:end].strip()
        elif "```" in generated_script:
            # Extract code from generic code block
            start = generated_script.find("```") + 3
            end = generated_script.find("```", start)
            if end > start:
                generated_script = generated_script[start:end].strip()
        
        # Save generated script
        script_file = BASE_DIR / "azure_100_percent_qc_improvement.py"
        
        # Create header comment
        header = f'''#!/usr/bin/env python3
"""
Azure 100/100 QC Improvement Script

This script was GENERATED by Azure GPT-4.1 to improve all 11 GitHub repositories
to achieve 100/100 QC score (100/10 Mindset).

**GENERATED:** {datetime.now().isoformat()}
**GENERATOR:** Azure GPT-4.1
**TARGET:** 100/100 QC Score
**CURRENT:** 86/100 QC Score
**REPOSITORIES:** 11 total

**REVIEW BEFORE EXECUTION:**
1. Review the script thoroughly
2. Verify all changes are appropriate
3. Test in dry-run mode first
4. Execute only after approval

**SECURITY:**
- All security checks are included
- No secrets will be committed
- All changes are logged

**LOGGING:**
- Comprehensive logging (who/what/where/when/why)
- All actions are logged
- Final report generated

**VERIFICATION:**
- Double-checks all changes
- Validates security
- Verifies QC improvements
- Generates final report

"""
'''
        
        full_script = header + "\n" + generated_script
        
        # Write script
        with open(script_file, 'w', encoding='utf-8') as f:
            f.write(full_script)
        
        # Create review document
        review_file = BASE_DIR / f"AZURE_GENERATED_SCRIPT_REVIEW_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        review_document = f"""# Azure Generated Script Review

**Generated:** {datetime.now().isoformat()}  
**Generator:** Azure GPT-4.1  
**Script:** `azure_100_percent_qc_improvement.py`  
**Status:** Ready for Review

---

## Generated Script

**File:** `azure_100_percent_qc_improvement.py`  
**Size:** {len(full_script)} characters  
**Lines:** {len(full_script.split(chr(10)))} lines

---

## Script Preview

```python
{generated_script[:2000]}...
```

[Full script available in: `azure_100_percent_qc_improvement.py`]

---

## Review Checklist

Before executing the script, review:

- [ ] Script structure and organization
- [ ] Security checks and validation
- [ ] Logging implementation
- [ ] QC improvement logic
- [ ] Error handling
- [ ] Verification steps
- [ ] Documentation quality
- [ ] Code quality and style

---

## Next Steps

1. **Review the script** thoroughly
2. **Check for any issues** or concerns
3. **Test in dry-run mode** (if available)
4. **Execute the script** after approval
5. **Review the results** and verify improvements

---

**Generated:** {datetime.now().isoformat()}  
**Status:** ✅ Script Generated - Ready for Review
"""
        
        with open(review_file, 'w', encoding='utf-8') as f:
            f.write(review_document)
        
        print("="*70)
        print("SCRIPT GENERATION COMPLETE")
        print("="*70)
        print(f"\nGenerated script saved to: {script_file.name}")
        print(f"Review document saved to: {review_file.name}")
        print(f"\nScript Preview:")
        print("-" * 70)
        print(generated_script[:500] + "..." if len(generated_script) > 500 else generated_script)
        print("-" * 70)
        print(f"\n⚠️  IMPORTANT: Review the script before execution!")
        print(f"   Full script: {script_file.name}")
        
        return script_file
        
    except Exception as e:
        print(f"\nERROR: Failed to generate script: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

