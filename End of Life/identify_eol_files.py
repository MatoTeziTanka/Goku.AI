#!/usr/bin/env python3
"""
Identify files that can be moved to End of Life folder.

This script identifies Python scripts and other files that have been run
and are no longer needed.
"""

from pathlib import Path
from datetime import datetime
import json

BASE_DIR = Path(r"C:\Users\sethp\Documents\Github")
EOL_DIR = BASE_DIR / "End of Life"

# Files to keep (active/current scripts)
KEEP_FILES = {
    # Current active scripts
    "azure_100_percent_qc_improvement_FIXED.py",
    "azure_implement_consensus_fixes.py",
    "azure_review_zencoder_fixed_script_review.py",
    "azure_review_master_prompt.py",
    "verify_fixed_file.py",
    "MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND.md",
    "api_keys_config.json",
    
    # Important documentation
    "REVIEW-TASKS-SUMMARY.md",
    "FILE-INTEGRITY-FIX-SUMMARY.md",
    "AZURE_REVIEW_ZENCODER_FIXED_SCRIPT_20251126_024847.md",
    "AZURE_REVIEW_MASTER_PROMPT_20251126_021458.md",
    "AZURE_FIX_AND_LEARN_20251126_013423.md",
    
    # Zencoder prompts (may still be used)
    "ZENCODER-REVIEW-FIXED-SCRIPT-PROMPT.md",
    "ZENCODER-REVIEW-MASTER-PROMPT-PROMPT.md",
}

# Patterns for files that can be moved
EOL_PATTERNS = {
    # Old Azure review scripts (replaced by newer versions)
    "azure_bitphoenix_*.py",
    "azure_repo_*.py",  # Generic versions replaced
    "azure_vm101_*.py",
    "azure_review_zencoder_audit.py",
    "azure_review_code_agent_execution.py",
    "azure_review_complete_github_project.py",
    "azure_fix_and_learn_from_mistakes.py",
    "azure_generate_100_percent_improvement_script.py",
    "azure_review_zencoder_findings.py",
    
    # Old orchestration scripts
    "master_repo_improvement_orchestrator.py",
    "run_all_repos_3_agent_process.py",
    "run_single_repo_3_agent.py",
    "iterative_repo_improvement_cycle.py",
    "compile_changes_from_consensus.py",
    
    # Old batch processing
    "batch_azure_review_all_repos.py",
    "generate_all_zencoder_prompts.py",
    "generate_master_batch_summary.py",
    "zencoder_manual_with_azure_review.py",
    "zencoder_auto_fix_with_azure_review.py",
    
    # Old phase scripts
    "phase1_fast_validate.py",
    "phase2_execute_batch.py",
    "phase3_testing.py",
    "phase4_consolidation.py",
    "validate_phase1.py",
    
    # Old analysis/cleanup scripts
    "apply_batch_consensus.py",
    "init_missing_repos.py",
    "CODE_REVIEW_ANALYSIS.py",
    "find_all_goku_files.py",
    "fix_bitphoenix_merge_conflicts.py",
    "fix_bitphoenix_markdown.py",
    "cleanup_bitphoenix_files.py",
    "ROLLBACK_BATCH.py",
    
    # Old review/status files
    "*STATUS*.md",
    "*SUMMARY*.md",
    "*REVIEW*.md",  # But keep recent ones
    "*CONSENSUS*.md",
    "*ANALYSIS*.md",
    
    # Old BitPhoenix specific files
    "BitPhoenix-*.md",
    "BitPhoenix-*.json",
    
    # Old repo-specific analysis files
    "*-CODE-AGENT-ANALYSIS.*",
    "*-REVIEW-AGENT-VALIDATION.*",
    "*-AZURE-REVIEW.*",
    "*-AZURE-CONSENSUS.*",
    "*-FINAL-CONSENSUS.md",
    "*-COMPILED-CHANGES.md",
    "*-ITERATION-*.md",
    "*-ZENCODER-IMPLEMENTATION.json",
}

def should_move_file(file_path: Path) -> tuple[bool, str]:
    """Determine if a file should be moved to EOL"""
    file_name = file_path.name
    
    # Never move keep files
    if file_name in KEEP_FILES:
        return False, "Keep file"
    
    # Never move directories
    if file_path.is_dir():
        return False, "Directory"
    
    # Never move files in subdirectories (only root level)
    if file_path.parent != BASE_DIR:
        return False, "In subdirectory"
    
    # Check specific patterns
    if file_name.startswith("azure_bitphoenix_"):
        return True, "Old BitPhoenix-specific script"
    if file_name.startswith("azure_repo_") and file_name != "azure_review_zencoder_fixed_script_review.py":
        return True, "Old generic repo script"
    if file_name.startswith("azure_vm101_"):
        return True, "Old VM101 script"
    if file_name in ["azure_review_zencoder_audit.py", "azure_review_code_agent_execution.py",
                     "azure_review_complete_github_project.py", "azure_fix_and_learn_from_mistakes.py",
                     "azure_generate_100_percent_improvement_script.py", "azure_review_zencoder_findings.py"]:
        return True, "Old review script"
    if file_name in ["master_repo_improvement_orchestrator.py", "run_all_repos_3_agent_process.py",
                     "run_single_repo_3_agent.py", "iterative_repo_improvement_cycle.py",
                     "compile_changes_from_consensus.py"]:
        return True, "Old orchestration script"
    if file_name in ["batch_azure_review_all_repos.py", "generate_all_zencoder_prompts.py",
                     "generate_master_batch_summary.py", "zencoder_manual_with_azure_review.py",
                     "zencoder_auto_fix_with_azure_review.py"]:
        return True, "Old batch processing script"
    if file_name.startswith("phase") and file_name.endswith(".py"):
        return True, "Old phase script"
    if file_name in ["apply_batch_consensus.py", "init_missing_repos.py", "CODE_REVIEW_ANALYSIS.py",
                     "find_all_goku_files.py", "fix_bitphoenix_merge_conflicts.py",
                     "fix_bitphoenix_markdown.py", "cleanup_bitphoenix_files.py", "ROLLBACK_BATCH.py"]:
        return True, "Old utility script"
    
    # Check for old review/status files (but keep recent ones from today)
    if file_name.endswith(".md"):
        if "STATUS" in file_name or "SUMMARY" in file_name or "REVIEW" in file_name:
            # Keep files from today (2025-11-26)
            if "20251126" not in file_name:
                return True, "Old status/review file"
        if file_name.startswith("BitPhoenix-"):
            return True, "Old BitPhoenix file"
        if "-CODE-AGENT-ANALYSIS" in file_name or "-REVIEW-AGENT-VALIDATION" in file_name:
            return True, "Old agent output file"
        if "-AZURE-REVIEW" in file_name or "-AZURE-CONSENSUS" in file_name:
            return True, "Old Azure review file"
        if "-FINAL-CONSENSUS" in file_name or "-COMPILED-CHANGES" in file_name:
            return True, "Old consensus file"
        if "-ITERATION-" in file_name:
            return True, "Old iteration file"
    
    if file_name.endswith(".json"):
        if "-CODE-AGENT-ANALYSIS" in file_name or "-REVIEW-AGENT-VALIDATION" in file_name:
            return True, "Old agent output JSON"
        if "-AZURE-REVIEW" in file_name or "-AZURE-CONSENSUS" in file_name:
            return True, "Old Azure review JSON"
        if "-ZENCODER-IMPLEMENTATION" in file_name:
            return True, "Old Zencoder implementation JSON"
    
    return False, "Keep (not matched)"

def main():
    """Main execution"""
    print("="*70)
    print("IDENTIFY FILES FOR END OF LIFE")
    print("="*70)
    print(f"\nBase Directory: {BASE_DIR}")
    print(f"EOL Directory: {EOL_DIR}")
    
    # Create EOL directory if it doesn't exist
    EOL_DIR.mkdir(exist_ok=True)
    
    # Find all files in root directory
    files_to_move = []
    files_to_keep = []
    
    for file_path in BASE_DIR.iterdir():
        if file_path.is_file():
            should_move, reason = should_move_file(file_path)
            if should_move:
                files_to_move.append((file_path, reason))
            else:
                files_to_keep.append((file_path, reason))
    
    # Print results
    print(f"\n{'='*70}")
    print(f"FILES TO MOVE TO EOL: {len(files_to_move)}")
    print(f"{'='*70}\n")
    
    for file_path, reason in sorted(files_to_move):
        print(f"  {file_path.name:60} - {reason}")
    
    print(f"\n{'='*70}")
    print(f"FILES TO KEEP: {len(files_to_keep)}")
    print(f"{'='*70}\n")
    
    for file_path, reason in sorted(files_to_keep)[:20]:  # Show first 20
        print(f"  {file_path.name:60} - {reason}")
    if len(files_to_keep) > 20:
        print(f"  ... and {len(files_to_keep) - 20} more files")
    
    # Create summary
    summary = {
        "date": datetime.now().isoformat(),
        "files_to_move": len(files_to_move),
        "files_to_keep": len(files_to_keep),
        "files_list": [
            {
                "file": str(f.name),
                "reason": r
            }
            for f, r in files_to_move
        ]
    }
    
    summary_file = BASE_DIR / "EOL_FILES_IDENTIFIED.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"\nTotal files to move: {len(files_to_move)}")
    print(f"Total files to keep: {len(files_to_keep)}")
    print(f"\nSummary saved to: {summary_file.name}")
    print(f"\nTo move files, run:")
    print(f"  python move_eol_files.py")

if __name__ == "__main__":
    main()

