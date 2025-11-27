"""
Analyze files in root GitHub directory to identify EOL candidates.
Categorizes files by type and identifies which are likely obsolete.
"""

import os
from pathlib import Path
from collections import defaultdict
from datetime import datetime

BASE_DIR = Path(r"C:\Users\sethp\Documents\Github")
EOL_DIR = BASE_DIR / "End of Life"

# Skip directories
SKIP_DIRS = {
    'End of Life', 'BitPhoenix', 'Dell-Server-Roadmap', 'Dino-Cloud', 'DinoCloud',
    'FamilyFork', 'GSMG.IO', 'Goku.AI', 'KeyHound', 'ScalpStorm', 'StreamForge',
    'Server-Roadmap', 'AICloakCoin', 'BackTrack', 'CryptoPuzzles', 'CursorAI',
    'DashDenCity', 'discord-bot-monetization', 'Family-Care-Ideas', 'Fiverr',
    'Flayer', 'FreeLancer', 'Games-with-Logan', 'InfraScan-Systems-Inc',
    'Marketing-Automation', 'MyHealth', 'PassiveIncome', 'project-repo-template',
    'pterodactyl-game-hosting', 'SethFlix-Plex', 'unknown', 'passive-income-infrastructure',
    'Keyhound-BACKUP-20251125-205203', 'azure_reviews', '.git'
}

# Patterns that suggest EOL files
EOL_PATTERNS = {
    'review': ['review', 'REVIEW', 'audit', 'AUDIT'],
    'summary': ['summary', 'SUMMARY', 'status', 'STATUS'],
    'fix': ['fix', 'FIX', 'bug', 'BUG'],
    'analysis': ['analysis', 'ANALYSIS', 'analyze'],
    'guide': ['guide', 'GUIDE', 'setup', 'SETUP', 'instructions'],
    'test': ['test', 'TEST', 'check', 'CHECK'],
    'old_scripts': ['move_', 'identify_', 'verify_', 'check_', 'analyze_', 'compile_'],
    'azure_outputs': ['AZURE_', 'azure_'],
    'intermediate': ['NEXT_STEPS', 'PHASE_', 'COMPLETE', 'COMPILED'],
    'documentation': ['.md', '.txt', '.json'],
}

# Files that should be KEPT (active/important)
KEEP_FILES = {
    'MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED.md',
    'MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND.md',
    'azure_100_percent_qc_improvement_FIXED_CONSENSUS.py',
    'azure_100_percent_qc_improvement_FIXED.py',
    'azure_100_percent_qc_improvement.py',
    'README.md',
    '.gitignore',
    'requirements.txt',
    'setup.py',
}

def categorize_file(filepath: Path) -> dict:
    """Categorize a file to determine if it's EOL."""
    name = filepath.name.lower()
    ext = filepath.suffix.lower()
    
    categories = []
    eol_score = 0
    reasons = []
    
    # Check against EOL patterns
    if any(pattern in name for pattern in EOL_PATTERNS['review']):
        categories.append('review')
        eol_score += 3
        reasons.append('Review/audit file')
    
    if any(pattern in name for pattern in EOL_PATTERNS['summary']):
        categories.append('summary')
        eol_score += 2
        reasons.append('Summary/status file')
    
    if any(pattern in name for pattern in EOL_PATTERNS['fix']):
        categories.append('fix')
        eol_score += 1
        reasons.append('Fix documentation')
    
    if any(pattern in name for pattern in EOL_PATTERNS['old_scripts']):
        categories.append('old_script')
        eol_score += 2
        reasons.append('Old cleanup/utility script')
    
    if any(pattern in name for pattern in EOL_PATTERNS['azure_outputs']):
        if 'FIXED_CONSENSUS' not in filepath.name and 'FIXED' not in filepath.name:
            categories.append('azure_output')
            eol_score += 2
            reasons.append('Azure output file')
    
    if ext in ['.md', '.txt'] and 'MASTER-PROMPT' not in filepath.name:
        categories.append('documentation')
        eol_score += 1
        reasons.append('Documentation file')
    
    # Check file age (if older than 30 days, more likely EOL)
    try:
        mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
        days_old = (datetime.now() - mtime).days
        if days_old > 30:
            eol_score += 1
            reasons.append(f'File is {days_old} days old')
    except:
        pass
    
    return {
        'path': filepath,
        'name': filepath.name,
        'categories': categories,
        'eol_score': eol_score,
        'reasons': reasons,
        'size': filepath.stat().st_size if filepath.exists() else 0,
    }

def main():
    """Analyze all files in root directory."""
    print("=" * 70)
    print("ANALYZING ROOT DIRECTORY FILES")
    print("=" * 70)
    print()
    
    files_by_category = defaultdict(list)
    eol_candidates = []
    keep_files = []
    
    # Get all files in root
    for item in BASE_DIR.iterdir():
        if item.is_file() and item.name not in KEEP_FILES:
            cat = categorize_file(item)
            if cat['eol_score'] >= 2:
                eol_candidates.append(cat)
            else:
                keep_files.append(cat)
            
            for category in cat['categories']:
                files_by_category[category].append(cat)
    
    # Sort by EOL score
    eol_candidates.sort(key=lambda x: x['eol_score'], reverse=True)
    
    print(f"📊 ANALYSIS RESULTS")
    print(f"{'='*70}")
    print(f"Total files analyzed: {len(eol_candidates) + len(keep_files)}")
    print(f"EOL candidates (score >= 2): {len(eol_candidates)}")
    print(f"Keep files (score < 2): {len(keep_files)}")
    print()
    
    print(f"📁 FILES BY CATEGORY")
    print(f"{'='*70}")
    for category, files in sorted(files_by_category.items()):
        print(f"  {category}: {len(files)} files")
    print()
    
    print(f"🗑️  TOP 50 EOL CANDIDATES (by score)")
    print(f"{'='*70}")
    for i, file_info in enumerate(eol_candidates[:50], 1):
        print(f"{i:3d}. [{file_info['eol_score']}] {file_info['name']}")
        print(f"     Reasons: {', '.join(file_info['reasons'])}")
    
    if len(eol_candidates) > 50:
        print(f"\n     ... and {len(eol_candidates) - 50} more candidates")
    
    print()
    print(f"💾 GENERATING EOL CANDIDATES LIST")
    print(f"{'='*70}")
    
    # Write EOL candidates to file
    eol_list_file = BASE_DIR / "EOL_CANDIDATES_ANALYSIS.json"
    import json
    with open(eol_list_file, 'w', encoding='utf-8') as f:
        json.dump({
            'total_files': len(eol_candidates) + len(keep_files),
            'eol_candidates': [
                {
                    'name': f['name'],
                    'path': str(f['path']),
                    'eol_score': f['eol_score'],
                    'reasons': f['reasons'],
                    'categories': f['categories'],
                    'size': f['size'],
                }
                for f in eol_candidates
            ],
            'keep_files': [
                {
                    'name': f['name'],
                    'path': str(f['path']),
                    'eol_score': f['eol_score'],
                }
                for f in keep_files[:20]  # Sample
            ]
        }, f, indent=2)
    
    print(f"✅ Analysis saved to: {eol_list_file.name}")
    print()
    print(f"💡 RECOMMENDATION")
    print(f"{'='*70}")
    print(f"Review the top candidates above. Files with score >= 3 are")
    print(f"highly likely to be EOL and safe to move.")
    print()

if __name__ == "__main__":
    main()

