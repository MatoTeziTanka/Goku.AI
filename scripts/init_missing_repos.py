#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path

repos_to_init = [
    "C:/Users/sethp/Documents/Github/Goku.AI",
    "C:/Users/sethp/Documents/Github/DinoCloud"
]

for repo_path in repos_to_init:
    print(f"[*] Initializing Git in {repo_path}...")
    try:
        os.chdir(repo_path)
        subprocess.run(["git", "init"], capture_output=True)
        subprocess.run(["git", "add", "."], capture_output=True)
        subprocess.run(["git", "commit", "-m", "Initialize repository for Phase 2"], capture_output=True)
        print(f"[OK] {repo_path} initialized")
    except Exception as e:
        print(f"[FAIL] {repo_path}: {e}")

print("\n[OK] Git initialization complete")
