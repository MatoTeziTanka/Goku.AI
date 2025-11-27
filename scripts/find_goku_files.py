<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/usr/bin/env python3
"""Find all Goku.AI related files without moving them."""

from pathlib import Path
import re

SEARCH_KEYWORDS = [
    'goku', 'shenron', 'dragonball', 'dragon ball',
    'vm100', 'vm101', '<VM100_IP>', '<VM101_IP>',
    'lm studio', 'lm-studio', 'personalities', 'control node',
]

SOURCE_ROOT = Path(r"C:\Users\sethp\Documents\Github")

def should_skip(path):
    skip = ['.git', '__pycache__', 'node_modules', '.venv', 'venv', 
            'env', '.pytest_cache', 'dist', 'build', '.idea', '.vscode']
    return any(s in str(path).lower() for s in skip)

def matches(file_path):
    name = file_path.name.lower()
    path_str = str(file_path).lower()
    
    matched = []
    for kw in SEARCH_KEYWORDS:
        if kw.lower() in name or kw.lower() in path_str:
            matched.append(kw)
    
    # Check content for text files
    if file_path.suffix in ['.md', '.txt', '.py', '.js', '.json', '.yaml', '.yml', '.sh', '.bat', '.ps1']:
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
            for kw in SEARCH_KEYWORDS:
                if kw.lower() in content and kw not in matched:
                    matched.append(kw)
        except:
            pass
    
    return matched

def main():
    print("=" * 70)
    print("FINDING GOKU.AI RELATED FILES")
    print("=" * 70)
    print()
    
    found = []
    
    for item in SOURCE_ROOT.rglob('*'):
        if should_skip(item) or not item.is_file():
            continue
        if item.parent.name == "Goku.AI":
            continue
            
        matched = matches(item)
        if matched:
            rel_path = item.relative_to(SOURCE_ROOT)
            found.append({
                'path': rel_path,
                'full_path': item,
                'keywords': matched,
                'size': item.stat().st_size
            })
            print(f"  {rel_path}")
            print(f"    Keywords: {', '.join(matched[:5])}")
    
    print()
    print(f"Total: {len(found)} files found")
    print()
    
    # Save list
    import json
    output = SOURCE_ROOT / "GOKU_FILES_LIST.json"
    with open(output, 'w', encoding='utf-8') as f:
        json.dump([{'path': str(f['path']), 'keywords': f['keywords']} for f in found], 
                  f, indent=2)
    
    print(f"List saved to: {output}")
    print()
    print("Run consolidate_goku_ai_files.py to move these files to Goku.AI")

if __name__ == "__main__":
    main()

