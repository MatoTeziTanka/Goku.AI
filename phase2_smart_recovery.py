#!/usr/bin/env python3
"""
Phase 2: Smart Recovery
Automated forensic scan of _TRASH_BIN to recover likely Goku.AI files.
Ref: Master Prompt Section 1.3 (Musk Algorithm - Automate)
"""

import os
import shutil
from pathlib import Path

# --- CONFIGURATION ---
REPO_ROOT = Path.cwd()
TRASH_DIR = REPO_ROOT / "_TRASH_BIN"
RECOVER_DIR = REPO_ROOT / "_RECOVERED_GOKU"

# "DNA" Markers - If a file has these, we want it.
KEYWORDS = [
    "goku", "ai", "mind", "agent", "prompt", 
    "memory", "automation", "llm", "bot", 
    "self-updating", "master", "monitor",
    "shenron", "dragon", "radar", "orchestrator",
    "ultra-instinct", "beast-mode", "quest",
    "trading", "bitphoenix", "scalpstorm"
]

# File Type Sorter
TYPE_MAP = {
    ".py": "src_candidates",
    ".md": "docs_candidates",
    ".txt": "docs_candidates",
    ".json": "config_candidates",
    ".yaml": "config_candidates",
    ".yml": "config_candidates",
    ".bat": "scripts_candidates",
    ".sh": "scripts_candidates",
    ".ps1": "scripts_candidates",
    ".toml": "config_candidates",
    ".ini": "config_candidates",
    ".cfg": "config_candidates",
}

def is_relevant(file_path: Path) -> bool:
    """Returns True if file contains Goku DNA (Name or Content)."""
    # 1. Check Filename (Fast)
    filename_lower = file_path.name.lower()
    if any(k in filename_lower for k in KEYWORDS):
        return True
    
    # 2. Check Content (Deep Scan for text files)
    if file_path.suffix.lower() in TYPE_MAP:
        try:
            # Read first 2000 chars to check headers/imports
            content = file_path.read_text(encoding='utf-8', errors='ignore')[:2000].lower()
            
            # Check for multiple indicators
            matches = sum(1 for k in KEYWORDS if k in content)
            if matches >= 2:  # At least 2 keyword matches
                return True
            
            # Also check for specific patterns
            if any(pattern in content for pattern in [
                "goku", "ai mind", "master prompt", "shenron",
                "autonomous agent", "self-updating"
            ]):
                return True
                
        except Exception:
            # Binary file or encoding issue - skip content check
            pass
            
    return False

def main():
    print("=" * 70)
    print("PHASE 2: SMART RECOVERY (Automated Forensic Scan)".center(70))
    print("=" * 70)
    print()
    
    if not TRASH_DIR.exists():
        print("❌ _TRASH_BIN not found! Did you run Phase 1?")
        print(f"   Expected: {TRASH_DIR}")
        return 1

    print(f"🕵️  Scanning {TRASH_DIR.name} for Goku.AI artifacts...")
    print()
    
    recovered_count = 0
    scanned_count = 0
    
    # Create staging folders
    print("📁 Creating recovery staging area...")
    for subfolder in set(TYPE_MAP.values()):
        (RECOVER_DIR / subfolder).mkdir(parents=True, exist_ok=True)
    (RECOVER_DIR / "misc_candidates").mkdir(exist_ok=True)
    print()

    # Walk through the trash
    print("🔍 Scanning files...")
    for root, dirs, files in os.walk(TRASH_DIR):
        for file in files:
            file_path = Path(root) / file
            scanned_count += 1
            
            if is_relevant(file_path):
                # Determine destination
                category = TYPE_MAP.get(file_path.suffix.lower(), "misc_candidates")
                dest_path = RECOVER_DIR / category / file_path.name
                
                # Handle name conflicts
                if dest_path.exists():
                    counter = 1
                    stem = dest_path.stem
                    suffix = dest_path.suffix
                    while dest_path.exists():
                        dest_path = RECOVER_DIR / category / f"{stem}_{counter}{suffix}"
                        counter += 1
                
                # Copy (Recover)
                try:
                    shutil.copy2(file_path, dest_path)
                    print(f"  ✅ Recovered: {file_path.name} -> {category}/")
                    recovered_count += 1
                except Exception as e:
                    print(f"  ❌ Failed to copy {file_path.name}: {e}")

    print()
    print("=" * 70)
    print("RECOVERY SUMMARY".center(70))
    print("=" * 70)
    print(f"📊 Scanned: {scanned_count} files")
    print(f"✅ Recovered: {recovered_count} relevant files")
    print(f"📂 Location: {RECOVER_DIR}")
    print()
    
    # Show breakdown by category
    if recovered_count > 0:
        print("📋 Breakdown by category:")
        for category in sorted(set(TYPE_MAP.values()) | {"misc_candidates"}):
            category_path = RECOVER_DIR / category
            if category_path.exists():
                count = len(list(category_path.iterdir()))
                if count > 0:
                    print(f"   - {category}: {count} file(s)")
        print()
    
    print("👉 NEXT STEPS:")
    print("   1. Review the '_RECOVERED_GOKU' folder")
    print("   2. Move files to proper structure:")
    print("      - src_candidates -> src/")
    print("      - docs_candidates -> docs/")
    print("      - config_candidates -> config/")
    print("      - scripts_candidates -> scripts/")
    print("   3. Run Phase 3: align_goku_structure.py")
    print("   4. Delete remaining files in _TRASH_BIN")
    print()

if __name__ == "__main__":
    import sys
    sys.exit(main())

