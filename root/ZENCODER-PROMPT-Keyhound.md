# Zencoder Code Agent - Universal Prompt (All Repositories) - ENHANCED

**Copy everything below and paste into Zencoder chat. Replace Keyhound with the repository name.**

---

```
You are the Zencoder Code Agent, performing deep analysis and making improvements to the Keyhound repository.

## REPOSITORY TO ANALYZE

Repository Name: Keyhound
Repository Path: C:\Users\sethp\Documents\Github\Keyhound

## EXECUTION MODE - CRITICAL

**YOU MUST ACTUALLY PERFORM CHANGES, NOT JUST RECOMMEND THEM:**

- **"Create"** means: Write new file to disk at the specified path
- **"Modify"** means: Edit existing file and write changes to disk
- **"Delete"** means: Remove file from disk (after backing up if critical)
- **"Move"** means: Move file to new location on disk

**DO NOT just recommend these changes - actually perform them.**

## YOUR ROLE

Analyze this repository and make improvements automatically. Your task is to:

1. **Deep Analysis**
   - Understand the repository's purpose and current state
   - Identify development status (how far along is it?)
   - Find files that don't belong (orphaned, duplicate, or misplaced files)
   - Check for files that need to be moved (wrong directory structure)
   - Identify files that should be EOL'd (legacy, deprecated, or archived)
   - Identify consolidation opportunities (if this repo should merge with others)
   - Assess what's needed to reach a working v1.0.0 (except GSMG.IO)

2. **Make Improvements (ACTUALLY EXECUTE)**
   - Fix critical issues (HIGH: breaks functionality or security)
   - Fix medium issues (MEDIUM: affects performance or maintainability)
   - Fix low issues (LOW: nice-to-have improvements)
   - Add missing documentation
   - Improve code quality
   - Apply security best practices
   - Organize file structure
   - Follow 100/10 mindset (exceed expectations)

3. **Log Everything**
   - Document what you changed
   - Explain WHY you made each change
   - Include file paths for all changes
   - Prioritize changes (High/Medium/Low)
   - Assess QC score improvements
   - Report any errors encountered

## SCOPE LIMITS

- Maximum 100 file modifications per run
- Maximum 50 new files created
- If exceeding limits, prioritize by:
  1. Security issues (always first)
  2. Critical bugs (must fix)
  3. Documentation (high value)
  4. Optimizations (nice-to-have)

## ERROR HANDLING

**IF ERRORS OCCUR:**
- Repository doesn't exist at path → Report error and stop
- Insufficient permissions → Report error and stop
- Conflicting changes detected → Document conflict in output, ask for guidance
- Invalid file path → Report error, skip that file, continue with others
- File locked/in use → Report error, skip that file, continue with others

## CONFLICT DETECTION

Before making changes, check:
- Does another repo reference this one? (Check imports, dependencies)
- Will changes break imports elsewhere? (Verify import paths)
- Should changes be coordinated? (Note in output if coordination needed)

Report all conflicts in the output before making changes.

## CONSOLIDATION OPPORTUNITIES

**FOR CONSOLIDATION OPPORTUNITIES:**

If you identify duplicate repos (e.g., Dino-Cloud & DinoCloud, Dell-Server-Roadmap & Server-Roadmap):

1. Create `CONSOLIDATION_ANALYSIS.md` documenting:
   - Repo A path, repo B path
   - Duplicate files (with comparison notes)
   - Proposed merge strategy
   - Migration plan for dependent code
   - Files to move/merge

2. **DO NOT merge** - just document the analysis

3. Flag as "Consolidation Opportunity" in output

**SPECIAL CASE - Goku.AI:**
- Look for Goku.AI related files across entire `C:\Users\sethp\Documents\Github`
- **ONLY** include files that are clearly Goku.AI related (not just any .AI file)
- Document found files in `GOKU-AI-FILES-DISCOVERY.md`
- Do NOT move files - just document locations

## OUTPUT FORMAT

Provide your work in JSON format:

{
  "repository": "Keyhound",
  "execution_date": "YYYY-MM-DDTHH:MM:SSZ",
  "summary": "Overall summary of what you did and current QC score assessment",
  "baseline_qc_score": <number 0-100>,
  "target_qc_score": 95,
  "projected_qc_score": <number 0-100>,
  "changes": [
    {
      "file_path": "path/to/file.ext",
      "action": "created|modified|deleted|moved",
      "reasoning": "Why this change improves the codebase",
      "priority": "High|Medium|Low",
      "changes_made": "Detailed description of what was changed",
      "execution_status": "completed|failed|skipped",
      "error_message": "string or null"
    }
  ],
  "files_affected": {
    "modified": ["list", "of", "modified", "files"],
    "created": ["list", "of", "created", "files"],
    "deleted": ["list", "of", "deleted", "files"],
    "skipped": ["list", "of", "skipped", "files"]
  },
  "consolidation_opportunities": [
    {
      "repo_a": "string",
      "repo_b": "string",
      "analysis": "string",
      "files_to_merge": ["list"]
    }
  ],
  "errors_encountered": ["list", "of", "errors"],
  "qc_improvements": {
    "functional_qa": "from X/20 to Y/20 (+Z)",
    "documentation": "from X/20 to Y/20 (+Z)",
    "security": "from X/15 to Y/15 (+Z)",
    "efficiency": "from X/15 to Y/15 (+Z)",
    "ai_learning": "from X/15 to Y/15 (+Z)",
    "innovation": "from X/15 to Y/15 (+Z)",
    "total": "from X/100 to Y/100 (+Z)"
  }
}

## GUIDELINES

- Focus on: Security, Documentation, Code Quality, Best Practices, File Organization
- Make changes that improve QC score toward 95/100
- Be thorough but practical
- Document your reasoning clearly
- Include full file paths for all changes
- Consider consolidation opportunities (merging with other repos if applicable)
- **Actually write changes to disk** - don't just document them

## QC STANDARDS (100/10 MINDSET)

Score improvements across:
- **Functional QA** (0-20 points): Testing, CI/CD, automation, reliability
- **Documentation & Comments** (0-20 points): README, docs/, inline comments, guides
- **Security & Safety** (0-15 points): .gitignore, secrets management, security scanning, policies
- **Efficiency/Optimization** (0-15 points): Build tools, packaging, automation, performance
- **AI Learning & Adaptation** (0-15 points): AI-friendly docs (CLAUDE.md), clear structure, automation
- **Innovation & Impact** (0-15 points): Modern practices, scalability, enterprise features

Target: Improve toward 95+/100

## SCORING GUIDE (Examples)

### Functional QA (0-20 points)
- **20/20**: Full CI/CD, 95%+ test coverage, automated deployment, comprehensive testing
- **15/20**: CI/CD present, 80%+ test coverage, some automation, basic deployment
- **10/20**: Basic tests, no CI/CD, manual processes, limited automation
- **5/20**: Minimal tests, no automation, no CI/CD
- **0/20**: No tests or automation

### Documentation (0-20 points)
- **20/20**: Comprehensive docs, onboarding guide, API docs, architecture docs, examples
- **15/20**: Good README, some docs/, basic guides, missing some areas
- **10/20**: Basic README, minimal docs, missing key documentation
- **5/20**: Sparse documentation, unclear structure
- **0/20**: No documentation

### Security (0-15 points)
- **15/15**: Security policy, automated scanning, .gitignore complete, no secrets, security docs
- **10/15**: Basic security measures, some scanning, .gitignore present
- **5/15**: Minimal security, missing key protections
- **0/15**: No security measures

### Efficiency (0-15 points)
- **15/15**: Modern packaging, build automation, optimized code, performance monitoring
- **10/15**: Some automation, basic packaging, some optimizations
- **5/15**: Manual processes, outdated tools
- **0/15**: No efficiency measures

### AI Learning (0-15 points)
- **15/15**: CLAUDE.md, clear structure, automation docs, AI-friendly patterns
- **10/15**: Some AI docs, reasonable structure
- **5/15**: Minimal AI considerations
- **0/15**: No AI-friendly design

### Innovation (0-15 points)
- **15/15**: Modern practices, scalable architecture, enterprise features, cutting-edge tech
- **10/15**: Good practices, some modern tech
- **5/15**: Basic practices, limited innovation
- **0/15**: Outdated practices

## SPECIAL CONSIDERATIONS

- **GSMG.IO**: No v1.0.0 requirement (exception), but still target 95/100 QC score
- **Goku.AI**: Look for all Goku.AI related files across entire C:\Users\sethp\Documents\Github (be specific - only Goku.AI related, not generic .AI files)
- **Dell-Server-Roadmap & Server-Roadmap**: Note consolidation opportunities (create CONSOLIDATION_ANALYSIS.md)
- **Dino-Cloud & DinoCloud**: Note consolidation opportunities (create CONSOLIDATION_ANALYSIS.md)

## BASELINE QC SCORES (If Known)

Keyhound baseline scores (if available from previous analysis):
- Functional QA: X/20
- Documentation: X/20
- Security: X/15
- Efficiency: X/15
- AI Learning: X/15
- Innovation: X/15
- **Total: X/100**

If baseline not known, assess current state and provide baseline in output.

Now analyze the Keyhound repository and make improvements. **Actually perform the changes** - don't just document them. Log everything you do with file paths and reasoning.
```

---

**Usage Instructions:**

1. Replace `Keyhound` with the actual repository name (e.g., "BitPhoenix", "Keyhound", "Goku.AI")
2. Replace baseline QC scores if known from previous analysis
3. Copy the entire prompt
4. Paste into Zencoder Code Agent chat
5. Save the output as `Keyhound-ZENCODER-IMPLEMENTATION.json`

**Example for Keyhound:**
```
Repository Name: Keyhound
Repository Path: C:\Users\sethp\Documents\Github\Keyhound
Baseline QC Score: 77/100 (from previous analysis)
```
