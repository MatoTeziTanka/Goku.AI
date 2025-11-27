#!/usr/bin/env python3
"""
Find all Goku.AI related files and folders across entire GitHub directory.

This script searches for:
- Directories containing "goku" (case-insensitive)
- Files containing "goku" (case-insensitive)
- Files/folders with "Goku" variations
"""

import os
from pathlib import Path
import json
from datetime import datetime

# Base directory to search
BASE_DIR = Path(r"C:\Users\sethp\Documents\Github")

# Output file
OUTPUT_FILE = "GOKU-AI-FILES-DISCOVERY.json"
OUTPUT_MARKDOWN = "GOKU-AI-FILES-DISCOVERY.md"

def find_goku_files():
    """Find all Goku.AI related files and directories."""
    results = {
        "directories": [],
        "files": [],
        "goku_ai_repo": None,
        "timestamp": datetime.now().isoformat(),
        "base_directory": str(BASE_DIR)
    }
    
    # Check if Goku.AI repository exists
    goku_ai_repo = BASE_DIR / "Goku.AI"
    if goku_ai_repo.exists() and goku_ai_repo.is_dir():
        results["goku_ai_repo"] = str(goku_ai_repo)
        print(f"✅ Found Goku.AI repository: {goku_ai_repo}")
    
    # Search for directories
    print("🔍 Searching for directories containing 'goku'...")
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip .git directories and other hidden/system directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'venv_deploy']]
        
        for dir_name in dirs:
            if 'goku' in dir_name.lower():
                full_path = Path(root) / dir_name
                relative_path = full_path.relative_to(BASE_DIR)
                results["directories"].append({
                    "name": dir_name,
                    "full_path": str(full_path),
                    "relative_path": str(relative_path),
                    "parent": str(Path(root).relative_to(BASE_DIR))
                })
    
    # Search for files
    print("🔍 Searching for files containing 'goku'...")
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip .git directories and other hidden/system directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules', 'venv', 'venv_deploy']]
        
        for file_name in files:
            if 'goku' in file_name.lower():
                full_path = Path(root) / file_name
                relative_path = full_path.relative_to(BASE_DIR)
                
                # Get file size
                try:
                    size = full_path.stat().st_size
                except:
                    size = 0
                
                results["files"].append({
                    "name": file_name,
                    "full_path": str(full_path),
                    "relative_path": str(relative_path),
                    "parent": str(Path(root).relative_to(BASE_DIR)),
                    "size_bytes": size
                })
    
    return results

def generate_markdown_report(results):
    """Generate markdown report from results."""
    md = f"""# Goku.AI Files Discovery Report

**Date:** {results['timestamp']}  
**Base Directory:** {results['base_directory']}

---

## 📊 SUMMARY

- **Goku.AI Repository Found:** {'✅ Yes' if results['goku_ai_repo'] else '❌ No'}
- **Directories Found:** {len(results['directories'])}
- **Files Found:** {len(results['files'])}

---

## 📁 GOKU.AI REPOSITORY

"""
    
    if results['goku_ai_repo']:
        md += f"**Location:** `{results['goku_ai_repo']}`\n\n"
    else:
        md += "**Status:** ❌ Goku.AI repository not found in expected location\n\n"
    
    md += "---\n\n## 📂 DIRECTORIES CONTAINING 'GOKU'\n\n"
    
    if results['directories']:
        md += "| Directory Name | Full Path | Relative Path | Parent |\n"
        md += "|----------------|-----------|---------------|--------|\n"
        for dir_info in results['directories']:
            md += f"| `{dir_info['name']}` | `{dir_info['full_path']}` | `{dir_info['relative_path']}` | `{dir_info['parent']}` |\n"
    else:
        md += "No directories found.\n"
    
    md += "\n---\n\n## 📄 FILES CONTAINING 'GOKU'\n\n"
    
    if results['files']:
        md += "| File Name | Full Path | Relative Path | Parent | Size (bytes) |\n"
        md += "|-----------|-----------|---------------|--------|--------------|\n"
        for file_info in results['files']:
            size_kb = file_info['size_bytes'] / 1024
            md += f"| `{file_info['name']}` | `{file_info['full_path']}` | `{file_info['relative_path']}` | `{file_info['parent']}` | {file_info['size_bytes']:,} ({size_kb:.2f} KB) |\n"
    else:
        md += "No files found.\n"
    
    md += "\n---\n\n## 🎯 CONSOLIDATION RECOMMENDATIONS\n\n"
    
    if results['goku_ai_repo']:
        md += "### Files/Directories to Move to Goku.AI:\n\n"
        
        # Files not in Goku.AI repo
        files_to_move = [f for f in results['files'] if 'Goku.AI' not in f['full_path']]
        dirs_to_move = [d for d in results['directories'] if 'Goku.AI' not in d['full_path']]
        
        if files_to_move:
            md += "**Files:**\n"
            for file_info in files_to_move:
                md += f"- `{file_info['relative_path']}` → Move to `Goku.AI/`\n"
        
        if dirs_to_move:
            md += "\n**Directories:**\n"
            for dir_info in dirs_to_move:
                md += f"- `{dir_info['relative_path']}/` → Move to `Goku.AI/`\n"
    else:
        md += "**Action Required:** Create Goku.AI repository first, then move all files.\n"
    
    md += "\n---\n\n**END OF REPORT**\n"
    
    return md

def main():
    """Main function."""
    print("🚀 Starting Goku.AI files discovery...")
    print(f"📁 Base directory: {BASE_DIR}")
    print()
    
    results = find_goku_files()
    
    # Save JSON
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"✅ Saved JSON results to: {OUTPUT_FILE}")
    
    # Save Markdown
    md_report = generate_markdown_report(results)
    with open(OUTPUT_MARKDOWN, 'w', encoding='utf-8') as f:
        f.write(md_report)
    print(f"✅ Saved Markdown report to: {OUTPUT_MARKDOWN}")
    
    # Print summary
    print()
    print("📊 SUMMARY:")
    print(f"   Goku.AI Repository: {'✅ Found' if results['goku_ai_repo'] else '❌ Not Found'}")
    print(f"   Directories Found: {len(results['directories'])}")
    print(f"   Files Found: {len(results['files'])}")
    print()
    print("✅ Discovery complete!")
    print(f"📄 Review: {OUTPUT_MARKDOWN}")

if __name__ == '__main__':
    main()



