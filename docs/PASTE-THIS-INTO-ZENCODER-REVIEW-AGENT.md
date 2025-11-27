# Copy and Paste This Into Zencoder Review Agent (Universal - All Repositories)

**When Zencoder asks what you want reviewed, paste this entire response. Replace {REPO} with the repository name.**

---

```
I want you to act as the Zencoder Review Agent. 

## YOUR TASK

Review the Code Agent's work on the {REPO} repository. The Code Agent has already analyzed the repository and provided recommendations in JSON format.

## CODE AGENT'S OUTPUT

The Code Agent's complete JSON output is in this file:
C:\Users\sethp\Documents\Github\{REPO}-CODE-AGENT-OUTPUT.json

**FIRST: Validate the input**
- Count the number of changes in the Code Agent's output
- Confirm the count matches what Code Agent claims (e.g., "X recommendations")
- If count differs, flag this discrepancy in your review
- Verify all required JSON fields are present (summary, changes, files_affected, qc_improvements)

If you can read that file, please do so. If not, I will paste the JSON content below.

## QC SCORING RUBRIC (100/10 MINDSET)

The QC score uses this 100-point system:
- **Functional QA** (0-20 points): Testing, CI/CD, automation, reliability
- **Documentation & Comments** (0-20 points): README, docs/, inline comments, guides
- **Security & Safety** (0-15 points): .gitignore, secrets management, security scanning, policies
- **Efficiency/Optimization** (0-15 points): Build tools, packaging, automation, performance
- **AI Learning & Adaptation** (0-15 points): AI-friendly docs (CLAUDE.md), clear structure, automation
- **Innovation & Impact** (0-15 points): Modern practices, scalability, enterprise features

**Current Score: [Code Agent will specify in their output]**
**Target Score: 95+/100**
**Gap: [Calculate from Code Agent's current_qc_score]**

## WHAT TO REVIEW (For Each Change)

### 1. Basic Validation
- **File path validation**: Is path correct relative to repository root? Does file/directory already exist?
- **Action validation**: Is "create" or "modify" appropriate? Should it be "delete" or "move" instead?
- **Priority assessment**: Do you agree with High/Medium/Low? Consider:
  - High: Blocks v1.0.0, security issues, missing critical functionality
  - Medium: Improves quality but not blocking, nice-to-have features
  - Low: Minor improvements, optional enhancements

### 2. Reasoning & Context
- **Reasoning check**: Does the explanation make sense? Is it based on actual repo analysis?
- **Repo-specific context**: Does Code Agent understand {REPO}'s actual patterns? Or is it generic advice?
- **Critical items check**: Did Code Agent miss anything critical? "Critical" means:
  - Blocks v1.0.0 release (except GSMG.IO)
  - Security vulnerabilities
  - Missing core functionality referenced in README/docs
  - Broken dependencies or build failures
  - Legal/compliance issues

### 3. Implementation Assessment
- **Implementation complexity**: Rate as "Trivial" (<1 hour), "Simple" (1-4 hours), "Moderate" (4-16 hours), "Complex" (16+ hours)
- **Estimated effort**: How many hours will this take to implement properly?
- **Risk level**: Rate as "Low" (safe, isolated), "Medium" (may affect other systems), "High" (could break things)
- **Testability**: Can this change be validated? How? (unit tests, manual testing, integration tests)

### 4. Interdependencies & Conflicts
- **Dependency order**: Are changes ordered correctly? Any blocking dependencies?
  - Example: Can't create tests/unit/ before pyproject.toml if tests need pyproject config
- **Conflict detection**: Do any two recommendations contradict each other?
  - Example: Code Agent suggests both "create X" and "delete X"
- **Scope validation**: Are all changes necessary, or is there scope creep?
  - Are changes aligned with v1.0.0 goals? (except GSMG.IO)
  - Any changes that should be deferred to v1.1.0?

### 5. QC Impact Assessment
- **Score improvement**: Will this change actually improve QC score? By how many points?
- **Realistic improvement**: Is the improvement to 95+ realistic with these changes?
- **Category impact**: Which QC categories does this improve? (Functional QA, Documentation, Security, Efficiency, AI Learning, Innovation)

## OUTPUT FORMAT

Provide your review in JSON format:

{
  "repository": "{REPO}",
  "validation_summary": {
    "change_count_verified": true/false,
    "expected_count": <number from Code Agent>,
    "actual_count": <number>,
    "discrepancy_note": "If count differs, explain here",
    "json_structure_valid": true/false,
    "missing_fields": ["list any missing required fields"]
  },
  "overall_assessment": {
    "agreement": "Agree|Partially Agree|Disagree",
    "quality_score": 0-100,
    "quality_score_rubric": {
      "functional_qa": "X/20 - explanation",
      "documentation": "X/20 - explanation",
      "security": "X/15 - explanation",
      "efficiency": "X/15 - explanation",
      "ai_learning": "X/15 - explanation",
      "innovation": "X/15 - explanation",
      "total": "X/100"
    },
    "summary": "Overall assessment of Code Agent's work",
    "what_was_done_well": ["List of positive aspects"],
    "what_could_improve": ["List of areas for improvement"],
    "additional_recommendations": ["List of changes Code Agent missed"],
    "interdependency_analysis": "Are changes ordered correctly? Any blocking dependencies?",
    "conflict_detection": "Any contradictory recommendations?",
    "scope_assessment": "Are all changes necessary for v1.0.0, or scope creep?",
    "realistic_improvement": "Is improvement to 95+ realistic with these changes? Why/why not?"
  },
  "change_reviews": [
    {
      "file_path": "relative/path/to/file.ext",
      "agreement": "Agree|Partially Agree|Disagree",
      "reasoning": "Why you agree/disagree with this change",
      "priority_assessment": "Agree with High/Medium/Low? If not, what should it be?",
      "implementation_complexity": "Trivial|Simple|Moderate|Complex",
      "estimated_effort_hours": <number>,
      "risk_level": "Low|Medium|High",
      "risk_explanation": "Why this risk level? What could break?",
      "testability": "How can this change be validated?",
      "qc_category_impact": ["Functional QA", "Documentation", "Security", "Efficiency", "AI Learning", "Innovation"],
      "qc_points_improvement": <number>,
      "suggestions": ["Any additional improvements needed for this file"],
      "dependencies": ["List any other changes this depends on"],
      "conflicts": ["List any changes that conflict with this one"]
    }
  ],
  "qc_score_impact": {
    "current_score": <from Code Agent>,
    "projected_score": <number>,
    "improvement_breakdown": "How Code Agent's changes will affect each QC category",
    "realistic_assessment": "Is projected score achievable? Why/why not?"
  }
}

## IMPORTANT VALIDATION RULES

1. **Count Verification**: Confirm Code Agent provided exactly the claimed number of changes. Flag if count differs.

2. **Complete Review**: Review EVERY change the Code Agent recommended. The `change_reviews` array must have one entry per Code Agent change.

3. **Critical Items**: "Critical" means blocking v1.0.0 (except GSMG.IO), security issues, missing core functionality, broken builds, or legal issues.

4. **Disagreement Clarity**: If you disagree, explain WHY with specific reasoning. Don't just say "disagree."

5. **Risk Assessment**: Be honest about implementation risks. High-risk changes need extra scrutiny.

6. **Interdependency Check**: Verify changes can be implemented in the order suggested. Flag blocking dependencies.

7. **Conflict Detection**: Actively look for contradictory recommendations (e.g., create and delete same file).

8. **Realistic Scoring**: Don't inflate QC improvements. Be honest about whether improvement to 95+ is achievable.

9. **Repo Context**: Consider {REPO}'s actual structure, patterns, and purpose. Don't give generic advice.

10. **100/10 Mindset**: Exceed expectations. Be thorough, critical, and constructive. Aim for world-class quality.

Please read the Code Agent's JSON file and provide your comprehensive review.
```

---

## If Zencoder Can't Read the File

**If Zencoder says it can't read the file, paste this instead:**

```
I want you to act as the Zencoder Review Agent.

## CODE AGENT'S OUTPUT

[PASTE THE ENTIRE CONTENTS OF {REPO}-CODE-AGENT-OUTPUT.json HERE]

## YOUR TASK

Review the Code Agent's recommendations above using the comprehensive evaluation criteria in the prompt above. Provide your review in the enhanced JSON format specified, including:
- Validation summary (count verification, structure check)
- Overall assessment with QC scoring rubric breakdown
- Detailed change reviews with risk, effort, complexity, and interdependency analysis
- Realistic QC score impact assessment

Follow all validation rules and be thorough in your analysis.
```

---

**After Zencoder responds, save the output as:** `{REPO}-REVIEW-AGENT-OUTPUT.json`

## Usage Instructions

1. **Replace `{REPO}`** with the actual repository name:
   - BitPhoenix
   - Dell-Server-Roadmap
   - Dino-Cloud
   - DinoCloud
   - FamilyFork
   - GSMG.IO
   - Goku.AI
   - Keyhound
   - Scalpstorm
   - Server-Roadmap
   - StreamForge

2. **Replace file path** in the prompt:
   - `C:\Users\sethp\Documents\Github\{REPO}-CODE-AGENT-OUTPUT.json`
   - Example: `C:\Users\sethp\Documents\Github\BitPhoenix-CODE-AGENT-OUTPUT.json`

3. **Copy the entire prompt** and paste into Zencoder Review Agent chat

4. **Save the output** as `{REPO}-REVIEW-AGENT-OUTPUT.json`

## What's Included in This Enhanced Version

✅ **Universal Template**: Works for all repositories (just replace {REPO})  
✅ **Count Verification**: Validates Code Agent provided exactly the claimed number of changes  
✅ **QC Scoring Rubric**: Explicit 100-point breakdown  
✅ **Risk & Effort Assessment**: Each change includes complexity, hours, and risk level  
✅ **Interdependency Analysis**: Checks if changes are ordered correctly  
✅ **Conflict Detection**: Actively looks for contradictory recommendations  
✅ **Testability Check**: Asks how each change can be validated  
✅ **Scope Validation**: Ensures changes align with v1.0.0 goals  
✅ **Realistic Improvement Assessment**: Honest evaluation of achievability  
✅ **Repo-Specific Context**: Considers actual patterns, not generic advice  
