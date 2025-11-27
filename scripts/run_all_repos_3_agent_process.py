#!/usr/bin/env python3
"""
Run 3-Agent Process for ALL Repositories

This script runs all three agents in sequence for each repository.
Alternative to PowerShell script (since PowerShell is broken).

Usage:
    python run_all_repos_3_agent_process.py
"""

import subprocess
import sys
from pathlib import Path

# Repositories to analyze
REPOS = [
    "BitPhoenix",
    "Dell-Server-Roadmap",
    "Server-Roadmap",
    "Dino-Cloud",
    "DinoCloud",
    "Family-Fork",
    "GSMG.IO",
    "Goku.AI",
    "Keyhound",
    "Scalpstorm",
    "StreamForge"
]

def run_command(cmd, repo_name, step_name):
    """Run a command and handle errors."""
    print(f"  {step_name}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"  ✓ {step_name} Complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  ✗ {step_name} Failed!")
        print(f"  Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"  ✗ {step_name} Failed!")
        print(f"  Error: {str(e)}")
        return False

def main():
    """Main execution function."""
    print("=" * 60)
    print("Starting 3-Agent Analysis Process for ALL Repositories")
    print("=" * 60)
    print("")
    
    total_repos = len(REPOS)
    current_repo = 0
    successful_repos = []
    failed_repos = []
    
    for repo in REPOS:
        current_repo += 1
        print(f"[{current_repo}/{total_repos}] Processing: {repo}")
        print("-" * 60)
        print("")
        
        repo_path = Path(repo)
        if not repo_path.exists():
            print(f"  ⚠ Repository '{repo}' not found, skipping...")
            failed_repos.append((repo, "Repository not found"))
            print("")
            continue
        
        # Step 1: Code Agent
        success = run_command(
            f'python azure_repo_code_agent.py "{repo}"',
            repo,
            "Step 1/3: Code Agent Analysis"
        )
        if not success:
            print(f"  Skipping remaining steps for {repo}...")
            failed_repos.append((repo, "Code Agent failed"))
            print("")
            continue
        print("")
        
        # Step 2: Review Agent
        success = run_command(
            f'python azure_repo_review_agent.py "{repo}"',
            repo,
            "Step 2/3: Review Agent Validation"
        )
        if not success:
            print(f"  Skipping consensus for {repo}...")
            failed_repos.append((repo, "Review Agent failed"))
            print("")
            continue
        print("")
        
        # Step 3: Azure Consensus
        success = run_command(
            f'python azure_repo_consensus.py "{repo}"',
            repo,
            "Step 3/3: Azure GPT-4.1 Consensus"
        )
        if not success:
            failed_repos.append((repo, "Azure Consensus failed"))
            print("")
            continue
        print("")
        
        print(f"  ✓ Repository {repo} complete!")
        successful_repos.append(repo)
        print("")
        print("=" * 60)
        print("")
    
    # Summary
    print("=" * 60)
    print("All Repositories Process Complete!")
    print("=" * 60)
    print("")
    print(f"Successful: {len(successful_repos)}/{total_repos}")
    print(f"Failed: {len(failed_repos)}/{total_repos}")
    print("")
    
    if successful_repos:
        print("Output Files Created for Successful Repositories:")
        for repo in successful_repos:
            print(f"  {repo}:")
            print(f"    - {repo}-CODE-AGENT-ANALYSIS.md")
            print(f"    - {repo}-REVIEW-AGENT-VALIDATION.md")
            print(f"    - {repo}-AZURE-CONSENSUS.md")
        print("")
    
    if failed_repos:
        print("Failed Repositories:")
        for repo, reason in failed_repos:
            print(f"  - {repo}: {reason}")
        print("")
    
    print("=" * 60)

if __name__ == "__main__":
    main()



