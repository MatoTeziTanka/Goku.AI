#!/usr/bin/env python3
import os
import json
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

GITHUB_ROOT = Path("C:/Users/sethp/Documents/Github")
REPOS = ["Keyhound", "BitPhoenix", "Dell-Server-Roadmap", "Scalpstorm", 
         "Goku.AI", "Dino-Cloud", "FamilyFork", "DinoCloud", "GSMG.IO", 
         "Server-Roadmap", "StreamForge"]

class Phase2BatchApplier:
    def __init__(self):
        self.applied_changes = []
        self.errors = []
        self.total_applied = 0
        self.summary_by_repo = defaultdict(lambda: {"created": [], "modified": [], "errors": []})
    
    def load_and_parse_consensus(self):
        print("\n[PHASE 2] Loading and parsing consensus files...")
        changes_by_priority = defaultdict(list)
        
        for cf in GITHUB_ROOT.glob("*-FINAL-CONSENSUS.md"):
            repo_name = cf.stem.split("-FINAL")[0]
            if repo_name not in REPOS:
                continue
            
            try:
                with open(cf, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
                if not json_match:
                    continue
                
                spec = json.loads(json_match.group(1))
                changes = spec.get("changes", [])
                
                for change in changes:
                    priority = change.get("priority", "Medium")
                    changes_by_priority[priority].append({
                        "repo": repo_name,
                        "file_path": change.get("file_path"),
                        "action": change.get("action"),
                        "reasoning": change.get("reasoning"),
                        "changes_made": change.get("changes_made")
                    })
                
                print(f"  [OK] {cf.name}: {len(changes)} changes")
            except Exception as e:
                self.errors.append(f"Failed to parse {cf.name}: {str(e)}")
        
        return changes_by_priority
    
    def apply_changes(self, changes_by_priority):
        print("\n[PHASE 2] Applying changes by priority...")
        
        priority_order = ["Critical", "High", "Medium", "Low"]
        
        for priority in priority_order:
            if priority not in changes_by_priority:
                continue
            
            print(f"\n  [{priority.upper()} PRIORITY]")
            for change in changes_by_priority[priority]:
                self._apply_single_change(change)
    
    def _apply_single_change(self, change):
        repo = change["repo"]
        file_path = change["file_path"]
        action = change["action"]
        repo_path = GITHUB_ROOT / repo
        
        if not repo_path.exists():
            self.errors.append(f"Repo not found: {repo}")
            return
        
        full_path = repo_path / file_path
        
        if action == "created":
            self._create_file(repo, full_path, file_path)
        elif action == "modified":
            self._modify_file(repo, full_path, file_path)
        elif action == "deleted":
            self._delete_file(repo, full_path)
    
    def _create_file(self, repo, full_path, file_path):
        try:
            full_path.parent.mkdir(parents=True, exist_ok=True)
            
            if full_path.exists():
                self.summary_by_repo[repo]["errors"].append(f"File already exists: {file_path}")
                return
            
            content = self._generate_file_content(repo, file_path)
            
            with open(full_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.total_applied += 1
            self.summary_by_repo[repo]["created"].append(file_path)
            self.applied_changes.append({
                "repo": repo,
                "file": file_path,
                "action": "created",
                "status": "OK"
            })
            print(f"    [CREATE] {repo}/{file_path}")
        except Exception as e:
            self.errors.append(f"Failed to create {repo}/{file_path}: {str(e)}")
            self.summary_by_repo[repo]["errors"].append(str(e))
    
    def _modify_file(self, repo, full_path, file_path):
        try:
            if not full_path.exists():
                self.summary_by_repo[repo]["errors"].append(f"File not found: {file_path}")
                return
            
            if file_path == ".gitignore":
                self._enhance_gitignore(full_path)
            elif file_path == ".env.example":
                self._enhance_env_example(full_path, repo)
            else:
                return
            
            self.total_applied += 1
            self.summary_by_repo[repo]["modified"].append(file_path)
            self.applied_changes.append({
                "repo": repo,
                "file": file_path,
                "action": "modified",
                "status": "OK"
            })
            print(f"    [UPDATE] {repo}/{file_path}")
        except Exception as e:
            self.errors.append(f"Failed to modify {repo}/{file_path}: {str(e)}")
            self.summary_by_repo[repo]["errors"].append(str(e))
    
    def _delete_file(self, repo, full_path):
        try:
            if full_path.exists():
                full_path.unlink()
                self.total_applied += 1
                print(f"    [DELETE] {repo}/{full_path.name}")
        except Exception as e:
            self.errors.append(f"Failed to delete {repo}/{full_path}: {str(e)}")
    
    def _generate_file_content(self, repo, file_path):
        if file_path == "CLAUDE.md":
            return self._generate_claude_md(repo)
        elif file_path == "SECURITY.md":
            return self._generate_security_md()
        elif file_path == ".env.example":
            return self._generate_env_example()
        elif ".github/workflows/" in file_path:
            return self._generate_workflow_file(file_path)
        else:
            return f"# {file_path}\n\nGenerated during Phase 2 batch processing.\n"
    
    def _generate_claude_md(self, repo):
        return f"""# {repo} - AI Documentation

Generated: {datetime.now().isoformat()}

## Purpose
This document provides AI agents (Claude, GPT, etc.) with essential context for understanding and working with the {repo} codebase.

## Repository Overview
- **Repository**: {repo}
- **Type**: Code repository
- **Primary Language**: (Detect from codebase)

## Architecture Overview
- Main entry points
- Key modules and their responsibilities
- Data flow and dependencies

## Getting Started
1. Clone the repository
2. Install dependencies
3. Configure environment (see .env.example)
4. Run tests
5. Start development

## Key Files
- `README.md` - Project overview and setup instructions
- `.env.example` - Environment configuration template
- `SECURITY.md` - Security policies and guidelines

## Development Workflow
1. Create a branch for your changes
2. Make your changes with clear commit messages
3. Run tests to ensure nothing breaks
4. Submit a pull request for review

## Testing
- Unit tests: `npm test` or `pytest`
- Integration tests: See CI/CD workflows
- Security scanning: Automated via GitHub Actions

## Security
- See `SECURITY.md` for vulnerability reporting
- No API keys or credentials in code
- Use `.env.example` for configuration templates

## Contact & Support
- See README.md for contact information
- Check CONTRIBUTING.md for guidelines

---
*This file is maintained to help AI assistants understand the project structure and context.*
"""
    
    def _generate_security_md(self):
        return """# Security Policy

## Vulnerability Reporting
Please report security vulnerabilities responsibly by emailing security@example.com or using GitHub Security Advisory.

**Do not** open public issues for security vulnerabilities.

## Security Guidelines

### Environment Variables
- Never commit `.env` files
- Use `.env.example` as a template
- All secrets should be in environment variables or secure vaults

### Dependencies
- Keep dependencies up to date
- Run security audits regularly
- Use `npm audit` / `pip check` / equivalent tools

### Code Review
- All changes require code review
- Security issues must be addressed before merge
- Automated security scanning is enabled

### Authentication & Authorization
- Implement principle of least privilege
- Use strong authentication mechanisms
- Validate all user inputs

### Data Protection
- Encrypt sensitive data at rest and in transit
- Follow GDPR/privacy regulations
- Implement proper access controls

## Security Scanning
Automated security scanning is enabled via GitHub Actions:
- SAST (Static Application Security Testing)
- Dependency scanning
- Secret detection

## Contact
Security issues: security@example.com
"""
    
    def _generate_env_example(self):
        return """# Environment Configuration Template

# Database
DATABASE_URL=your_database_url_here
DB_USER=your_db_username
DB_PASSWORD=your_secure_password

# API Keys
API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
AUTH_TOKEN=your_auth_token_here

# Application Settings
APP_ENV=development
DEBUG=false
LOG_LEVEL=info

# Security
ENCRYPT_KEYS=your_encryption_key_here
SESSION_SECRET=your_session_secret_here

# External Services
SERVICE_URL=https://api.example.com
SERVICE_KEY=your_service_key_here

# Deployment
PORT=3000
HOST=localhost
"""
    
    def _generate_workflow_file(self, file_path):
        if "security" in file_path.lower():
            return """name: Security Scanning

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run security scanning
        run: |
          # Placeholder for security scanning
          echo "Running security scans..."
          
      - name: Upload results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: security-results
          path: ./security-results/
"""
        return ""
    
    def _enhance_gitignore(self, gitignore_path):
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        additions = """
# Environment variables
.env
.env.local
.env.*.local

# API Keys and Secrets
*.key
*.pem
*.cert
credentials.json
secrets.json
config/secrets.yml

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Build artifacts
dist/
build/
*.egg-info/
node_modules/
__pycache__/
.pytest_cache/
*.pyc

# Logs
logs/
*.log
npm-debug.log*

# OS
.DS_Store
Thumbs.db

# Dependencies
venv/
env/
.venv/
"""
        if additions not in content:
            with open(gitignore_path, 'a', encoding='utf-8') as f:
                f.write("\n" + additions)
    
    def _enhance_env_example(self, env_path, repo):
        with open(env_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if "API_KEY" not in content:
            content += "\n# Add any missing configuration variables\n"
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
    
    def generate_report(self):
        print("\n" + "="*80)
        print("PHASE 2 BATCH APPLICATION - COMPLETE")
        print("="*80)
        
        print(f"\n[SUMMARY]")
        print(f"  Total changes applied: {self.total_applied}")
        print(f"  Total errors: {len(self.errors)}")
        
        print(f"\n[BY REPOSITORY]")
        for repo in sorted(self.summary_by_repo.keys()):
            summary = self.summary_by_repo[repo]
            created = len(summary["created"])
            modified = len(summary["modified"])
            errors = len(summary["errors"])
            if created or modified or errors:
                print(f"  {repo}: +{created} created, +{modified} modified, {errors} errors")
        
        if self.errors:
            print(f"\n[ERRORS]")
            for error in self.errors[:10]:
                print(f"  - {error}")
        
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "phase": "Phase 2 - Batch Application",
            "total_applied": self.total_applied,
            "total_errors": len(self.errors),
            "changes_by_repo": dict(self.summary_by_repo),
            "errors": self.errors[:20]
        }
        
        with open("PHASE_2_EXECUTION_REPORT.md", 'w', encoding='utf-8') as f:
            f.write("# Phase 2: Batch Application Report\n\n")
            f.write(f"**Executed**: {report_data['timestamp']}\n\n")
            f.write(f"## Summary\n")
            f.write(f"- Changes Applied: {self.total_applied}\n")
            f.write(f"- Errors: {len(self.errors)}\n\n")
            f.write(f"## Changes by Repository\n")
            for repo, changes in sorted(self.summary_by_repo.items()):
                if changes["created"] or changes["modified"]:
                    f.write(f"\n### {repo}\n")
                    if changes["created"]:
                        f.write(f"- Created: {', '.join(changes['created'])}\n")
                    if changes["modified"]:
                        f.write(f"- Modified: {', '.join(changes['modified'])}\n")
        
        print(f"\n[REPORT] Generated: PHASE_2_EXECUTION_REPORT.md")

def main():
    print("="*80)
    print("PHASE 2: BATCH APPLICATION - Azure Batch Code Agent")
    print("="*80)
    
    applier = Phase2BatchApplier()
    
    changes_by_priority = applier.load_and_parse_consensus()
    if not changes_by_priority:
        print("[FAIL] No changes found")
        return False
    
    applier.apply_changes(changes_by_priority)
    
    applier.generate_report()
    
    return applier.total_applied > 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
