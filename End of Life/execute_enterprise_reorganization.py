#!/usr/bin/env python3
"""
Master Execution Script for Enterprise Reorganization
Orchestrates the entire reorganization process using multi-agent system
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List
from scan_github_account import GitHubAccountScanner
from generate_reorganization_plan import ReorganizationPlanGenerator
from multi_agent_system import (
    TaskScheduler, Task, TaskPriority, AgentType, create_agent,
    TaskStatus
)
from foundry_local_agent import FoundryClaudeAgent
from comprehensive_analysis_logger import ComprehensiveAnalysisLogger


class EnterpriseReorganizationExecutor:
    """Execute enterprise reorganization using multi-agent system"""
    
    def __init__(self):
        self.scanner = GitHubAccountScanner()
        self.plan_generator = ReorganizationPlanGenerator()
        self.scheduler = TaskScheduler()
        self.azure_agent = FoundryClaudeAgent(model="gpt-4.1")
        self.analysis_logger = ComprehensiveAnalysisLogger()
        self.priority_repos = ["BitPhoenix", "Goku.AI", "ScalpStorm", "DinoCloud", "GSMG.IO"]
        
        # Load enterprise standards
        self.standards_path = Path("enterprise_standards.json")
        if self.standards_path.exists():
            with open(self.standards_path, 'r', encoding='utf-8') as f:
                self.standards = json.load(f)
        else:
            self.standards = {}
            print("⚠ Enterprise standards file not found - using defaults")
    
    def initialize_agents(self):
        """Initialize all specialized agents"""
        print("="*70)
        print("Initializing Multi-Agent System")
        print("="*70)
        
        agents = [
            create_agent(AgentType.SKEPTICAL_REVIEWER),
            create_agent(AgentType.RUTHLESS_OPTIMIZER),
            create_agent(AgentType.DOCSTRING_GURU),
            create_agent(AgentType.SECURITY_SENTINEL),
            create_agent(AgentType.MULTI_MODAL_EXPERT),
            create_agent(AgentType.SILENT_OPERATOR),
            create_agent(AgentType.PORT_MANAGER),
            create_agent(AgentType.FILE_CLASSIFIER),
        ]
        
        for agent in agents:
            self.scheduler.register_agent(agent)
        
        print(f"✓ Initialized {len(agents)} agents")
        return agents
    
    def phase_1_scan(self) -> Dict:
        """Phase 1: Scan all repositories"""
        print("\n" + "="*70)
        print("PHASE 1: Scanning GitHub Account")
        print("="*70)
        
        scan_results = self.scanner.scan_all_repositories(priority_repos=self.priority_repos)
        
        if scan_results:
            self.scanner.save_scan_results(scan_results)
            print("\n✓ Phase 1 Complete: Scan results saved")
        else:
            print("⚠ Phase 1 Warning: No scan results generated")
        
        return scan_results
    
    def phase_2_plan(self, scan_results: Dict = None) -> Dict:
        """Phase 2: Generate reorganization plan"""
        print("\n" + "="*70)
        print("PHASE 2: Generating Reorganization Plan")
        print("="*70)
        
        if scan_results:
            self.plan_generator.scan_results = scan_results
        
        plan = self.plan_generator.generate_master_plan(priority_repos=self.priority_repos)
        
        if plan:
            self.plan_generator.save_plan()
            print("\n✓ Phase 2 Complete: Reorganization plan generated")
        else:
            print("⚠ Phase 2 Warning: No plan generated")
        
        return plan
    
    def phase_2_5_comprehensive_analysis(self, scan_results: Dict = None) -> Dict:
        """Phase 2.5: Comprehensive Analysis - Log all issues for later fixing"""
        print("\n" + "="*70)
        print("PHASE 2.5: Comprehensive Analysis & Issue Logging")
        print("="*70)
        print("\nAnalyzing all files for:")
        print("  - Project understanding")
        print("  - Bugs")
        print("  - Security flaws")
        print("  - Bad code practices")
        print("  - Missing documentation (all types: inline, block, docstring, TODO)")
        print("\n⚠ All issues will be LOGGED for later fixing (not fixed now)")
        print("="*70)
        
        if not scan_results:
            # Try to load existing scan results
            scan_path = Path("github_scan_results.json")
            if scan_path.exists():
                with open(scan_path, 'r', encoding='utf-8') as f:
                    scan_results = json.load(f)
            else:
                print("⚠ No scan results available - skipping comprehensive analysis")
                return {}
        
        analysis_results = {
            "repositories_analyzed": [],
            "total_files_analyzed": 0,
            "total_issues_found": 0
        }
        
        # Analyze priority repositories first
        repos = scan_results.get("repositories", [])
        priority_repos_list = [r for r in repos if r.get("name") in self.priority_repos]
        
        print(f"\n📊 Analyzing {len(priority_repos_list)} priority repositories...")
        
        for repo in priority_repos_list:
            repo_name = repo.get("name", "unknown")
            repo_path = Path(repo.get("local_path", f"./{repo_name}"))
            
            if not repo_path.exists():
                print(f"\n⚠ Repository {repo_name} not found locally at {repo_path}")
                continue
            
            print(f"\n{'='*70}")
            print(f"Analyzing: {repo_name}")
            print(f"{'='*70}")
            
            # Analyze repository
            repo_analysis = self.analysis_logger.analyze_repository(repo_path, repo_name)
            
            if "error" not in repo_analysis:
                analysis_results["repositories_analyzed"].append(repo_name)
                analysis_results["total_files_analyzed"] += repo_analysis.get("files_analyzed", 0)
                analysis_results["total_issues_found"] += repo_analysis.get("total_issues", 0)
        
        # Save all issues logged
        self.analysis_logger.save_issues_log()
        
        print("\n" + "="*70)
        print("Comprehensive Analysis Complete")
        print("="*70)
        print(f"Repositories Analyzed: {len(analysis_results['repositories_analyzed'])}")
        print(f"Total Files Analyzed: {analysis_results['total_files_analyzed']}")
        print(f"Total Issues Logged: {analysis_results['total_issues_found']}")
        print(f"\n✓ Issues logged to: comprehensive_issues_log.json")
        print(f"✓ Summary report: comprehensive_issues_summary.md")
        print("\n⚠ All issues are LOGGED for later fixing - review the log files to prioritize fixes")
        
        return analysis_results
    
    def phase_3_create_tasks(self, plan: Dict) -> List[Task]:
        """Phase 3: Create tasks from plan"""
        print("\n" + "="*70)
        print("PHASE 3: Creating Tasks from Plan")
        print("="*70)
        
        tasks = []
        
        # Load plan if not provided
        if not plan:
            plan_path = Path("reorganization_plan.json")
            if plan_path.exists():
                with open(plan_path, 'r', encoding='utf-8') as f:
                    plan_data = json.load(f)
                    plan = plan_data.get("plan", {})
            else:
                print("⚠ No plan available - cannot create tasks")
                return tasks
        
        master_plan = plan.get("master_plan", {})
        execution_plan = master_plan.get("execution_plan", {})
        
        # Phase 1: Priority repos
        phase_1_repos = execution_plan.get("phase_1_priority_repos", [])
        
        for repo_info in phase_1_repos:
            repo_name = repo_info.get("repo", "unknown")
            print(f"\n  Creating tasks for: {repo_name}")
            
            # Task 1: Review and analyze repository
            task_review = Task(
                id=f"{repo_name}_review",
                description=f"Review and analyze {repo_name} repository structure",
                priority=TaskPriority.CRITICAL,
                agent_type=AgentType.SKEPTICAL_REVIEWER,
                estimated_runtime=1800,  # 30 minutes
                dependencies=[],
                repo_name=repo_name
            )
            tasks.append(task_review)
            
            # Task 2: Classify files
            task_classify = Task(
                id=f"{repo_name}_classify",
                description=f"Classify files in {repo_name} and identify misplaced files",
                priority=TaskPriority.HIGH,
                agent_type=AgentType.FILE_CLASSIFIER,
                estimated_runtime=1800,
                dependencies=[task_review.id],
                repo_name=repo_name
            )
            tasks.append(task_classify)
            
            # Task 3: Security scan
            task_security = Task(
                id=f"{repo_name}_security",
                description=f"Perform security scan on {repo_name}",
                priority=TaskPriority.CRITICAL,
                agent_type=AgentType.SECURITY_SENTINEL,
                estimated_runtime=1200,  # 20 minutes
                dependencies=[task_review.id],
                repo_name=repo_name
            )
            tasks.append(task_security)
            
            # Task 4: Port conflict check
            task_ports = Task(
                id=f"{repo_name}_ports",
                description=f"Check and resolve port conflicts for {repo_name}",
                priority=TaskPriority.HIGH,
                agent_type=AgentType.PORT_MANAGER,
                estimated_runtime=600,  # 10 minutes
                dependencies=[],
                repo_name=repo_name
            )
            tasks.append(task_ports)
            
            # Task 5: Optimize code
            task_optimize = Task(
                id=f"{repo_name}_optimize",
                description=f"Optimize code in {repo_name} for efficiency",
                priority=TaskPriority.MEDIUM,
                agent_type=AgentType.RUTHLESS_OPTIMIZER,
                estimated_runtime=3600,  # 1 hour
                dependencies=[task_review.id, task_security.id],
                repo_name=repo_name
            )
            tasks.append(task_optimize)
            
            # Task 6: Add documentation
            task_docs = Task(
                id=f"{repo_name}_documentation",
                description=f"Add comprehensive documentation to {repo_name}",
                priority=TaskPriority.HIGH,
                agent_type=AgentType.DOCSTRING_GURU,
                estimated_runtime=3600,  # 1 hour
                dependencies=[task_optimize.id],
                repo_name=repo_name
            )
            tasks.append(task_docs)
        
        # Register all tasks
        for task in tasks:
            self.scheduler.register_task(task)
        
        print(f"\n✓ Phase 3 Complete: Created {len(tasks)} tasks")
        return tasks
    
    def phase_4_execute(self, silent_mode: bool = False):
        """Phase 4: Execute tasks using multi-agent system"""
        print("\n" + "="*70)
        print("PHASE 4: Executing Tasks with Multi-Agent System")
        print("="*70)
        
        if not self.scheduler.tasks:
            print("⚠ No tasks available - skipping execution")
            return
        
        print(f"\nExecuting {len(self.scheduler.tasks)} tasks...")
        print("Progress will be logged to: multi_agent_system.log")
        
        # Execute tasks
        self.scheduler.execute_tasks(silent_mode=silent_mode)
        
        # Get summary
        summary = self.scheduler.get_summary()
        
        print("\n" + "="*70)
        print("Execution Summary")
        print("="*70)
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Completed: {summary['completed']}")
        print(f"Failed: {summary['failed']}")
        print(f"Pending: {summary['pending']}")
        print(f"Blocked: {summary['blocked']}")
        
        # Save execution report
        report = {
            "execution_date": datetime.now().isoformat(),
            "summary": summary,
            "completed_tasks": [
                {
                    "id": task.id,
                    "description": task.description,
                    "status": task.status.value,
                    "quality_score": task.quality_score
                }
                for task in self.scheduler.completed_tasks
            ],
            "failed_tasks": [
                {
                    "id": task.id,
                    "description": task.description,
                    "error": task.error
                }
                for task in self.scheduler.failed_tasks
            ]
        }
        
        report_path = Path("execution_report.json")
        report_path.write_text(json.dumps(report, indent=2, default=str), encoding='utf-8')
        print(f"\n✓ Execution report saved to: {report_path}")
        
        return summary
    
    def execute_full_pipeline(self, skip_scan: bool = False, silent_mode: bool = False):
        """Execute the full reorganization pipeline"""
        print("\n" + "="*70)
        print("ENTERPRISE REORGANIZATION PIPELINE")
        print("="*70)
        print(f"Priority Repositories: {', '.join(self.priority_repos)}")
        print(f"Standards File: {self.standards_path}")
        print(f"Start Time: {datetime.now().isoformat()}")
        print("="*70)
        
        # Initialize agents
        self.initialize_agents()
        
        # Phase 1: Scan
        scan_results = None
        if not skip_scan:
            scan_results = self.phase_1_scan()
        else:
            # Load existing scan results
            scan_path = Path("github_scan_results.json")
            if scan_path.exists():
                with open(scan_path, 'r', encoding='utf-8') as f:
                    scan_results = json.load(f)
                print("\n✓ Loaded existing scan results")
        
        # Phase 2: Generate plan
        plan = self.phase_2_plan(scan_results)
        
        # Phase 2.5: Comprehensive Analysis (Log all issues for later fixing)
        analysis_results = self.phase_2_5_comprehensive_analysis(scan_results)
        
        # Phase 3: Create tasks
        tasks = self.phase_3_create_tasks(plan)
        
        if not tasks:
            print("\n⚠ No tasks created - cannot proceed with execution")
            return
        
        # Phase 4: Execute
        summary = self.phase_4_execute(silent_mode=silent_mode)
        
        # Final summary
        print("\n" + "="*70)
        print("PIPELINE COMPLETE")
        print("="*70)
        print(f"End Time: {datetime.now().isoformat()}")
        print(f"Total Tasks: {summary['total_tasks']}")
        print(f"Success Rate: {(summary['completed'] / summary['total_tasks'] * 100):.1f}%")
        print("\nGenerated Files:")
        print("  - github_scan_results.json (scan results)")
        print("  - reorganization_plan.json (master plan)")
        print("  - comprehensive_issues_log.json (ALL ISSUES LOGGED - bugs, security, code quality, documentation)")
        print("  - comprehensive_issues_summary.md (human-readable summary)")
        print("  - execution_report.json (execution summary)")
        print("  - multi_agent_system.log (detailed logs)")
        print("\nNext Steps:")
        print("1. Review execution_report.json for results")
        print("2. Review multi_agent_system.log for detailed execution logs")
        print("3. Verify changes in repositories")
        print("4. Commit and push changes if satisfied")
    
    def create_summary_report(self) -> str:
        """Create a comprehensive summary report"""
        report_lines = [
            "# Enterprise Reorganization Summary Report",
            f"Generated: {datetime.now().isoformat()}",
            "",
            "## Priority Repositories",
            ""
        ]
        
        for repo in self.priority_repos:
            report_lines.append(f"- **{repo}** (Tier 1 - Highest Priority)")
        
        report_lines.extend([
            "",
            "## Multi-Agent System",
            "",
            "The reorganization uses a multi-agent system with specialized agents:",
            "",
            "1. **Skeptical Reviewer** - Critically inspects outputs for inconsistencies",
            "2. **Ruthless Optimizer** - Maximizes efficiency and enforces best practices",
            "3. **Docstring Guru** - Enforces comprehensive documentation",
            "4. **Security Sentinel** - Scans for security issues and vulnerabilities",
            "5. **Multi-Modal Expert** - Manages frontend, backend, and documentation",
            "6. **Silent Operator** - Executes tasks quietly",
            "7. **Port Manager** - Resolves port conflicts",
            "8. **File Classifier** - Classifies files for reorganization",
            "",
            "## Execution Pipeline",
            "",
            "1. **Phase 1**: Scan all GitHub repositories",
            "2. **Phase 2**: Generate master reorganization plan using Azure API",
            "3. **Phase 3**: Create tasks from plan",
            "4. **Phase 4**: Execute tasks using multi-agent system",
            "",
            "## Generated Files",
            "",
            "- `github_scan_results.json` - Complete scan of all repositories",
            "- `reorganization_plan.json` - Master reorganization plan",
            "- `execution_report.json` - Task execution summary",
            "- `multi_agent_system.log` - Detailed execution logs",
            "- `enterprise_standards.json` - Enterprise standards configuration",
            "",
            "## Standards Enforcement",
            "",
            "All repositories will be reorganized to follow enterprise standards:",
            "",
            "- **Versioning**: Semantic versioning (semver) - do not reset existing versions",
            "- **Documentation**: Comprehensive inline comments, docstrings, TODO comments",
            "- **Commit Messages**: Structured format (type(scope): subject)",
            "- **Coding Style**: Language-specific style guides (PEP 8, Airbnb, etc.)",
            "- **Port Management**: Centralized port registry to prevent conflicts",
            "- **Security**: Automated security scanning and secret detection",
            "",
            "## Special Considerations",
            "",
            "- Repos like GSMG.IO have existing versions - update, don't reset to v1.0.0",
            "- Goku.AI project files scattered across repos - need consolidation",
            "- Files with 'Shenron', 'Goku', 'Vegeta' themes belong in Goku.AI repo",
            "- Must understand every file's purpose before reorganization",
            "",
            "---",
            "",
            "For detailed execution results, see `execution_report.json` and `multi_agent_system.log`"
        ])
        
        report_path = Path("REORGANIZATION_SUMMARY.md")
        report_path.write_text("\n".join(report_lines), encoding='utf-8')
        
        print(f"\n✓ Summary report saved to: {report_path}")
        return str(report_path)


def main():
    """Main execution"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Execute enterprise reorganization using multi-agent system"
    )
    parser.add_argument(
        "--skip-scan",
        action="store_true",
        help="Skip repository scan (use existing scan results)"
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Run in silent mode (minimal output)"
    )
    parser.add_argument(
        "--scan-only",
        action="store_true",
        help="Only run the scan phase"
    )
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="Only generate the plan (requires scan results)"
    )
    parser.add_argument(
        "--analysis-only",
        action="store_true",
        help="Only run comprehensive analysis (logs bugs, security, code quality, documentation issues)"
    )
    
    args = parser.parse_args()
    
    executor = EnterpriseReorganizationExecutor()
    
    if args.scan_only:
        executor.phase_1_scan()
    elif args.plan_only:
        executor.phase_2_plan()
    elif args.analysis_only:
        # Run comprehensive analysis only
        print("="*70)
        print("COMPREHENSIVE ANALYSIS MODE")
        print("="*70)
        print("\nThis will analyze all files and log:")
        print("  - Project understanding")
        print("  - Bugs")
        print("  - Security flaws")
        print("  - Bad code practices")
        print("  - Missing documentation (all types)")
        print("\n⚠ Issues will be LOGGED, not fixed")
        print("="*70)
        
        # Load scan results
        scan_results = None
        scan_path = Path("github_scan_results.json")
        if scan_path.exists():
            with open(scan_path, 'r', encoding='utf-8') as f:
                scan_results = json.load(f)
            print(f"✓ Loaded scan results: {len(scan_results.get('repositories', []))} repositories")
        else:
            print("⚠ No scan results found - running scan first...")
            scan_results = executor.phase_1_scan()
        
        # Run comprehensive analysis
        executor.phase_2_5_comprehensive_analysis(scan_results)
    else:
        executor.execute_full_pipeline(
            skip_scan=args.skip_scan,
            silent_mode=args.silent
        )
        
        # Create summary report
        executor.create_summary_report()


if __name__ == "__main__":
    main()

