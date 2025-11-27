#!/usr/bin/env python3
"""
Move approved files to End of Life folder.

This script moves only files that are clearly obsolete and safe to archive.
"""

from pathlib import Path
import json
import shutil
from datetime import datetime

BASE_DIR = Path(r"C:\Users\sethp\Documents\Github")
EOL_DIR = BASE_DIR / "End of Life"
SUMMARY_FILE = BASE_DIR / "EOL_FILES_IDENTIFIED.json"

# Files to KEEP (don't move these even if identified)
KEEP_FILES = {
    # Recent/active files
    "ZENCODER-REVIEW-FIXED-SCRIPT-PROMPT.md",
    "ZENCODER-REVIEW-MASTER-PROMPT-PROMPT.md",
    "REVIEW-TASKS-SUMMARY.md",
    "FILE-INTEGRITY-FIX-SUMMARY.md",
    "NEXT_STEPS_CONSENSUS_FIXES.md",
    "verify_consensus_fixes.py",
    "verify_fixed_file.py",
    "identify_eol_files.py",
    "move_eol_files.py",
    "move_approved_eol_files.py",
    
    # Current active scripts
    "azure_100_percent_qc_improvement_FIXED.py",
    "azure_100_percent_qc_improvement_FIXED_CONSENSUS.py",
    "azure_implement_consensus_fixes.py",
    "azure_review_zencoder_fixed_script_review.py",
    "azure_review_master_prompt.py",
    
    # Master prompt and config
    "MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND.md",
    "api_keys_config.json",
    
    # Recent review outputs (keep for reference)
    "AZURE_REVIEW_ZENCODER_FIXED_SCRIPT_20251126_024847.md",
    "AZURE_REVIEW_MASTER_PROMPT_20251126_021458.md",
    "AZURE_FIX_AND_LEARN_20251126_013423.md",
    "AZURE_IMPLEMENTATION_CONSENSUS_FIXES_20251126_025254.md",
}

# Patterns I AGREE should be moved (clearly obsolete)
APPROVED_PATTERNS = {
    # Old Azure scripts (replaced by newer versions)
    "azure_bitphoenix_",
    "azure_repo_",  # Generic old versions
    "azure_vm101_",
    "azure_review_zencoder_audit.py",
    "azure_review_code_agent_execution.py",
    "azure_review_complete_github_project.py",
    "azure_fix_and_learn_from_mistakes.py",
    "azure_generate_100_percent_improvement_script.py",
    "azure_review_zencoder_findings.py",
    
    # Old orchestration scripts (replaced)
    "master_repo_improvement_orchestrator.py",
    "run_all_repos_3_agent_process.py",
    "run_single_repo_3_agent.py",
    "iterative_repo_improvement_cycle.py",
    "compile_changes_from_consensus.py",
    
    # Old batch processing (replaced)
    "batch_azure_review_all_repos.py",
    "generate_all_zencoder_prompts.py",
    "generate_master_batch_summary.py",
    "zencoder_auto_fix_with_azure_review.py",
    "zencoder_manual_with_azure_review.py",
    
    # Old phase scripts
    "phase1_fast_validate.py",
    "phase2_execute_batch.py",
    "phase3_testing.py",
    "phase4_consolidation.py",
    
    # Old utility scripts
    "apply_batch_consensus.py",
    "init_missing_repos.py",
    "CODE_REVIEW_ANALYSIS.py",
    "find_all_goku_files.py",
    "fix_bitphoenix_merge_conflicts.py",
    "fix_bitphoenix_markdown.py",
    "cleanup_bitphoenix_files.py",
    "ROLLBACK_BATCH.py",
    
    # Old repo-specific outputs (analysis/validation files)
    "-CODE-AGENT-ANALYSIS.",
    "-REVIEW-AGENT-VALIDATION.",
    "-AZURE-REVIEW.",
    "-AZURE-CONSENSUS.",
    "-FINAL-CONSENSUS.md",
    "-ITERATION-",
    "-COMPILED-CHANGES.md",
    "-ZENCODER-IMPLEMENTATION.json",
}

def is_approved_for_move(file_name: str) -> tuple[bool, str]:
    """Check if file should be moved (approved)"""
    
    # Never move keep files
    if file_name in KEEP_FILES:
        return False, "Keep file (active/recent)"
    
    # Check against approved patterns
    for pattern in APPROVED_PATTERNS:
        if pattern in file_name:
            return True, f"Matches approved pattern: {pattern}"
    
    # Old status/summary files (but not recent ones from today)
    if "STATUS" in file_name or "SUMMARY" in file_name:
        # Keep files from today (2025-11-26)
        if "20251126" not in file_name:
            return True, "Old status/summary file"
    
    # Old review files (but not recent ones)
    if "REVIEW" in file_name and "20251126" not in file_name:
        # But keep some useful ones
        if "ZENCODER-REVIEW-FIXED-SCRIPT-PROMPT" in file_name:
            return False, "Keep (active prompt)"
        if "ZENCODER-REVIEW-MASTER-PROMPT-PROMPT" in file_name:
            return False, "Keep (active prompt)"
        return True, "Old review file"
    
    return False, "Not in approved list (keeping for safety)"

def main():
    """Main execution"""
    print("="*70)
    print("MOVE APPROVED FILES TO END OF LIFE")
    print("="*70)
    
    # Load summary
    if not SUMMARY_FILE.exists():
        print(f"\nERROR: Summary file not found: {SUMMARY_FILE}")
        print("Please run identify_eol_files.py first")
        return
    
    with open(SUMMARY_FILE, 'r', encoding='utf-8') as f:
        summary = json.load(f)
    
    all_files = summary.get("files_list", [])
    
    # Filter to only approved files
    approved_files = []
    skipped_files = []
    
    for file_info in all_files:
        file_name = file_info["file"]
        should_move, reason = is_approved_for_move(file_name)
        if should_move:
            approved_files.append((file_name, reason))
        else:
            skipped_files.append((file_name, reason))
    
    print(f"\nTotal files identified: {len(all_files)}")
    print(f"Approved to move: {len(approved_files)}")
    print(f"Skipped (keeping): {len(skipped_files)}")
    
    if not approved_files:
        print("\nNo files approved for moving")
        return
    
    print(f"\n{'='*70}")
    print("APPROVED FILES TO MOVE")
    print(f"{'='*70}\n")
    
    for file_name, reason in sorted(approved_files)[:30]:  # Show first 30
        print(f"  ✅ {file_name:60} - {reason}")
    if len(approved_files) > 30:
        print(f"  ... and {len(approved_files) - 30} more files")
    
    print(f"\n{'='*70}")
    print("FILES BEING KEPT (NOT MOVED)")
    print(f"{'='*70}\n")
    
    for file_name, reason in sorted(skipped_files)[:20]:  # Show first 20
        print(f"  ⏭️  {file_name:60} - {reason}")
    if len(skipped_files) > 20:
        print(f"  ... and {len(skipped_files) - 20} more files")
    
    # Confirm
    print(f"\n{'='*70}")
    print(f"Ready to move {len(approved_files)} approved files")
    print(f"{'='*70}")
    
    # Create EOL directory
    EOL_DIR.mkdir(exist_ok=True)
    
    # Move files
    moved = []
    failed = []
    
    print(f"\nMoving files to: {EOL_DIR}\n")
    
    for file_name, reason in approved_files:
        file_path = BASE_DIR / file_name
        
        if not file_path.exists():
            print(f"  ⚠️  {file_name} - File not found, skipping")
            continue
        
        try:
            dest_path = EOL_DIR / file_name
            # Handle name conflicts
            if dest_path.exists():
                counter = 1
                while dest_path.exists():
                    stem = file_path.stem
                    suffix = file_path.suffix
                    dest_path = EOL_DIR / f"{stem}_{counter}{suffix}"
                    counter += 1
            
            shutil.move(str(file_path), str(dest_path))
            moved.append(file_name)
            if len(moved) <= 10:  # Show first 10 moves
                print(f"  ✅ {file_name}")
        except Exception as e:
            failed.append((file_name, str(e)))
            print(f"  ❌ {file_name} - Error: {e}")
    
    # Print summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    print(f"\n✅ Moved: {len(moved)} files")
    print(f"❌ Failed: {len(failed)} files")
    print(f"⏭️  Skipped: {len(skipped_files)} files (kept)")
    
    if failed:
        print(f"\nFailed files:")
        for file_name, error in failed:
            print(f"  {file_name}: {error}")
    
    print(f"\nFiles moved to: {EOL_DIR}")
    print(f"\n✅ Complete!")

if __name__ == "__main__":
    main()

