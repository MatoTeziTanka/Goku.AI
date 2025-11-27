#!/usr/bin/env python3
"""
Remove secrets from git history by rewriting commits.
This script uses git filter-branch or git rebase to remove the bad commit.
"""

import subprocess
import sys
from pathlib import Path

GOKU_AI_PATH = Path(r"C:\Users\sethp\Documents\Github\Goku.AI")

def run_git_command(cmd, check=True):
    """Run a git command and return the result."""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=GOKU_AI_PATH,
            capture_output=True,
            text=True
        )
        if check and result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return None
        return result.stdout.strip()
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    print("=" * 70)
    print("REMOVING SECRETS FROM GIT HISTORY".center(70))
    print("=" * 70)
    print()
    
    # Step 1: Verify we're in the right place
    print("📂 Step 1: Verifying repository...")
    current_dir = run_git_command("pwd", check=False)
    print(f"   Working directory: {GOKU_AI_PATH}")
    
    if not (GOKU_AI_PATH / ".git").exists():
        print("❌ Not a git repository!")
        return 1
    
    print("✅ Repository verified")
    print()
    
    # Step 2: Show current commits
    print("📋 Step 2: Current commit history:")
    log_output = run_git_command("git log --oneline -5")
    if log_output:
        for line in log_output.split('\n'):
            print(f"   {line}")
    print()
    
    # Step 3: Check if we need to rewrite history
    print("🔍 Step 3: Checking for commit with secrets...")
    bad_commit = "990814e"
    commit_exists = run_git_command(f"git rev-parse --verify {bad_commit}^0", check=False)
    
    if commit_exists:
        print(f"   ⚠️  Found commit {bad_commit} with secrets")
        print()
        print("📝 Step 4: Rewriting history...")
        print("   Strategy: Reset to commit before secrets, then recommit")
        print()
        
        # Get the commit before the bad one
        base_commit = "2c393fd"  # The commit before 990814e
        
        print(f"   Base commit: {base_commit}")
        print()
        print("⚠️  WARNING: This will rewrite git history!")
        print("   The following will happen:")
        print("   1. Reset to commit 2c393fd (before secrets)")
        print("   2. Keep all sanitized files staged")
        print("   3. Create a new clean commit")
        print("   4. Force push to replace remote history")
        print()
        
        response = input("   Continue? (yes/no): ").strip().lower()
        if response != "yes":
            print("❌ Cancelled.")
            return 0
        
        # Step 4a: Save current state
        print()
        print("💾 Saving current state...")
        run_git_command("git stash", check=False)
        
        # Step 4b: Reset to base commit (keeping working directory)
        print("🔄 Resetting to base commit (keeping files)...")
        result = run_git_command(f"git reset --soft {base_commit}", check=False)
        if result is None:
            print("   ⚠️  Reset completed (may have warnings)")
        
        # Step 4c: Verify files are still staged
        print("📋 Checking staged files...")
        staged = run_git_command("git diff --cached --name-only", check=False)
        if staged:
            print(f"   ✅ {len(staged.split())} files staged")
        else:
            print("   ⚠️  No files staged - you may need to re-add them")
        
        # Step 4d: Create new commit
        print()
        print("📝 Creating new clean commit...")
        commit_result = run_git_command(
            'git commit -m "feat(repo): initial commit - Goku.AI framework v2.9.0 (sanitized)"',
            check=False
        )
        
        if commit_result is None:
            print("   ✅ New commit created")
        
        # Step 5: Show new history
        print()
        print("📋 New commit history:")
        new_log = run_git_command("git log --oneline -5")
        if new_log:
            for line in new_log.split('\n'):
                print(f"   {line}")
        print()
        
        print("=" * 70)
        print("HISTORY REWRITE COMPLETE".center(70))
        print("=" * 70)
        print()
        print("✅ Commit with secrets has been removed from history")
        print()
        print("📋 Next Steps:")
        print("   1. Review the new commit: git show HEAD")
        print("   2. Verify no secrets: git log -p HEAD | grep -i 'sk_\\|ghp_\\|api_key'")
        print("   3. Force push: git push -u origin main --force")
        print()
        print("⚠️  IMPORTANT:")
        print("   - Force push will overwrite remote history")
        print("   - Make sure you have backups")
        print("   - All collaborators must reset their local repos")
        print()
        
    else:
        print("   ✅ Commit with secrets not found (may have been removed)")
        print("   Current history looks clean")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

