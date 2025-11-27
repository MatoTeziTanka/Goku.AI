#!/usr/bin/env python3
"""
Phase 3: Automated Migration from _RECOVERED_GOKU to v2.9.0 Structure
Moves files from recovery staging area to proper locations.
"""

import os
import shutil
from pathlib import Path

# Configuration
REPO_ROOT = Path.cwd()
RECOVER_DIR = REPO_ROOT / "_RECOVERED_GOKU"
TRASH_BIN = REPO_ROOT / "_TRASH_BIN"

# Mapping: recovery category -> destination directory
MIGRATION_MAP = {
    "src_candidates": "src",
    "docs_candidates": "docs",
    "config_candidates": "config",
    "scripts_candidates": "scripts",
    "misc_candidates": "docs/archive"  # Archive misc files in docs
}

# File type to subdirectory mapping within src/
SRC_SUBDIR_MAP = {
    ".py": None,  # Will go to src/ root or appropriate subdir based on name
}

# Special handling for known file patterns
SPECIAL_PATTERNS = {
    # API-related files
    "api": "src/api",
    "orchestrator": "src/services",
    "reporter": "src/services",
    "manager": "src/services",
    "quest": "src/services",
    "trading": "src/services",
    
    # Utility scripts
    "align": "scripts",
    "phase": "scripts",
    "consolidate": "scripts",
    "fix": "scripts",
    "remove": "scripts",
    "run": "scripts",
    "test": "scripts",
    "validate": "scripts",
    "scan": "scripts",
    "analyze": "scripts",
    "generate": "scripts",
    "execute": "scripts",
    "apply": "scripts",
    "check": "scripts",
    "batch": "scripts",
    "azure": "scripts",
    "find": "scripts",
    "estimate": "scripts",
    "master": "scripts",
    "multi": "scripts",
    "phase": "scripts",
    "rollback": "scripts",
    "cleanup": "scripts",
    "identify": "scripts",
    "init": "scripts",
    "move": "scripts",
    "read": "scripts",
    "continue": "scripts",
}

def determine_src_destination(file_path: Path) -> Path:
    """Determine the best destination for a Python file in src/."""
    filename_lower = file_path.stem.lower()
    
    # Check special patterns
    for pattern, subdir in SPECIAL_PATTERNS.items():
        if pattern in filename_lower:
            if subdir.startswith("src/"):
                return REPO_ROOT / subdir
            elif subdir == "scripts":
                return REPO_ROOT / "scripts"
    
    # Default: put in src/ root
    return REPO_ROOT / "src"

def migrate_file(source: Path, dest_dir: Path, category: str):
    """Move a file from recovery to destination, handling conflicts."""
    if not source.exists():
        return False
    
    # Determine final destination
    if category == "src_candidates" and source.suffix == ".py":
        final_dest_dir = determine_src_destination(source)
    elif category == "scripts_candidates":
        # Scripts go to scripts/ (OS-specific subdirs handled later)
        final_dest_dir = REPO_ROOT / "scripts"
    else:
        final_dest_dir = dest_dir
    
    final_dest_dir.mkdir(parents=True, exist_ok=True)
    final_dest = final_dest_dir / source.name
    
    # Handle conflicts
    if final_dest.exists():
        # Create a numbered version
        counter = 1
        while final_dest.exists():
            stem = source.stem
            suffix = source.suffix
            new_name = f"{stem}_{counter}{suffix}"
            final_dest = final_dest_dir / new_name
            counter += 1
    
    try:
        shutil.move(str(source), str(final_dest))
        return True
    except Exception as e:
        print(f"  ❌ Error moving {source.name}: {e}")
        return False

def organize_scripts_by_os(scripts_dir: Path):
    """Organize scripts into windows/ and linux/ subdirectories."""
    if not scripts_dir.exists():
        return
    
    windows_dir = scripts_dir / "windows"
    linux_dir = scripts_dir / "linux"
    windows_dir.mkdir(exist_ok=True)
    linux_dir.mkdir(exist_ok=True)
    
    for script in scripts_dir.iterdir():
        if script.is_file():
            if script.suffix == ".ps1" or script.suffix == ".bat":
                # Windows script
                dest = windows_dir / script.name
                if not dest.exists():
                    shutil.move(str(script), str(dest))
                    print(f"  📦 Organized: {script.name} -> scripts/windows/")
            elif script.suffix == ".sh":
                # Linux script
                dest = linux_dir / script.name
                if not dest.exists():
                    shutil.move(str(script), str(dest))
                    print(f"  📦 Organized: {script.name} -> scripts/linux/")
            # Python scripts stay in scripts/ root

def main():
    print("=" * 70)
    print("PHASE 3: AUTOMATED MIGRATION TO v2.9.0 STRUCTURE".center(70))
    print("=" * 70)
    print()
    
    if not RECOVER_DIR.exists():
        print("❌ _RECOVERED_GOKU not found! Did you run Phase 2?")
        return
    
    migrated_count = 0
    skipped_count = 0
    
    # Process each category
    for category, dest_name in MIGRATION_MAP.items():
        category_dir = RECOVER_DIR / category
        if not category_dir.exists():
            continue
        
        print(f"📦 Migrating {category} -> {dest_name}/...")
        dest_dir = REPO_ROOT / dest_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        files = list(category_dir.iterdir())
        for file_path in files:
            if file_path.is_file():
                if migrate_file(file_path, dest_dir, category):
                    migrated_count += 1
                else:
                    skipped_count += 1
        
        print(f"  ✅ Processed {len(files)} file(s) from {category}")
        print()
    
    # Organize scripts by OS
    print("🔧 Organizing scripts by OS...")
    scripts_dir = REPO_ROOT / "scripts"
    organize_scripts_by_os(scripts_dir)
    print()
    
    # Summary
    print("=" * 70)
    print("MIGRATION SUMMARY".center(70))
    print("=" * 70)
    print(f"✅ Migrated: {migrated_count} file(s)")
    if skipped_count > 0:
        print(f"⚠️  Skipped: {skipped_count} file(s)")
    print()
    print("📋 Next Steps:")
    print("   1. Review the migrated files in src/, docs/, config/, scripts/")
    print("   2. Verify file organization is correct")
    print("   3. Delete _RECOVERED_GOKU and _TRASH_BIN when satisfied")
    print("   4. Commit the new structure")
    print()

if __name__ == "__main__":
    main()

