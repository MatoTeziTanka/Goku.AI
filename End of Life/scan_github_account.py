#!/usr/bin/env python3
"""
GitHub Account Scanner
Scans all repositories in the MatoTeziTanka GitHub account and creates a comprehensive inventory
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
from foundry_local_agent import FoundryClaudeAgent


class GitHubAccountScanner:
    """Scan and analyze all repositories in a GitHub account"""
    
    def __init__(self, username: str = "MatoTeziTanka"):
        self.username = username
        self.agent = FoundryClaudeAgent()
        self.repositories = []
        self.scan_results = {}
    
    def get_repositories(self) -> List[Dict]:
        """Fetch all repositories from GitHub account"""
        print("="*70)
        print(f"Scanning GitHub Account: {self.username}")
        print("="*70)
        
        try:
            # Use GitHub CLI if available, otherwise use API
            result = subprocess.run(
                ["gh", "repo", "list", self.username, "--limit", "100", "--json", "name,description,isPrivate,updatedAt,language,defaultBranch"],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode == 0:
                repos = json.loads(result.stdout)
                print(f"✓ Found {len(repos)} repositories via GitHub CLI")
                return repos
            else:
                # Fallback: Scan local directories or use known repositories
                print("⚠ GitHub CLI not available, scanning local directories...")
                return self._get_local_repositories()
        except Exception as e:
            print(f"⚠ Error fetching repositories via GitHub CLI: {e}")
            print("\nScanning local directories for repositories...")
            return self._get_local_repositories()
    
    def _get_local_repositories(self) -> List[Dict]:
        """Get repositories from local directories"""
        local_repos = []
        current_dir = Path(".")
        
        # Known repositories that should exist locally (priority first)
        known_repo_names = [
            "BitPhoenix",
            "Goku.AI", 
            "ScalpStorm",
            "DinoCloud",
            "GSMG.IO",
            "FamilyFork",
            "KeyHound",
            "passive-income-infrastructure",
            "wordpress-stripe-automation",
            "pterodactyl-game-hosting",
            "discord-bot-monetization"
        ]
        
        # Scan for repositories
        for repo_name in known_repo_names:
            repo_path = current_dir / repo_name
            if repo_path.exists() and repo_path.is_dir():
                # Detect language
                language = None
                if list(repo_path.rglob("*.py")):
                    language = "Python"
                elif list(repo_path.rglob("*.js")):
                    language = "JavaScript"
                
                local_repos.append({
                    "name": repo_name,
                    "description": f"Local repository: {repo_name}",
                    "language": language,
                    "isPrivate": None,
                    "updatedAt": None,
                    "defaultBranch": "main"
                })
        
        # Also scan for any other git repositories
        for item in current_dir.iterdir():
            if item.is_dir() and (item / ".git").exists():
                if item.name not in known_repo_names:  # Don't duplicate
                    language = None
                    if list(item.rglob("*.py")):
                        language = "Python"
                    elif list(item.rglob("*.js")):
                        language = "JavaScript"
                    
                    local_repos.append({
                        "name": item.name,
                        "description": f"Local git repository: {item.name}",
                        "language": language,
                        "isPrivate": None,
                        "updatedAt": None,
                        "defaultBranch": "main"
                    })
        
        if local_repos:
            print(f"✓ Found {len(local_repos)} local repositories")
        else:
            print("⚠ No local repositories found")
        
        return local_repos
    
    def analyze_repository_structure(self, repo_name: str, local_path: Optional[Path] = None) -> Dict:
        """Analyze the structure of a repository"""
        print(f"\n📦 Analyzing: {repo_name}...")
        
        # Check if repo exists locally
        if local_path is None:
            local_path = Path(f"./{repo_name}")
        
        analysis = {
            "name": repo_name,
            "local_path": str(local_path),
            "exists_locally": local_path.exists(),
            "files": [],
            "directories": [],
            "file_types": {},
            "has_config": False,
            "has_docs": False,
            "has_tests": False,
            "port_configs": [],
            "version_info": None,
        }
        
        if not local_path.exists():
            print(f"  ⚠ Not found locally - will clone for analysis")
            return analysis
        
        # Scan directory structure
        try:
            for item in local_path.rglob("*"):
                if item.is_file():
                    rel_path = item.relative_to(local_path)
                    # Skip common ignored files
                    if any(skip in str(rel_path) for skip in ['.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build']):
                        continue
                    
                    analysis["files"].append(str(rel_path))
                    
                    # Track file types
                    ext = item.suffix.lower() or 'no-extension'
                    analysis["file_types"][ext] = analysis["file_types"].get(ext, 0) + 1
                    
                    # Check for config files
                    if item.name in ['package.json', 'requirements.txt', 'setup.py', 'pyproject.toml', 'Cargo.toml', 'go.mod']:
                        analysis["has_config"] = True
                    
                    # Check for docs
                    if item.suffix == '.md' or item.parent.name in ['docs', 'documentation']:
                        analysis["has_docs"] = True
                    
                    # Check for tests
                    if 'test' in item.name.lower() or 'spec' in item.name.lower() or 'tests' in str(rel_path):
                        analysis["has_tests"] = True
                    
                    # Check for port configurations
                    if self._check_for_port_config(item):
                        analysis["port_configs"].append(str(rel_path))
                
                elif item.is_dir():
                    rel_path = item.relative_to(local_path)
                    if rel_path.name not in ['.git', '__pycache__', 'node_modules', '.venv', 'venv', 'dist', 'build', '.idea']:
                        analysis["directories"].append(str(rel_path))
        except Exception as e:
            print(f"  ⚠ Error scanning structure: {e}")
        
        print(f"  ✓ Found {len(analysis['files'])} files, {len(analysis['directories'])} directories")
        return analysis
    
    def _check_for_port_config(self, file_path: Path) -> bool:
        """Check if file contains port configuration"""
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore').lower()
            # Look for common port patterns
            port_patterns = ['port', 'listen', 'bind', 'host:', 'localhost:', ':8080', ':3000', ':5000', ':8000']
            if any(pattern in content for pattern in port_patterns):
                # Read actual content to extract port numbers
                return True
        except:
            pass
        return False
    
    def extract_port_configs(self, repo_path: Path) -> List[Dict]:
        """Extract all port configurations from a repository"""
        ports = []
        try:
            for config_file in repo_path.rglob("*"):
                if config_file.is_file() and self._check_for_port_config(config_file):
                    try:
                        content = config_file.read_text(encoding='utf-8', errors='ignore')
                        # Try to extract port numbers (simple regex pattern)
                        import re
                        port_matches = re.findall(r'(?:port|PORT|listen|LISTEN)[\s:=]+(\d+)', content)
                        for port in port_matches:
                            ports.append({
                                "file": str(config_file.relative_to(repo_path)),
                                "port": int(port),
                                "repo": repo_path.name
                            })
                    except:
                        pass
        except Exception as e:
            print(f"  ⚠ Error extracting ports: {e}")
        return ports
    
    def get_version_info(self, repo_path: Path) -> Optional[Dict]:
        """Extract version information from repository"""
        version_files = ['package.json', 'setup.py', 'pyproject.toml', 'Cargo.toml', 'go.mod', 'VERSION', 'version.txt']
        
        for vfile in version_files:
            version_path = repo_path / vfile
            if version_path.exists():
                try:
                    content = version_path.read_text(encoding='utf-8')
                    if vfile == 'package.json':
                        import json
                        data = json.loads(content)
                        return {"file": vfile, "version": data.get("version"), "type": "semver"}
                    elif vfile in ['setup.py', 'pyproject.toml']:
                        # Try to extract version
                        import re
                        match = re.search(r'version\s*=\s*["\']([^"\']+)["\']', content)
                        if match:
                            return {"file": vfile, "version": match.group(1), "type": "semver"}
                except:
                    pass
        
        # Check git tags
        try:
            result = subprocess.run(
                ["git", "tag", "--sort=-version:refname"],
                cwd=str(repo_path),
                capture_output=True,
                text=True,
                check=False
            )
            if result.returncode == 0 and result.stdout.strip():
                tags = result.stdout.strip().split('\n')
                latest = tags[0]
                return {"file": "git_tag", "version": latest, "type": "git_tag", "all_tags": tags[:10]}
        except:
            pass
        
        return None
    
    def analyze_with_azure(self, repo_analysis: Dict, priority_repos: List[str]) -> Dict:
        """Use Azure API to analyze repository purpose and organization needs"""
        repo_name = repo_analysis["name"]
        is_priority = repo_name in priority_repos
        
        prompt = f"""Analyze this repository and provide a comprehensive assessment:

Repository: {repo_name}
Local Path: {repo_analysis.get('local_path', 'N/A')}
Priority Level: {'HIGH (Tier 1)' if is_priority else 'STANDARD (Tier 2)'}

Repository Structure:
- Total Files: {len(repo_analysis.get('files', []))}
- Directories: {len(repo_analysis.get('directories', []))}
- File Types: {json.dumps(repo_analysis.get('file_types', {}), indent=2)}
- Has Config Files: {repo_analysis.get('has_config', False)}
- Has Documentation: {repo_analysis.get('has_docs', False)}
- Has Tests: {repo_analysis.get('has_tests', False)}
- Port Configurations Found: {len(repo_analysis.get('port_configs', []))}
- Version Info: {json.dumps(repo_analysis.get('version_info', {}), indent=2)}

Sample Files (first 20):
{json.dumps(repo_analysis.get('files', [])[:20], indent=2)}

Requirements for analysis:
1. **Repository Purpose**: What is this repository's primary purpose? Is it clearly defined?
2. **File Organization**: Are files properly organized? Are there files that belong in other repositories?
3. **Documentation Quality**: Assess documentation completeness (README, inline comments, docstrings)
4. **Code Quality**: Identify issues with code structure, naming, conventions
5. **Versioning**: Current version status and recommendations
6. **Security Concerns**: Identify potential security issues, hardcoded secrets, deprecated dependencies
7. **Port Conflicts**: Any port configurations that might conflict with other repositories
8. **Misplaced Files**: Files that belong in other repositories (e.g., Goku.AI files, Shenron files)
9. **Standards Compliance**: Does it follow enterprise standards (versioning, commit messages, coding style)?
10. **Reorganization Needs**: Specific recommendations for reorganization

Provide a detailed JSON response with this structure:
{{
    "purpose": "Brief description",
    "organization_score": 0-10,
    "documentation_score": 0-10,
    "code_quality_score": 0-10,
    "security_score": 0-10,
    "standards_compliance_score": 0-10,
    "issues": [
        {{"severity": "critical|high|medium|low", "category": "category", "description": "..."}}
    ],
    "misplaced_files": [
        {{"file": "path/to/file", "should_be_in": "repository_name", "reason": "..."}}
    ],
    "reorganization_plan": {{
        "immediate_actions": [],
        "file_movements": [],
        "documentation_needs": [],
        "versioning_updates": []
    }},
    "port_conflicts": [],
    "recommendations": []
}}"""

        try:
            # Use analyze_file on a sample README or main file if available
            repo_path = Path(repo_analysis.get('local_path', f"./{repo_name}"))
            readme_path = repo_path / "README.md"
            
            if readme_path.exists():
                context = readme_path.read_text(encoding='utf-8', errors='ignore')[:5000]
                analysis = self.agent.analyze_file(str(readme_path), prompt)
            else:
                # Create a summary file for analysis
                summary_content = f"""
Repository: {repo_name}
Files: {len(repo_analysis.get('files', []))}
Structure: {json.dumps(repo_analysis, indent=2)[:10000]}
"""
                summary_path = Path(f"./temp_{repo_name}_summary.txt")
                summary_path.write_text(summary_content, encoding='utf-8')
                analysis = self.agent.analyze_file(str(summary_path), prompt)
                summary_path.unlink()
            
            return {"analysis": analysis, "source": "azure_api"}
        except Exception as e:
            print(f"  ⚠ Error analyzing with Azure: {e}")
            return {"analysis": None, "error": str(e)}
    
    def scan_all_repositories(self, priority_repos: Optional[List[str]] = None) -> Dict:
        """Scan all repositories and create comprehensive analysis"""
        if priority_repos is None:
            priority_repos = ["BitPhoenix", "Goku.AI", "ScalpStorm", "DinoCloud", "GSMG.IO"]
        
        print("\n" + "="*70)
        print("GitHub Account Comprehensive Scan")
        print("="*70)
        
        # Get all repositories
        repos = self.get_repositories()
        
        if not repos:
            print("⚠ No repositories found. Please ensure GitHub CLI is installed or provide repository list manually.")
            return {}
        
        all_ports = []
        scan_results = {
            "scan_date": datetime.now().isoformat(),
            "username": self.username,
            "total_repositories": len(repos),
            "repositories": [],
            "port_conflicts": [],
            "misplaced_files": [],
            "summary": {}
        }
        
        for repo in repos:
            repo_name = repo.get("name", "unknown")
            print(f"\n{'='*70}")
            print(f"Repository {repos.index(repo) + 1}/{len(repos)}: {repo_name}")
            print(f"{'='*70}")
            
            # Analyze structure
            repo_analysis = self.analyze_repository_structure(repo_name)
            repo_analysis.update(repo)
            
            # Extract port configs
            if repo_analysis["exists_locally"]:
                repo_path = Path(repo_analysis["local_path"])
                ports = self.extract_port_configs(repo_path)
                all_ports.extend(ports)
                repo_analysis["ports"] = ports
                
                # Get version info
                version_info = self.get_version_info(repo_path)
                if version_info:
                    repo_analysis["version_info"] = version_info
            
            # Analyze with Azure API (for priority repos or if requested)
            if repo_name in priority_repos or True:  # Analyze all for now
                print(f"  🤖 Analyzing with Azure API...")
                azure_analysis = self.analyze_with_azure(repo_analysis, priority_repos)
                repo_analysis["azure_analysis"] = azure_analysis
            
            scan_results["repositories"].append(repo_analysis)
        
        # Detect port conflicts
        port_usage = {}
        for port_info in all_ports:
            port = port_info["port"]
            if port not in port_usage:
                port_usage[port] = []
            port_usage[port].append(port_info)
        
        conflicts = {port: repos for port, repos in port_usage.items() if len(repos) > 1}
        scan_results["port_conflicts"] = conflicts
        
        # Generate summary
        scan_results["summary"] = {
            "total_files": sum(len(r.get("files", [])) for r in scan_results["repositories"]),
            "repos_with_docs": sum(1 for r in scan_results["repositories"] if r.get("has_docs")),
            "repos_with_tests": sum(1 for r in scan_results["repositories"] if r.get("has_tests")),
            "port_conflicts_count": len(conflicts),
            "priority_repos_scanned": len([r for r in scan_results["repositories"] if r["name"] in priority_repos])
        }
        
        return scan_results
    
    def save_scan_results(self, results: Dict, output_file: str = "github_scan_results.json"):
        """Save scan results to JSON file"""
        output_path = Path(output_file)
        output_path.write_text(json.dumps(results, indent=2, default=str), encoding='utf-8')
        print(f"\n✓ Scan results saved to: {output_file}")
        return output_path


def main():
    """Main execution"""
    scanner = GitHubAccountScanner("MatoTeziTanka")
    
    priority_repos = ["BitPhoenix", "Goku.AI", "ScalpStorm", "DinoCloud", "GSMG.IO"]
    
    # Scan all repositories
    results = scanner.scan_all_repositories(priority_repos=priority_repos)
    
    # Save results
    if results:
        scanner.save_scan_results(results)
        
        print("\n" + "="*70)
        print("Scan Summary")
        print("="*70)
        print(f"Total Repositories: {results['summary']['total_repositories']}")
        print(f"Total Files: {results['summary']['total_files']}")
        print(f"Port Conflicts: {results['summary']['port_conflicts_count']}")
        print(f"Priority Repos Scanned: {results['summary']['priority_repos_scanned']}")
        
        if results.get('port_conflicts'):
            print("\n⚠ Port Conflicts Detected:")
            for port, repos in results['port_conflicts'].items():
                print(f"  Port {port}: {', '.join([r['repo'] for r in repos])}")


if __name__ == "__main__":
    main()

