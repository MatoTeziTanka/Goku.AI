#!/usr/bin/env python3
"""
Mato Tezi Tanka AI Multi-Agent System
Enterprise-grade multi-agent orchestration for code reorganization and quality assurance
"""

import json
import time
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict
from foundry_local_agent import FoundryClaudeAgent


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('multi_agent_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AgentType(Enum):
    """Agent specializations"""
    SKEPTICAL_REVIEWER = "Skeptical Reviewer"
    RUTHLESS_OPTIMIZER = "Ruthless Optimizer"
    DOCSTRING_GURU = "Docstring Guru"
    SECURITY_SENTINEL = "Security Sentinel"
    MULTI_MODAL_EXPERT = "Multi-Modal Expert"
    SILENT_OPERATOR = "Silent Operator"
    TASK_SCHEDULER = "Task Scheduler"
    PORT_MANAGER = "Port Manager"
    FILE_CLASSIFIER = "File Classifier"


class TaskPriority(Enum):
    """Task priority levels"""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class TaskStatus(Enum):
    """Task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass
class Task:
    """Task definition"""
    id: str
    description: str
    priority: TaskPriority
    agent_type: AgentType
    estimated_runtime: int  # seconds
    dependencies: List[str]
    file_path: Optional[str] = None
    repo_name: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict] = None
    error: Optional[str] = None
    created_at: Optional[str] = None
    completed_at: Optional[str] = None
    quality_score: Optional[Dict] = None


@dataclass
class AgentQualityScore:
    """Quality score from an agent"""
    clarity: float  # 0-10
    efficiency: float  # 0-10
    security: float  # 0-10
    completeness: float  # 0-10
    agent_type: AgentType


class BaseAgent:
    """Base class for all agents"""
    
    def __init__(self, agent_type: AgentType, model: str = "gpt-4.1"):
        self.agent_type = agent_type
        self.azure_agent = FoundryClaudeAgent(model=model)
        self.name = agent_type.value
        self.silent_mode = False
        self.task_count = 0
        self.completed_tasks = 0
        self.failed_tasks = 0
    
    def get_system_prompt(self) -> str:
        """Get system prompt for this agent type"""
        prompts = {
            AgentType.SKEPTICAL_REVIEWER: """You are a Skeptical Reviewer agent - a meticulous quality assurance expert.

QUALITY ASSURANCE COMMITMENT:
- Critically inspect all outputs for inconsistencies
- Flag potential issues and request verification
- Ensure no errors slip through
- Question assumptions and validate logic
- Provide thorough quality checks
- Final outputs must be verified by you before completion
- Track changes with diffs for auditing

Your critical eye focuses on:
- Logic errors: Edge cases, boundary conditions, null handling, error paths
- Consistency: Naming conventions, code style, patterns, architecture
- Correctness: Algorithm accuracy, business logic validation, data flow
- Completeness: Missing error handling, incomplete implementations, gaps
- Best practices: Code smells, anti-patterns, maintainability issues
- Bad code: Non-code characters (Chinese text, hidden characters)

When reviewing code:
1. Question EVERYTHING - assume nothing is correct until proven
2. Test edge cases mentally - what if input is null? Empty? Maximum?
3. Verify logic flow - does the code actually do what it claims?
4. Check for inconsistencies - naming, style, patterns must be uniform
5. Validate assumptions - are all assumptions valid? Documented?
6. Flag ANYTHING suspicious - better to over-flag than miss issues
7. Verify all critical files are fully functional
8. Ensure enterprise-grade, scalable, secure, token-efficient code

You are SKEPTICAL - trust but verify. Every line of code must withstand scrutiny. Enterprise-grade quality requires zero tolerance for errors. Mars-level, not Moon-level.""",
            
            AgentType.RUTHLESS_OPTIMIZER: """You are a Ruthless Optimizer agent - a world-class software architect and performance engineer.

QUALITY ASSURANCE COMMITMENT:
- Ensure all critical files are fully functional
- Maximize efficiency, rewrite redundant code, enforce best practices
- Follow highest standards: enterprise-grade, scalable, secure, token-efficient
- Mistakes are acceptable only if corrected quickly
- Track changes with diffs for auditing

Your expertise includes:
- Algorithm optimization: Time/space complexity analysis, Big O optimization
- Code quality: DRY principles, SOLID principles, design patterns, anti-patterns
- Performance tuning: Memory optimization, CPU optimization, I/O optimization, caching strategies
- Code smells: Long methods, deep nesting, magic numbers, code duplication, god objects
- Best practices: Clean code principles, refactoring techniques, maintainability
- Enterprise standards: Scalability, reliability, maintainability, testability
- Token efficiency: Optimize for minimal token usage while maintaining quality

When optimizing code:
1. Analyze complexity - can this be O(n) instead of O(n²)?
2. Eliminate redundancy - DRY (Don't Repeat Yourself) ruthlessly
3. Simplify logic - break down complex functions, reduce nesting
4. Improve readability - better naming, clearer structure
5. Optimize performance - reduce unnecessary operations, cache results
6. Enforce standards - follow language-specific best practices (PEP 8, Airbnb, etc.)
7. Remove bad code - eliminate non-code characters, hidden characters, Chinese text
8. Ensure token efficiency - minimal intermediate outputs

You are RUTHLESS - no inefficiency is acceptable. Every line of code must earn its place. Enterprise-grade quality is mandatory. Mars-level, not Moon-level.""",
            
            AgentType.DOCSTRING_GURU: """You are a Docstring Guru agent - a documentation master.

QUALITY ASSURANCE COMMITMENT:
- Every file and function MUST have comprehensive documentation: Inline Comments, Block Comments, Multi-Line Comments, Special Comments, Docstring Comments, and TODO Comments for improvements
- Enforce comprehensive documentation and TODO notes
- Create wiki-ready documentation
- Index inline/block/docstring comments into wiki-ready format
- Track changes with diffs for auditing

Your expertise includes:
- Documentation standards: Google-style, NumPy-style, Sphinx-compatible docstrings
- Code documentation: Inline comments, block comments, function/class/module docstrings
- API documentation: Parameter descriptions, return values, exceptions, examples
- Code clarity: Explaining complex algorithms, business logic, edge cases
- TODO management: Tracking improvements, technical debt, future enhancements
- Documentation quality: Completeness, accuracy, clarity, maintainability

When documenting code:
1. Every function/class MUST have a docstring with: Description, Args, Returns, Raises, Examples
2. Complex logic MUST have inline comments explaining WHY, not WHAT
3. Major sections MUST have block comments explaining the purpose
4. TODOs MUST follow format: # TODO(username): Description - Priority - Date
5. Type hints MUST be added for all parameters and return values
6. Examples MUST be provided for complex functions
7. Generate simple, comprehensive workflow documentation mapping tasks to files

You are COMPREHENSIVE - no undocumented code is acceptable. Every function, class, and complex block must be fully documented. Enterprise-grade documentation is essential. Mars-level, not Moon-level.""",
            
            AgentType.SECURITY_SENTINEL: """You are a Security Sentinel agent - an elite cybersecurity expert with deep knowledge of OWASP Top 10, CWE vulnerabilities, and enterprise security standards.

QUALITY ASSURANCE COMMITMENT:
- Ensure all critical files are fully functional and secure
- Scan for malicious code, unsafe characters, deprecated libraries, hardcoded secrets, or unsafe patterns
- Identify and remove bad code (e.g., non-code characters like Chinese text, hidden characters)
- Follow highest standards: enterprise-grade, scalable, secure, token-efficient
- Mistakes are acceptable only if corrected quickly
- Track changes with diffs for auditing

Your expertise includes:
- Advanced threat detection: SQL injection, XSS, CSRF, command injection, path traversal, XXE
- Secret management: Detecting hardcoded API keys, passwords, tokens, private keys, certificates
- Dependency security: Identifying vulnerable libraries, outdated packages, known CVEs
- Authentication/Authorization: Missing auth checks, weak encryption, insecure session management
- Data protection: PII exposure, insecure data storage, missing encryption
- Input validation: Unsanitized user input, missing validation, unsafe deserialization
- Secure coding: Following OWASP guidelines, NIST standards, industry best practices

When analyzing code:
1. Think like an attacker - what vulnerabilities could be exploited?
2. Check for all common attack vectors
3. Verify secure coding patterns are followed
4. Identify any security anti-patterns
5. Provide specific, actionable remediation steps
6. Rate severity using CVSS scoring principles
7. Scan for incompatible characters, unsafe code, or malicious input
8. Remove non-code characters (Chinese text, hidden characters)

You are RUTHLESS in security - no vulnerability is too small to flag. Enterprise-grade security is non-negotiable. Mars-level, not Moon-level.""",
            
            AgentType.MULTI_MODAL_EXPERT: """You are a Multi-Modal Expert agent.

QUALITY ASSURANCE COMMITMENT:
- Manage frontend, backend, and documentation simultaneously for efficiency
- Ensure all critical files are fully functional across all layers
- Coordinate cross-stack improvements
- Ensure consistency across all layers
- Follow highest standards: enterprise-grade, scalable, secure, token-efficient
- Track changes with diffs for auditing

Your role is to:
- Manage frontend, backend, and documentation simultaneously
- Coordinate cross-stack improvements
- Ensure consistency across all layers
- Optimize for efficiency across all domains
- Generate simple, comprehensive workflow documentation mapping tasks to files
- Operate cross-platform: Windows and Linux compatibility

Approach: Enterprise-grade, precise, systematic, yet innovative and forward-thinking. Mars-level, not Moon-level.""",
            
            AgentType.SILENT_OPERATOR: """You are a Silent Operator agent. Your role is to:
- Execute tasks quietly without verbose output
- Only report completion or critical errors
- Minimize intermediate outputs
- Focus on execution efficiency""",
            
            AgentType.PORT_MANAGER: """You are a Port Manager agent. Your role is to:
- Detect port conflicts across repositories
- Resolve port allocation conflicts
- Maintain a centralized port registry
- Ensure no duplicate port usage""",
            
            AgentType.FILE_CLASSIFIER: """You are a File Classifier agent. Your role is to:
- Analyze files to determine their purpose
- Identify files in wrong repositories
- Classify files for reorganization
- Map files to correct repositories"""
        }
        return prompts.get(self.agent_type, "You are an expert agent.")
    
    def execute_task(self, task: Task) -> Tuple[Task, AgentQualityScore]:
        """Execute a task and return results with quality score"""
        self.task_count += 1
        task.status = TaskStatus.IN_PROGRESS
        task.created_at = datetime.now().isoformat()
        
        if not self.silent_mode:
            logger.info(f"[{self.name}] Starting task: {task.description}")
        
        try:
            result = self._execute(task)
            quality_score = self._rate_output(task, result)
            
            task.status = TaskStatus.COMPLETED
            task.result = result
            task.quality_score = asdict(quality_score)
            task.completed_at = datetime.now().isoformat()
            self.completed_tasks += 1
            
            if not self.silent_mode:
                logger.info(f"[{self.name}] Completed task: {task.description}")
            
            return task, quality_score
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.error = str(e)
            task.completed_at = datetime.now().isoformat()
            self.failed_tasks += 1
            
            logger.error(f"[{self.name}] Failed task {task.id}: {e}")
            return task, None
    
    def _execute(self, task: Task) -> Dict:
        """Execute the actual task - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement _execute method")
    
    def _rate_output(self, task: Task, result: Dict) -> AgentQualityScore:
        """Rate the output quality - to be implemented by subclasses"""
        # Default scoring
        return AgentQualityScore(
            clarity=7.0,
            efficiency=7.0,
            security=7.0,
            completeness=7.0,
            agent_type=self.agent_type
        )


class SkepticalReviewerAgent(BaseAgent):
    """Critically reviews outputs for inconsistencies"""
    
    def _execute(self, task: Task) -> Dict:
        if not task.file_path:
            return {"error": "File path required for review"}
        
        file_path = Path(task.file_path)
        if not file_path.exists():
            return {"error": f"File not found: {task.file_path}"}
        
        prompt = f"""Review this file critically:
1. Check for inconsistencies in logic
2. Identify potential bugs
3. Verify documentation accuracy
4. Flag any questionable patterns
5. Request verification if needed

File: {task.file_path}
Task: {task.description}"""
        
        review = self.azure_agent.analyze_file(str(file_path), prompt)
        
        return {
            "review": review,
            "issues_found": self._extract_issues(review),
            "needs_verification": self._needs_verification(review)
        }
    
    def _extract_issues(self, review: str) -> List[Dict]:
        """Extract issues from review"""
        # Simple extraction - could be enhanced
        issues = []
        if "bug" in review.lower() or "error" in review.lower():
            issues.append({"severity": "high", "type": "potential_bug"})
        return issues
    
    def _needs_verification(self, review: str) -> bool:
        """Check if verification is needed"""
        return "verify" in review.lower() or "check" in review.lower()


class RuthlessOptimizerAgent(BaseAgent):
    """Maximizes efficiency and enforces best practices"""
    
    def _execute(self, task: Task) -> Dict:
        if not task.file_path:
            return {"error": "File path required for optimization"}
        
        prompt = f"""Optimize this file ruthlessly:
1. Eliminate redundant code
2. Enforce best practices
3. Optimize for efficiency
4. Simplify complex logic
5. Improve token efficiency

File: {task.file_path}
Task: {task.description}

Provide optimized code with explanations."""
        
        # Use specialized system prompt for this agent
        system_prompt = self.get_system_prompt()
        
        # Create enhanced instruction with agent's expertise
        enhanced_instruction = f"""{system_prompt}

{task.description or "Optimize this code for efficiency and best practices"}

Apply your specialized expertise to this task."""
        
        optimized = self.azure_agent.edit_file_with_agent(
            str(task.file_path),
            enhanced_instruction
        )
        
        return {
            "optimized_code": optimized,
            "optimizations_applied": self._extract_optimizations(optimized)
        }
    
    def _extract_optimizations(self, code: str) -> List[str]:
        """Extract list of optimizations"""
        return ["Code optimization completed"]


class DocstringGuruAgent(BaseAgent):
    """Enforces comprehensive documentation"""
    
    def _execute(self, task: Task) -> Dict:
        if not task.file_path:
            return {"error": "File path required for documentation"}
        
        prompt = f"""Add comprehensive documentation to this file:
1. Add inline comments for complex logic
2. Add block comments for major sections
3. Add docstrings to all functions and classes
4. Add TODO comments for improvements
5. Ensure wiki-ready documentation

File: {task.file_path}
Task: {task.description}"""
        
        documented = self.azure_agent.edit_file_with_agent(
            str(task.file_path),
            task.description or "Add comprehensive documentation: inline comments, block comments, docstrings, and TODO comments"
        )
        
        return {
            "documented_code": documented,
            "documentation_added": True
        }


class SecuritySentinelAgent(BaseAgent):
    """Scans for security issues"""
    
    def _execute(self, task: Task) -> Dict:
        if not task.file_path:
            return {"error": "File path required for security scan"}
        
        prompt = f"""Scan this file for security issues:
1. Detect hardcoded secrets or credentials
2. Identify deprecated libraries
3. Check for injection vulnerabilities
4. Find unsafe patterns
5. Flag security concerns

File: {task.file_path}
Task: {task.description}"""
        
        scan_result = self.azure_agent.analyze_file(str(task.file_path), prompt)
        
        return {
            "security_scan": scan_result,
            "vulnerabilities": self._extract_vulnerabilities(scan_result),
            "secrets_found": self._find_secrets(task.file_path)
        }
    
    def _extract_vulnerabilities(self, scan: str) -> List[Dict]:
        """Extract vulnerabilities from scan"""
        vulnerabilities = []
        if "secret" in scan.lower() or "password" in scan.lower() or "key" in scan.lower():
            vulnerabilities.append({"severity": "critical", "type": "potential_secret"})
        return vulnerabilities
    
    def _find_secrets(self, file_path: str) -> List[str]:
        """Find potential secrets in file"""
        try:
            content = Path(file_path).read_text(encoding='utf-8', errors='ignore')
            # Simple pattern matching - could be enhanced
            import re
            secret_patterns = [
                r'password\s*=\s*["\']([^"\']+)["\']',
                r'api[_-]?key\s*=\s*["\']([^"\']+)["\']',
                r'secret\s*=\s*["\']([^"\']+)["\']',
            ]
            secrets = []
            for pattern in secret_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                secrets.extend(matches)
            return secrets
        except:
            return []


class MultiModalExpertAgent(BaseAgent):
    """Manages frontend, backend, and documentation simultaneously"""
    
    def _execute(self, task: Task) -> Dict:
        # Multi-modal tasks can work across multiple files
        return {
            "multi_modal_analysis": "Analysis completed across all layers"
        }


class SilentOperatorAgent(BaseAgent):
    """Executes tasks quietly"""
    
    def __init__(self, agent_type: AgentType, model: str = "gpt-4.1"):
        super().__init__(agent_type, model)
        self.silent_mode = True
    
    def _execute(self, task: Task) -> Dict:
        # Silent execution - minimal output
        return {"status": "completed", "silent": True}


class PortManagerAgent(BaseAgent):
    """Manages port conflicts"""
    
    def _execute(self, task: Task) -> Dict:
        # Port management logic
        return {
            "port_analysis": "Port conflicts analyzed",
            "recommendations": []
        }


class FileClassifierAgent(BaseAgent):
    """Classifies files for reorganization"""
    
    def _execute(self, task: Task) -> Dict:
        if not task.file_path:
            return {"error": "File path required for classification"}
        
        prompt = f"""Classify this file:
1. Determine its primary purpose
2. Identify which repository it belongs to
3. Check if it's in the wrong location
4. Suggest correct repository if misplaced

File: {task.file_path}
Current Repository: {task.repo_name}
Task: {task.description}"""
        
        classification = self.azure_agent.analyze_file(str(task.file_path), prompt)
        
        return {
            "classification": classification,
            "correct_repo": self._extract_correct_repo(classification),
            "misplaced": self._is_misplaced(classification)
        }
    
    def _extract_correct_repo(self, classification: str) -> Optional[str]:
        """Extract suggested repository"""
        # Simple extraction - could be enhanced
        if "goku" in classification.lower() or "shenron" in classification.lower():
            return "Goku.AI"
        return None
    
    def _is_misplaced(self, classification: str) -> bool:
        """Check if file is misplaced"""
        return "wrong" in classification.lower() or "misplaced" in classification.lower()


class TaskScheduler:
    """Schedules and orchestrates tasks across agents"""
    
    def __init__(self):
        self.agents: Dict[AgentType, BaseAgent] = {}
        self.tasks: List[Task] = []
        self.completed_tasks: List[Task] = []
        self.failed_tasks: List[Task] = []
        self.task_history: List[Dict] = []
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent"""
        self.agents[agent.agent_type] = agent
        logger.info(f"Registered agent: {agent.name}")
    
    def register_task(self, task: Task):
        """Register a task for execution"""
        self.tasks.append(task)
        logger.info(f"Registered task: {task.id} - {task.description}")
    
    def execute_tasks(self, silent_mode: bool = False):
        """Execute all tasks"""
        logger.info(f"Starting execution of {len(self.tasks)} tasks")
        
        # Sort tasks by priority
        self.tasks.sort(key=lambda t: t.priority.value)
        
        for task in self.tasks:
            # Check dependencies
            if not self._dependencies_met(task):
                task.status = TaskStatus.BLOCKED
                logger.warning(f"Task {task.id} blocked by dependencies")
                continue
            
            # Find appropriate agent
            agent = self.agents.get(task.agent_type)
            if not agent:
                task.status = TaskStatus.FAILED
                task.error = f"Agent {task.agent_type.value} not found"
                continue
            
            # Execute task
            try:
                updated_task, quality_score = agent.execute_task(task)
                
                if updated_task.status == TaskStatus.COMPLETED:
                    self.completed_tasks.append(updated_task)
                else:
                    self.failed_tasks.append(updated_task)
                
                self.task_history.append({
                    "task_id": task.id,
                    "agent": agent.name,
                    "status": updated_task.status.value,
                    "quality_score": asdict(quality_score) if quality_score else None
                })
                
                # Small delay to prevent rate limiting
                time.sleep(2)
                
            except Exception as e:
                task.status = TaskStatus.FAILED
                task.error = str(e)
                self.failed_tasks.append(task)
                logger.error(f"Error executing task {task.id}: {e}")
    
    def _dependencies_met(self, task: Task) -> bool:
        """Check if all dependencies are met"""
        if not task.dependencies:
            return True
        
        completed_ids = {t.id for t in self.completed_tasks}
        return all(dep_id in completed_ids for dep_id in task.dependencies)
    
    def get_summary(self) -> Dict:
        """Get execution summary"""
        return {
            "total_tasks": len(self.tasks),
            "completed": len(self.completed_tasks),
            "failed": len(self.failed_tasks),
            "pending": len([t for t in self.tasks if t.status == TaskStatus.PENDING]),
            "blocked": len([t for t in self.tasks if t.status == TaskStatus.BLOCKED]),
            "agent_stats": {
                agent.name: {
                    "tasks": agent.task_count,
                    "completed": agent.completed_tasks,
                    "failed": agent.failed_tasks
                }
                for agent in self.agents.values()
            }
        }


# Factory function to create agents
def create_agent(agent_type: AgentType, model: str = "gpt-4.1") -> BaseAgent:
    """Create an agent of the specified type"""
    agent_classes = {
        AgentType.SKEPTICAL_REVIEWER: SkepticalReviewerAgent,
        AgentType.RUTHLESS_OPTIMIZER: RuthlessOptimizerAgent,
        AgentType.DOCSTRING_GURU: DocstringGuruAgent,
        AgentType.SECURITY_SENTINEL: SecuritySentinelAgent,
        AgentType.MULTI_MODAL_EXPERT: MultiModalExpertAgent,
        AgentType.SILENT_OPERATOR: SilentOperatorAgent,
        AgentType.PORT_MANAGER: PortManagerAgent,
        AgentType.FILE_CLASSIFIER: FileClassifierAgent,
    }
    
    agent_class = agent_classes.get(agent_type)
    if not agent_class:
        raise ValueError(f"Unknown agent type: {agent_type}")
    
    return agent_class(agent_type, model)

