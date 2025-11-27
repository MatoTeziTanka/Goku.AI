#!/usr/bin/env python3
"""
Generate Master Batch Summary

Creates a master summary of all Zencoder implementations and Azure reviews.

Usage:
    python generate_master_batch_summary.py
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

def check_files(repo_name):
    """Check which files exist for a repository."""
    files = {
        "zencoder": Path(f"{repo_name}-ZENCODER-IMPLEMENTATION.json"),
        "azure_review": Path(f"{repo_name}-AZURE-REVIEW-OF-ZENCODER.md"),
        "consensus": Path(f"{repo_name}-FINAL-CONSENSUS.md")
    }
    
    status = {
        "zencoder_exists": files["zencoder"].exists(),
        "azure_review_exists": files["azure_review"].exists(),
        "consensus_exists": files["consensus"].exists(),
        "complete": all(f.exists() for f in files.values())
    }
    
    return status, files

def main():
    """Generate master summary."""
    print("📊 Generating master batch summary...\n")
    
    summary_lines = [
        "# Batch Zencoder Implementation - Master Summary",
        "",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "**Status:** All Repositories Processed",
        "",
        "---",
        "",
        "## 📊 Repository Status",
        ""
    ]
    
    complete_count = 0
    partial_count = 0
    pending_count = 0
    
    for repo in REPOSITORIES:
        status, files = check_files(repo)
        
        if status["complete"]:
            status_icon = "✅ Complete"
            complete_count += 1
        elif status["zencoder_exists"]:
            status_icon = "⏳ Azure Review Pending"
            partial_count += 1
        else:
            status_icon = "❌ Not Started"
            pending_count += 1
        
        summary_lines.append(f"### {repo}")
        summary_lines.append(f"- **Status:** {status_icon}")
        summary_lines.append("")
        
        if status["zencoder_exists"]:
            summary_lines.append(f"- ✅ Zencoder Output: `{files['zencoder'].name}`")
        else:
            summary_lines.append(f"- ❌ Zencoder Output: Missing")
        
        if status["azure_review_exists"]:
            summary_lines.append(f"- ✅ Azure Review: `{files['azure_review'].name}`")
        else:
            summary_lines.append(f"- ⏳ Azure Review: Pending")
        
        if status["consensus_exists"]:
            summary_lines.append(f"- ✅ Final Consensus: `{files['consensus'].name}`")
        else:
            summary_lines.append(f"- ⏳ Final Consensus: Pending")
        
        summary_lines.append("")
    
    # Add summary statistics
    summary_lines.extend([
        "---",
        "",
        "## 📈 Progress Summary",
        "",
        f"- ✅ **Complete:** {complete_count}/{len(REPOSITORIES)} repositories",
        f"- ⏳ **Partial:** {partial_count}/{len(REPOSITORIES)} repositories",
        f"- ❌ **Pending:** {pending_count}/{len(REPOSITORIES)} repositories",
        "",
        "---",
        "",
        "## 📁 Generated Files",
        "",
        "### Per Repository:",
        "- `{REPO}-ZENCODER-IMPLEMENTATION.json` - Zencoder's work",
        "- `{REPO}-AZURE-REVIEW-OF-ZENCODER.md` - Azure's review",
        "- `{REPO}-FINAL-CONSENSUS.md` - Final consensus",
        "",
        "### Master Files:",
        "- `BATCH-ZENCODER-IMPLEMENTATION-SUMMARY.md` - This file",
        "",
        "---",
        "",
        "## 🎯 Next Steps",
        "",
        "1. Review all `{REPO}-FINAL-CONSENSUS.md` files",
        "2. Identify agreed-upon changes across all repos",
        "3. Apply fixes using master orchestrator or manually",
        "4. Re-run analysis to validate improvements",
        "",
        "---",
        "",
        "**End of Summary**"
    ])
    
    summary_content = "\n".join(summary_lines)
    
    output_file = Path("BATCH-ZENCODER-IMPLEMENTATION-SUMMARY.md")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(summary_content)
    
    print(f"✅ Master summary generated: {output_file.name}")
    print(f"\n📊 Statistics:")
    print(f"   ✅ Complete: {complete_count}/{len(REPOSITORIES)}")
    print(f"   ⏳ Partial: {partial_count}/{len(REPOSITORIES)}")
    print(f"   ❌ Pending: {pending_count}/{len(REPOSITORIES)}")

if __name__ == "__main__":
    main()


