<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/usr/bin/env python3
r"""
Consolidate all Goku.AI, Shenron, DragonBall Z, VM100/VM101 related files
to C:\Users\sethp\Documents\Github\Goku.AI

This script:
1. Finds all files related to the specified topics
2. Moves them to Goku.AI repository
3. Preserves git history where possible
4. Creates a detailed log of all moves
"""

import os
import shutil
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import re

# Search keywords
SEARCH_KEYWORDS = [
    'goku',
    'shenron',
    'dragonball',
    'dragon ball',
    'vm100',
    'vm101',
    '<VM100_IP>',
    '<VM101_IP>',
    'lm studio',
    'lm-studio',
    'personalities',
    'control node',
]

# Target directory
TARGET_REPO = Path(r"C:\Users\sethp\Documents\Github\Goku.AI")
SOURCE_ROOT = Path(r"C:\Users\sethp\Documents\Github")

def should_skip_path(path: Path) -> bool:
    """Check if path should be skipped."""
    skip_patterns = [
        '.git',
        '__pycache__',
        'node_modules',
        '.venv',
        'venv',
        'env',
        '.pytest_cache',
        'dist',
        'build',
        '.idea',
        '.vscode',
        'Goku.AI',  # Don't move files from target repo
    ]
    
    path_str = str(path).lower()
    return any(pattern.lower() in path_str for pattern in skip_patterns)

def file_matches_keywords(file_path: Path) -> Tuple[bool, List[str]]:
    """
    Check if file matches search keywords.
    
    Returns:
        (matches, matched_keywords)
    """
    file_name_lower = file_path.name.lower()
    file_path_lower = str(file_path).lower()
    
    matched_keywords = []
    
    for keyword in SEARCH_KEYWORDS:
        keyword_lower = keyword.lower()
        if keyword_lower in file_name_lower or keyword_lower in file_path_lower:
            matched_keywords.append(keyword)
    
    # Also check file content for text files
    if file_path.suffix in ['.md', '.txt', '.py', '.js', '.json', '.yaml', '.yml', '.sh', '.bat', '.ps1']:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
            for keyword in SEARCH_KEYWORDS:
                if keyword.lower() in content and keyword not in matched_keywords:
                    matched_keywords.append(keyword)
        except Exception:
            pass
    
    return len(matched_keywords) > 0, matched_keywords

def find_matching_files(root_dir: Path) -> List[Dict]:
    """Find all files matching search criteria."""
    matching_files = []
    
    print("🔍 Searching for matching files...")
    print("-" * 70)
    
    # Skip target repo itself
    if root_dir.name == "Goku.AI":
        return []
    
    for item in root_dir.rglob('*'):
        # Skip if should be ignored
        if should_skip_path(item):
            continue
        
        # Only process files
        if not item.is_file():
            continue
        
        # Check if matches
        matches, keywords = file_matches_keywords(item)
        
        if matches:
            relative_path = item.relative_to(SOURCE_ROOT)
            matching_files.append({
                'source': item,
                'relative_path': relative_path,
                'keywords': keywords,
                'size': item.stat().st_size,
            })
            print(f"  ✅ Found: {relative_path}")
            print(f"     Keywords: {', '.join(keywords[:5])}")
    
    return matching_files

def determine_target_path(source_file: Path, source_repo: Path) -> Path:
    """Determine target path in Goku.AI repository."""
    # Get relative path from source repo root
    if source_repo != SOURCE_ROOT:
        relative = source_file.relative_to(source_repo)
    else:
        relative = source_file.relative_to(SOURCE_ROOT)
        # If file is in root, use repo name as subdirectory
        repo_name = source_file.parent.name if source_file.parent != SOURCE_ROOT else "root"
        relative = Path(repo_name) / source_file.name
    
    # Create target path
    target_path = TARGET_REPO / relative
    
    # Avoid overwriting existing files
    if target_path.exists():
        # Add source repo name as prefix
        if source_repo != SOURCE_ROOT:
            repo_name = source_repo.name
            target_path = TARGET_REPO / repo_name / relative
    
    return target_path

def move_file_safely(source: Path, target: Path, dry_run: bool = False) -> Tuple[bool, str]:
    """Move file safely, creating directories as needed."""
    if dry_run:
        return (True, f"Would move to: {target}")
    
    try:
        # Create target directory
        target.parent.mkdir(parents=True, exist_ok=True)
        
        # If target exists, create unique name
        if target.exists():
            counter = 1
            stem = target.stem
            suffix = target.suffix
            while target.exists():
                target = target.parent / f"{stem}_{counter}{suffix}"
                counter += 1
        
        # Move file
        shutil.move(str(source), str(target))
        return (True, f"Moved to: {target.relative_to(TARGET_REPO)}")
    except Exception as e:
        return (False, str(e))

def get_repo_root(file_path: Path) -> Path:
    """Find git repository root for a file."""
    current = file_path.parent
    while current != current.parent:
        if (current / '.git').exists():
            return current
        current = current.parent
    return SOURCE_ROOT  # Not in a repo

def main():
    """Main execution."""
    print("=" * 70)
    print("CONSOLIDATE GOKU.AI RELATED FILES")
    print("=" * 70)
    print()
    print("Searching for files related to:")
    print("  - Goku.AI, Shenron, DragonBall Z")
    print("  - VM100, VM101")
    print("  - IPs <VM100_IP>, <VM101_IP>")
    print("  - LM Studio, Personalities")
    print("  - Control node, Knowledge base")
    print()
    
    # Ensure target exists
    TARGET_REPO.mkdir(parents=True, exist_ok=True)
    
    # Initialize git if needed
    if not (TARGET_REPO / '.git').exists():
        print("📦 Initializing git in Goku.AI...")
        subprocess.run(["git", "init"], cwd=TARGET_REPO, capture_output=True)
        print("  ✅ Git initialized")
        print()
    
    # Find all matching files
    print("🔍 Step 1: Finding matching files...")
    print("-" * 70)
    
    all_matches = []
    
    # Search in each repository
    for item in SOURCE_ROOT.iterdir():
        if not item.is_dir() or item.name == "Goku.AI":
            continue
        
        if should_skip_path(item):
            continue
        
        matches = find_matching_files(item)
        all_matches.extend(matches)
    
    # Also search root directory
    for item in SOURCE_ROOT.iterdir():
        if item.is_file() and not should_skip_path(item):
            matches, keywords = file_matches_keywords(item)
            if matches:
                all_matches.append({
                    'source': item,
                    'relative_path': item.name,
                    'keywords': keywords,
                    'size': item.stat().st_size,
                })
    
    print()
    print(f"✅ Found {len(all_matches)} matching files")
    print()
    
    if not all_matches:
        print("No matching files found.")
        return
    
    # Group by source repository
    print("📋 Step 2: Organizing files...")
    print("-" * 70)
    
    files_by_repo = {}
    for match in all_matches:
        repo_root = get_repo_root(match['source'])
        repo_name = repo_root.name if repo_root != SOURCE_ROOT else "root"
        
        if repo_name not in files_by_repo:
            files_by_repo[repo_name] = []
        files_by_repo[repo_name].append(match)
    
    print(f"Files found in {len(files_by_repo)} locations:")
    for repo_name, files in files_by_repo.items():
        print(f"  - {repo_name}: {len(files)} files")
    print()
    
    # Show preview
    print("📋 Step 3: Preview of files to move...")
    print("-" * 70)
    
    total_size = 0
    for repo_name, files in files_by_repo.items():
        print(f"\n  📁 From {repo_name}:")
        for match in files[:10]:  # Show first 10
            size_kb = match['size'] / 1024
            total_size += match['size']
            print(f"    - {match['relative_path']} ({size_kb:.1f} KB)")
            print(f"      Keywords: {', '.join(match['keywords'][:3])}")
        if len(files) > 10:
            print(f"    ... and {len(files) - 10} more files")
    
    print()
    print(f"Total size: {total_size / 1024 / 1024:.2f} MB")
    print()
    
    # Confirm
    response = input("Continue with move? (yes/no): ").strip().lower()
    if response != 'yes':
        print("❌ Cancelled")
        return
    
    # Move files
    print()
    print("📦 Step 4: Moving files...")
    print("-" * 70)
    
    moved_count = 0
    error_count = 0
    move_log = []
    
    for repo_name, files in files_by_repo.items():
        print(f"\n  📁 {repo_name}: {len(files)} files")
        
        for match in files:
            source = match['source']
            repo_root = get_repo_root(source)
            target = determine_target_path(source, repo_root)
            
            success, message = move_file_safely(source, target, dry_run=False)
            
            if success:
                print(f"    ✅ {source.name} → {target.relative_to(TARGET_REPO)}")
                moved_count += 1
                move_log.append({
                    'source': str(source.relative_to(SOURCE_ROOT)),
                    'target': str(target.relative_to(TARGET_REPO)),
                    'keywords': match['keywords'],
                    'timestamp': datetime.now().isoformat()
                })
            else:
                print(f"    ❌ {source.name}: {message}")
                error_count += 1
    
    print()
    print("=" * 70)
    print("MOVE COMPLETE")
    print("=" * 70)
    print()
    print(f"✅ Moved: {moved_count} files")
    print(f"❌ Errors: {error_count} files")
    print(f"📁 Target: {TARGET_REPO}")
    print()
    
    # Save log
    import json
    log_path = SOURCE_ROOT / "GOKU_AI_CONSOLIDATION_LOG.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(move_log, f, indent=2)
    
    print(f"📄 Move log: {log_path}")
    print()
    
    # Create README in Goku.AI
    readme_path = TARGET_REPO / "CONSOLIDATION_README.md"
    readme_content = f"""# Goku.AI File Consolidation

**Date:** {datetime.now().isoformat()}

## Overview

This repository contains all files related to:
- Goku.AI
- Shenron
- DragonBall Z
- VM100 and VM101
- IPs <VM100_IP> and <VM101_IP>
- LM Studio knowledge base
- Personalities
- Control node configurations

## Files Consolidated

**Total files moved:** {moved_count}

### By Source Repository

"""
    
    for repo_name, files in files_by_repo.items():
        readme_content += f"\n#### {repo_name}\n"
        readme_content += f"- Files: {len(files)}\n"
        for match in files[:20]:
            readme_content += f"  - `{match['relative_path']}`\n"
        if len(files) > 20:
            readme_content += f"  - ... and {len(files) - 20} more\n"
    
    readme_content += f"""

## Structure

Files are organized by their source repository to maintain context.

## Next Steps

1. Review consolidated files
2. Organize into logical structure
3. Update documentation
4. Commit to git

---
**Consolidation log:** See GOKU_AI_CONSOLIDATION_LOG.json in parent directory
"""
    
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"📄 Created README: {readme_path}")
    print()

if __name__ == "__main__":
    main()

