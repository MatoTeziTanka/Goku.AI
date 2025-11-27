#!/usr/bin/env python3
"""
Phase 1: The "Sorting Hat" Method
Moves everything to _TRASH_BIN except .git and critical files.
Ref: Master Prompt Section 1.3 (Musk Algorithm - Delete & Sort)
"""

import shutil
from pathlib import Path

GOKU_AI_ROOT = Path(r"C:\Users\sethp\Documents\Github\Goku.AI")
TRASH_BIN = GOKU_AI_ROOT / "_TRASH_BIN"

# Files/folders to KEEP in root (don't move to trash)
KEEP_IN_ROOT = {
    ".git",
    ".gitignore",
    "MASTER_PROMPT_PRODUCTION.md",  # If it exists here
    "README.md",  # Will be recreated by structure script
}

def main():
    print("=" * 70)
    print("PHASE 1: THE SORTING HAT (Musk Algorithm)".center(70))
    print("=" * 70)
    print()
    print("⚠️  WARNING: This will move ALL files to _TRASH_BIN")
    print("   except: .git, .gitignore, and critical files")
    print()
    
    response = input("Continue? (yes/no): ").strip().lower()
    if response != "yes":
        print("❌ Cancelled.")
        return 1
    
    print()
    print("📦 Creating _TRASH_BIN...")
    TRASH_BIN.mkdir(exist_ok=True)
    print()
    
    print("🔄 Moving files to _TRASH_BIN...")
    moved_count = 0
    skipped_count = 0
    
    for item in GOKU_AI_ROOT.iterdir():
        # Skip if it's in the keep list or is _TRASH_BIN itself
        if item.name in KEEP_IN_ROOT or item.name == "_TRASH_BIN":
            print(f"  ⏭️  Skipped: {item.name} (protected)")
            skipped_count += 1
            continue
        
        # Skip if it's a hidden file starting with .
        if item.name.startswith('.') and item.name not in ['.git', '.gitignore']:
            print(f"  ⏭️  Skipped: {item.name} (hidden)")
            skipped_count += 1
            continue
        
        try:
            target = TRASH_BIN / item.name
            if target.exists():
                # Add timestamp to avoid conflicts
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                target = TRASH_BIN / f"{item.name}_{timestamp}"
            
            shutil.move(str(item), str(target))
            print(f"  📦 Moved: {item.name}")
            moved_count += 1
        except Exception as e:
            print(f"  ❌ Error moving {item.name}: {e}")
    
    print()
    print("=" * 70)
    print("PHASE 1 COMPLETE".center(70))
    print("=" * 70)
    print(f"✅ Moved: {moved_count} items to _TRASH_BIN")
    print(f"⏭️  Skipped: {skipped_count} protected items")
    print()
    print("📋 Next Steps:")
    print("   1. Review _TRASH_BIN/")
    print("   2. Move back ONLY files relevant to Goku.AI")
    print("   3. Delete everything else in _TRASH_BIN")
    print("   4. Run Phase 2: align_goku_structure.py")
    print()

if __name__ == "__main__":
    import sys
    sys.exit(main())

