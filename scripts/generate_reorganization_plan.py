#!/usr/bin/env python3
"""
Generate Enterprise Reorganization Plan
Creates a comprehensive plan for reorganizing all repositories to enterprise standards
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime
from foundry_local_agent import FoundryClaudeAgent
from multi_agent_system import (
    AgentType, TaskPriority, Task, TaskScheduler, create_agent,
    BaseAgent
)
from scan_github_account import GitHubAccountScanner


class ReorganizationPlanGenerator:
    """Generate comprehensive reorganization plan using Azure API"""
    
    def __init__(self, scan_results_path: str = "github_scan_results.json"):
        self.agent = FoundryClaudeAgent(model="gpt-4.1")
        self.scan_results_path = Path(scan_results_path)
        self.scan_results = None
        self.plan = {}
        
    def load_scan_results(self):
        """Load scan results from JSON"""
        if not self.scan_results_path.exists():
            print(f"⚠ Scan results not found: {self.scan_results_path}")
            print("Running scan first...")
            scanner = GitHubAccountScanner()
            results = scanner.scan_all_repositories()
            scanner.save_scan_results(results)
            self.scan_results = results
        else:
            with open(self.scan_results_path, 'r', encoding='utf-8') as f:
                self.scan_results = json.load(f)
            print(f"✓ Loaded scan results: {len(self.scan_results.get('repositories', []))} repositories")
    
    def generate_master_plan(self, priority_repos: List[str] = None) -> Dict:
        """Generate master reorganization plan using Azure API"""
        if priority_repos is None:
            priority_repos = ["BitPhoenix", "Goku.AI", "ScalpStorm", "DinoCloud", "GSMG.IO"]
        
        print("="*70)
        print("Generating Master Reorganization Plan")
        print("="*70)
        
        prompt = f"""Generate a comprehensive enterprise-level reorganization plan for all repositories.

Priority Repositories (Tier 1 - Highest Focus):
{json.dumps(priority_repos, indent=2)}

Scan Results Summary:
- Total Repositories: {self.scan_results.get('total_repositories', 0)}
- Port Conflicts: {self.scan_results.get('summary', {}).get('port_conflicts_count', 0)}
- Total Files: {self.scan_results.get('summary', {}).get('total_files', 0)}

Repository Details (first 20000 chars):
{json.dumps(self.scan_results.get('repositories', [])[:5], indent=2)[:20000]}

Requirements:
1. **Repository Hierarchy**: Define a clear hierarchy and structure all repos must follow
2. **Versioning Standards**: Establish versioning rules (semver, but handle existing versions)
3. **Documentation Standards**: Define requirements for README, inline comments, docstrings, TODOs
4. **Commit Message Standards**: Establish commit message format requirements
5. **Coding Style Standards**: Define coding style, comment formats, TODO comment style
6. **Port Management**: Create a centralized port registry to prevent conflicts
7. **File Organization**: Identify files that need to move between repositories
8. **Security Standards**: Define security requirements and scanning protocols
9. **Network Configuration**: Understand reverse proxy VM setup and network requirements
10. **Execution Priority**: Prioritize actions for Tier 1 repos (BitPhoenix, Goku.AI, ScalpStorm, DinoCloud, GSMG.IO)

Special Considerations:
- Repos like GSMG.IO have existing versions - update to new version, don't reset to v1.0.0
- Goku.AI project files are scattered across repos - need to consolidate
- Files with "Shenron", "Goku", "Vegeta" themes belong in Goku.AI repo
- Files in "Doesnt Belong" directory need proper classification
- Must understand every file's purpose before reorganization

Provide a detailed JSON plan with this structure:
{{
    "master_plan": {{
        "repository_hierarchy": {{
            "tier_1_priority": ["BitPhoenix", "Goku.AI", "ScalpStorm", "DinoCloud", "GSMG.IO"],
            "tier_2_standard": ["..."],
            "structure_rules": {{...}},
            "naming_conventions": {{...}}
        }},
        "versioning_standards": {{
            "format": "semver",
            "rules": {{...}},
            "existing_version_handling": {{...}}
        }},
        "documentation_standards": {{
            "readme_requirements": {{...}},
            "inline_comment_style": {{...}},
            "docstring_requirements": {{...}},
            "todo_comment_format": {{...}}
        }},
        "commit_message_standards": {{
            "format": "...",
            "examples": [...]
        }},
        "coding_style_standards": {{
            "comment_formats": {{...}},
            "todo_format": "...",
            "language_specific_rules": {{...}}
        }},
        "port_registry": {{
            "bitphoenix": 8000,
            "goku_ai": 8001,
            "scalpstorm": 8002,
            "dinocloud": 8003,
            "gsmg_io": 8004,
            "conflict_resolution": {{...}}
        }},
        "file_reorganization": {{
            "files_to_move": [
                {{
                    "file": "path/to/file",
                    "from_repo": "BitPhoenix",
                    "to_repo": "Goku.AI",
                    "reason": "..."
                }}
            ],
            "new_repos_needed": [
                {{
                    "repo_name": "Goku.AI",
                    "description": "...",
                    "files_to_migrate": [...]
                }}
            ]
        }},
        "security_standards": {{
            "scanning_protocols": {{...}},
            "secret_detection": {{...}},
            "dependency_checking": {{...}}
        }},
        "network_configuration": {{
            "reverse_proxy_setup": {{...}},
            "port_requirements": {{...}},
            "vm_configuration": {{...}}
        }},
        "execution_plan": {{
            "phase_1_priority_repos": [
                {{
                    "repo": "BitPhoenix",
                    "actions": [...],
                    "estimated_time": "...",
                    "dependencies": []
                }}
            ],
            "phase_2_standard_repos": [...],
            "multi_agent_assignment": {{
                "skeptical_reviewer": [...],
                "ruthless_optimizer": [...],
                "docstring_guru": [...],
                "security_sentinel": [...]
            }}
        }}
    }},
    "immediate_actions": [
        {{
            "action": "...",
            "priority": "critical|high|medium|low",
            "repo": "...",
            "agent_type": "..."
        }}
    ]
}}"""

        try:
            # Generate plan using Azure API
            print("\n🤖 Generating master plan with Azure API (GPT-4.1)...")
            
            # Create a temporary summary file for analysis
            summary_content = json.dumps({
                "priority_repos": priority_repos,
                "scan_summary": self.scan_results.get('summary', {}),
                "repositories": self.scan_results.get('repositories', [])[:5]  # Sample
            }, indent=2)
            
            summary_path = Path("./temp_plan_generation_summary.json")
            summary_path.write_text(summary_content, encoding='utf-8')
            
            # Use analyze_file to generate plan
            plan_output = self.agent.analyze_file(
                str(summary_path),
                prompt
            )
            
            # Clean up temp file
            summary_path.unlink()
            
            # Try to extract JSON from response
            plan_json = self._extract_json_from_response(plan_output)
            
            if plan_json:
                self.plan = plan_json
                print("✓ Master plan generated successfully")
            else:
                # Fallback: create structure from text response
                self.plan = self._create_plan_from_text(plan_output, priority_repos)
                print("✓ Master plan created from analysis")
            
            return self.plan
            
        except Exception as e:
            print(f"⚠ Error generating plan: {e}")
            # Create a basic plan structure
            self.plan = self._create_basic_plan(priority_repos)
            return self.plan
    
    def _extract_json_from_response(self, response: str) -> Dict:
        """Extract JSON from Azure API response"""
        try:
            # Try to find JSON in the response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
        except:
            pass
        return None
    
    def _create_plan_from_text(self, text: str, priority_repos: List[str]) -> Dict:
        """Create plan structure from text analysis"""
        return {
            "master_plan": {
                "repository_hierarchy": {
                    "tier_1_priority": priority_repos,
                    "tier_2_standard": [],
                    "structure_rules": {},
                    "naming_conventions": {}
                },
                "versioning_standards": {
                    "format": "semver",
                    "rules": {}
                },
                "documentation_standards": {},
                "commit_message_standards": {},
                "coding_style_standards": {},
                "port_registry": {},
                "file_reorganization": {},
                "security_standards": {},
                "network_configuration": {},
                "execution_plan": {
                    "phase_1_priority_repos": [],
                    "multi_agent_assignment": {}
                }
            },
            "immediate_actions": [],
            "raw_analysis": text
        }
    
    def _create_basic_plan(self, priority_repos: List[str]) -> Dict:
        """Create basic plan structure"""
        return {
            "master_plan": {
                "repository_hierarchy": {
                    "tier_1_priority": priority_repos,
                    "tier_2_standard": []
                },
                "port_registry": {
                    "BitPhoenix": 8000,
                    "Goku.AI": 8001,
                    "ScalpStorm": 8002,
                    "DinoCloud": 8003,
                    "GSMG.IO": 8004
                },
                "execution_plan": {
                    "phase_1_priority_repos": [
                        {"repo": repo, "actions": []} for repo in priority_repos
                    ]
                }
            },
            "immediate_actions": []
        }
    
    def save_plan(self, output_file: str = "reorganization_plan.json"):
        """Save reorganization plan to JSON file"""
        output_path = Path(output_file)
        plan_with_metadata = {
            "generated_date": datetime.now().isoformat(),
            "plan": self.plan
        }
        output_path.write_text(json.dumps(plan_with_metadata, indent=2, default=str), encoding='utf-8')
        print(f"\n✓ Plan saved to: {output_file}")
        return output_path
    
    def create_tasks_from_plan(self) -> List[Task]:
        """Create tasks from reorganization plan"""
        tasks = []
        
        if not self.plan:
            print("⚠ No plan available - generate plan first")
            return tasks
        
        plan = self.plan.get("master_plan", {})
        execution_plan = plan.get("execution_plan", {})
        
        # Phase 1: Priority repos
        phase_1_repos = execution_plan.get("phase_1_priority_repos", [])
        
        for repo_info in phase_1_repos:
            repo_name = repo_info.get("repo", "unknown")
            actions = repo_info.get("actions", [])
            
            # Create tasks for each action
            for i, action in enumerate(actions):
                task = Task(
                    id=f"task_{repo_name}_{i}",
                    description=f"{repo_name}: {action.get('description', action)}",
                    priority=TaskPriority.HIGH,
                    agent_type=AgentType.MULTI_MODAL_EXPERT,  # Default
                    estimated_runtime=3600,  # 1 hour default
                    dependencies=[],
                    repo_name=repo_name
                )
                tasks.append(task)
        
        return tasks


def main():
    """Main execution"""
    print("="*70)
    print("Enterprise Reorganization Plan Generator")
    print("="*70)
    
    generator = ReorganizationPlanGenerator()
    
    # Load scan results
    generator.load_scan_results()
    
    if not generator.scan_results:
        print("⚠ No scan results available")
        return
    
    # Priority repositories
    priority_repos = ["BitPhoenix", "Goku.AI", "ScalpStorm", "DinoCloud", "GSMG.IO"]
    
    # Generate master plan
    plan = generator.generate_master_plan(priority_repos=priority_repos)
    
    # Save plan
    generator.save_plan()
    
    # Create tasks
    tasks = generator.create_tasks_from_plan()
    print(f"\n✓ Created {len(tasks)} tasks from plan")
    
    print("\n" + "="*70)
    print("Plan Generation Complete")
    print("="*70)
    print("\nNext steps:")
    print("1. Review reorganization_plan.json")
    print("2. Run execute_reorganization.py to begin execution")


if __name__ == "__main__":
    main()






