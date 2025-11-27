#!/usr/bin/env python3
"""
Continue Azure Review from where it left off
"""

import sys
import shutil
from pathlib import Path
from foundry_local_agent import FoundryClaudeAgent
import time

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
DINOCLOUD_PATH = GITHUB_ROOT / "DinoCloud"

def determine_file_destination(agent: FoundryClaudeAgent, file_path: Path) -> Path:
    """Determine where file should go"""
    # Quick keyword check first
    file_lower = file_path.name.lower()
    path_lower = str(file_path).lower()
    
    # Goku.AI keywords
    if any(kw in file_lower or kw in path_lower for kw in ["shenron", "goku", "dragonball", "dragon ball", "lm studio", "vm100"]):
        return GOKU_AI_PATH
    
    # DinoCloud
    if "dinocloud" in file_lower or "dinocloud" in path_lower:
        return DINOCLOUD_PATH
    
    # Marketing Automation - check if there's a marketing repo, otherwise keep in BitPhoenix or create new
    if "marketing" in file_lower or "marketing" in path_lower:
        # For now, we'll move to a Marketing repo if it exists, otherwise analyze with Azure
        marketing_repo = GITHUB_ROOT / "Marketing-Automation"
        if marketing_repo.exists():
            return marketing_repo
        # Use Azure to determine
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')[:2000]
            prompt = f"""Where should this marketing automation file go?

File: {file_path.name}
Content: {content[:500]}

Options:
- If it's general marketing automation → Create/use Marketing-Automation repo
- If it's BitPhoenix-specific → Keep in BitPhoenix
- If it's for another project → Identify the project

Respond with just the repo name."""
            result = agent.analyze_file(str(file_path), prompt)
            if "bitphoenix" in result.lower():
                return BITPHOENIX_PATH
            elif "marketing" in result.lower():
                return GITHUB_ROOT / "Marketing-Automation"
        except:
            pass
        return GITHUB_ROOT / "Marketing-Automation"  # Default
    
    return None

def finish_phase2(agent: FoundryClaudeAgent):
    """Finish moving files from 'Doesnt Belong'"""
    print("="*70)
    print("PHASE 2: FINISHING FILE MOVEMENT")
    print("="*70)
    
    if not DOESNT_BELONG_PATH.exists():
        print("✅ 'Doesnt Belong' folder already deleted!")
        return
    
    # Ensure destination folders exist
    GOKU_AI_PATH.mkdir(parents=True, exist_ok=True)
    DINOCLOUD_PATH.mkdir(parents=True, exist_ok=True)
    (GITHUB_ROOT / "Marketing-Automation").mkdir(parents=True, exist_ok=True)
    
    # Skip patterns
    skip_patterns = ["venv", "shenron-env", "__pycache__", ".git", "node_modules", "lib64", ".pytest_cache", ".pyc"]
    
    files_to_move = []
    for item in DOESNT_BELONG_PATH.rglob("*"):
        if any(pattern in str(item) for pattern in skip_patterns):
            continue
        if item.is_dir():
            continue
        if item.name.startswith('.'):
            continue
        try:
            if item.is_file():
                files_to_move.append(item)
        except:
            continue
    
    print(f"\n📋 Found {len(files_to_move)} files to move")
    
    moved = 0
    for file_path in files_to_move:
        rel_path = file_path.relative_to(DOESNT_BELONG_PATH)
        print(f"\n📄 Processing: {rel_path}")
        
        # Determine destination
        dest = determine_file_destination(agent, file_path)
        
        if not dest:
            print(f"  ⚠ Could not determine destination, skipping")
            continue
        
        dest_file = dest / rel_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            if dest_file.exists():
                dest_file = dest_file.with_stem(f"{dest_file.stem}_moved")
            shutil.move(str(file_path), str(dest_file))
            print(f"  ✅ Moved to: {dest_file.relative_to(GITHUB_ROOT)}")
            moved += 1
            time.sleep(0.5)  # Rate limiting
        except Exception as e:
            print(f"  ❌ Error: {e}")
    
    print(f"\n✅ Moved {moved} files")
    
    # Clean up empty directories
    print(f"\n🧹 Cleaning empty directories...")
    for dir_path in sorted(DOESNT_BELONG_PATH.rglob("*"), reverse=True):
        if dir_path == DOESNT_BELONG_PATH:
            continue
        try:
            # Check if it's a directory and accessible
            if not dir_path.is_dir():
                continue
            # Check if directory is empty
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"  ✅ Removed empty directory: {dir_path.relative_to(DOESNT_BELONG_PATH)}")
            except (OSError, PermissionError):
                # Skip inaccessible directories (symlinks, junctions, etc.)
                pass
        except (OSError, PermissionError):
            # Skip inaccessible items
            continue
    
    # Delete "Doesnt Belong" if empty
    remaining = list(DOESNT_BELONG_PATH.iterdir())
    if not remaining:
        try:
            DOESNT_BELONG_PATH.rmdir()
            print(f"✅ 'Doesnt Belong' folder deleted!")
        except Exception as e:
            print(f"⚠ Could not delete folder: {e}")
    else:
        print(f"⚠ 'Doesnt Belong' still has {len(remaining)} items (may be directories)")

def finish_phase3(agent: FoundryClaudeAgent):
    """Clean BitPhoenix files"""
    print("\n" + "="*70)
    print("PHASE 3: CLEANING BITPHOENIX FILES")
    print("="*70)
    
    EOL_PATH.mkdir(parents=True, exist_ok=True)
    
    skip_patterns = ["node_modules", ".git", "venv", "__pycache__", "EOL", ".env", ".backup"]
    
    files_to_check = []
    for item in BITPHOENIX_PATH.rglob("*"):
        if any(pattern in str(item) for pattern in skip_patterns):
            continue
        if item.is_dir():
            continue
        try:
            if item.is_file():
                files_to_check.append(item)
        except:
            continue
    
    print(f"\n📋 Checking {len(files_to_check)} files...")
    
    eol_count = 0
    for i, file_path in enumerate(files_to_check):
        if (i + 1) % 20 == 0:
            print(f"  Progress: {i + 1}/{len(files_to_check)}...")
        
        rel_path = file_path.relative_to(BITPHOENIX_PATH)
        if "EOL" in str(file_path):
            continue
        
        # Quick check - skip if clearly BitPhoenix related
        if any(kw in str(file_path).lower() for kw in ["recovery", "carving", "bitphoenix", "backend", "frontend"]):
            continue
        
        # Use Azure for questionable files
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')[:2000]
            prompt = f"""Is this file relevant to BitPhoenix v1.0.0 (data recovery platform)?

File: {rel_path}
Content: {content[:500]}

BitPhoenix is a data recovery platform. Respond with "EOL" if file is old/irrelevant, or "KEEP" if relevant."""
            
            result = agent.analyze_file(str(file_path), prompt)
            time.sleep(0.5)
            
            if "eol" in result.lower() and "keep" not in result.lower():
                dest_file = EOL_PATH / rel_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                try:
                    if dest_file.exists():
                        dest_file = dest_file.with_stem(f"{dest_file.stem}_moved")
                    shutil.move(str(file_path), str(dest_file))
                    eol_count += 1
                except:
                    pass
        except:
            pass
    
    print(f"\n✅ Moved {eol_count} files to EOL")

def finish_phase4(agent: FoundryClaudeAgent):
    """Review and delete EOL files"""
    print("\n" + "="*70)
    print("PHASE 4: REVIEWING AND DELETING EOL FILES")
    print("="*70)
    
    if not EOL_PATH.exists():
        print("✅ EOL folder does not exist")
        return
    
    eol_files = []
    for item in EOL_PATH.rglob("*"):
        try:
            if item.is_file():
                eol_files.append(item)
        except:
            continue
    
    if not eol_files:
        print("✅ EOL folder is already empty")
        return
    
    print(f"\n📋 Found {len(eol_files)} files in EOL")
    print("🗑️  Deleting EOL files...")
    
    deleted = 0
    for file_path in eol_files:
        try:
            file_path.unlink()
            deleted += 1
        except Exception as e:
            print(f"  ⚠ Could not delete {file_path.relative_to(EOL_PATH)}: {e}")
    
    print(f"✅ Deleted {deleted} files")
    
    # Clean empty directories
    for dir_path in sorted(EOL_PATH.rglob("*"), reverse=True):
        if dir_path == EOL_PATH:
            continue
        try:
            if not dir_path.is_dir():
                continue
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
            except (OSError, PermissionError):
                # Skip inaccessible directories
                pass
        except (OSError, PermissionError):
            continue
    
    print("✅ EOL cleanup complete (folder kept)")

def main():
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    print("="*70, flush=True)
    print("CONTINUING AZURE REVIEW", flush=True)
    print("="*70, flush=True)
    print(flush=True)
    
    agent = FoundryClaudeAgent(model="gpt-4.1")
    print("✅ Azure agent initialized\n", flush=True)
    
    finish_phase2(agent)
    finish_phase3(agent)
    finish_phase4(agent)
    
    print("\n" + "="*70)
    print("✅ ALL PHASES COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()

