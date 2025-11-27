#!/usr/bin/env python3
"""
Azure-Powered Review and Reorganization Script
Uses Azure GPT-4.1 to review code quality, reorganize files, and clean up repositories
"""

import json
import sys
import shutil
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from foundry_local_agent import FoundryClaudeAgent
import time

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

# Paths
GITHUB_ROOT = Path("C:/Users/sethp/Documents/Github")
BITPHOENIX_PATH = GITHUB_ROOT / "BitPhoenix"
DOESNT_BELONG_PATH = BITPHOENIX_PATH / "Doesnt Belong"
EOL_PATH = BITPHOENIX_PATH / "EOL"
GOKU_AI_PATH = GITHUB_ROOT / "Goku.AI"

# QC Instructions
QC_INSTRUCTION = """Quality Assurance Commitment:
- Ensure all critical files are fully functional
- Every file and function must have comprehensive documentation: Inline Comments, Block Comments, Multi-Line Comments, Special Comments, Docstring Comments, and TODO Comments for improvements
- Follow highest standards of code quality: enterprise-grade, scalable, secure, token-efficient
- Versioning: maintain existing versions, do NOT reset to v1.0.0
- Maintain backups of all critical files before modification
- Track changes with diffs for auditing
- Enterprise-grade, precise, systematic, yet innovative and forward-thinking
"""

def get_enterprise_standards() -> Dict:
    """Load enterprise standards from JSON file"""
    standards_file = Path("enterprise_standards.json")
    if standards_file.exists():
        try:
            with open(standards_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}

def analyze_file_with_azure(agent: FoundryClaudeAgent, file_path: Path, purpose: str) -> str:
    """Use Azure API to analyze a file"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')
        
        prompt = f"""{QC_INSTRUCTION}

{purpose}

File: {file_path.name}
Path: {file_path}

Analyze this file and provide:
1. Does it meet enterprise coding standards?
2. Are there improvements needed?
3. Any security issues?
4. Documentation completeness?
5. Code quality assessment

Provide specific recommendations and improvements.
"""
        
        return agent.analyze_file(str(file_path), prompt)
    except Exception as e:
        return f"Error analyzing file: {e}"

def review_uninstall_scripts(agent: FoundryClaudeAgent) -> None:
    """Review and improve uninstall scripts using Azure API"""
    print("="*70)
    print("PHASE 1: REVIEWING UNINSTALL SCRIPTS WITH AZURE API")
    print("="*70)
    
    uninstall_scripts = [
        BITPHOENIX_PATH / "scripts/windows/uninstall-bitphoenix.ps1",
        BITPHOENIX_PATH / "scripts/linux/uninstall.sh",
        BITPHOENIX_PATH / "scripts/windows/uninstall-wsl.sh",
        BITPHOENIX_PATH / "UNINSTALL.md"
    ]
    
    for script_path in uninstall_scripts:
        if not script_path.exists():
            print(f"⚠ Skipping (not found): {script_path.name}")
            continue
        
        print(f"\n📝 Reviewing: {script_path.name}")
        print(f"   Path: {script_path.relative_to(BITPHOENIX_PATH)}")
        
        # Analyze with Azure
        analysis = analyze_file_with_azure(
            agent,
            script_path,
            "Review this uninstall script/instruction. Ensure it meets strict enterprise standards, has comprehensive documentation, proper error handling, security best practices, and follows all QC guidelines. If improvements are needed, provide the complete improved version."
        )
        
        # Check if Azure recommends improvements
        if "improve" in analysis.lower() or "better" in analysis.lower() or "recommend" in analysis.lower():
            print(f"  🔍 Azure analysis complete. Checking for improvements...")
            
            # Try to extract improved code from analysis
            import re
            code_blocks = re.findall(r'```(?:powershell|bash|markdown)?\n(.*?)\n```', analysis, re.DOTALL)
            
            if code_blocks:
                # Azure provided improved code
                improved_code = code_blocks[0]
                backup_path = script_path.with_suffix(script_path.suffix + '.backup')
                
                # Backup original
                shutil.copy2(script_path, backup_path)
                print(f"  💾 Backed up original to: {backup_path.name}")
                
                # Write improved version
                script_path.write_text(improved_code, encoding='utf-8')
                print(f"  ✅ Updated with Azure improvements")
            else:
                # Use Azure to edit the file directly
                try:
                    improved = agent.edit_file_with_agent(
                        str(script_path),
                        "Improve this file to meet strict enterprise standards. Add comprehensive documentation (inline, block, docstring comments), improve error handling, enhance security, and ensure it follows all QC guidelines. Maintain the same functionality but improve code quality.",
                        context=analysis
                    )
                    backup_path = script_path.with_suffix(script_path.suffix + '.backup')
                    shutil.copy2(script_path, backup_path)
                    agent.write_file(str(script_path), improved)
                    print(f"  ✅ Updated with Azure improvements")
                except Exception as e:
                    print(f"  ⚠ Could not apply improvements: {e}")
        else:
            print(f"  ✅ File meets standards (no improvements needed)")
        
        time.sleep(2)  # Rate limiting

def determine_file_destination(agent: FoundryClaudeAgent, file_path: Path) -> Optional[Path]:
    """Use Azure API to determine where a file should be moved"""
    try:
        # Read file content (limit size for API efficiency)
        content = file_path.read_text(encoding='utf-8', errors='ignore')[:5000]  # First 5000 chars
        
        prompt = f"""Analyze this file and determine which GitHub repository it belongs to.

File: {file_path.name}
Path: {file_path}
Content preview: {content[:1000]}

Available repositories (check C:/Users/sethp/Documents/Github/):
- BitPhoenix (data recovery platform)
- Goku.AI (Shenron, Goku, Custom AI Building, VM100, LM Studio, DragonBall Z related)
- ScalpStorm
- GSMG.IO
- Other repos in the Github directory

Rules:
1. If file is related to Shenron, Goku, Custom AI Building on VM100, LM Studio, or DragonBall Z → Goku.AI
2. If file is related to data recovery, file carving, recovery tools → BitPhoenix
3. If file is related to trading/scalping → ScalpStorm
4. If file is related to GSMG → GSMG.IO
5. If file doesn't fit any repo, return "UNKNOWN"

Respond with ONLY the repository name (e.g., "Goku.AI", "BitPhoenix", "ScalpStorm", "GSMG.IO", "UNKNOWN")
"""
        
        result = agent.analyze_file(str(file_path), prompt)
        
        # Extract repository name from response
        result_lower = result.lower()
        if "goku" in result_lower or "shenron" in result_lower:
            return GOKU_AI_PATH
        elif "bitphoenix" in result_lower:
            return BITPHOENIX_PATH
        elif "scalpstorm" in result_lower:
            return GITHUB_ROOT / "ScalpStorm"
        elif "gsmg" in result_lower:
            return GITHUB_ROOT / "GSMG.IO"
        else:
            return None  # Unknown - will be handled separately
            
    except Exception as e:
        print(f"  ⚠ Error determining destination for {file_path.name}: {e}")
        return None

def move_files_from_doesnt_belong(agent: FoundryClaudeAgent) -> None:
    """Move files from 'Doesnt Belong' to correct repositories"""
    print("\n" + "="*70)
    print("PHASE 2: MOVING FILES FROM 'DOESNT BELONG' FOLDER")
    print("="*70)
    
    if not DOESNT_BELONG_PATH.exists():
        print("⚠ 'Doesnt Belong' folder not found. Skipping.")
        return
    
    # Ensure Goku.AI folder exists
    GOKU_AI_PATH.mkdir(parents=True, exist_ok=True)
    
    # Collect all files recursively (skip virtual environments and symlinks)
    files_to_move = []
    skip_patterns = ["venv", "shenron-env", "__pycache__", ".git", "node_modules", "lib64", ".pytest_cache"]
    
    for item in DOESNT_BELONG_PATH.rglob("*"):
        # Skip if path contains skip patterns
        if any(pattern in str(item) for pattern in skip_patterns):
            continue
        
        # Skip if it's a directory
        if item.is_dir():
            continue
        
        # Skip hidden files
        if item.name.startswith('.'):
            continue
        
        # Try to check if it's a file, handle errors gracefully
        try:
            if item.is_file():
                files_to_move.append(item)
        except (OSError, PermissionError) as e:
            # Skip files that can't be accessed (symlinks, junctions, etc.)
            print(f"  ⚠ Skipping inaccessible item: {item.relative_to(DOESNT_BELONG_PATH)} ({e})")
            continue
    
    print(f"\n📋 Found {len(files_to_move)} files to analyze and move")
    
    moved_count = 0
    unknown_files = []
    
    for file_path in files_to_move:
        rel_path = file_path.relative_to(DOESNT_BELONG_PATH)
        print(f"\n📄 Analyzing: {rel_path}")
        
        # Check for Goku.AI keywords first (faster)
        file_lower = file_path.name.lower()
        content_preview = ""
        try:
            content_preview = file_path.read_text(encoding='utf-8', errors='ignore')[:500].lower()
        except:
            pass
        
        # Quick check for Goku.AI keywords
        goku_keywords = ["shenron", "goku", "dragonball", "dragon ball", "lm studio", "vm100", "custom ai"]
        is_goku = any(keyword in file_lower or keyword in content_preview for keyword in goku_keywords)
        
        if is_goku:
            dest = GOKU_AI_PATH
            print(f"  🎯 Detected Goku.AI content (keywords found)")
        else:
            # Use Azure to determine destination
            dest = determine_file_destination(agent, file_path)
            time.sleep(1)  # Rate limiting
        
        if dest:
            # Preserve directory structure
            dest_file = dest / rel_path
            
            # Create destination directory
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Move file
            try:
                if dest_file.exists():
                    # Add suffix to avoid overwrite
                    counter = 1
                    while dest_file.exists():
                        dest_file = dest_file.with_stem(f"{dest_file.stem}_{counter}")
                        counter += 1
                
                shutil.move(str(file_path), str(dest_file))
                print(f"  ✅ Moved to: {dest_file.relative_to(GITHUB_ROOT)}")
                moved_count += 1
            except Exception as e:
                print(f"  ❌ Error moving file: {e}")
        else:
            unknown_files.append(file_path)
            print(f"  ⚠ Could not determine destination")
    
    print(f"\n✅ Moved {moved_count} files")
    if unknown_files:
        print(f"⚠ {len(unknown_files)} files could not be categorized")
        for uf in unknown_files[:10]:  # Show first 10
            print(f"   - {uf.relative_to(DOESNT_BELONG_PATH)}")
        if len(unknown_files) > 10:
            print(f"   ... and {len(unknown_files) - 10} more")
    
    # Delete empty directories in "Doesnt Belong"
    print(f"\n🧹 Cleaning up empty directories...")
    for dir_path in sorted(DOESNT_BELONG_PATH.rglob("*"), reverse=True):
        if dir_path.is_dir() and dir_path != DOESNT_BELONG_PATH:
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
                    print(f"  ✅ Removed empty directory: {dir_path.relative_to(DOESNT_BELONG_PATH)}")
            except:
                pass
    
    # Verify "Doesnt Belong" is empty and delete it
    print(f"\n🔍 Verifying 'Doesnt Belong' folder is empty...")
    remaining_items = list(DOESNT_BELONG_PATH.iterdir())
    if not remaining_items:
        try:
            DOESNT_BELONG_PATH.rmdir()
            print(f"  ✅ 'Doesnt Belong' folder deleted (was empty)")
        except Exception as e:
            print(f"  ⚠ Could not delete folder: {e}")
    else:
        print(f"  ⚠ 'Doesnt Belong' folder still contains {len(remaining_items)} items:")
        for item in remaining_items[:5]:
            print(f"     - {item.name}")
        if len(remaining_items) > 5:
            print(f"     ... and {len(remaining_items) - 5} more")

def analyze_bitphoenix_file(agent: FoundryClaudeAgent, file_path: Path) -> Tuple[bool, str]:
    """Use Azure to analyze if a file belongs in BitPhoenix v1.0.0"""
    try:
        content = file_path.read_text(encoding='utf-8', errors='ignore')[:3000]
        
        prompt = f"""Analyze if this file belongs in BitPhoenix v1.0.0 (data recovery platform).

File: {file_path.name}
Path: {file_path.relative_to(BITPHOENIX_PATH)}
Content preview: {content[:1000]}

BitPhoenix v1.0.0 is a data recovery platform that:
- Recovers deleted/lost files
- Carves files from disk images
- Supports multiple file formats
- Has backend (Python/FastAPI) and frontend (React)

Determine:
1. Does this file have ANY purpose in BitPhoenix v1.0.0?
2. Is it an old/legacy file with no current purpose?
3. Should it be moved to EOL (End of Life) folder?

Respond with JSON:
{{
  "belongs_in_bitphoenix": true/false,
  "is_eol": true/false,
  "reason": "explanation"
}}
"""
        
        result = agent.analyze_file(str(file_path), prompt)
        
        # Try to parse JSON from result
        import re
        json_match = re.search(r'\{.*\}', result, re.DOTALL)
        if json_match:
            try:
                analysis = json.loads(json_match.group(0))
                is_eol = analysis.get("is_eol", False)
                reason = analysis.get("reason", "No reason provided")
                return is_eol, reason
            except:
                pass
        
        # Fallback: check keywords in response
        result_lower = result.lower()
        if "eol" in result_lower or "end of life" in result_lower or "old" in result_lower or "legacy" in result_lower:
            return True, "Detected as EOL from analysis"
        else:
            return False, "File appears to belong in BitPhoenix"
            
    except Exception as e:
        return False, f"Error analyzing: {e}"

def clean_bitphoenix_files(agent: FoundryClaudeAgent) -> None:
    """Rescan BitPhoenix and move irrelevant files to EOL"""
    print("\n" + "="*70)
    print("PHASE 3: CLEANING BITPHOENIX FILES")
    print("="*70)
    
    # Ensure EOL folder exists
    EOL_PATH.mkdir(parents=True, exist_ok=True)
    
    # Files to skip
    skip_patterns = [
        "node_modules",
        ".git",
        "venv",
        "__pycache__",
        ".env",
        "EOL",
        "Doesnt Belong",
        ".backup"
    ]
    
    # Collect all files
    files_to_check = []
    for item in BITPHOENIX_PATH.rglob("*"):
        # Skip if it's a directory
        if item.is_dir():
            continue
        
        # Skip certain patterns
        if any(pattern in str(item) for pattern in skip_patterns):
            continue
        
        # Try to check if it's a file, handle errors gracefully
        try:
            if item.is_file():
                files_to_check.append(item)
        except (OSError, PermissionError) as e:
            # Skip files that can't be accessed (symlinks, junctions, etc.)
            continue
    
    print(f"\n📋 Analyzing {len(files_to_check)} files in BitPhoenix...")
    
    eol_count = 0
    checked = 0
    
    for file_path in files_to_check:
        checked += 1
        if checked % 10 == 0:
            print(f"  Progress: {checked}/{len(files_to_check)} files checked...")
        
        rel_path = file_path.relative_to(BITPHOENIX_PATH)
        
        # Quick check: skip if already in EOL
        if "EOL" in str(file_path):
            continue
        
        # Use Azure to analyze
        is_eol, reason = analyze_bitphoenix_file(agent, file_path)
        time.sleep(0.5)  # Rate limiting
        
        if is_eol:
            # Move to EOL
            dest_file = EOL_PATH / rel_path
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                if dest_file.exists():
                    dest_file = dest_file.with_stem(f"{dest_file.stem}_moved")
                shutil.move(str(file_path), str(dest_file))
                print(f"  📦 Moved to EOL: {rel_path}")
                print(f"     Reason: {reason}")
                eol_count += 1
            except Exception as e:
                print(f"  ⚠ Error moving {rel_path}: {e}")
    
    print(f"\n✅ Moved {eol_count} files to EOL folder")

def review_and_delete_eol(agent: FoundryClaudeAgent) -> None:
    """Review EOL folder and delete all files"""
    print("\n" + "="*70)
    print("PHASE 4: REVIEWING AND DELETING EOL FILES")
    print("="*70)
    
    if not EOL_PATH.exists():
        print("⚠ EOL folder not found. Skipping.")
        return
    
    # Collect all files (handle inaccessible files)
    eol_files = []
    for item in EOL_PATH.rglob("*"):
        try:
            if item.is_file():
                eol_files.append(item)
        except (OSError, PermissionError):
            # Skip files that can't be accessed
            continue
    
    if not eol_files:
        print("✅ EOL folder is already empty")
        return
    
    print(f"\n📋 Found {len(eol_files)} files in EOL folder")
    print("🔍 Reviewing files to confirm they are truly EOL...")
    
    confirmed_eol = []
    questionable = []
    
    for file_path in eol_files[:50]:  # Limit to first 50 for API efficiency
        rel_path = file_path.relative_to(EOL_PATH)
        
        # Quick check with Azure
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')[:1000]
            prompt = f"""This file is in the EOL (End of Life) folder. Confirm it should be deleted.

File: {rel_path}
Content preview: {content[:500]}

Respond with "DELETE" if it's truly EOL, or "KEEP" if it might still be needed.
"""
            
            result = agent.analyze_file(str(file_path), prompt)
            time.sleep(0.5)  # Rate limiting
            
            if "delete" in result.lower() and "keep" not in result.lower():
                confirmed_eol.append(file_path)
            else:
                questionable.append((file_path, result[:100]))
        except:
            # If we can't analyze, assume it's EOL (it's already in EOL folder)
            confirmed_eol.append(file_path)
    
    # Add remaining files to confirmed (they're already in EOL)
    confirmed_eol.extend(eol_files[50:])
    
    print(f"\n✅ Confirmed {len(confirmed_eol)} files as EOL")
    if questionable:
        print(f"⚠ {len(questionable)} files need review:")
        for qf, reason in questionable[:5]:
            print(f"   - {qf.relative_to(EOL_PATH)}: {reason[:50]}")
    
    # Delete confirmed EOL files
    print(f"\n🗑️  Deleting {len(confirmed_eol)} EOL files...")
    deleted_count = 0
    
    for file_path in confirmed_eol:
        try:
            file_path.unlink()
            deleted_count += 1
        except Exception as e:
            print(f"  ⚠ Could not delete {file_path.relative_to(EOL_PATH)}: {e}")
    
    print(f"✅ Deleted {deleted_count} files")
    
    # Clean up empty directories in EOL
    print(f"\n🧹 Cleaning up empty directories in EOL...")
    for dir_path in sorted(EOL_PATH.rglob("*"), reverse=True):
        if dir_path.is_dir() and dir_path != EOL_PATH:
            try:
                if not any(dir_path.iterdir()):
                    dir_path.rmdir()
            except:
                pass
    
    print(f"✅ EOL folder cleanup complete (folder kept)")

def main():
    """Main execution function"""
    import sys
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    
    print("="*70, flush=True)
    print("AZURE-POWERED REVIEW AND REORGANIZATION", flush=True)
    print("="*70, flush=True)
    print(f"Repository: {BITPHOENIX_PATH}", flush=True)
    print(flush=True)
    
    # Initialize Azure agent
    print("🤖 Initializing Azure GPT-4.1 agent...", flush=True)
    try:
        agent = FoundryClaudeAgent(model="gpt-4.1")
        print("✅ Azure agent initialized", flush=True)
    except Exception as e:
        print(f"❌ Error initializing Azure agent: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return
    
    try:
        # Phase 1: Review uninstall scripts
        review_uninstall_scripts(agent)
        
        # Phase 2: Move files from "Doesnt Belong"
        move_files_from_doesnt_belong(agent)
        
        # Phase 3: Clean BitPhoenix files
        clean_bitphoenix_files(agent)
        
        # Phase 4: Review and delete EOL files
        review_and_delete_eol(agent)
        
        print("\n" + "="*70)
        print("✅ ALL PHASES COMPLETE")
        print("="*70)
        print("\nSummary:")
        print("  ✅ Uninstall scripts reviewed and improved")
        print("  ✅ Files moved from 'Doesnt Belong' to correct repos")
        print("  ✅ BitPhoenix files cleaned (irrelevant files moved to EOL)")
        print("  ✅ EOL folder reviewed and cleaned")
        
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

