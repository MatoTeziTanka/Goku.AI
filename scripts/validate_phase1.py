#!/usr/bin/env python3
import os
import json
import re
import sys
from pathlib import Path
from datetime import datetime

GITHUB_ROOT = Path("C:/Users/sethp/Documents/Github")
REPOS = ["Keyhound", "BitPhoenix", "Dell-Server-Roadmap", "Scalpstorm", 
         "Goku.AI", "Dino-Cloud", "FamilyFork", "DinoCloud", "GSMG.IO", 
         "Server-Roadmap", "StreamForge"]

SECURITY_PATTERNS = {
    "api_key": r"(?i)(api_key|apikey|api-key)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-]+)['\"]?",
    "secret": r"(?i)(secret|password|passwd|pwd)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-!@#$%]+)['\"]?",
    "token": r"(?i)(token|auth_token|bearer)\s*[:=]\s*['\"]?([a-zA-Z0-9_\-.]+)['\"]?",
    "credentials": r"(?i)(username|user)\s*[:=]\s*['\"]([^'\"]+)['\"]",
    "aws_key": r"AKIA[0-9A-Z]{16}",
    "github_token": r"ghp_[A-Za-z0-9_]{36,255}",
    "private_key": r"-----BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY"
}

def log_msg(msg, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {msg}")

def verify_repos():
    log_msg("TASK 1: Verifying 11 repositories...")
    found_repos = []
    missing_repos = []
    
    for repo in REPOS:
        repo_path = GITHUB_ROOT / repo
        if repo_path.exists() and (repo_path / ".git").exists():
            found_repos.append(repo)
            log_msg(f"  [OK] {repo}", "OK")
        else:
            missing_repos.append(repo)
            log_msg(f"  [FAIL] {repo} NOT FOUND or NO .git folder", "ERROR")
    
    return len(found_repos) == 11, found_repos, missing_repos

def verify_consensus_files():
    log_msg("TASK 2: Verifying *-FINAL-CONSENSUS.md files...")
    consensus_files = list(GITHUB_ROOT.glob("*-FINAL-CONSENSUS.md"))
    
    if len(consensus_files) < 24:
        log_msg(f"  [WARN] Expected 24 consensus files, found {len(consensus_files)}", "WARN")
    else:
        log_msg(f"  [OK] Found {len(consensus_files)} consensus files", "OK")
    
    readable_files = []
    for cf in consensus_files:
        try:
            with open(cf, 'r', encoding='utf-8') as f:
                content = f.read()
                readable_files.append((cf.name, len(content)))
                log_msg(f"  [OK] {cf.name} ({len(content)} bytes)", "OK")
        except Exception as e:
            log_msg(f"  [FAIL] {cf.name}: {e}", "ERROR")
    
    return len(readable_files), consensus_files

def security_scan():
    log_msg("TASK 3: Security scan for exposed secrets...")
    security_issues = []
    scan_files = []
    
    for root, dirs, files in os.walk(GITHUB_ROOT):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__', 'node_modules']]
        for file in files:
            if file.endswith(('.md', '.py', '.js', '.env', '.txt', '.yaml', '.yml')):
                scan_files.append(os.path.join(root, file))
    
    log_msg(f"  Scanning {len(scan_files)} files for secrets...", "INFO")
    
    for file_path in scan_files:
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                for pattern_name, pattern in SECURITY_PATTERNS.items():
                    matches = re.finditer(pattern, content, re.MULTILINE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        security_issues.append({
                            'file': file_path,
                            'pattern': pattern_name,
                            'line': line_num,
                            'match': match.group(0)[:50]
                        })
                        log_msg(f"  [WARN] {file_path}:{line_num} - {pattern_name}", "WARN")
        except Exception as e:
            pass
    
    return security_issues

def verify_env_files():
    log_msg("TASK 4: Verifying .env.example files for real values...")
    env_issues = []
    
    for root, dirs, files in os.walk(GITHUB_ROOT):
        dirs[:] = [d for d in dirs if d not in ['.git', '__pycache__']]
        for file in files:
            if file == '.env.example':
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(SECURITY_PATTERNS['api_key'], content) or \
                           re.search(SECURITY_PATTERNS['secret'], content):
                            env_issues.append(file_path)
                            log_msg(f"  [FAIL] {file_path} contains real values!", "ERROR")
                        else:
                            log_msg(f"  [OK] {file_path} - placeholders only", "OK")
                except Exception as e:
                    pass
    
    return env_issues

def check_path_compatibility():
    log_msg("TASK 5: Checking Windows path compatibility...")
    issues = []
    
    for root, dirs, files in os.walk(GITHUB_ROOT):
        for file in files:
            file_path = os.path.join(root, file)
            if len(file_path) >= 260:
                issues.append(file_path)
                log_msg(f"  [WARN] Path too long ({len(file_path)} chars): {file_path[:80]}", "WARN")
    
    if not issues:
        log_msg(f"  [OK] All paths under 260 character limit", "OK")
    
    return issues

def parse_consensus_json():
    log_msg("TASK 6: Parsing JSON from consensus files...")
    json_specs = {}
    
    for cf in GITHUB_ROOT.glob("*-FINAL-CONSENSUS.md"):
        try:
            with open(cf, 'r', encoding='utf-8') as f:
                content = f.read()
                json_matches = re.findall(r'```json\n(.*?)\n```', content, re.DOTALL)
                if json_matches:
                    for match in json_matches:
                        try:
                            spec = json.loads(match)
                            json_specs[cf.name] = spec
                            log_msg(f"  [OK] {cf.name}: {len(match)} bytes of JSON", "OK")
                        except json.JSONDecodeError:
                            pass
        except Exception as e:
            pass
    
    return json_specs

def main():
    print("\n" + "="*80)
    print("PHASE 1: VALIDATION - Azure Batch Code Agent")
    print("="*80 + "\n")
    
    repos_ok, found_repos, missing_repos = verify_repos()
    print()
    
    readable_count, consensus_files = verify_consensus_files()
    print()
    
    security_issues = security_scan()
    print()
    
    env_issues = verify_env_files()
    print()
    
    path_issues = check_path_compatibility()
    print()
    
    json_specs = parse_consensus_json()
    print()
    
    log_msg("="*80, "")
    log_msg("PHASE 1 VALIDATION SUMMARY", "SUMMARY")
    log_msg("="*80, "")
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "repos_verified": len(found_repos),
        "repos_expected": 11,
        "repos_ok": repos_ok,
        "consensus_files": len(consensus_files),
        "security_issues_found": len(security_issues),
        "env_issues_found": len(env_issues),
        "path_issues_found": len(path_issues),
        "json_specs_found": len(json_specs),
        "repositories": found_repos,
        "missing_repositories": missing_repos,
        "security_issues": security_issues[:10],
        "env_issues": env_issues
    }
    
    log_msg(f"[OK] Repositories verified: {len(found_repos)}/11", "OK")
    log_msg(f"[OK] Consensus files readable: {readable_count}", "OK")
    log_msg(f"[WARN] Security issues detected: {len(security_issues)}", "WARN" if security_issues else "OK")
    log_msg(f"[OK] .env.example issues: {len(env_issues)}", "OK" if not env_issues else "ERROR")
    log_msg(f"[WARN] Path compatibility issues: {len(path_issues)}", "WARN" if path_issues else "OK")
    log_msg(f"[OK] JSON specs parsed: {len(json_specs)}", "OK")
    
    with open("validation_log.txt", 'w', encoding='utf-8') as f:
        f.write(json.dumps(summary, indent=2))
    
    log_msg(f"\n[OK] Validation log saved to: validation_log.txt", "OK")
    
    if security_issues:
        log_msg("\n[ALERT] SECURITY CHECKPOINT ALERT!", "ALERT")
        log_msg(f"Found {len(security_issues)} potential security issues.", "ALERT")
        log_msg("Review SECURITY_ALERT.md before proceeding to Phase 2.", "ALERT")
        
        with open("SECURITY_ALERT.md", 'w', encoding='utf-8') as f:
            f.write("# Security Alert - Phase 1 Validation\n\n")
            f.write(f"**Timestamp**: {datetime.now().isoformat()}\n\n")
            f.write(f"## Issues Found: {len(security_issues)}\n\n")
            for issue in security_issues[:20]:
                f.write(f"- **{issue['pattern']}** in `{issue['file']}`:{issue['line']}\n")
                f.write(f"  Match: `{issue['match']}`\n\n")
    
    return repos_ok and not security_issues and not env_issues

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
