#!/usr/bin/env python3
import os
import json
from pathlib import Path
from datetime import datetime

GITHUB_ROOT = Path("C:/Users/sethp/Documents/Github")
REPOS = ["Keyhound", "BitPhoenix", "Dell-Server-Roadmap", "Scalpstorm", 
         "Goku.AI", "Dino-Cloud", "FamilyFork", "DinoCloud", "GSMG.IO", 
         "Server-Roadmap", "StreamForge"]

SKIP_DIRS = {'.git', '__pycache__', 'node_modules', '.venv', 'venv', 'env', 
             '.idea', '.pytest_cache', '.zencoder', 'site-packages', 'dist', 'build'}

print("[PHASE 1 VALIDATION - FAST MODE]")
print("="*80)

found_repos = []
for repo in REPOS:
    repo_path = GITHUB_ROOT / repo
    has_git = (repo_path / ".git").exists()
    if repo_path.exists():
        found_repos.append(f"[OK] {repo}" if has_git else f"[WARN] {repo} (no .git)")
        print(f"  {found_repos[-1]}")
    else:
        print(f"  [FAIL] {repo} - NOT FOUND")

print(f"\nRepositories verified: {len(found_repos)}/11")

consensus_files = list(GITHUB_ROOT.glob("*-FINAL-CONSENSUS.md"))
print(f"Consensus files found: {len(consensus_files)}")

for cf in consensus_files[:5]:
    print(f"  - {cf.name}")

print("\n[CHECKING .env.example FILES]")
env_files = []
for root, dirs, files in os.walk(GITHUB_ROOT):
    dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
    for file in files:
        if file == '.env.example':
            env_files.append(os.path.join(root, file))

print(f"Found {len(env_files)} .env.example files")
for ef in env_files[:10]:
    print(f"  - {ef}")

summary = {
    "timestamp": datetime.now().isoformat(),
    "repos_found": len(found_repos),
    "consensus_files": len(consensus_files),
    "env_example_files": len(env_files),
    "repositories": found_repos
}

with open("validation_summary.txt", 'w', encoding='utf-8') as f:
    f.write(json.dumps(summary, indent=2))

print(f"\n[SUMMARY] Validation Summary saved to: validation_summary.txt")
print(f"Ready for Phase 2: {len(found_repos) >= 9 and len(consensus_files) >= 24}")
