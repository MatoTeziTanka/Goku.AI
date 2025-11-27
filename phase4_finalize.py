#!/usr/bin/env python3
"""
Phase 4: Finalize Goku.AI Repository Structure
- Verifies v2.9.0 compliance
- Cleans up recovery folders
- Prepares for commit
"""

import os
import shutil
from pathlib import Path

REPO_ROOT = Path.cwd()

# Required directories (v2.9.0 standard)
REQUIRED_DIRS = [
    ".github/ISSUE_TEMPLATE",
    ".vscode",
    "config",
    "docs",
    "docs/architecture",
    "scripts/windows",
    "scripts/linux",
    "src",
    "src/api",
    "src/services",
    "src/utils",
    "tests/unit",
    "tests/integration",
]

# Required files
REQUIRED_FILES = [
    ".gitignore",
    "README.md",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "LICENSE",
    ".vscode/settings.json",
    ".vscode/extensions.json",
    ".editorconfig",
    "scripts/windows/install.bat",
    "scripts/windows/uninstall.bat",
    "scripts/linux/install.sh",
    "scripts/linux/uninstall.sh",
]

def verify_structure():
    """Verify the repository structure meets v2.9.0 standards."""
    print("🔍 Verifying v2.9.0 structure compliance...")
    print()
    
    missing_dirs = []
    missing_files = []
    
    # Check directories
    for dir_path in REQUIRED_DIRS:
        full_path = REPO_ROOT / dir_path
        if not full_path.exists():
            missing_dirs.append(dir_path)
        else:
            print(f"  ✅ {dir_path}/")
    
    # Check files
    for file_path in REQUIRED_FILES:
        full_path = REPO_ROOT / file_path
        if not full_path.exists():
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    print()
    if missing_dirs or missing_files:
        print("⚠️  Missing items:")
        for item in missing_dirs:
            print(f"  ❌ Directory: {item}/")
        for item in missing_files:
            print(f"  ❌ File: {item}")
        return False
    else:
        print("✅ Structure verification passed!")
        return True

def count_files_by_category():
    """Count files in each major directory."""
    print("\n📊 File Distribution:")
    print("-" * 50)
    
    categories = {
        "src/": REPO_ROOT / "src",
        "docs/": REPO_ROOT / "docs",
        "config/": REPO_ROOT / "config",
        "scripts/": REPO_ROOT / "scripts",
        "tests/": REPO_ROOT / "tests",
    }
    
    for name, path in categories.items():
        if path.exists():
            count = sum(1 for _ in path.rglob("*") if _.is_file())
            print(f"  {name:15} {count:4} file(s)")

def cleanup_recovery_folders():
    """Remove _RECOVERED_GOKU and _TRASH_BIN folders."""
    print("\n🧹 Cleaning up recovery folders...")
    
    folders_to_remove = [
        REPO_ROOT / "_RECOVERED_GOKU",
        REPO_ROOT / "_TRASH_BIN",
    ]
    
    removed_count = 0
    for folder in folders_to_remove:
        if folder.exists():
            try:
                shutil.rmtree(folder)
                print(f"  🗑️  Removed: {folder.name}/")
                removed_count += 1
            except Exception as e:
                print(f"  ❌ Error removing {folder.name}: {e}")
        else:
            print(f"  ⏭️  Skipped: {folder.name}/ (not found)")
    
    if removed_count > 0:
        print(f"\n✅ Cleanup complete! Removed {removed_count} folder(s)")
    else:
        print("\n✅ No cleanup needed")

def generate_commit_message():
    """Generate a standardized commit message."""
    message = """refactor(repo): align Goku.AI to Master Prompt v2.9.0 standards

- Implemented Strangler Fig remediation pattern
- Created v2.9.0 compliant directory structure
- Migrated 441 files from legacy structure
- Organized scripts by OS (Windows/Linux)
- Added mandatory configuration files (.vscode, .editorconfig)
- Created installation/uninstallation scripts per OS
- Standardized repository organization (src/, docs/, config/, scripts/, tests/)

BREAKING CHANGE: Repository structure completely reorganized
Ref: Master Prompt v2.9.0 Section 18.10"""
    
    return message

def main():
    print("=" * 70)
    print("PHASE 4: FINALIZE GOKU.AI REPOSITORY".center(70))
    print("=" * 70)
    print()
    
    # 1. Verify structure
    structure_ok = verify_structure()
    if not structure_ok:
        print("\n⚠️  Structure verification failed. Please fix missing items before proceeding.")
        return
    
    # 2. Count files
    count_files_by_category()
    
    # 3. Cleanup
    print("\n" + "=" * 70)
    response = input("Delete _RECOVERED_GOKU and _TRASH_BIN folders? (yes/no): ").strip().lower()
    if response == "yes":
        cleanup_recovery_folders()
    else:
        print("⏭️  Skipping cleanup (folders preserved)")
    
    # 4. Generate commit message
    print("\n" + "=" * 70)
    print("📝 SUGGESTED COMMIT MESSAGE:".center(70))
    print("=" * 70)
    print()
    print(generate_commit_message())
    print()
    print("=" * 70)
    print("✅ FINALIZATION COMPLETE".center(70))
    print("=" * 70)
    print()
    print("📋 Next Steps:")
    print("   1. Review the repository structure")
    print("   2. Test installation scripts: scripts/windows/install.bat")
    print("   3. Stage changes: git add .")
    print("   4. Commit with the suggested message above")
    print("   5. Push to GitHub: git push origin main")
    print()

if __name__ == "__main__":
    main()

