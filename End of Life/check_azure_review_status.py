#!/usr/bin/env python3
"""
Check status of Azure Review and Reorganization script
"""

import sys
from pathlib import Path
import psutil
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

GITHUB_ROOT = Path("C:/Users/sethp/Documents/Github")
BITPHOENIX_PATH = GITHUB_ROOT / "BitPhoenix"
DOESNT_BELONG_PATH = BITPHOENIX_PATH / "Doesnt Belong"
EOL_PATH = BITPHOENIX_PATH / "EOL"
GOKU_AI_PATH = GITHUB_ROOT / "Goku.AI"

def check_process_running():
    """Check if azure_review_and_reorganize.py is still running"""
    script_name = "azure_review_and_reorganize.py"
    
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and script_name in ' '.join(cmdline):
                return True, proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return False, None

def count_files_in_directory(path):
    """Count files in directory"""
    if not path.exists():
        return 0
    count = 0
    try:
        for item in path.rglob("*"):
            if item.is_file():
                count += 1
    except:
        pass
    return count

def check_status():
    """Check overall status"""
    print("="*70)
    print("AZURE REVIEW STATUS CHECK")
    print("="*70)
    print()
    
    # Check if process is running
    is_running, pid = check_process_running()
    if is_running:
        print(f"🟢 Script is RUNNING (PID: {pid})")
    else:
        print("🔴 Script is NOT running")
    print()
    
    # Check "Doesnt Belong" folder
    print("📁 'Doesnt Belong' Folder Status:")
    if DOESNT_BELONG_PATH.exists():
        file_count = count_files_in_directory(DOESNT_BELONG_PATH)
        if file_count > 0:
            print(f"   ⚠ Still contains {file_count} files")
            print(f"   📍 Location: {DOESNT_BELONG_PATH}")
        else:
            print(f"   ✅ Folder is EMPTY (ready to delete)")
    else:
        print(f"   ✅ Folder DELETED (Phase 2 complete!)")
    print()
    
    # Check Goku.AI folder
    print("📁 Goku.AI Folder Status:")
    if GOKU_AI_PATH.exists():
        file_count = count_files_in_directory(GOKU_AI_PATH)
        print(f"   ✅ Folder exists with {file_count} files")
        
        # Check for Shenron files
        shenron_files = list(GOKU_AI_PATH.rglob("*shenron*"))
        if shenron_files:
            print(f"   ✅ Found {len(shenron_files)} Shenron-related files")
    else:
        print(f"   ⚠ Folder does not exist yet")
    print()
    
    # Check EOL folder
    print("📁 EOL Folder Status:")
    if EOL_PATH.exists():
        file_count = count_files_in_directory(EOL_PATH)
        if file_count > 0:
            print(f"   ⚠ Still contains {file_count} files")
            print(f"   📍 Phase 4 (EOL cleanup) may still be running")
        else:
            print(f"   ✅ Folder is EMPTY (Phase 4 complete!)")
    else:
        print(f"   ⚠ EOL folder does not exist")
    print()
    
    # Check for backup files (indicates Phase 1 completed)
    print("📝 Uninstall Scripts Status:")
    backup_files = list(BITPHOENIX_PATH.rglob("*.backup"))
    if backup_files:
        print(f"   ✅ Found {len(backup_files)} backup files (Phase 1 completed)")
        for bf in backup_files[:5]:
            print(f"      - {bf.name}")
    else:
        print(f"   ⚠ No backup files found (Phase 1 may not have completed)")
    print()
    
    # Overall status
    print("="*70)
    if not is_running:
        if not DOESNT_BELONG_PATH.exists() and count_files_in_directory(EOL_PATH) == 0:
            print("✅ SCRIPT COMPLETED - All phases done!")
        elif not DOESNT_BELONG_PATH.exists():
            print("🟡 SCRIPT COMPLETED - EOL cleanup may be pending")
        else:
            print("🟡 SCRIPT STOPPED - May have encountered an error")
    else:
        print("🟢 SCRIPT RUNNING - Check back in a few minutes")
    print("="*70)

if __name__ == "__main__":
    try:
        check_status()
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        import traceback
        traceback.print_exc()





