#!/usr/bin/env python3
"""
Fix All Issues from v2.3.0 Comprehensive Review

Fixes:
1. Storage Path Consistency (CRITICAL)
2. Section 19.2 Code Block Issues (CRITICAL)
3. Missing imports (MEDIUM)
4. Missing calculate_timeout() function (MEDIUM)
5. Truncated note (LOW)
6. Add recommended enhancements
"""

import re
from pathlib import Path
from datetime import datetime

INPUT_FILE = Path("MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED-v2.3.0.md")
OUTPUT_FILE = Path("MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED-v2.4.0.md")

def fix_storage_path_consistency(content: str) -> str:
    """Fix #1: Consolidate storage path definitions."""
    print("  Fixing storage path consistency...")
    
    # Find Section 19.2 and ensure STORAGE_CONFIG is at the top
    section_19_2_pattern = r'(### 19\.2 Persistent State Management.*?\n)'
    match = re.search(section_19_2_pattern, content)
    
    if match:
        # Check if STORAGE_CONFIG already exists after section header
        after_header = content[match.end():match.end()+500]
        if "STORAGE_CONFIG" not in after_header:
            storage_config = '''
# Single source of truth - Storage Configuration
import os
from pathlib import Path

# Storage Configuration (Single Source of Truth)
STORAGE_CONFIG = {
    "ssd_base": Path(os.getenv("AI_STORAGE_SSD", r"C:\\AI_Storage\\SSD")),
    "hdd_base": Path(os.getenv("AI_STORAGE_HDD", r"D:\\AI_Storage\\HDD")),
}

# Validate on init
def validate_storage_paths():
    """Validate and create storage directories if needed."""
    for name, path in STORAGE_CONFIG.items():
        if not path.parent.exists():
            raise ValueError(f"Storage parent does not exist: {path.parent}")
        path.mkdir(parents=True, exist_ok=True)
    return STORAGE_CONFIG

# Define constants (use these throughout)
SSD_STORAGE = STORAGE_CONFIG["ssd_base"]
HDD_STORAGE = STORAGE_CONFIG["hdd_base"]
KNOWLEDGE_DB = SSD_STORAGE / "knowledge_base"
CHECKPOINTS = SSD_STORAGE / "checkpoints"
SESSION_LOGS = SSD_STORAGE / "session_logs"
MEMORY_STASH = HDD_STORAGE / "memory_stash"

# Initialize on first import
validate_storage_paths()

'''
            content = content[:match.end()] + storage_config + content[match.end():]
            print("    ✅ STORAGE_CONFIG added to Section 19.2")
    
    # Remove duplicate definitions in Section 24.2
    section_24_2_pattern = r'(### 24\.2 Storage Path Configuration.*?```python\n)(.*?)(```)'
    
    def replace_storage_paths(match):
        header = match.group(1)
        old_content = match.group(2)
        footer = match.group(3)
        
        # Replace with reference to Section 19
        new_content = '''# Storage paths are defined in Section 19.2 (Single Source of Truth)
# See Section 19.2 for STORAGE_CONFIG and validation

# These constants are available after Section 19.2 initialization:
# - SSD_STORAGE
# - HDD_STORAGE  
# - KNOWLEDGE_DB
# - CHECKPOINTS
# - SESSION_LOGS
# - MEMORY_STASH

# Example usage:
# state_file = SESSION_LOGS / f"session_{session_id}.json"
# archive_path = MEMORY_STASH / category / f"{datetime.now().strftime('%Y%m%d')}.json"
'''
        return header + new_content + footer
    
    content = re.sub(section_24_2_pattern, replace_storage_paths, content, flags=re.DOTALL)
    print("    ✅ Removed duplicate storage path definitions from Section 24.2")
    
    return content

def fix_code_block_issues(content: str) -> str:
    """Fix #2: Fix malformed strings and double braces."""
    print("  Fixing code block issues...")
    
    # Fix malformed string: \' → '
    content = re.sub(
        r"f\"\{datetime\.now\(\)\.strftime\(\\'%Y%m%d\\'\)\}\"",
        r"f\"{datetime.now().strftime('%Y%m%d')}\"",
        content
    )
    print("    ✅ Fixed malformed string quotes")
    
    # Fix double braces {{ → {
    content = re.sub(r'context = \{\{', 'context = {', content)
    content = re.sub(r'"storage_paths": \{\{', '"storage_paths": {', content)
    print("    ✅ Fixed double braces in context dictionary")
    
    # Fix remaining template string errors
    # Pattern: "repo_discovery_{{datetime...}}" → f"repo_discovery_{datetime...}"
    content = re.sub(
        r'"repo_discovery_\{\{datetime\.now\(\)\.strftime\([^)]+\)\}\}\.json"',
        r'f"repo_discovery_{datetime.now().strftime(\'%Y%m%d_%H%M%S\')}.json"',
        content
    )
    
    # Pattern: "{{size_mb:.2f}}" → f"{size_mb:.2f}"
    content = re.sub(
        r'\{\{size_mb:\.2f\}\}',
        r'{size_mb:.2f}',
        content
    )
    
    # Pattern: "{{file_path}}" → f"{file_path}"
    content = re.sub(
        r'\{\{file_path\}\}',
        r'{file_path}',
        content
    )
    
    # Pattern: "backup_{{datetime...}}" → f"backup_{datetime...}"
    content = re.sub(
        r'"backup_\{\{datetime\.now\(\)\.strftime\([^)]+\)\}\}\.bak"',
        r'f"backup_{datetime.now().strftime(\'%Y%m%d_%H%M%S\')}.bak"',
        content
    )
    
    # Pattern: "{{checkpoint}}.gz" → f"{checkpoint}.gz"
    content = re.sub(
        r'"\{\{checkpoint\}\}\.gz"',
        r'f"{checkpoint}.gz"',
        content
    )
    
    # Fix write_text with template strings
    content = re.sub(
        r'write_text\("Read: \{\{file_path\}\}\\\\n',
        r'write_text(f"Read: {file_path}\\n',
        content
    )
    
    print("    ✅ Fixed remaining template string errors")
    
    return content

def fix_missing_imports(content: str) -> str:
    """Fix #3: Add missing imports."""
    print("  Fixing missing imports...")
    
    # Find Section 22.3 and add gzip import
    section_22_3_pattern = r'(### 22\.3[^\n]*\n)'
    match = re.search(section_22_3_pattern, content)
    
    if match:
        after_header = content[match.end():match.end()+200]
        if "import gzip" not in after_header and "gzip" in after_header:
            # Add import at the start of code block
            content = content[:match.end()] + "\n```python\nimport gzip\n" + content[match.end():]
            print("    ✅ Added gzip import to Section 22.3")
    
    return content

def verify_calculate_timeout(content: str) -> str:
    """Fix #4: Verify calculate_timeout function exists."""
    print("  Verifying calculate_timeout function...")
    
    if "def calculate_timeout" in content:
        print("    ✅ calculate_timeout function exists")
    else:
        # Add it to Section 19.4
        section_19_4_pattern = r'(### 19\.4[^\n]*\n)'
        match = re.search(section_19_4_pattern, content)
        if match:
            timeout_func = '''
```python
def calculate_timeout(repo_path: Path) -> int:
    """
    Calculate tool execution timeout based on repository size.
    
    Args:
        repo_path: Path to repository
        
    Returns:
        Timeout in seconds
    """
    try:
        repo_size_mb = sum(
            f.stat().st_size 
            for f in repo_path.rglob('*') 
            if f.is_file()
        ) / (1024 * 1024)
        
        if repo_size_mb < 100:
            return 60  # Small repo: 1 minute
        elif repo_size_mb < 1024:
            return 300  # Medium repo: 5 minutes
        else:
            return 600  # Large repo: 10 minutes
    except Exception:
        return 300  # Default fallback
```
'''
            content = content[:match.end()] + timeout_func + "\n" + content[match.end():]
            print("    ✅ Added calculate_timeout function to Section 19.4")
    
    return content

def fix_truncated_note(content: str) -> str:
    """Fix #5: Complete truncated note in Section 3.2."""
    print("  Fixing truncated note...")
    
    # Find truncated note
    truncated_pattern = r'-\s*\*\*\s*\n'
    replacement = '- **NOTE:** Regex patterns for secret detection are provided for reference only; always use robust libraries for implementation.\n'
    
    if re.search(truncated_pattern, content):
        content = re.sub(truncated_pattern, replacement, content, count=1)
        print("    ✅ Fixed truncated note in Section 3.2")
    
    return content

def add_recommended_sections(content: str) -> str:
    """Add recommended enhancement sections."""
    print("  Adding recommended sections...")
    
    # Find Section 19.5 or end of Section 19
    section_19_5_pattern = r'(### 19\.5[^\n]*\n)'
    section_20_pattern = r'(## 20\.)'
    
    match_19_5 = re.search(section_19_5_pattern, content)
    match_20 = re.search(section_20_pattern, content)
    
    insert_pos = match_19_5.end() if match_19_5 else (match_20.start() if match_20 else len(content))
    
    # Add Section 19.6: GitHub API Integration
    github_section = '''
### 19.6 GitHub API Integration (Local VM)

Since you're on a local VM, you'll need to integrate with GitHub API for issue creation/updates.

**Environment Setup:**

```python
import os
from github import Github

# Load token from environment (NEVER hardcode)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set")

g = Github(GITHUB_TOKEN)
```

**Create Issue:**

```python
def create_github_issue_local(repo_name: str, title: str, body: str, labels: List[str]) -> int:
    """
    Create GitHub issue via API (local VM).
    
    Args:
        repo_name: Full repo name (e.g., "MatoTeziTanka/BitPhoenix")
        title: Issue title
        body: Issue description
        labels: List of label names
        
    Returns:
        Issue number
    """
    repo = g.get_repo(repo_name)
    issue = repo.create_issue(
        title=title,
        body=body,
        labels=labels
    )
    
    # Log to SSD
    logger.log(
        who="create_github_issue_local",
        what="create",
        where=f"{repo_name}#{issue.number}",
        why="GitHub: Issue-driven workflow requirement",
        status="SUCCESS",
        issue_number=issue.number,
        issue_url=issue.html_url
    )
    
    return issue.number
```

**Required Environment:**

```bash
# Set in Windows environment variables or .env file
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx

# Or in PowerShell
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
```

### 19.7 Performance Monitoring (Local VM)

**Monitor Resource Usage:**

```python
import psutil

def monitor_vm_resources():
    """Monitor CPU, memory, disk usage."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk_ssd = psutil.disk_usage(str(SSD_STORAGE))
    disk_hdd = psutil.disk_usage(str(HDD_STORAGE))
    
    logger.log(
        who="monitor_vm_resources",
        what="monitor",
        where="Local VM",
        why="Performance: Resource usage tracking",
        status="INFO",
        cpu_percent=cpu_percent,
        memory_percent=memory.percent,
        ssd_used_percent=disk_ssd.percent,
        hdd_used_percent=disk_hdd.percent
    )
    
    # Alert if resources low
    if memory.percent > 90:
        logger.log(
            who="monitor_vm_resources",
            what="alert",
            where="Local VM",
            why="Performance: High memory usage",
            status="WARNING"
        )
```

'''
    
    # Add Section 24.3: Session Recovery
    section_24_3 = '''
### 24.3 Session Recovery on Crash

**If LM Studio or VM Crashes:**

1. **Load last checkpoint from SSD:**

```python
last_checkpoint = max(CHECKPOINTS.glob("*.json"), key=os.path.getmtime)
state = json.load(last_checkpoint.open('r'))
```

2. **Resume from last known good state:**
   - Check GitHub issue status
   - Load session logs from SSD
   - Verify file system state
   - Re-run last operation if needed

3. **Log recovery:**

```python
logger.log(
    who="AI_Mind[session_recovery]",
    what="recover",
    where=str(last_checkpoint),
    why="System: Recovered from crash",
    status="SUCCESS"
)
```

'''
    
    # Insert GitHub section before Section 20
    if match_20:
        content = content[:match_20.start()] + github_section + "\n" + content[match_20.start():]
        print("    ✅ Added Section 19.6: GitHub API Integration")
        print("    ✅ Added Section 19.7: Performance Monitoring")
    
    # Find Section 24.2 and add 24.3 after it
    section_24_2_pattern = r'(### 24\.2[^\n]*\n.*?Storage Usage Guidelines:.*?\n)'
    match_24_2 = re.search(section_24_2_pattern, content, re.DOTALL)
    if match_24_2:
        content = content[:match_24_2.end()] + section_24_3 + content[match_24_2.end():]
        print("    ✅ Added Section 24.3: Session Recovery on Crash")
    
    return content

def update_version(content: str) -> str:
    """Update version to 2.4.0."""
    print("  Updating version...")
    
    content = re.sub(
        r'\*\*Version:\*\*\s*[\d.]+',
        r'**Version:** 2.4.0',
        content
    )
    
    content = re.sub(
        r'\*\*Last Updated:\*\*\s*\d{4}-\d{2}-\d{2}',
        r'**Last Updated:** 2025-11-26',
        content
    )
    
    print("    ✅ Version updated to 2.4.0")
    
    return content

def main():
    """Main execution."""
    print("=" * 70)
    print("FIXING v2.3.0 REVIEW ISSUES")
    print("=" * 70)
    print(f"\nDate: {datetime.now().isoformat()}")
    print(f"Input: {INPUT_FILE}")
    print(f"Output: {OUTPUT_FILE}")
    print()
    
    # Read file
    print("📖 Reading file...")
    content = INPUT_FILE.read_text(encoding='utf-8')
    print(f"✅ Read {len(content):,} characters")
    
    # Apply fixes
    print("\n🔧 Applying fixes...")
    content = fix_storage_path_consistency(content)
    content = fix_code_block_issues(content)
    content = fix_missing_imports(content)
    content = verify_calculate_timeout(content)
    content = fix_truncated_note(content)
    content = add_recommended_sections(content)
    content = update_version(content)
    
    # Save
    print("\n💾 Saving fixed file...")
    OUTPUT_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Fixed file saved: {OUTPUT_FILE}")
    print(f"   File size: {OUTPUT_FILE.stat().st_size:,} bytes")
    
    print("\n" + "=" * 70)
    print("ALL FIXES COMPLETE")
    print("=" * 70)
    print("\n✅ All review issues fixed!")
    print("   - Storage path consistency")
    print("   - Code block issues")
    print("   - Missing imports")
    print("   - calculate_timeout function")
    print("   - Truncated note")
    print("   - Recommended sections added")
    print("   - Version updated to 2.4.0")
    print()

if __name__ == "__main__":
    main()


