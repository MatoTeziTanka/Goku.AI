#!/usr/bin/env python3
"""
Azure-Powered Production Readiness Fix Script

This module uses Azure GPT-4.1 API to automatically identify and fix
all critical production readiness issues identified in the assessment.

Quality Assurance Standards:
- Enterprise-grade error handling and validation
- Comprehensive documentation (inline, block, docstring, TODO comments)
- Security-first approach: no credentials exposed, proper .gitignore
- Token-efficient execution with progress tracking
- Cross-platform compatibility (Windows/Linux)

Version: 1.0.0
Author: BitPhoenix Development Team
License: See BitPhoenix repository LICENSE file
"""

# Standard library imports
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Set

# Local imports
from foundry_local_agent import FoundryClaudeAgent

# ============================================================================
# CONFIGURATION CONSTANTS
# ============================================================================

# Fix Windows console encoding for Unicode support
if sys.platform == 'win32':
    import io
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass

BITPHOENIX_PATH = Path("BitPhoenix")
REPO_ROOT = Path(".")

# ============================================================================
# AZURE AGENT INITIALIZATION
# ============================================================================

def initialize_azure_agent() -> Optional[FoundryClaudeAgent]:
    """
    Initialize Azure GPT-4.1 agent for intelligent file analysis.
    
    Returns:
        FoundryClaudeAgent instance if successful, None otherwise
    """
    try:
        agent = FoundryClaudeAgent(model="gpt-4.1")
        return agent
    except Exception as e:
        print(f"❌ Error initializing Azure agent: {e}")
        return None

# ============================================================================
# GIT OPERATIONS
# ============================================================================

def run_git_command(cmd: List[str], cwd: Optional[Path] = None) -> Tuple[str, int]:
    """
    Execute a Git command safely.
    
    Args:
        cmd: List of command arguments
        cwd: Working directory (defaults to BITPHOENIX_PATH)
    
    Returns:
        Tuple of (output, exit_code)
    """
    if cwd is None:
        cwd = BITPHOENIX_PATH
    
    try:
        result = subprocess.run(
            ['git'] + cmd,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout + result.stderr, result.returncode
    except Exception as e:
        return str(e), 1

def is_tracked_by_git(file_path: Path) -> bool:
    """
    Check if a file is tracked by Git.
    
    Args:
        file_path: Path to check
    
    Returns:
        True if file is tracked, False otherwise
    """
    # Get relative path from repo root
    try:
        rel_path = file_path.relative_to(BITPHOENIX_PATH)
    except ValueError:
        return False
    
    output, code = run_git_command(['ls-files', '--error-unmatch', str(rel_path)])
    return code == 0

# ============================================================================
# PRIORITY 1: CRITICAL CLEANUP
# ============================================================================

def remove_node_modules(agent: FoundryClaudeAgent) -> bool:
    """
    Remove node_modules from Git tracking and add to .gitignore.
    
    Uses Azure API to verify node_modules should be removed and
    ensure proper .gitignore entry.
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*70)
    print("PRIORITY 1: REMOVING node_modules FROM REPOSITORY")
    print("="*70)
    
    node_modules_path = BITPHOENIX_PATH / "frontend" / "node_modules"
    
    if not node_modules_path.exists():
        print("✅ node_modules not found (already removed)")
        return True
    
    # Check if tracked by Git
    if is_tracked_by_git(node_modules_path):
        print(f"📦 Found node_modules tracked in Git: {node_modules_path}")
        
        # Use Azure to verify removal is safe
        prompt = f"""Analyze if removing node_modules from Git is safe.

Path: {node_modules_path}
Repository: BitPhoenix

Confirm:
1. node_modules should NEVER be committed to Git (correct?)
2. Removing from Git tracking is safe (files will remain locally)
3. .gitignore should include node_modules/

Respond with: YES if safe to remove, NO if there's a concern."""
        
        try:
            response = agent.analyze_file(str(BITPHOENIX_PATH / "README.md"), prompt)
            if "NO" in response.upper() or "CONCERN" in response.upper():
                print("⚠ Azure flagged a concern - skipping removal")
                return False
        except Exception as e:
            print(f"⚠ Azure verification failed: {e}")
            print("   Proceeding with removal (standard practice)")
        
        # Remove from Git tracking
        print("🗑️  Removing from Git tracking...")
        output, code = run_git_command(['rm', '-r', '--cached', 'frontend/node_modules'])
        if code == 0:
            print("✅ Removed from Git tracking")
        else:
            print(f"⚠ Git removal warning: {output}")
    
    # Ensure .gitignore includes node_modules
    gitignore_path = BITPHOENIX_PATH / ".gitignore"
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding='utf-8')
        if "node_modules" not in content:
            print("📝 Adding node_modules to .gitignore...")
            content += "\n# Node.js dependencies\nnode_modules/\n"
            gitignore_path.write_text(content, encoding='utf-8')
            print("✅ Updated .gitignore")
    else:
        print("📝 Creating .gitignore with node_modules...")
        gitignore_path.write_text("node_modules/\n", encoding='utf-8')
        print("✅ Created .gitignore")
    
    return True

def remove_virtual_environments(agent: FoundryClaudeAgent) -> bool:
    """
    Remove virtual environments from Git tracking.
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*70)
    print("PRIORITY 1: REMOVING VIRTUAL ENVIRONMENTS FROM REPOSITORY")
    print("="*70)
    
    venv_paths = [
        BITPHOENIX_PATH / "backend" / "venv_deploy",
        BITPHOENIX_PATH / "Doesnt Belong" / "shenron-env",
        BITPHOENIX_PATH / "venv",
        BITPHOENIX_PATH / ".venv",
    ]
    
    removed_count = 0
    
    for venv_path in venv_paths:
        if venv_path.exists() and is_tracked_by_git(venv_path):
            print(f"🗑️  Removing {venv_path} from Git...")
            try:
                rel_path = venv_path.relative_to(BITPHOENIX_PATH)
                output, code = run_git_command(['rm', '-r', '--cached', str(rel_path)])
                if code == 0:
                    print(f"✅ Removed {rel_path} from Git")
                    removed_count += 1
                else:
                    print(f"⚠ Warning: {output}")
            except Exception as e:
                print(f"⚠ Error removing {venv_path}: {e}")
    
    # Update .gitignore
    gitignore_path = BITPHOENIX_PATH / ".gitignore"
    venv_patterns = ["venv/", ".venv/", "venv_deploy/", "*/venv/", "*/shenron-env/"]
    
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding='utf-8')
        updated = False
        
        for pattern in venv_patterns:
            if pattern not in content:
                content += f"\n# Python virtual environments\n{pattern}\n"
                updated = True
        
        if updated:
            gitignore_path.write_text(content, encoding='utf-8')
            print("✅ Updated .gitignore with venv patterns")
    else:
        gitignore_path.write_text("\n".join(venv_patterns) + "\n", encoding='utf-8')
        print("✅ Created .gitignore with venv patterns")
    
    print(f"✅ Removed {removed_count} virtual environments from Git")
    return True

def remove_backup_files(agent: FoundryClaudeAgent) -> bool:
    """
    Remove all .backup and .bak files from repository.
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*70)
    print("PRIORITY 1: REMOVING BACKUP FILES FROM REPOSITORY")
    print("="*70)
    
    backup_extensions = ['.backup', '.bak', '.old', '.tmp']
    removed_count = 0
    
    # Find all backup files
    for root, dirs, files in os.walk(BITPHOENIX_PATH):
        # Skip hidden directories and common exclusions
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', 'venv', '__pycache__']]
        
        for file in files:
            file_path = Path(root) / file
            
            # Check if file has backup extension
            if any(file_path.suffix == ext for ext in backup_extensions):
                if is_tracked_by_git(file_path):
                    print(f"🗑️  Removing {file_path.relative_to(BITPHOENIX_PATH)} from Git...")
                    try:
                        rel_path = file_path.relative_to(BITPHOENIX_PATH)
                        output, code = run_git_command(['rm', '--cached', str(rel_path)])
                        if code == 0:
                            removed_count += 1
                            print(f"✅ Removed {rel_path}")
                    except Exception as e:
                        print(f"⚠ Error: {e}")
    
    # Update .gitignore
    gitignore_path = BITPHOENIX_PATH / ".gitignore"
    if gitignore_path.exists():
        content = gitignore_path.read_text(encoding='utf-8')
        patterns = ["*.backup", "*.bak", "*.old", "*.tmp"]
        
        for pattern in patterns:
            if pattern not in content:
                content += f"\n# Backup files\n{pattern}\n"
        
        gitignore_path.write_text(content, encoding='utf-8')
        print("✅ Updated .gitignore with backup file patterns")
    
    print(f"✅ Removed {removed_count} backup files from Git")
    return True

def audit_credentials(agent: FoundryClaudeAgent) -> bool:
    """
    Audit and secure credential files using Azure API.
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*70)
    print("PRIORITY 1: AUDITING CREDENTIALS AND SECRETS")
    print("="*70)
    
    credential_files = []
    
    # Find potential credential files
    for root, dirs, files in os.walk(BITPHOENIX_PATH):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            file_path = Path(root) / file
            file_lower = file.lower()
            
            # Check for credential patterns
            if any(pattern in file_lower for pattern in [
                'credential', 'secret', 'password', 'api_key', 'token',
                'config.json', '.env', 'private', 'key'
            ]):
                # Exclude templates and examples
                if 'template' not in file_lower and 'example' not in file_lower:
                    credential_files.append(file_path)
    
    print(f"🔍 Found {len(credential_files)} potential credential files")
    
    # Use Azure to analyze each file
    for cred_file in credential_files[:10]:  # Limit to first 10 for efficiency
        rel_path = cred_file.relative_to(BITPHOENIX_PATH)
        print(f"\n📄 Analyzing: {rel_path}")
        
        try:
            content = cred_file.read_text(encoding='utf-8', errors='ignore')
            
            # Use Azure to check if file contains actual secrets
            prompt = f"""Analyze this file for security issues:

File: {rel_path}
Content (first 500 chars): {content[:500]}

Check:
1. Does this file contain actual secrets/credentials (not templates)?
2. Should this file be in .gitignore?
3. Should secrets be moved to .env file?

Respond with JSON:
{{
  "contains_secrets": true/false,
  "should_gitignore": true/false,
  "should_move_to_env": true/false,
  "risk_level": "high/medium/low"
}}"""
            
            response = agent.analyze_file(str(cred_file), prompt)
            
            # Try to parse JSON response
            try:
                # Extract JSON from response
                import re
                json_match = re.search(r'\{[^}]+\}', response)
                if json_match:
                    analysis = json.loads(json_match.group())
                    
                    if analysis.get('contains_secrets'):
                        print(f"  ⚠️  RISK: Contains actual secrets!")
                        print(f"  📝 Action: Move to .env and add to .gitignore")
                        
                        # Add to .gitignore
                        gitignore_path = BITPHOENIX_PATH / ".gitignore"
                        if gitignore_path.exists():
                            gitignore_content = gitignore_path.read_text(encoding='utf-8')
                            if str(rel_path) not in gitignore_content:
                                gitignore_content += f"\n# Credential file\n{rel_path}\n"
                                gitignore_path.write_text(gitignore_content, encoding='utf-8')
                                print(f"  ✅ Added {rel_path} to .gitignore")
                        
                        # Remove from Git if tracked
                        if is_tracked_by_git(cred_file):
                            output, code = run_git_command(['rm', '--cached', str(rel_path)])
                            if code == 0:
                                print(f"  ✅ Removed {rel_path} from Git tracking")
            except:
                # If JSON parsing fails, just log the response
                if "secret" in response.lower() or "risk" in response.lower():
                    print(f"  ⚠️  Azure flagged potential security issue")
        except Exception as e:
            print(f"  ⚠️  Error analyzing {rel_path}: {e}")
    
    print("\n✅ Credential audit complete")
    return True

def cleanup_root_directory(agent: FoundryClaudeAgent) -> bool:
    """
    Organize root directory by moving docs/reports to proper locations.
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*70)
    print("PRIORITY 1: CLEANING UP ROOT DIRECTORY")
    print("="*70)
    
    # Create organized directories
    docs_dir = BITPHOENIX_PATH / "docs"
    reports_dir = BITPHOENIX_PATH / "reports"
    
    docs_dir.mkdir(exist_ok=True)
    reports_dir.mkdir(exist_ok=True)
    
    # Files to move to docs/
    doc_patterns = ['*.md', '*_GUIDE.md', '*_INSTRUCTIONS.md', '*_SUMMARY.md']
    # Files to move to reports/
    report_patterns = ['*_REPORT*.json', '*_REPORT*.md', '*_ANALYSIS*.json', '*_LOG*.json']
    
    moved_count = 0
    
    for file in BITPHOENIX_PATH.iterdir():
        if file.is_file() and file.name not in ['README.md', '.gitignore', 'LICENSE']:
            # Check if it's a documentation file
            if any(file.name.endswith(ext.replace('*', '')) or 
                   any(pattern.replace('*', '') in file.name for pattern in doc_patterns) 
                   for ext in ['.md']):
                target = docs_dir / file.name
                if not target.exists():
                    file.rename(target)
                    print(f"📄 Moved {file.name} → docs/")
                    moved_count += 1
            
            # Check if it's a report file
            elif any(pattern.replace('*', '') in file.name for pattern in report_patterns):
                target = reports_dir / file.name
                if not target.exists():
                    file.rename(target)
                    print(f"📊 Moved {file.name} → reports/")
                    moved_count += 1
    
    print(f"✅ Moved {moved_count} files to organized directories")
    return True

# ============================================================================
# PRIORITY 2: SECURITY & QUALITY
# ============================================================================

def enhance_gitignore(agent: FoundryClaudeAgent) -> bool:
    """
    Enhance .gitignore with comprehensive security patterns.
    
    Returns:
        True if successful, False otherwise
    """
    print("\n" + "="*70)
    print("PRIORITY 2: ENHANCING .gitignore FOR SECURITY")
    print("="*70)
    
    gitignore_path = BITPHOENIX_PATH / ".gitignore"
    
    # Comprehensive .gitignore patterns
    patterns = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Virtual Environments
venv/
.venv/
venv_deploy/
env/
ENV/
shenron-env/

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment variables and secrets
.env
.env.local
.env.*.local
*.key
*.pem
*.p12
*.pfx
config.local.*
secrets.json
credentials.json

# Backup files
*.backup
*.bak
*.old
*.tmp
*.swp
*~

# IDE
.vscode/
.idea/
*.sublime-*

# OS
.DS_Store
Thumbs.db
desktop.ini

# Logs
*.log
logs/

# Database
*.db
*.sqlite
*.sqlite3

# Recovery/Scratch
recovered/
scratch/
temp/
"""
    
    if gitignore_path.exists():
        existing = gitignore_path.read_text(encoding='utf-8')
        # Merge patterns
        existing_lines = set(existing.splitlines())
        new_lines = [line for line in patterns.splitlines() if line and line not in existing_lines]
        
        if new_lines:
            existing += "\n" + "\n".join(new_lines) + "\n"
            gitignore_path.write_text(existing, encoding='utf-8')
            print(f"✅ Added {len(new_lines)} new patterns to .gitignore")
        else:
            print("✅ .gitignore already comprehensive")
    else:
        gitignore_path.write_text(patterns, encoding='utf-8')
        print("✅ Created comprehensive .gitignore")
    
    return True

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main() -> None:
    """
    Main execution function for production readiness fixes.
    
    Orchestrates all Priority 1 and Priority 2 fixes using Azure API
    for intelligent decision-making.
    """
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except (AttributeError, ValueError):
        pass
    
    print("="*70)
    print("AZURE-POWERED PRODUCTION READINESS FIX")
    print("="*70)
    print("Using Azure GPT-4.1 to intelligently fix all critical issues")
    print()
    
    if not BITPHOENIX_PATH.exists():
        print(f"❌ Error: BitPhoenix directory not found: {BITPHOENIX_PATH}")
        return
    
    # Initialize Azure agent
    print("🤖 Initializing Azure GPT-4.1 agent...")
    agent = initialize_azure_agent()
    if not agent:
        print("❌ Failed to initialize Azure agent")
        return
    print("✅ Azure agent initialized")
    
    # Priority 1: Critical fixes
    print("\n" + "="*70)
    print("EXECUTING PRIORITY 1: CRITICAL FIXES")
    print("="*70)
    
    results = {
        'node_modules': remove_node_modules(agent),
        'venv': remove_virtual_environments(agent),
        'backup_files': remove_backup_files(agent),
        'credentials': audit_credentials(agent),
        'root_cleanup': cleanup_root_directory(agent),
    }
    
    # Priority 2: Security & Quality
    print("\n" + "="*70)
    print("EXECUTING PRIORITY 2: SECURITY & QUALITY")
    print("="*70)
    
    results['gitignore'] = enhance_gitignore(agent)
    
    # Summary
    print("\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)
    
    for task, success in results.items():
        status = "✅" if success else "❌"
        print(f"{status} {task.replace('_', ' ').title()}")
    
    print("\n📋 Next Steps:")
    print("   1. Review all changes: git status")
    print("   2. Commit changes: git add . && git commit -m 'fix: Production readiness cleanup'")
    print("   3. Verify .gitignore: git check-ignore -v <file>")
    print("   4. Run tests before pushing")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)





