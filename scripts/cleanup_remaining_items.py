#!/usr/bin/env python3
"""
Clean up remaining items in "Doesnt Belong" folder
"""

import sys
import shutil
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

DOESNT_BELONG_PATH = Path("BitPhoenix/Doesnt Belong")
GITHUB_ROOT = Path("C:/Users/sethp/Documents/Github")
MARKETING_REPO = GITHUB_ROOT / "Marketing-Automation"

def cleanup():
    """Clean up remaining items"""
    print("="*70)
    print("CLEANING UP REMAINING ITEMS IN 'DOESNT BELONG'")
    print("="*70)
    print()
    
    if not DOESNT_BELONG_PATH.exists():
        print("✅ 'Doesnt Belong' folder already deleted!")
        return
    
    items = list(DOESNT_BELONG_PATH.iterdir())
    print(f"📋 Found {len(items)} items remaining")
    print()
    
    for item in items:
        print(f"📄 Processing: {item.name}")
        
        # Virtual environments - DELETE (not moved to repos)
        if item.name in ["venv", "shenron-env"]:
            try:
                shutil.rmtree(str(item), ignore_errors=True)
                print(f"  ✅ Deleted virtual environment: {item.name}")
            except Exception as e:
                print(f"  ⚠ Could not delete {item.name}: {e}")
            continue
        
        # Marketing-Automation subfolder - check for files
        if item.name == "Marketing-Automation":
            ma_path = item / "social-media-automation"
            if ma_path.exists():
                # Check for any files
                files = []
                try:
                    for f in ma_path.rglob("*"):
                        if f.is_file():
                            files.append(f)
                except:
                    pass
                
                if files:
                    print(f"  📦 Found {len(files)} files in subfolder")
                    # Move to Marketing-Automation repo
                    MARKETING_REPO.mkdir(parents=True, exist_ok=True)
                    for f in files:
                        rel_path = f.relative_to(item)
                        dest = MARKETING_REPO / rel_path
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        try:
                            shutil.move(str(f), str(dest))
                            print(f"    ✅ Moved: {rel_path}")
                        except Exception as e:
                            print(f"    ⚠ Error moving {rel_path}: {e}")
                
                # Try to remove empty directories
                try:
                    if not any(ma_path.iterdir()):
                        ma_path.rmdir()
                    if not any(item.iterdir()):
                        item.rmdir()
                        print(f"  ✅ Removed empty Marketing-Automation folder")
                except:
                    pass
    
    # Final cleanup - try to remove "Doesnt Belong" if empty
    print()
    print("🧹 Final cleanup...")
    remaining = []
    try:
        for item in DOESNT_BELONG_PATH.iterdir():
            remaining.append(item.name)
    except:
        pass
    
    if not remaining:
        try:
            DOESNT_BELONG_PATH.rmdir()
            print("✅ 'Doesnt Belong' folder deleted!")
        except Exception as e:
            print(f"⚠ Could not delete folder: {e}")
    else:
        print(f"⚠ 'Doesnt Belong' still contains: {', '.join(remaining)}")
        print("   These may be virtual environments or inaccessible directories")
        print("   You may need to delete them manually")
    
    print()
    print("="*70)
    print("✅ CLEANUP COMPLETE")
    print("="*70)

if __name__ == "__main__":
    cleanup()





