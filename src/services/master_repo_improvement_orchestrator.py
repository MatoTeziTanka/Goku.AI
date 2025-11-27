#!/usr/bin/env python3
"""
Master Repository Improvement Orchestrator

Implements the full iterative improvement cycle for ALL repositories:
1. Discovery Phase: Map all repos, understand structure
2. For each repo:
   a. Code Agent Analysis → Log
   b. Review Agent Validation → Log
   c. Azure API Consensus → Log
   d. Compile Changes
   e. Apply Fixes
   f. Code Agent Analysis (AGAIN) → Log
   g. Review Agent Validation (AGAIN) → Log
   h. Azure API Consensus (AGAIN) → Log
   i. Compile Final Consensus
   j. Repeat until v1.0.0 achieved (QC Score 95+/100)

Follows: Perpetual Self-Updating AI Mind (100/10 Mindset)
QC Standards: Functional QA (20), Documentation (20), Security (15), Efficiency (15), AI Learning (15), Innovation (15)

Usage:
    python master_repo_improvement_orchestrator.py [--repo REPO_NAME] [--max-iterations N] [--target-score N]
    
Example:
    python master_repo_improvement_orchestrator.py                    # All repos
    python master_repo_improvement_orchestrator.py --repo BitPhoenix  # Single repo
"""

import subprocess
import sys
import json
import re
import io
import time
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# Windows Unicode fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# QC Standards (100/10 Mindset)
QC_STANDARDS = {
    "Functional QA": 20,
    "Documentation & Comment Quality": 20,
    "Security & Safety": 15,
    "Efficiency / Optimization": 15,
    "AI Learning & Adaptation": 15,
    "Innovation & Impact": 15,
    "TOTAL": 100
}

# Target settings
DEFAULT_MAX_ITERATIONS = 10
DEFAULT_TARGET_SCORE = 95

# Repositories to process
REPOSITORIES = [
    "BitPhoenix",
    "Dell-Server-Roadmap",  # Will merge with Server-Roadmap
    "Dino-Cloud",  # Will merge with DinoCloud
    "DinoCloud",  # Will merge into Dino-Cloud
    "FamilyFork",
    "GSMG.IO",
    "Goku.AI",  # Will consolidate all Goku.AI files
    "Keyhound",
    "Scalpstorm",
    "Server-Roadmap",  # Will merge into Dell-Server-Roadmap
    "StreamForge"
]

# Consolidation rules
CONSOLIDATION_RULES = {
    "Dell-Server-Roadmap": ["Server-Roadmap"],  # Merge Server-Roadmap into Dell-Server-Roadmap
    "Dino-Cloud": ["DinoCloud"],  # Merge DinoCloud into Dino-Cloud
    "Goku.AI": "ALL_FILES_IN_GITHUB"  # Special: consolidate all Goku.AI files from entire GitHub folder
}

def run_command(cmd: str, step_name: str, silent: bool = False) -> Tuple[bool, str, bool]:
    """Run a command and handle errors.
    
    Returns:
        (success: bool, output: str, is_rate_limit: bool)
    """
    if not silent:
        print(f"  {step_name}...")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        if not silent:
            print(f"  ✓ {step_name} Complete")
        return True, result.stdout, False
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or e.stdout or str(e)
        is_rate_limit = (
            "RateLimit" in error_output or 
            "429" in error_output or 
            "rate limit" in error_output.lower() or
            "RateLimitReached" in error_output
        )
        if not silent:
            print(f"  ✗ {step_name} Failed!")
            print(f"  Error: {error_output[:500]}")  # Limit error output length
        return False, error_output, is_rate_limit
    except Exception as e:
        error_str = str(e)
        is_rate_limit = (
            "RateLimit" in error_str or 
            "429" in error_str or 
            "rate limit" in error_str.lower() or
            "RateLimitReached" in error_str
        )
        if not silent:
            print(f"  ✗ {step_name} Failed!")
            print(f"  Error: {error_str[:500]}")
        return False, error_str, is_rate_limit

def extract_qc_score(consensus_file: str) -> Optional[int]:
    """Extract QC score from consensus file."""
    try:
        with open(consensus_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for patterns like "87/100" or "QC Score: 87/100"
        patterns = [
            r'QC Score[:\s]+(\d+)/100',
            r'Final QC Score[:\s]+(\d+)/100',
            r'Consensus Total[:\s]+(\d+)/100',
            r'Total Score[:\s]+(\d+)/100',
            r'(\d+)/100.*QC',
            r'Score[:\s]+(\d+)/100'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                score = int(match.group(1))
                return score
        
        # Fallback: look for any "XX/100" pattern
        match = re.search(r'(\d+)/100', content)
        if match:
            return int(match.group(1))
        
        return None
    except Exception as e:
        print(f"  Warning: Could not extract QC score: {e}")
        return None

def extract_v1_ready_status(consensus_file: str) -> Optional[bool]:
    """Extract v1.0.0 readiness status from consensus file."""
    try:
        with open(consensus_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for readiness status
        if re.search(r'v1\.0\.0.*ready|ready.*v1\.0\.0', content, re.IGNORECASE):
            if re.search(r'not.*ready|not ready|❌|✗|NO', content, re.IGNORECASE):
                return False
            if re.search(r'ready|✅|✓|YES', content, re.IGNORECASE):
                return True
        
        return None
    except Exception as e:
        print(f"  Warning: Could not extract readiness status: {e}")
        return None

def discovery_phase() -> Dict[str, Dict]:
    """Phase 0: Discover and map all repositories."""
    print("\n" + "="*80)
    print("PHASE 0: DISCOVERY")
    print("="*80 + "\n")
    
    github_path = Path("C:/Users/sethp/Documents/Github")
    discovery_results = {}
    
    # Directories to skip (common build/cache dirs that may have locked files)
    SKIP_DIRS = {
        'node_modules', '.git', '__pycache__', '.venv', 'venv', 
        'dist', 'build', '.next', '.nuxt', '.cache', '.pytest_cache',
        'target', 'bin', 'obj', '.idea', '.vscode', '.vs'
    }
    
    def should_skip_path(path: Path) -> bool:
        """Check if path should be skipped."""
        parts = path.parts
        for part in parts:
            if part in SKIP_DIRS:
                return True
        return False
    
    def safe_count_files(repo_path: Path) -> Tuple[int, int, float]:
        """Safely count files and directories, skipping inaccessible ones."""
        file_count = 0
        dir_count = 0
        total_size = 0
        
        try:
            for item in repo_path.rglob("*"):
                # Skip if path contains skip directories
                if should_skip_path(item):
                    continue
                
                try:
                    if item.is_file():
                        file_count += 1
                        try:
                            total_size += item.stat().st_size
                        except (OSError, PermissionError):
                            pass  # Skip if can't access
                    elif item.is_dir():
                        dir_count += 1
                except (OSError, PermissionError):
                    # Skip inaccessible files/dirs
                    continue
        except (OSError, PermissionError) as e:
            print(f"    Warning: Could not fully scan {repo_path.name}: {e}")
        
        return file_count, dir_count, total_size / (1024*1024)
    
    print("Discovering repositories...")
    for repo_name in REPOSITORIES:
        repo_path = github_path / repo_name
        if repo_path.exists() and repo_path.is_dir():
            # Count files safely
            file_count, dir_count, size_mb = safe_count_files(repo_path)
            
            discovery_results[repo_name] = {
                "path": str(repo_path),
                "exists": True,
                "file_count": file_count,
                "dir_count": dir_count,
                "size_mb": round(size_mb, 2)
            }
            print(f"  ✓ {repo_name}: {file_count} files, {dir_count} dirs, {size_mb:.2f} MB")
        else:
            discovery_results[repo_name] = {
                "path": str(repo_path),
                "exists": False
            }
            print(f"  ✗ {repo_name}: NOT FOUND")
    
    # Special: Find all Goku.AI files
    print("\nDiscovering Goku.AI files across entire GitHub folder...")
    goku_files = []
    for item in github_path.rglob("*"):
        # Skip inaccessible paths
        if should_skip_path(item):
            continue
        
        try:
            if "goku" in item.name.lower() or "goku" in str(item).lower():
                if item.is_file():
                    goku_files.append(str(item))
        except (OSError, PermissionError):
            continue  # Skip inaccessible files
    
    discovery_results["Goku.AI"]["scattered_files"] = goku_files
    discovery_results["Goku.AI"]["scattered_file_count"] = len(goku_files)
    print(f"  Found {len(goku_files)} Goku.AI related files")
    
    # Save discovery results
    discovery_file = "REPO-DISCOVERY-RESULTS.json"
    with open(discovery_file, 'w', encoding='utf-8') as f:
        json.dump(discovery_results, f, indent=2)
    
    print(f"\n✓ Discovery complete. Results saved to: {discovery_file}")
    return discovery_results

def run_code_agent(repo_name: str, iteration: int, phase: str = "initial", max_retries: int = 3) -> bool:
    """Run Code Agent analysis with rate limit retry."""
    phase_label = f"{phase.upper()} Analysis"
    for attempt in range(max_retries):
        success, output, is_rate_limit = run_command(
            f'python azure_repo_code_agent.py "{repo_name}"',
            f"Code Agent: {phase_label} (Iteration {iteration})" + (f" [Attempt {attempt + 1}/{max_retries}]" if attempt > 0 else ""),
            silent=(attempt > 0)
        )
        if success:
            return True
        # Check if it's a rate limit error
        if is_rate_limit:
            if attempt < max_retries - 1:
                wait_time = 60 * (attempt + 1)  # 60, 120, 180 seconds
                print(f"  Rate limit hit. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"  Rate limit persists after {max_retries} attempts. Skipping for now.")
                return False
        # Non-rate-limit error - don't retry
        return False
    return False

def run_review_agent(repo_name: str, iteration: int, phase: str = "initial", max_retries: int = 3) -> bool:
    """Run Review Agent validation with rate limit retry."""
    phase_label = f"{phase.upper()} Validation"
    for attempt in range(max_retries):
        success, output, is_rate_limit = run_command(
            f'python azure_repo_review_agent.py "{repo_name}"',
            f"Review Agent: {phase_label} (Iteration {iteration})" + (f" [Attempt {attempt + 1}/{max_retries}]" if attempt > 0 else ""),
            silent=(attempt > 0)
        )
        if success:
            return True
        # Check if it's a rate limit error
        if is_rate_limit:
            if attempt < max_retries - 1:
                wait_time = 60 * (attempt + 1)
                print(f"  Rate limit hit. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"  Rate limit persists after {max_retries} attempts. Skipping for now.")
                return False
        # Non-rate-limit error - don't retry
        return False
    return False

def run_azure_consensus(repo_name: str, iteration: int, phase: str = "initial", max_retries: int = 3) -> Tuple[bool, Optional[int], Optional[bool]]:
    """Run Azure GPT-4.1 consensus with rate limit retry."""
    phase_label = f"{phase.upper()} Consensus"
    for attempt in range(max_retries):
        success, output, is_rate_limit = run_command(
            f'python azure_repo_consensus.py "{repo_name}"',
            f"Azure GPT-4.1: {phase_label} (Iteration {iteration})" + (f" [Attempt {attempt + 1}/{max_retries}]" if attempt > 0 else ""),
            silent=(attempt > 0)
        )
        
        if success:
            consensus_file = f"{repo_name}-AZURE-CONSENSUS.md"
            qc_score = extract_qc_score(consensus_file)
            v1_ready = extract_v1_ready_status(consensus_file)
            return True, qc_score, v1_ready
        
        # Check if it's a rate limit error
        if is_rate_limit:
            if attempt < max_retries - 1:
                wait_time = 60 * (attempt + 1)
                print(f"  Rate limit hit. Waiting {wait_time} seconds before retry...")
                time.sleep(wait_time)
                continue
            else:
                print(f"  Rate limit persists after {max_retries} attempts. Skipping for now.")
                return False, None, None
        
        # Non-rate-limit error - don't retry
        return False, None, None
    
    return False, None, None

def compile_changes(repo_name: str, iteration: int, phase: str = "initial") -> bool:
    """Compile changes from consensus."""
    success, _, _ = run_command(
        f'python compile_changes_from_consensus.py "{repo_name}" {iteration}',
        f"Compile Changes: {phase.upper()} (Iteration {iteration})"
    )
    return success

def apply_fixes(repo_name: str, iteration: int, auto_apply: bool = False, skip_manual: bool = False) -> bool:
    """Apply fixes based on compiled changes."""
    compiled_file = f"{repo_name}-ITERATION-{iteration}-COMPILED-CHANGES.md"
    
    if not Path(compiled_file).exists():
        print(f"  ⚠ Compiled changes file not found: {compiled_file}")
        print(f"  Please create it manually or run compile_changes() first")
        return False
    
    if auto_apply:
        print(f"  Auto-applying fixes from {compiled_file}...")
        print(f"  (Auto-apply not yet implemented - manual application required)")
        return True
    elif skip_manual:
        print(f"  ⚠ Skipping manual fix application (--skip-manual flag)")
        print(f"  Compiled changes available in: {compiled_file}")
        print(f"  You can apply fixes later and re-run the script")
        return True
    else:
        print(f"\n  {'='*60}")
        print(f"  MANUAL FIX APPLICATION REQUIRED")
        print(f"  {'='*60}")
        print(f"  1. Review: {compiled_file}")
        print(f"  2. Apply fixes manually")
        print(f"  3. Press Enter when fixes are applied (or 's' to skip)")
        print(f"     Note: Use --skip-manual flag to skip this step automatically")
        try:
            user_input = input("  > ").strip().lower()
            if user_input == 's' or user_input == 'skip':
                print(f"  ⚠ Skipping manual fix application")
                print(f"  Compiled changes available in: {compiled_file}")
                return True
            return True
        except KeyboardInterrupt:
            print("\n  Stopped by user")
            return False

def run_full_cycle(repo_name: str, iteration: int, max_iterations: int, target_score: int) -> Tuple[bool, Optional[int], Optional[bool]]:
    """Run the complete improvement cycle for one iteration."""
    print(f"\n{'#'*80}")
    print(f"REPOSITORY: {repo_name} | ITERATION: {iteration}/{max_iterations}")
    print(f"{'#'*80}\n")
    
    # PHASE 1: Initial 3-Agent Analysis
    print(f"{'='*80}")
    print(f"PHASE 1: INITIAL 3-AGENT ANALYSIS")
    print(f"{'='*80}\n")
    
    # Step 1: Code Agent
    if not run_code_agent(repo_name, iteration, "initial"):
        return False, None, None
    
    # Step 2: Review Agent
    if not run_review_agent(repo_name, iteration, "initial"):
        return False, None, None
    
    # Step 3: Azure Consensus
    success, qc_score, v1_ready = run_azure_consensus(repo_name, iteration, "initial")
    if not success:
        return False, None, None
    
    print(f"\n  Initial QC Score: {qc_score}/100 (Target: {target_score}/100)")
    if v1_ready is not None:
        status = "✓ READY" if v1_ready else "✗ NOT READY"
        print(f"  v1.0.0 Status: {status}")
    
    # Check if already achieved
    if qc_score is not None and qc_score >= target_score and v1_ready:
        print(f"\n  🎉 TARGET ALREADY ACHIEVED!")
        return True, qc_score, v1_ready
    
    # PHASE 2: Compile and Apply
    print(f"\n{'='*80}")
    print(f"PHASE 2: COMPILE CHANGES & APPLY FIXES")
    print(f"{'='*80}\n")
    
    if not compile_changes(repo_name, iteration, "initial"):
        print("  Warning: Compile changes failed, continuing anyway...")
    
    # Check for skip-manual flag from command line args
    skip_manual = "--skip-manual" in sys.argv or "-s" in sys.argv
    if not apply_fixes(repo_name, iteration, auto_apply=False, skip_manual=skip_manual):
        print("  Warning: Fix application cancelled or failed")
        return False, qc_score, v1_ready
    
    # PHASE 3: Re-Analysis (After Fixes)
    print(f"\n{'='*80}")
    print(f"PHASE 3: RE-ANALYSIS AFTER FIXES (3-AGENT CYCLE)")
    print(f"{'='*80}\n")
    
    # Step 1: Code Agent (AGAIN)
    if not run_code_agent(repo_name, iteration, "post-fix"):
        return False, qc_score, v1_ready
    
    # Step 2: Review Agent (AGAIN)
    if not run_review_agent(repo_name, iteration, "post-fix"):
        return False, qc_score, v1_ready
    
    # Step 3: Azure Consensus (AGAIN)
    success, new_qc_score, new_v1_ready = run_azure_consensus(repo_name, iteration, "post-fix")
    if not success:
        return False, qc_score, v1_ready
    
    # PHASE 4: Final Consensus Compilation
    print(f"\n{'='*80}")
    print(f"PHASE 4: FINAL CONSENSUS COMPILATION")
    print(f"{'='*80}\n")
    
    # Compile final consensus from both cycles
    final_consensus_file = f"{repo_name}-ITERATION-{iteration}-FINAL-CONSENSUS.md"
    print(f"  Creating final consensus document: {final_consensus_file}")
    
    # Read both consensus files
    initial_consensus = f"{repo_name}-AZURE-CONSENSUS.md"
    post_fix_consensus = f"{repo_name}-AZURE-CONSENSUS.md"  # Same file, overwritten
    
    try:
        with open(initial_consensus, 'r', encoding='utf-8') as f:
            initial_content = f.read()
        
        with open(post_fix_consensus, 'r', encoding='utf-8') as f:
            post_fix_content = f.read()
        
        with open(final_consensus_file, 'w', encoding='utf-8') as f:
            f.write(f"# {repo_name} - Final Consensus (Iteration {iteration})\n\n")
            f.write(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            f.write("## Initial Analysis Consensus\n\n")
            f.write(initial_content)
            f.write("\n\n---\n\n")
            f.write("## Post-Fix Analysis Consensus\n\n")
            f.write(post_fix_content)
            f.write("\n\n---\n\n")
            f.write("## Summary\n\n")
            f.write(f"- Initial QC Score: {qc_score}/100\n")
            f.write(f"- Post-Fix QC Score: {new_qc_score}/100\n")
            f.write(f"- Improvement: {new_qc_score - qc_score if (qc_score and new_qc_score) else 'N/A'} points\n")
            f.write(f"- v1.0.0 Ready: {new_v1_ready}\n")
        
        print(f"  ✓ Final consensus saved to: {final_consensus_file}")
    except Exception as e:
        print(f"  ⚠ Could not create final consensus: {e}")
    
    print(f"\n  Post-Fix QC Score: {new_qc_score}/100 (Target: {target_score}/100)")
    if new_v1_ready is not None:
        status = "✓ READY" if new_v1_ready else "✗ NOT READY"
        print(f"  v1.0.0 Status: {status}")
    
    return True, new_qc_score, new_v1_ready

def process_repository(repo_name: str, max_iterations: int, target_score: int) -> Dict:
    """Process a single repository through the improvement cycle."""
    print("\n" + "="*80)
    print(f"PROCESSING REPOSITORY: {repo_name}")
    print("="*80)
    
    # Check if repo exists
    repo_path = Path(repo_name)
    if not repo_path.exists():
        print(f"  ✗ Repository '{repo_name}' not found! Skipping...")
        return {"status": "not_found", "iterations": 0, "final_score": None}
    
    iteration = 0
    scores = []
    v1_ready_status = []
    
    while iteration < max_iterations:
        iteration += 1
        
        success, qc_score, v1_ready = run_full_cycle(repo_name, iteration, max_iterations, target_score)
        
        if not success:
            print(f"\n  ✗ Iteration {iteration} failed - stopping")
            break
        
        scores.append(qc_score)
        v1_ready_status.append(v1_ready)
        
        # Check if target achieved
        if qc_score is not None and qc_score >= target_score and v1_ready:
            print(f"\n  🎉 TARGET ACHIEVED FOR {repo_name}!")
            print(f"  Final QC Score: {qc_score}/100")
            print(f"  v1.0.0 Status: READY")
            break
        
        # If skip-manual flag is set, only do 1 iteration per repo (for discovery)
        skip_manual = "--skip-manual" in sys.argv or "-s" in sys.argv
        if skip_manual:
            print(f"\n  ⚠ --skip-manual flag: Stopping after iteration {iteration}")
            print(f"  Analysis files generated. Apply fixes and re-run without --skip-manual to improve scores.")
            break
        
        # If not last iteration, continue
        if iteration < max_iterations:
            print(f"\n  Ready for iteration {iteration + 1}...")
            print("  Press Enter to continue or Ctrl+C to stop...")
            try:
                input()
            except KeyboardInterrupt:
                print("\n  Stopped by user")
                break
    
    return {
        "status": "completed",
        "iterations": iteration,
        "scores": scores,
        "final_score": scores[-1] if scores else None,
        "v1_ready": v1_ready_status[-1] if v1_ready_status else None
    }

def main():
    """Main execution function."""
    # Parse arguments
    repo_filter = None
    max_iterations = DEFAULT_MAX_ITERATIONS
    target_score = DEFAULT_TARGET_SCORE
    
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "--repo" and i + 1 < len(sys.argv):
            repo_filter = sys.argv[i + 1]
            i += 2
        elif sys.argv[i] == "--max-iterations" and i + 1 < len(sys.argv):
            max_iterations = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == "--target-score" and i + 1 < len(sys.argv):
            target_score = int(sys.argv[i + 1])
            i += 2
        else:
            i += 1
    
    print("="*80)
    print("MASTER REPOSITORY IMPROVEMENT ORCHESTRATOR")
    print("Perpetual Self-Updating AI Mind (100/10 Mindset)")
    print("="*80)
    print(f"Target QC Score: {target_score}/100")
    print(f"Max Iterations per Repo: {max_iterations}")
    if repo_filter:
        print(f"Filter: {repo_filter} only")
    print("="*80)
    
    # Phase 0: Discovery
    discovery_results = discovery_phase()
    
    # Determine which repos to process
    repos_to_process = [repo_filter] if repo_filter else REPOSITORIES
    
    # Filter out non-existent repos
    github_path = Path("C:/Users/sethp/Documents/Github")
    existing_repos = []
    for repo_name in repos_to_process:
        repo_path = github_path / repo_name
        if repo_path.exists():
            existing_repos.append(repo_name)
        else:
            print(f"\n⚠ Skipping {repo_name}: Not found")
    
    if not existing_repos:
        print("\n✗ No repositories to process!")
        sys.exit(1)
    
    # Process each repository
    results = {}
    for repo_name in existing_repos:
        result = process_repository(repo_name, max_iterations, target_score)
        results[repo_name] = result
    
    # Final summary
    print("\n" + "="*80)
    print("FINAL SUMMARY - ALL REPOSITORIES")
    print("="*80 + "\n")
    
    for repo_name, result in results.items():
        print(f"{repo_name}:")
        print(f"  Status: {result['status']}")
        print(f"  Iterations: {result['iterations']}")
        print(f"  Final Score: {result['final_score']}/100" if result['final_score'] else "  Final Score: N/A")
        print(f"  v1.0.0 Ready: {result['v1_ready']}")
        if result.get('scores'):
            print(f"  Score Progression: {' → '.join(str(s) for s in result['scores'])}")
        print()
    
    # Save results
    results_file = "MASTER-REPO-IMPROVEMENT-RESULTS.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "target_score": target_score,
            "max_iterations": max_iterations,
            "results": results
        }, f, indent=2)
    
    print(f"✓ Results saved to: {results_file}")
    print("="*80)

if __name__ == "__main__":
    main()


