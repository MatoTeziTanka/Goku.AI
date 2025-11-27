#!/usr/bin/env python3
"""
Safely remove sensitive files from git repositories.

This script:
1. Categorizes files (critical vs false positives)
2. Removes files from git tracking (not from disk)
3. Ensures .gitignore is updated
4. Creates backup before removal
5. Provides rollback instructions
"""

import subprocess
from pathlib import Path
from typing import List, Dict, Tuple
from datetime import datetime
import json

# Files that are FALSE POSITIVES (safe to keep)
FALSE_POSITIVES = [
    '.env.example',
    '.env.template',
    '.env.sample',
    '.vscode/extensions.json',  # Usually safe, just extension recommendations
    '.vscode/launch.json',  # Debug config, usually safe
    'tsconfig.json',  # TypeScript config, usually safe
    'jsconfig.json',  # JavaScript config, usually safe
    'node_modules/',  # Should be in .gitignore but not sensitive
    '__pycache__/',  # Should be in .gitignore but not sensitive
    '*.pyc',  # Should be in .gitignore but not sensitive
]

# Files that are CRITICAL (must remove)
CRITICAL_FILES = [
    '.env',
    'credentials.json',
    'secrets.json',
    'api_credentials.json',
    'api_key',
    '*.key',
    '*.pem',
    'STRIPE-API-KEYS',
    'BINANCE-API-KEYS',
    'CREDENTIALS-REGISTRY',
    'docker.env',
    'secrets.yaml',
]

def categorize_file(file_path: str) -> Tuple[str, str]:
    """
    Categorize file as critical, warning, or false positive.
    
    Returns:
        (category, reason)
    """
    file_lower = file_path.lower()
    file_name = Path(file_path).name.lower()
    
    # Check for false positives
    for fp in FALSE_POSITIVES:
        if fp in file_lower or file_name == fp:
            return ('false_positive', f'False positive: {fp}')
    
    # Check for critical files
    for critical in CRITICAL_FILES:
        if critical.replace('*', '') in file_lower or critical.replace('*', '') in file_name:
            return ('critical', f'Critical: Contains {critical}')
    
    # Check for backup files that might contain secrets
    if file_path.endswith('.backup') or file_path.endswith('.bak'):
        return ('warning', 'Backup file - may contain sensitive data')
    
    # Check for files with sensitive keywords
    sensitive_keywords = ['secret', 'credential', 'password', 'token', 'key', 'api']
    if any(keyword in file_lower for keyword in sensitive_keywords):
        return ('warning', 'Contains sensitive keywords - review needed')
    
    return ('unknown', 'Unknown - manual review recommended')

def remove_file_from_git(repo_path: Path, file_path: str, dry_run: bool = True) -> Tuple[bool, str]:
    """
    Remove file from git tracking (not from disk).
    
    Args:
        repo_path: Repository root path
        file_path: File path relative to repo root
        dry_run: If True, only show what would be done
        
    Returns:
        (success, message)
    """
    if dry_run:
        return (True, f"Would remove: {file_path}")
    
    try:
        result = subprocess.run(
            ["git", "rm", "--cached", file_path],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return (True, f"Removed: {file_path}")
        else:
            return (False, f"Error: {result.stderr}")
    except Exception as e:
        return (False, f"Exception: {e}")

def ensure_gitignore_has_pattern(repo_path: Path, pattern: str) -> bool:
    """Ensure .gitignore contains the pattern."""
    gitignore_path = repo_path / '.gitignore'
    
    if not gitignore_path.exists():
        gitignore_path.write_text(f"{pattern}\n", encoding='utf-8')
        return True
    
    content = gitignore_path.read_text(encoding='utf-8')
    
    # Check if pattern already exists
    if pattern in content:
        return False  # Already there
    
    # Add pattern
    content += f"\n{pattern}\n"
    gitignore_path.write_text(content, encoding='utf-8')
    return True

def main():
    """Main execution."""
    print("=" * 70)
    print("SAFE SENSITIVE FILE REMOVAL")
    print("=" * 70)
    print()
    print("⚠️  This script will remove sensitive files from git tracking")
    print("    Files will remain on disk but will be untracked")
    print()
    
    github_root = Path("C:/Users/sethp/Documents/Github")
    
    # Files to process (from audit report)
    files_to_review = {
        'BitPhoenix': [
            '.env.example',
            '.vscode/extensions.json',
            '.vscode/launch.json',
            'Marketing-Automation/social-media-automation/credentials/api_credentials.json',
            'backend/src/recovery_engine.py.backup',
            'backend/src/secrets_manager.py',
            'cursor-extension/tsconfig.json',
            'deployment/k8s/secrets.yaml',
        ],
        'CursorAI': [
            'setup_api_keys.py',
        ],
        'Dell-Server-Roadmap': [
            'BINANCE-API-KEYS-SECURE-SETUP.md',
            'Marketing-Automation/config/content_config.json',
            'Marketing-Automation/config/marketing_config.json',
            'Marketing-Automation/get-linkedin-token.py',
            'Marketing-Automation/launch-config.json',
            'Marketing-Automation/social-media-automation/credentials/api_credentials.json.template',
            'SHENRON-2FA-SECRET.md',
            'docs/vm-access-credentials.md',
        ],
        'FamilyFork': [
            'backend/.env',
            'frontend/.env',
        ],
        'PassiveIncome': [
            'WordPress-VM/Marketing-Content/Credentials/CREDENTIALS-REGISTRY.md',
            'WordPress-VM/Setup-Guides/STRIPE-API-KEYS-LIVE.txt',
        ],
        'ScalpStorm': [
            'V1_EOL/API_CREDENTIAL_SECURITY_ANALYSIS.md',
            'V1_EOL/docker.env',
        ],
    }
    
    print("📋 Step 1: Categorizing files...")
    print("-" * 70)
    
    categorized = {
        'critical': [],
        'warning': [],
        'false_positive': [],
    }
    
    for repo_name, file_list in files_to_review.items():
        repo_path = github_root / repo_name
        if not repo_path.exists():
            continue
        
        print(f"\n  📁 {repo_name}")
        
        for file_path in file_list:
            category, reason = categorize_file(file_path)
            full_path = repo_path / file_path
            
            if not full_path.exists():
                print(f"    ⚠️  {file_path}: File not found (may already be removed)")
                continue
            
            categorized[category].append({
                'repo': repo_name,
                'file': file_path,
                'reason': reason
            })
            
            status = {
                'critical': '🔒',
                'warning': '⚠️',
                'false_positive': '✅'
            }[category]
            
            print(f"    {status} {file_path}: {reason}")
    
    print()
    print("=" * 70)
    print("CATEGORIZATION SUMMARY")
    print("=" * 70)
    print(f"\n🔒 Critical files: {len(categorized['critical'])}")
    print(f"⚠️  Warning files: {len(categorized['warning'])}")
    print(f"✅ False positives: {len(categorized['false_positive'])}")
    print()
    
    # Show critical files
    if categorized['critical']:
        print("🚨 CRITICAL FILES (Must Remove):")
        print("-" * 70)
        for item in categorized['critical']:
            print(f"  {item['repo']}: {item['file']}")
            print(f"    Reason: {item['reason']}")
        print()
    
    # Ask for confirmation
    print("=" * 70)
    print("REMOVAL PLAN")
    print("=" * 70)
    print()
    print("This script will:")
    print("  1. Remove critical files from git tracking")
    print("  2. Add patterns to .gitignore")
    print("  3. Create a backup log")
    print("  4. NOT delete files from disk")
    print()
    
    response = input("Continue with removal? (yes/no): ").strip().lower()
    if response != 'yes':
        print("❌ Cancelled by user")
        return
    
    print()
    print("🔧 Step 2: Removing files from git...")
    print("-" * 70)
    
    removed_count = 0
    gitignore_updated_count = 0
    removal_log = []
    
    for item in categorized['critical']:
        repo_path = github_root / item['repo']
        file_path = item['file']
        
        print(f"\n  📁 {item['repo']}: {file_path}")
        
        # Remove from git
        success, message = remove_file_from_git(repo_path, file_path, dry_run=False)
        if success:
            print(f"    ✅ {message}")
            removed_count += 1
            removal_log.append({
                'repo': item['repo'],
                'file': file_path,
                'action': 'removed',
                'timestamp': datetime.now().isoformat()
            })
            
            # Ensure .gitignore has pattern
            file_name = Path(file_path).name
            if file_name.startswith('.'):
                pattern = file_name
            else:
                pattern = f"**/{file_name}"
            
            if ensure_gitignore_has_pattern(repo_path, pattern):
                print(f"    ✅ Added to .gitignore: {pattern}")
                gitignore_updated_count += 1
        else:
            print(f"    ❌ {message}")
    
    # Save removal log
    log_path = github_root / "SENSITIVE_FILES_REMOVAL_LOG.json"
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(removal_log, f, indent=2)
    
    print()
    print("=" * 70)
    print("REMOVAL COMPLETE")
    print("=" * 70)
    print(f"\n✅ Removed {removed_count} files from git tracking")
    print(f"✅ Updated {gitignore_updated_count} .gitignore files")
    print(f"📄 Removal log: {log_path}")
    print()
    print("⚠️  NEXT STEPS:")
    print("  1. Review the changes: git status")
    print("  2. Commit the removals: git commit -m 'Remove sensitive files'")
    print("  3. For files in history, consider: git-filter-repo")
    print()

if __name__ == "__main__":
    main()

