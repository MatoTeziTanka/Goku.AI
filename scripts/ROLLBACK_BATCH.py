#!/usr/bin/env python3
"""
ROLLBACK_BATCH.py - Rollback script for Code Agent Phase 2 changes

This script reverts all changes made during Phase 2 batch application.
It removes created files and restores modified files to their original state.

Usage:
    python ROLLBACK_BATCH.py

WARNING: This will delete all files created in Phase 2 and restore modified files.
Make sure you have a backup before running this script.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from datetime import datetime

# Windows Unicode fix
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Base directory
BASE_DIR = Path(r"C:\Users\sethp\Documents\Github")

# Phase 2 changes log (if exists)
CHANGES_LOG = BASE_DIR / "CODE_AGENT_CHANGES_LOG.md"
PHASE_2_REPORT = BASE_DIR / "PHASE_2_EXECUTION_REPORT.md"

# Rollback log
ROLLBACK_LOG = BASE_DIR / f"ROLLBACK_LOG_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

# Files to remove (created in Phase 2)
FILES_TO_REMOVE = {
    "BitPhoenix": [
        "CLAUDE.md",
        "SECURITY.md",
        ".github/workflows/security.yml"
    ],
    "Dell-Server-Roadmap": [
        "CLAUDE.md",
        ".github/workflows/ci.yml",
        ".env.example",
        "SECURITY_POLICY.md",
        "docs/DEPLOYMENT_CHECKLIST.md"
    ],
    "Dino-Cloud": [
        "CLAUDE.md",
        ".github/workflows/ci.yml",
        ".env.example",
        "docs/DEPLOYMENT.md",
        "tests/integration_tests.py"
    ],
    "DinoCloud": [
        "README.md",
        "CLAUDE.md",
        ".gitignore",
        ".env.example",
        ".github/workflows/ci.yml",
        "docs/ARCHITECTURE.md"
    ],
    "FamilyFork": [
        "CLAUDE.md",
        ".env.example",
        ".github/workflows/ci.yml",
        "backend/pyproject.toml",
        "backend/tests/conftest.py",
        "frontend/.eslintrc.json"
    ],
    "GSMG.IO": [
        "CLAUDE.md",
        ".github/workflows/ci.yml",
        ".env.example",
        "SECURITY.md",
        "pyproject.toml"
    ],
    "Goku.AI": [
        "README.md",
        "CLAUDE.md",
        ".github/workflows/ci.yml",
        "pyproject.toml",
        "docs/MODEL_TRAINING.md"
    ],
    "Keyhound": [
        "CLAUDE.md",
        "pyproject.toml",
        ".env.example",
        "docs/AI_COLLABORATION.md",
        "tests/conftest.py"
    ],
    "Scalpstorm": [
        "CLAUDE.md",
        ".env.example",
        "pyproject.toml",
        "docs/API_GUIDE.md"
    ],
    "Server-Roadmap": [
        "README.md",
        ".gitignore",
        "docs/ROADMAP.md",
        "docs/ARCHITECTURE.md",
        "CONTRIBUTING.md",
        ".github/ISSUE_TEMPLATE/bug_report.md"
    ],
    "StreamForge": [
        "README.md",
        ".gitignore",
        "src/main.py",
        "docs/PROJECT_PLAN.md",
        "CONTRIBUTING.md"
    ]
}

# Files to restore (modified in Phase 2)
FILES_TO_RESTORE = {
    "BitPhoenix": [
        ".gitignore"  # Note: May have encoding issues, restore from git if needed
    ]
}

# Consolidation rollback (Phase 4)
CONSOLIDATION_ROLLBACK = {
    "Server-Roadmap": {
        "source": "Dell-Server-Roadmap",
        "files": []  # Files would need to be extracted from Dell-Server-Roadmap
    },
    "DinoCloud": {
        "source": "Dino-Cloud",
        "files": []  # Files would need to be extracted from Dino-Cloud
    }
}


def log_message(message, file_handle):
    """Log message to both console and file"""
    print(message)
    file_handle.write(message + "\n")
    file_handle.flush()


def remove_file(repo_path, file_path, log_file):
    """Remove a file if it exists"""
    full_path = repo_path / file_path
    if full_path.exists():
        try:
            if full_path.is_file():
                full_path.unlink()
                log_message(f"  ✓ Removed: {file_path}", log_file)
                return True
            elif full_path.is_dir():
                shutil.rmtree(full_path)
                log_message(f"  ✓ Removed directory: {file_path}", log_file)
                return True
        except Exception as e:
            log_message(f"  ✗ Error removing {file_path}: {e}", log_file)
            return False
    else:
        log_message(f"  - Not found (already removed?): {file_path}", log_file)
        return True


def restore_file(repo_path, file_path, log_file):
    """Restore a file from git if it was modified"""
    full_path = repo_path / file_path
    if full_path.exists():
        try:
            # Try to restore from git
            import subprocess
            result = subprocess.run(
                ["git", "checkout", "--", str(file_path)],
                cwd=repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                log_message(f"  ✓ Restored from git: {file_path}", log_file)
                return True
            else:
                log_message(f"  ⚠ Could not restore from git: {file_path}", log_file)
                log_message(f"    Git error: {result.stderr}", log_file)
                return False
        except Exception as e:
            log_message(f"  ✗ Error restoring {file_path}: {e}", log_file)
            return False
    else:
        log_message(f"  - File not found: {file_path}", log_file)
        return False


def rollback_repository(repo_name, log_file):
    """Rollback changes for a single repository"""
    log_message(f"\n{'='*60}", log_file)
    log_message(f"Rolling back: {repo_name}", log_file)
    log_message(f"{'='*60}", log_file)
    
    repo_path = BASE_DIR / repo_name
    if not repo_path.exists():
        log_message(f"  ✗ Repository not found: {repo_name}", log_file)
        return False
    
    success = True
    
    # Remove created files
    if repo_name in FILES_TO_REMOVE:
        log_message(f"\n  Removing created files:", log_file)
        for file_path in FILES_TO_REMOVE[repo_name]:
            if not remove_file(repo_path, file_path, log_file):
                success = False
    
    # Restore modified files
    if repo_name in FILES_TO_RESTORE:
        log_message(f"\n  Restoring modified files:", log_file)
        for file_path in FILES_TO_RESTORE[repo_name]:
            if not restore_file(repo_path, file_path, log_file):
                success = False
    
    return success


def main():
    """Main rollback function"""
    print("="*60)
    print("CODE AGENT ROLLBACK SCRIPT")
    print("="*60)
    print(f"\nThis script will:")
    print("  1. Remove all files created in Phase 2")
    print("  2. Restore all files modified in Phase 2")
    print("  3. Log all actions to rollback log")
    print("\nWARNING: This action cannot be undone!")
    print("Make sure you have a backup before proceeding.")
    
    response = input("\nDo you want to proceed? (yes/no): ").strip().lower()
    if response != "yes":
        print("Rollback cancelled.")
        return
    
    # Open rollback log
    with open(ROLLBACK_LOG, 'w', encoding='utf-8') as log_file:
        log_message("="*60, log_file)
        log_message("CODE AGENT ROLLBACK LOG", log_file)
        log_message(f"Started: {datetime.now().isoformat()}", log_file)
        log_message("="*60, log_file)
        
        total_repos = len(FILES_TO_REMOVE)
        successful = 0
        failed = 0
        
        # Rollback each repository
        for repo_name in FILES_TO_REMOVE.keys():
            if rollback_repository(repo_name, log_file):
                successful += 1
            else:
                failed += 1
        
        # Summary
        log_message("\n" + "="*60, log_file)
        log_message("ROLLBACK SUMMARY", log_file)
        log_message("="*60, log_file)
        log_message(f"Total Repositories: {total_repos}", log_file)
        log_message(f"Successful: {successful}", log_file)
        log_message(f"Failed: {failed}", log_file)
        log_message(f"Completed: {datetime.now().isoformat()}", log_file)
        
        if failed == 0:
            log_message("\n✅ Rollback completed successfully!", log_file)
        else:
            log_message(f"\n⚠️ Rollback completed with {failed} errors.", log_file)
            log_message("Please review the log for details.", log_file)
    
    print(f"\nRollback log saved to: {ROLLBACK_LOG}")
    print("Rollback complete.")


if __name__ == "__main__":
    main()

