#!/usr/bin/env python3
"""
Batch Azure Review for All Repositories

Reviews Zencoder's implementation work for all repositories using Azure GPT-4.1.

Usage:
    python batch_azure_review_all_repos.py

Requirements:
    - All {REPO}-ZENCODER-IMPLEMENTATION.json files must exist
    - zencoder_manual_with_azure_review.py must be in same directory
"""

import subprocess
import sys
import io
from pathlib import Path
from datetime import datetime

# Windows Unicode fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

REPOSITORIES = [
    "Keyhound",
    "Dell-Server-Roadmap",
    "Scalpstorm",
    "Goku.AI",
    "Dino-Cloud",
    "FamilyFork",
    "DinoCloud",
    "GSMG.IO",
    "Server-Roadmap",
    "StreamForge",
    "BitPhoenix"
]

def review_repo(repo_name):
    """Review a single repository with Azure."""
    json_file = f"{repo_name}-ZENCODER-IMPLEMENTATION.json"
    json_path = Path(json_file)
    
    if not json_path.exists():
        print(f"⚠️  Skipping {repo_name}: {json_file} not found")
        return False, "File not found"
    
    print(f"\n{'='*60}")
    print(f"Reviewing: {repo_name}")
    print(f"{'='*60}")
    print(f"⏳ Calling Azure API (this may take 30-60 seconds)...")
    sys.stdout.flush()  # Force output to appear immediately
    
    try:
        cmd = [
            sys.executable,
            "zencoder_manual_with_azure_review.py",
            repo_name,
            "--zencoder-json",
            json_file
        ]
        
        result = subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        print(f"✅ {repo_name}: Review complete")
        
        # Check if output files were created
        review_file = Path(f"{repo_name}-AZURE-REVIEW-OF-ZENCODER.md")
        consensus_file = Path(f"{repo_name}-FINAL-CONSENSUS.md")
        
        if review_file.exists():
            print(f"   ✓ Generated: {review_file.name}")
        if consensus_file.exists():
            print(f"   ✓ Generated: {consensus_file.name}")
        
        sys.stdout.flush()
        return True, "Success"
        
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr if e.stderr else str(e)
        print(f"❌ {repo_name}: Error")
        print(f"   {error_msg[:200]}")  # Truncate long errors
        sys.stdout.flush()
        return False, error_msg
    except Exception as e:
        error_msg = str(e)
        print(f"❌ {repo_name}: Unexpected error")
        print(f"   {error_msg[:200]}")
        sys.stdout.flush()
        return False, error_msg

def main():
    """Review all repositories."""
    print("🚀 Starting batch Azure review for all repositories...")
    print(f"Total repositories: {len(REPOSITORIES)}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n⏳ This will take approximately {len(REPOSITORIES) * 1} minutes (30-60 seconds per repo)")
    print("💡 Each repository will be reviewed by Azure GPT-4.1\n")
    sys.stdout.flush()
    
    results = {}
    for idx, repo in enumerate(REPOSITORIES, 1):
        print(f"\n[{idx}/{len(REPOSITORIES)}] Processing {repo}...")
        sys.stdout.flush()
        success, message = review_repo(repo)
        results[repo] = {"success": success, "message": message}
    
    # Summary
    print(f"\n{'='*60}")
    print("BATCH REVIEW SUMMARY")
    print(f"{'='*60}")
    
    successful = sum(1 for r in results.values() if r["success"])
    failed = len(REPOSITORIES) - successful
    
    print(f"✅ Successful: {successful}/{len(REPOSITORIES)}")
    print(f"❌ Failed: {failed}/{len(REPOSITORIES)}")
    
    if successful > 0:
        print("\n✅ Successful repositories:")
        for repo, result in results.items():
            if result["success"]:
                print(f"   - {repo}")
    
    if failed > 0:
        print("\n❌ Failed repositories:")
        for repo, result in results.items():
            if not result["success"]:
                print(f"   - {repo}: {result['message']}")
    
    print(f"\n📁 All outputs saved in: {Path.cwd()}")
    print("📖 Review individual consensus files for each repository")
    print("\n💡 Next step: Run 'python generate_master_batch_summary.py' to create master summary")
    sys.stdout.flush()

if __name__ == "__main__":
    main()
