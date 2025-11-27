# Zencoder + Azure Review Complete Workflow (All Repositories)

## Overview

This workflow uses your **actual Zencoder Code Agent and Review Agent** (not simulated) to analyze repositories, then uses Azure GPT-4.1 to build consensus and compile prioritized changes.

## Repositories to Process

1. **BitPhoenix** - Data recovery platform
2. **Dell-Server-Roadmap** - Server infrastructure roadmap (will merge with Server-Roadmap)
3. **Dino-Cloud** - Cloud project (will merge with DinoCloud)
4. **DinoCloud** - Will merge into Dino-Cloud
5. **FamilyFork** - Family-related project
6. **GSMG.IO** - Web project (exception: no v1.0.0 requirement)
7. **Goku.AI** - AI project (consolidate all Goku.AI files from entire GitHub folder)
8. **Keyhound** - Security/key management project
9. **Scalpstorm** - Trading/scalping project
10. **Server-Roadmap** - Will merge into Dell-Server-Roadmap
11. **StreamForge** - Streaming project

## Workflow Steps

### Step 1: Code Agent Analysis

**For each repository:**

1. Open `ZENCODER-CODE-AGENT-PROMPT.md`
2. **Replace `{REPO}`** with the repository name (e.g., "BitPhoenix", "Keyhound", "Goku.AI")
3. Copy the entire prompt
4. Paste into **Zencoder Code Agent** chat
5. Wait for Zencoder to analyze the repository
6. Zencoder will provide JSON output with:
   - Current QC score
   - List of recommended changes
   - File paths for all changes
   - Priority levels (High/Medium/Low)
   - Reasoning for each change
7. **Save the output** as `{REPO}-CODE-AGENT-OUTPUT.json`

**Example for Keyhound:**
```
Repository Name: Keyhound
Repository Path: C:\Users\sethp\Documents\Github\Keyhound
```

**Output file:** `Keyhound-CODE-AGENT-OUTPUT.json`

---

### Step 2: Review Agent Validation

**For each repository:**

1. Open `PASTE-THIS-INTO-ZENCODER-REVIEW-AGENT.md`
2. **Replace `{REPO}`** with the repository name
3. **Replace the file path**: `C:\Users\sethp\Documents\Github\{REPO}-CODE-AGENT-OUTPUT.json`
   - Example: `C:\Users\sethp\Documents\Github\Keyhound-CODE-AGENT-OUTPUT.json`
4. Copy the entire prompt
5. Paste into **Zencoder Review Agent** chat
6. **If Zencoder can't read the file:**
   - Open `{REPO}-CODE-AGENT-OUTPUT.json`
   - Copy the entire JSON content
   - Paste it into the prompt where it says `[PASTE THE ENTIRE CONTENTS HERE]`
7. Wait for Zencoder to review the Code Agent's work
8. Zencoder will provide JSON output with:
   - Validation summary (count verification, structure check)
   - Overall assessment (Agree/Partially Agree/Disagree)
   - Review of each change (agreement, risk, effort, complexity)
   - Interdependency analysis
   - Conflict detection
   - Realistic QC improvement assessment
9. **Save the output** as `{REPO}-REVIEW-AGENT-OUTPUT.json`

**Example for Keyhound:**
```
Repository: Keyhound
Code Agent Output: C:\Users\sethp\Documents\Github\Keyhound-CODE-AGENT-OUTPUT.json
```

**Output file:** `Keyhound-REVIEW-AGENT-OUTPUT.json`

---

### Step 3: Azure API Consensus

**After you have both Code Agent and Review Agent outputs:**

1. Open terminal in `C:\Users\sethp\Documents\Github`
2. Run the Python script:

```bash
python zencoder_manual_with_azure_review.py \
  --repo {REPO} \
  --code-agent-json {REPO}-CODE-AGENT-OUTPUT.json \
  --review-agent-json {REPO}-REVIEW-AGENT-OUTPUT.json
```

**Example for Keyhound:**
```bash
python zencoder_manual_with_azure_review.py \
  --repo Keyhound \
  --code-agent-json Keyhound-CODE-AGENT-OUTPUT.json \
  --review-agent-json Keyhound-REVIEW-AGENT-OUTPUT.json
```

3. The script will:
   - Read both JSON files
   - Extract file paths from Code Agent's recommendations
   - Have Azure GPT-4.1 review both analyses
   - Build consensus between Code Agent and Review Agent
   - Generate `{REPO}-AZURE-CONSENSUS.md`
   - Create `{REPO}-COMPILED-CHANGES.md` with prioritized action items

**Output files:**
- `{REPO}-AZURE-CONSENSUS.md` - Full consensus document
- `{REPO}-COMPILED-CHANGES.md` - Prioritized action items ready for implementation

---

## Complete Example: Keyhound

### Step 1: Code Agent
```
1. Open ZENCODER-CODE-AGENT-PROMPT.md
2. Replace {REPO} with "Keyhound"
3. Paste into Zencoder Code Agent
4. Save output as: Keyhound-CODE-AGENT-OUTPUT.json
```

### Step 2: Review Agent
```
1. Open PASTE-THIS-INTO-ZENCODER-REVIEW-AGENT.md
2. Replace {REPO} with "Keyhound"
3. Replace file path with: C:\Users\sethp\Documents\Github\Keyhound-CODE-AGENT-OUTPUT.json
4. Paste into Zencoder Review Agent
5. Save output as: Keyhound-REVIEW-AGENT-OUTPUT.json
```

### Step 3: Azure Consensus
```bash
python zencoder_manual_with_azure_review.py \
  --repo Keyhound \
  --code-agent-json Keyhound-CODE-AGENT-OUTPUT.json \
  --review-agent-json Keyhound-REVIEW-AGENT-OUTPUT.json
```

**Result:**
- `Keyhound-AZURE-CONSENSUS.md`
- `Keyhound-COMPILED-CHANGES.md`

---

## Special Cases

### GSMG.IO
- **Exception**: No v1.0.0 requirement
- Still analyze for QC improvements
- Use same workflow, but don't require v1.0.0 readiness

### Goku.AI
- **Consolidation task**: Code Agent should look for all Goku.AI files across entire `C:\Users\sethp\Documents\Github`
- Note files that need to be moved to Goku.AI repository
- Review Agent should validate consolidation plan

### Consolidation Repositories
- **Dell-Server-Roadmap & Server-Roadmap**: Code Agent should note merge opportunities
- **Dino-Cloud & DinoCloud**: Code Agent should note merge opportunities
- Review Agent should validate consolidation plans

---

## File Naming Convention

All outputs follow this pattern:
- Code Agent: `{REPO}-CODE-AGENT-OUTPUT.json`
- Review Agent: `{REPO}-REVIEW-AGENT-OUTPUT.json`
- Azure Consensus: `{REPO}-AZURE-CONSENSUS.md`
- Compiled Changes: `{REPO}-COMPILED-CHANGES.md`

**Examples:**
- `BitPhoenix-CODE-AGENT-OUTPUT.json`
- `Keyhound-REVIEW-AGENT-OUTPUT.json`
- `Goku.AI-AZURE-CONSENSUS.md`
- `StreamForge-COMPILED-CHANGES.md`

---

## Tips

1. **One repository at a time**: Complete the full workflow (Code Agent → Review Agent → Azure) for each repo before moving to the next
2. **Save all outputs**: Keep all JSON and markdown files for reference
3. **Check file paths**: Make sure file paths in prompts match your actual file locations
4. **If Zencoder can't read files**: Paste the JSON content directly into the prompt
5. **Batch processing**: After completing all repos, use `master_repo_improvement_orchestrator.py` to apply fixes

---

## Next Steps After All Repositories

1. **Review all compiled changes**: Read all `{REPO}-COMPILED-CHANGES.md` files
2. **Prioritize across repos**: Identify high-priority fixes that affect multiple repos
3. **Apply fixes**: Use the master orchestrator or apply manually
4. **Re-run analysis**: After fixes, re-run the 3-agent process to validate improvements
5. **Iterate**: Continue until all repos reach v1.0.0 with QC score 95+/100

---

## Troubleshooting

### Zencoder Can't Read File
- **Solution**: Copy the JSON content from `{REPO}-CODE-AGENT-OUTPUT.json` and paste it directly into the Review Agent prompt

### File Path Errors
- **Solution**: Verify the file path in the prompt matches your actual file location
- Windows paths: `C:\Users\sethp\Documents\Github\{REPO}-CODE-AGENT-OUTPUT.json`

### Python Script Errors
- **Solution**: Make sure both JSON files exist in the current directory
- Check that `zencoder_manual_with_azure_review.py` is in `C:\Users\sethp\Documents\Github`

### Missing Repository
- **Solution**: Verify the repository name matches exactly (case-sensitive)
- Check `master_repo_improvement_orchestrator.py` for the exact repository names
