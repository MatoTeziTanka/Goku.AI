#!/usr/bin/env python3
"""
Generate All Zencoder Prompts for Batch Processing

Creates individual prompt files for each repository, ready to copy-paste into Zencoder.

Usage:
    python generate_all_zencoder_prompts.py

Output:
    Creates ZENCODER-PROMPT-{REPO}.md for each repository
"""

import sys
import io
from pathlib import Path
from datetime import datetime

# Windows Unicode fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REPOSITORIES = [
    "Keyhound",
    "Dell-Server-Roadmap",
    "Scalpstorm",
    "Goku.AI",
    "Dino-Cloud",
    "FamilyFork",
    "DinoCloud",
    "GSMG.IO",
    "Server-Roadmap",
    "StreamForge",
    "BitPhoenix"
]

# Baseline QC scores from previous analysis (if known)
BASELINE_SCORES = {
    "Keyhound": 77,
    "Dell-Server-Roadmap": 78,
    "Scalpstorm": 62,
    "Goku.AI": 59,
    "Dino-Cloud": 57,
    "FamilyFork": 42,
    "DinoCloud": 34,
    "GSMG.IO": None,  # Exception: No v1.0.0 requirement
    "Server-Roadmap": 5,
    "StreamForge": 2,
    "BitPhoenix": None  # Rate limited
}

def main():
    """Generate prompts for all repositories."""
    template_file = Path("ZENCODER-CODE-AGENT-PROMPT.md")
    
    # Read the enhanced template file
    if template_file.exists():
        with open(template_file, "r", encoding="utf-8") as f:
            template_content = f.read()
    else:
        print("❌ Error: ZENCODER-CODE-AGENT-PROMPT.md not found!")
        return
    
    print("🚀 Generating enhanced Zencoder prompts for all repositories...\n")
    
    generated = []
    for repo in REPOSITORIES:
        # Replace {REPO} placeholder
        prompt = template_content.replace("{REPO}", repo)
        
        # Handle file paths
        prompt = prompt.replace(f"C:\\\\Users\\\\sethp\\\\Documents\\\\Github\\\\{{REPO}}", 
                               f"C:\\\\Users\\\\sethp\\\\Documents\\\\Github\\\\{repo}")
        
        # Add baseline QC score if known
        baseline = BASELINE_SCORES.get(repo)
        if baseline is not None:
            baseline_section = f"""
## BASELINE QC SCORES (From Previous Analysis)

{repo} baseline scores:
- **Total: {baseline}/100**
- Functional QA: ~{int(baseline * 0.20)}/20
- Documentation: ~{int(baseline * 0.20)}/20
- Security: ~{int(baseline * 0.15)}/15
- Efficiency: ~{int(baseline * 0.15)}/15
- AI Learning: ~{int(baseline * 0.15)}/15
- Innovation: ~{int(baseline * 0.15)}/15

**Target: Improve from {baseline}/100 to 95/100 (need {95 - baseline} points)**
"""
            # Insert baseline section before "Now analyze" line
            prompt = prompt.replace(
                "Now analyze the {REPO} repository",
                f"{baseline_section}\nNow analyze the {repo} repository"
            )
        elif repo == "GSMG.IO":
            baseline_section = """
## BASELINE QC SCORES

GSMG.IO: No v1.0.0 requirement (exception), but still target 95/100 QC score.
Assess current state and provide baseline in output.
"""
            prompt = prompt.replace(
                "Now analyze the {REPO} repository",
                f"{baseline_section}\nNow analyze the GSMG.IO repository"
            )
        
        filename = f"ZENCODER-PROMPT-{repo}.md"
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(prompt)
        
        generated.append(filename)
        baseline_info = f" (Baseline: {baseline}/100)" if baseline is not None else ""
        print(f"✅ Generated: {filename}{baseline_info}")
    
    print(f"\n📁 Generated {len(generated)} enhanced prompt files")
    print("\n💡 Next steps:")
    print("   1. Open each prompt file")
    print("   2. Copy the content")
    print("   3. Paste into Zencoder Code Agent chat")
    print("   4. Zencoder will ACTUALLY MAKE CHANGES (not just recommend)")
    print("   5. Save output as: {REPO}-ZENCODER-IMPLEMENTATION.json")
    print("\n🚀 Run Zencoder for all repos in parallel if supported!")
    print("\n⚠️  IMPORTANT: Zencoder will actually modify files - make sure you have backups!")

if __name__ == "__main__":
    main()
