# Enterprise Reorganization Multi-Agent System

**Mato Tezi Tanka AI Multi-Agent System** - Enterprise-grade code reorganization and quality assurance

## Overview

This multi-agent system scans, analyzes, and reorganizes all repositories in your GitHub account (`MatoTeziTanka`) to enterprise-level standards using specialized AI agents powered by Azure GPT-4.1.

## Features

### Multi-Agent System

The system uses specialized agents for different tasks:

1. **Skeptical Reviewer** - Critically inspects outputs, flags inconsistencies, requests verification
2. **Ruthless Optimizer** - Maximizes efficiency, rewrites redundant code, enforces best practices
3. **Docstring Guru** - Enforces comprehensive documentation (inline comments, docstrings, TODOs)
4. **Security Sentinel** - Scans for malicious code, unsafe patterns, hardcoded secrets
5. **Multi-Modal Expert** - Manages frontend, backend, and documentation simultaneously
6. **Silent Operator** - Executes tasks quietly, only reports completion or critical errors
7. **Port Manager** - Detects and resolves port conflicts across repositories
8. **File Classifier** - Classifies files and identifies misplaced files across repositories

### Enterprise Standards

All repositories are reorganized to follow strict enterprise standards:

- **Versioning**: Semantic versioning (semver) - existing versions are preserved, not reset
- **Documentation**: Comprehensive inline comments, block comments, docstrings, TODO comments
- **Commit Messages**: Structured format (`type(scope): subject`)
- **Coding Style**: Language-specific style guides (PEP 8, Airbnb, etc.)
- **Port Management**: Centralized port registry to prevent conflicts
- **Security**: Automated security scanning and secret detection

### Priority Repositories

The system prioritizes these repositories (Tier 1):

1. **BitPhoenix** - Enterprise data recovery platform
2. **Goku.AI** - Local AI agent project (consolidating scattered files)
3. **ScalpStorm** - Scalping automation platform
4. **DinoCloud** - Cloud infrastructure management
5. **GSMG.IO** - Existing version - update, don't reset to v1.0.0

## Installation

### Prerequisites

1. **Python 3.8+**
2. **Azure CLI** (for authentication) or **Azure API Key**
3. **GitHub CLI** (optional, for repository scanning)

### Setup

1. **Install Python dependencies:**
   ```bash
   pip install requests azure-identity pathlib
   ```

2. **Configure Azure API:**
   - Ensure `foundry_config.json` is configured with your Azure endpoint and API key
   - Or use Azure CLI authentication (`az login`)

3. **Verify configuration:**
   ```bash
   python -c "from foundry_local_agent import FoundryClaudeAgent; agent = FoundryClaudeAgent(); print('✓ Configuration OK')"
   ```

## Usage

### Quick Start

Run the full reorganization pipeline:

```bash
python execute_enterprise_reorganization.py
```

This will:
1. Scan all repositories in your GitHub account
2. Generate a master reorganization plan using Azure API
3. Create tasks from the plan
4. Execute tasks using the multi-agent system

### Step-by-Step Execution

#### 1. Scan Repositories Only

```bash
python execute_enterprise_reorganization.py --scan-only
```

This creates `github_scan_results.json` with a complete inventory of all repositories.

#### 2. Generate Plan Only

```bash
python execute_enterprise_reorganization.py --plan-only
```

This creates `reorganization_plan.json` with the master reorganization plan.

#### 3. Skip Scan (Use Existing Results)

```bash
python execute_enterprise_reorganization.py --skip-scan
```

This uses existing scan results instead of re-scanning.

#### 4. Silent Mode

```bash
python execute_enterprise_reorganization.py --silent
```

This runs in silent mode with minimal output (progress logged to file).

### Manual Component Usage

#### Scan GitHub Account

```bash
python scan_github_account.py
```

Scans all repositories and saves results to `github_scan_results.json`.

#### Generate Reorganization Plan

```bash
python generate_reorganization_plan.py
```

Generates a master reorganization plan using Azure API analysis.

#### Use Multi-Agent System

```python
from multi_agent_system import TaskScheduler, Task, TaskPriority, AgentType, create_agent

# Create scheduler
scheduler = TaskScheduler()

# Register agents
scheduler.register_agent(create_agent(AgentType.SKEPTICAL_REVIEWER))
scheduler.register_agent(create_agent(AgentType.DOCSTRING_GURU))

# Create task
task = Task(
    id="task_1",
    description="Add documentation to file",
    priority=TaskPriority.HIGH,
    agent_type=AgentType.DOCSTRING_GURU,
    estimated_runtime=1800,
    dependencies=[],
    file_path="path/to/file.py"
)

# Register and execute
scheduler.register_task(task)
scheduler.execute_tasks()
```

## Output Files

After execution, the following files are generated:

1. **`github_scan_results.json`** - Complete scan of all repositories
   - Repository structure
   - File inventory
   - Port configurations
   - Version information

2. **`reorganization_plan.json`** - Master reorganization plan
   - Repository hierarchy
   - Versioning standards
   - Documentation standards
   - Port registry
   - File reorganization plan
   - Execution plan

3. **`execution_report.json`** - Task execution summary
   - Completed tasks
   - Failed tasks
   - Quality scores
   - Execution statistics

4. **`multi_agent_system.log`** - Detailed execution logs
   - Task execution details
   - Agent actions
   - Errors and warnings

5. **`enterprise_standards.json`** - Enterprise standards configuration
   - Versioning rules
   - Documentation requirements
   - Commit message format
   - Coding style standards
   - Port registry

6. **`REORGANIZATION_SUMMARY.md`** - Human-readable summary report

## Special Considerations

### Version Handling

- **Existing Versions**: Repos like GSMG.IO have existing versions - the system will **update** to a new version, not reset to v1.0.0
- **New Repos**: New repositories will start at v1.0.0 following semver

### File Classification

The system identifies misplaced files:

- **Goku.AI Files**: Files with "Shenron", "Goku", "Vegeta", "Dragonball" themes are consolidated into the Goku.AI repository
- **BitPhoenix Files**: Data recovery related files stay in BitPhoenix
- **Misplaced Files**: Files in "Doesnt Belong" directories are properly classified

### Port Conflicts

- The system maintains a centralized port registry
- Detects conflicts automatically
- Resolves conflicts by assigning unique ports
- Default port assignments:
  - BitPhoenix: 8000
  - Goku.AI: 8001
  - ScalpStorm: 8002
  - DinoCloud: 8003
  - GSMG.IO: 8004

## Agent Collaboration Protocol

- Agents can collaborate or cross-validate outputs
- Disagreements are resolved by weighted voting based on agent specialization
- Final outputs are verified by Skeptical Reviewer and Security Sentinel before completion

## Task Execution Flow

1. **Task Registration** - Tasks are registered with description, priority, and required agent type
2. **Agent Assignment** - Scheduler assigns optimal agents based on specialization and load
3. **Execution** - Agents execute tasks in silent mode (progress logged locally)
4. **Quality Scoring** - Each agent rates outputs on clarity, efficiency, security, and completeness
5. **Completion** - Final output collation with results, logs, and quality metrics

## Security Features

- **Secret Detection**: Automatically detects hardcoded API keys, passwords, secrets
- **Vulnerability Scanning**: Identifies deprecated libraries and security vulnerabilities
- **Injection Detection**: Scans for code injection patterns
- **Dependency Checking**: Checks for vulnerable dependencies

## Network Configuration

The system understands:

- **Reverse Proxy VM**: Reverse proxy setup and configuration
- **Port Requirements**: Network port allocation and management
- **VM Configuration**: VM100 (Windows 2025) for local AI agent (Goku.AI)

## Troubleshooting

### Azure Authentication Issues

If you get authentication errors:

1. **Check Azure CLI:**
   ```bash
   az login
   az account show
   ```

2. **Or use API Key:**
   - Update `foundry_config.json` with your API key
   - Set `auth_method` to `"api_key"`

### Rate Limiting

If you hit Azure API rate limits:

- The system implements exponential backoff and retry logic
- Tasks are executed with delays between requests
- Consider running in batches if needed

### Missing Repositories

If repositories are not found:

- Ensure GitHub CLI is installed: `gh auth login`
- Or manually add repositories to the scan

## Next Steps

After execution:

1. **Review Results:**
   - Check `execution_report.json` for task completion status
   - Review `multi_agent_system.log` for detailed execution logs

2. **Verify Changes:**
   - Review changes in each repository
   - Test functionality of modified files

3. **Commit Changes:**
   - Stage changes: `git add .`
   - Commit with structured message: `git commit -m "feat(reorganization): Enterprise standards enforcement"`
   - Push to GitHub: `git push`

4. **Iterate:**
   - Run the system again if needed
   - Update `enterprise_standards.json` for custom requirements
   - Adjust priorities in `execute_enterprise_reorganization.py`

## Enterprise Standards

All repositories follow these standards:

- **Versioning**: Semantic versioning (MAJOR.MINOR.PATCH)
- **Documentation**: Comprehensive (inline comments, docstrings, TODOs)
- **Commit Messages**: Structured format (`type(scope): subject`)
- **Coding Style**: Language-specific (PEP 8, Airbnb, etc.)
- **Port Management**: Centralized registry
- **Security**: Automated scanning

See `enterprise_standards.json` for detailed configuration.

## Support

For issues or questions:

1. Check execution logs: `multi_agent_system.log`
2. Review generated reports: `execution_report.json`
3. Verify Azure configuration: `foundry_config.json`

---

**Note**: This system is designed to be **enterprise-grade** and follows the **"Mars-level, not Moon-level"** approach - precise, systematic, yet innovative and forward-thinking.






