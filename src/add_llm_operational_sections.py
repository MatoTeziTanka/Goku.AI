#!/usr/bin/env python3
"""
Add LLM Operational Requirements Sections (19-22)
Adapted for Local VM with LM Studio, SSD/HDD storage
"""

import re
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(r"C:\Users\sethp\Documents\Github")
INPUT_FILE = BASE_DIR / "MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED.md"
OUTPUT_FILE = BASE_DIR / "MASTER-PROMPT-PERPETUAL-SELF-UPDATING-AI-MIND-IMPROVED.md"

# Storage paths for local VM
SSD_STORAGE = Path(r"C:\AI_Storage\SSD")  # Fast access storage
HDD_STORAGE = Path(r"D:\AI_Storage\HDD")  # Long-term storage
KNOWLEDGE_DB = SSD_STORAGE / "knowledge_base"
CHECKPOINTS = SSD_STORAGE / "checkpoints"
SESSION_LOGS = SSD_STORAGE / "session_logs"
MEMORY_STASH = HDD_STORAGE / "memory_stash"


def add_llm_sections(content: str) -> str:
    """Add Sections 19-22 for LLM operational requirements"""
    
    # Use regular string (not f-string) to avoid evaluating f-strings in code examples
    # We'll replace storage path placeholders manually
    sections = r'''

---

## 19. LLM OPERATIONAL REQUIREMENTS (LOCAL VM / LM STUDIO)

> **Context:** This framework operates on a local VM using LM Studio with Dell R730 server infrastructure. SSD and HDD storage are available for persistent state, knowledge databases, and memory stashing.

### 19.1 Context Window Management (Local Model)

**Local Model Advantages:**
- **Extended Context:** Local models can support larger context windows (100K-200K+ tokens)
- **No API Limits:** No rate limiting or token costs
- **Persistent Sessions:** Can maintain longer conversation contexts

**Token Budget Strategy:**

```python
class LocalModelContextManager:
    """
    Manages context window for local LM Studio model.
    
    Optimized for local VM with SSD/HDD storage for persistence.
    """
    
    def __init__(self, max_tokens: int = 200000):
        self.max_tokens = max_tokens
        self.reserved_tokens = int(max_tokens * 0.15)  # 15% for framework (local models have more headroom)
        self.available_tokens = max_tokens - self.reserved_tokens
        self.knowledge_db_path = KNOWLEDGE_DB
        self.memory_stash_path = MEMORY_STASH
        
    def prioritize_context(self, conversation_history: List[dict]) -> List[dict]:
        """
        Prioritize and trim context, using SSD/HDD storage for overflow.
        
        Priorities (highest to lowest):
        1. Current user request
        2. Core framework principles (Sections 1, 13)
        3. Active task context (current repository, files being modified)
        4. Recent conversation history (last 10 turns - local models can handle more)
        5. Historical learnings from knowledge database
        6. General conversation history (stash to HDD if needed)
        """
        # Implementation: Use SSD for active context, HDD for archival
        pass
```

**Context Preservation with Local Storage:**

- **SSD Storage:** Active context, recent sessions, current knowledge base
- **HDD Storage:** Long-term memory stash, archived conversations, historical patterns
- **Compression Strategy:** Summarize conversations >50% context window, store full version to HDD
- **Framework Core:** Sections 1, 13 must always remain in context (pinned)

### 19.2 Persistent State Management (Local VM)

**LLM Has No Native Memory, BUT We Have Persistent Storage:**

**State Persistence Strategy:**

```python
class PersistentStateManager:
    """
    Manages persistent state across sessions using SSD/HDD storage.
    """
    
    def __init__(self):
        self.ssd_path = SSD_STORAGE
        self.hdd_path = HDD_STORAGE
        self.knowledge_db = KNOWLEDGE_DB
        self.checkpoints = CHECKPOINTS
        self.session_logs = SESSION_LOGS
        self.memory_stash = MEMORY_STASH
        
        # Initialize storage directories
        for path in [self.ssd_path, self.hdd_path, self.knowledge_db, 
                     self.checkpoints, self.session_logs, self.memory_stash]:
            path.mkdir(parents=True, exist_ok=True)
    
    def save_session_state(self, session_id: str, state: dict):
        """
        Save session state to SSD for fast retrieval.
        
        Args:
            session_id: Unique session identifier
            state: Session state dictionary
        """
        state_file = self.session_logs / "session_{{session_id}}.json"
        json.dump(state, state_file.open('w'), indent=2)
        
    def load_session_state(self, session_id: str) -> Optional[dict]:
        """Load session state from SSD."""
        state_file = self.session_logs / "session_{{session_id}}.json"
        if state_file.exists():
            return json.load(state_file.open('r'))
        return None
    
    def stash_to_hdd(self, data: dict, category: str):
        """
        Archive data to HDD for long-term storage.
        
        Args:
            data: Data to archive
            category: Category (conversations, learnings, patterns)
        """
        archive_path = self.memory_stash / category / "{{datetime.now().strftime('%Y%m%d')}}.json"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        json.dump(data, archive_path.open('w'), indent=2)
```

**Required Persistent Files:**

1. **Knowledge Base (SSD):** `{KNOWLEDGE_DB}/ai_learning_log.md`
2. **Session Logs (SSD):** `{SESSION_LOGS}/session_[id].json`
3. **Checkpoints (SSD):** `{CHECKPOINTS}/task_[id].json`
4. **Memory Stash (HDD):** `{MEMORY_STASH}/conversations/[date].json`
5. **Collaboration Logs (SSD):** `{SSD_STORAGE}/collaboration_logs/`

### 19.3 State Reconstruction Protocol (Local VM)

**At Start of Every Session:**

```python
def reconstruct_session_context(repo_path: Path, session_id: str) -> dict:
    """
    Reconstruct working context from persistent storage (SSD/HDD).
    
    Args:
        repo_path: Current repository path
        session_id: Session identifier
        
    Returns:
        Dictionary with current state, recent changes, open issues
    """
    state_mgr = PersistentStateManager()
    
    # Load from SSD (fast access)
    recent_logs = load_recent_logs_from_ssd(hours=24)
    last_session = state_mgr.load_session_state(session_id)
    current_checkpoints = load_checkpoints_from_ssd()
    
    # Load from knowledge database
    knowledge_base = load_knowledge_base_from_ssd()
    
    # Load from HDD if needed (archived data)
    archived_context = load_archived_context_from_hdd(days=7)
    
    context = {{
        "recent_logs": recent_logs,
        "open_issues": fetch_open_github_issues(),  # Still use GitHub API
        "last_session_summary": last_session,
        "current_repo_state": analyze_repo_state(repo_path),
        "pending_todos": extract_todos_from_logs(),
        "knowledge_base": knowledge_base,
        "checkpoints": current_checkpoints,
        "archived_context": archived_context,
        "storage_paths": {{
            "ssd": str(SSD_STORAGE),
            "hdd": str(HDD_STORAGE),
            "knowledge_db": str(KNOWLEDGE_DB),
            "checkpoints": str(CHECKPOINTS)
        }}
    }}
    return context
```

### 19.4 Tool Calling & Function Execution (Local VM)

**Local Execution Advantages:**
- **No API Rate Limits:** Execute tools without throttling
- **Direct File System Access:** Full access to local storage
- **Parallel Execution:** Can run multiple tools simultaneously

**Tool Invocation Standards:**

```python
def invoke_security_tool_local(tool_name: str, repo_path: Path, retry_count: int = 3) -> dict:
    """
    Invoke security scanning tool with retry logic (local execution).
    
    Args:
        tool_name: Name of tool (detect-secrets, bandit, etc.)
        repo_path: Repository to scan
        retry_count: Maximum retry attempts
        
    Returns:
        Tool output or error details
    """
    for attempt in range(retry_count):
        try:
            # Local execution - no API limits
            result = subprocess.run(
                [tool_name, str(repo_path)],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout for local
            )
            
            # Log to SSD for fast access
            log_file = SESSION_LOGS / "tool_{{tool_name}}_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.log"
            log_file.write_text(result.stdout)
            
            logger.log(
                who="invoke_security_tool_local[{{tool_name}}]",
                what="scan",
                where=str(repo_path),
                why="Security: Automated tool invocation (local)",
                status="SUCCESS",
                output_file=str(log_file)
            )
            return result
            
        except Exception as e:
            if attempt == retry_count - 1:
                logger.log(
                    who="invoke_security_tool_local[{{tool_name}}]",
                    what="scan",
                    where=str(repo_path),
                    why="Security: Tool invocation failed after retries",
                    status="FAILURE",
                    error=str(e)
                )
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
```

### 19.5 Storage Optimization Strategy

**SSD Usage (Fast Access):**
- Active session logs
- Current knowledge base
- Recent checkpoints
- Frequently accessed files

**HDD Usage (Long-term Storage):**
- Archived conversations
- Historical learning patterns
- Long-term memory stash
- Backup copies

**Storage Management:**

```python
def optimize_storage():
    """
    Optimize storage usage by moving old data from SSD to HDD.
    """
    # Move sessions older than 7 days to HDD
    for session_file in SESSION_LOGS.glob("session_*.json"):
        if (datetime.now() - datetime.fromtimestamp(session_file.stat().st_mtime)).days > 7:
            # Move to HDD archive
            hdd_archive = MEMORY_STASH / "sessions" / session_file.name
            hdd_archive.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(session_file), str(hdd_archive))
```

---

## 20. EFFECTIVE PROMPTING FOR THIS FRAMEWORK

### 20.1 Prompt Structure Template

**For Maximum Effectiveness, Structure All Requests As:**

```
CONTEXT: [Brief description of current state]
GOAL: [What you want to achieve]
CONSTRAINTS: [Any limitations or requirements]
FRAMEWORK REFERENCE: [Relevant sections: e.g., "Apply Section 3.2 Security Requirements"]
STORAGE: [SSD/HDD paths if relevant]
SUCCESS CRITERIA: [How to know when done]
```

**Example (Local VM Context):**

```
CONTEXT: Working on BitPhoenix repository, need to add secret scanning. 
         Previous session state loaded from SSD: {SESSION_LOGS}/session_abc123.json
GOAL: Implement pre-commit hook for detect-secrets
CONSTRAINTS: Must follow Section 15.1 security requirements, Section 18 issue workflow
FRAMEWORK REFERENCE: Sections 3.2, 15.1, 15.3, 18.0
STORAGE: Use SSD for active logs, HDD for archival
SUCCESS CRITERIA: 
- Pre-commit hook installed and configured
- Test run passes
- GitHub issue created and closed
- All logs saved to {SESSION_LOGS}
- Knowledge base updated in {KNOWLEDGE_DB}
```

### 20.2 Multi-Step Task Prompting

**For Complex Tasks (Leverage Local Storage for Checkpoints):**

```
Task: Improve documentation for FamilyFork repository

Step 1: Analyze current documentation state (Section 16.2.2)
        → Save checkpoint to {CHECKPOINTS}/doc_analysis.json
        
Step 2: Create GitHub issue for improvements (Section 18.0)
        → Update checkpoint
        
Step 3: Generate comprehensive docstrings (Section 2.2)
        → Save progress to checkpoint
        
Step 4: Update README and technical docs (Section 16.2.2)
        → Final checkpoint
        
Step 5: Verify and close issue (Section 18.0)
        → Archive session to HDD

Please complete Step 1 and save checkpoint before proceeding.
```

### 20.3 Framework Section Quick Reference

**When to reference which sections:**

- Creating/modifying code → Sections 2, 3, 11
- Security scanning → Sections 3.2, 15
- Testing → Section 3.6
- Documentation → Sections 2.2, 8, 16.2.2
- GitHub workflow → Section 18
- Logging → Section 14
- Agent collaboration → Section 4
- Quality scoring → Section 9
- **Local storage operations → Section 19**
- **State persistence → Section 19.2**

---

## 21. FILE SYSTEM INTERACTION REQUIREMENTS (LOCAL VM)

### 21.1 Repository Discovery & Access

**Local VM Advantages:**
- Direct file system access
- No network latency
- Can process multiple repositories in parallel

**Before Any File Operations:**

```python
def discover_repositories_local(base_path: Path) -> List[Path]:
    """
    Discover all repositories in workspace (local VM).
    
    Returns:
        List of repository paths with validation
    """
    repos = []
    for item in base_path.iterdir():
        if item.is_dir() and (item / ".git").exists():
            # Validate access (local VM has full access)
            if not os.access(item, os.R_OK | os.W_OK):
                logger.log(
                    who="discover_repositories_local",
                    what="access_check",
                    where=str(item),
                    why="Validation: Check repository access",
                    status="WARNING",
                    issue="Insufficient permissions (unusual on local VM)"
                )
                continue
            repos.append(item)
    
    # Log discovery to SSD
    discovery_log = SESSION_LOGS / "repo_discovery_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.json"
    discovery_log.write_text(json.dumps([str(r) for r in repos], indent=2))
    
    return repos
```

### 21.2 Safe File Reading (Local VM)

**Always:**
- Check file exists before reading
- Handle encoding errors (UTF-8, fallback to latin-1)
- Validate file size before loading into memory
- Log all file reads to SSD
- Use HDD for large file archival

```python
def safe_read_file_local(file_path: Path, max_size_mb: int = 50) -> Optional[str]:
    """
    Safely read file with validation (local VM - larger size limits).
    
    Args:
        file_path: Path to file
        max_size_mb: Maximum file size to read into memory (50MB for local)
        
    Returns:
        File contents or None if error
    """
    if not file_path.exists():
        logger.log(
            who="safe_read_file_local",
            what="read",
            where=str(file_path),
            why="File operation: Read attempt on non-existent file",
            status="FAILURE"
        )
        return None
        
    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > max_size_mb:
        # For very large files, use chunked reading or move to HDD processing
        logger.log(
            who="safe_read_file_local",
            what="read",
            where=str(file_path),
            why="File operation: File too large ({{size_mb:.2f}}MB > {{max_size_mb}}MB), using chunked processing",
            status="INFO"
        )
        return read_file_in_chunks(file_path)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Log read operation to SSD
        read_log = SESSION_LOGS / "file_read_{{file_path.name}}_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.log"
        read_log.write_text("Read: {{file_path}}\\nSize: {{size_mb:.2f}}MB\\nTimestamp: {{datetime.now()}}")
        
        return content
    except UnicodeDecodeError:
        # Fallback encoding
        with open(file_path, 'r', encoding='latin-1') as f:
            return f.read()
```

### 21.3 File Modification Protocol (Local VM)

**Before ANY file modification:**

1. Create backup to HDD (long-term storage)
2. Create GitHub issue if none exists (Section 18.0)
3. Run pre-change security scan (Section 15.1)
4. Log intent with WHO/WHAT/WHERE/WHEN/WHY to SSD (Section 14)
5. Make modification
6. Verify modification
7. Run post-change security scan (Section 15.2)
8. Update GitHub issue
9. Log completion to SSD
10. Archive session summary to HDD

```python
def safe_modify_file_local(file_path: Path, new_content: str):
    """
    Safely modify file with full backup and logging (local VM).
    """
    # 1. Backup to HDD
    backup_path = MEMORY_STASH / "backups" / file_path.name / "backup_{{datetime.now().strftime('%Y%m%d_%H%M%S')}}.bak"
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(file_path, backup_path)
    
    # 2. Log intent to SSD
    logger.log(
        who="safe_modify_file_local",
        what="modify",
        where=str(file_path),
        why="File operation: Safe modification with backup",
        status="IN_PROGRESS",
        backup_path=str(backup_path)
    )
    
    # 3. Make modification
    file_path.write_text(new_content, encoding='utf-8')
    
    # 4. Verify
    if file_path.read_text(encoding='utf-8') == new_content:
        logger.log(
            who="safe_modify_file_local",
            what="modify",
            where=str(file_path),
            why="File operation: Modification verified",
            status="SUCCESS"
        )
    else:
        # Restore from backup
        shutil.copy2(backup_path, file_path)
        logger.log(
            who="safe_modify_file_local",
            what="modify",
            where=str(file_path),
            why="File operation: Verification failed, restored from backup",
            status="FAILURE"
        )
```

---

## 22. INCREMENTAL EXECUTION REQUIREMENTS (LOCAL VM)

### 22.1 Task Decomposition with Local Storage

**For Tasks Requiring >30 Minutes:**

1. Break into 5-10 minute subtasks
2. Create checkpoint after each subtask (save to SSD)
3. Save state to persistent storage (SSD for active, HDD for archival)
4. Allow resume from checkpoint (load from SSD)

**Example: Processing 11 Repositories (Local VM)**

```python
def process_repositories_incrementally_local(repos: List[Path], checkpoint_file: Path):
    """
    Process repositories with checkpointing (local VM with SSD/HDD storage).
    
    Args:
        repos: List of repositories
        checkpoint_file: File to store progress (on SSD for fast access)
    """
    # Load checkpoint from SSD
    completed = load_checkpoint(checkpoint_file) if checkpoint_file.exists() else set()
    
    for repo in repos:
        if repo.name in completed:
            logger.log(
                who="process_repositories_incrementally_local",
                what="skip",
                where=str(repo),
                why="Checkpoint: Repository already processed",
                status="INFO"
            )
            continue
            
        # Process repository
        try:
            process_single_repository(repo)
            
            # Update checkpoint on SSD (fast)
            completed.add(repo.name)
            save_checkpoint(checkpoint_file, completed)
            
            # Archive progress to HDD periodically
            if len(completed) % 5 == 0:
                archive_checkpoint_to_hdd(checkpoint_file)
            
            logger.log(
                who="process_repositories_incrementally_local",
                what="process",
                where=str(repo),
                why="Incremental execution: Repository processed",
                status="SUCCESS",
                checkpoint_saved=True,
                checkpoint_location=str(checkpoint_file)
            )
        except Exception as e:
            logger.log(
                who="process_repositories_incrementally_local",
                what="process",
                where=str(repo),
                why="Incremental execution: Repository processing failed",
                status="FAILURE",
                error=str(e),
                checkpoint_saved=True
            )
            continue
```

### 22.2 Session Handoff Protocol (Local VM)

**When Approaching Context/Time Limits:**

1. Save comprehensive session summary to SSD
2. Archive full session state to HDD
3. Document current state, next steps
4. Close current GitHub issue or add "paused" comment
5. Create handoff document for next session (save to SSD)

**Handoff Document Template (Local VM):**

```markdown
# Session Handoff: [Date/Time]

## Current State

- Repository: [Name]
- Task: [Description]
- Progress: [X of Y subtasks completed]
- Session ID: [Unique ID]
- Storage Locations:
  - SSD Active: {SESSION_LOGS}/session_[id].json
  - HDD Archive: {MEMORY_STASH}/sessions/session_[id].json

## Completed

- [x] Task 1
- [x] Task 2

## In Progress

- [ ] Task 3 (50% complete)
  - Checkpoint: {CHECKPOINTS}/task3_[timestamp].json

## Remaining

- [ ] Task 4
- [ ] Task 5

## Next Steps

1. Load checkpoint from {CHECKPOINTS}/task3_[timestamp].json
2. Complete Task 3
3. Run security scan
4. Update GitHub issue

## Context Files (SSD)

- Logs: {SESSION_LOGS}/session_[timestamp].log
- Checkpoint: {CHECKPOINTS}/task_[id].json
- Knowledge Base: {KNOWLEDGE_DB}/ai_learning_log.md

## Archived Files (HDD)

- Full Session Archive: {MEMORY_STASH}/sessions/session_[id].json
- Historical Patterns: {MEMORY_STASH}/patterns/[date].json

## GitHub Issue

- Issue: MatoTeziTanka/Repo#123
- Status: In Progress (paused for handoff)

## Notes

- Special consideration: [Any important context]
- Storage optimization: [Any cleanup needed]
```

### 22.3 Resource Limits & Optimization (Local VM)

**Local VM Resource Management:**

**Memory Limits (Dell R730):**
- Maximum file size to load: 100MB (local VM can handle larger)
- Maximum simultaneous file operations: 20 (local has more resources)
- Buffer sizes: 500 operations before flush (SSD is fast)

**Processing Limits:**
- Maximum repositories per session: 11 (all repos, use checkpointing)
- Maximum test execution time: 30 minutes (local, no API limits)
- Maximum security scan time: 15 minutes per repository (parallel processing)

**Storage Optimization:**

```python
def optimize_local_storage():
    """
    Optimize SSD/HDD storage usage on local VM.
    """
    # Move old sessions from SSD to HDD (>7 days)
    for session_file in SESSION_LOGS.glob("session_*.json"):
        age_days = (datetime.now() - datetime.fromtimestamp(session_file.stat().st_mtime)).days
        if age_days > 7:
            hdd_archive = MEMORY_STASH / "sessions" / session_file.name
            hdd_archive.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(session_file), str(hdd_archive))
    
    # Compress old checkpoints
    for checkpoint in CHECKPOINTS.glob("*.json"):
        age_days = (datetime.now() - datetime.fromtimestamp(checkpoint.stat().st_mtime)).days
        if age_days > 30:
            # Compress and move to HDD
            compressed = "{{checkpoint}}.gz"
            with gzip.open(compressed, 'wb') as f:
                f.write(checkpoint.read_bytes())
            shutil.move(compressed, MEMORY_STASH / "checkpoints" / Path(compressed).name)
            checkpoint.unlink()
```

---

## 23. SELF-CORRECTION PROTOCOL

### 23.1 Error Detection & Acknowledgment

**When LLM Realizes a Mistake:**

1. **Immediate Acknowledgment:**
   - Stop current execution
   - Explicitly state: "I made an error. Here's what went wrong..."
   - Identify which framework rule was violated
   - Log error to SSD immediately

2. **Root Cause Analysis:**
   - Explain why the error occurred
   - Reference specific framework section that was violated
   - Document in knowledge base (Section 7.1, save to {KNOWLEDGE_DB})
   - Archive error pattern to HDD for long-term learning

3. **Correction Action:**
   - Propose corrective steps
   - Apply rollback if needed (restore from HDD backup)
   - Re-execute correctly
   - Log correction in GitHub issue
   - Update checkpoint on SSD

4. **Learning Integration:**
   - Record mistake pattern (Section 7.1, save to {KNOWLEDGE_DB})
   - Update prediction model (Section 7.2)
   - Add to self-documentation (Section 7.3)
   - Archive to HDD for historical analysis

**Example:**

```
❌ ERROR DETECTED

I violated Section 18.0 by beginning work without creating a GitHub issue.

ROOT CAUSE: 
- Did not follow Issue-Driven Workflow (Section 18.0)
- No pre-check for existing issue
- Error logged to: {SESSION_LOGS}/error_[timestamp].log

CORRECTION:
1. Stop all work immediately
2. Create GitHub issue: "Add secret scanning to BitPhoenix"
3. Resume work with proper issue tracking
4. Log this mistake in {KNOWLEDGE_DB}/ai_learning_log.md
5. Archive error pattern to {MEMORY_STASH}/error_patterns/[date].json

LEARNING:
Pattern: "started_work_without_issue"
Prevention: Always check for GitHub issue FIRST before any work
Storage: Saved to SSD knowledge base, archived to HDD
```

### 23.2 Framework Violation Severity Levels

**CRITICAL (Stop Immediately):**
- Working without GitHub issue (Section 18.0)
- Using regex-only secret detection (Section 3.2)
- Skipping security scans (Section 15)
- No logging (Section 14)
- **Action:** Immediate rollback from HDD backup, log to SSD, archive to HDD

**HIGH (Fix Before Proceeding):**
- Missing docstrings (Section 2.2)
- Incomplete error handling (Section 3.5)
- No test coverage (Section 3.6)
- **Action:** Fix immediately, update checkpoint on SSD

**MEDIUM (Fix in Next Iteration):**
- Suboptimal performance (Section 9.1.4)
- Incomplete documentation (Section 9.1.2)
- **Action:** Log to knowledge base, address in next cycle

**LOW (Improvement Opportunity):**
- Code style inconsistencies
- Minor optimization opportunities
- **Action:** Note in knowledge base for future improvement

---

## 24. AGENT SELF-IDENTIFICATION (LOCAL VM)

### 24.1 Agent Identity

**In All Logs and Communications:**

- **Agent Name:** "Perpetual Self-Updating AI Mind"
- **Short Name:** "AI Mind" or "PSAM"
- **Version:** [Track framework version]
- **Session ID:** [Unique ID per session]
- **VM Context:** "Local VM (Dell R730) / LM Studio"
- **Storage:** "SSD: {SSD_STORAGE}, HDD: {HDD_STORAGE}"

**Logging Standard (Local VM):**

```python
logger.log(
    who="AI_Mind_v2.0.0[session_abc123][LocalVM]",
    what="create",
    where="BitPhoenix/CLAUDE.md",
    why="Documentation: Add AI collaboration guide",
    status="SUCCESS",
    storage_ssd=str(SESSION_LOGS),
    storage_hdd=str(MEMORY_STASH)
)
```

**In GitHub Issues:**

- Sign all comments with: `— AI Mind (Framework v2.0.0, Local VM, Session: abc123)`
- Include storage paths for traceability: `[SSD: {path}, HDD: {path}]`

### 24.2 Storage Path Configuration

**Default Storage Paths (Local VM):**

```python
# Fast access storage (SSD)
SSD_STORAGE = Path(r"C:\\AI_Storage\\SSD")
KNOWLEDGE_DB = SSD_STORAGE / "knowledge_base"
CHECKPOINTS = SSD_STORAGE / "checkpoints"
SESSION_LOGS = SSD_STORAGE / "session_logs"

# Long-term storage (HDD)
HDD_STORAGE = Path(r"D:\\AI_Storage\\HDD")
MEMORY_STASH = HDD_STORAGE / "memory_stash"

# Initialize on first run
for path in [SSD_STORAGE, HDD_STORAGE, KNOWLEDGE_DB, CHECKPOINTS, SESSION_LOGS, MEMORY_STASH]:
    path.mkdir(parents=True, exist_ok=True)
```

**Storage Usage Guidelines:**

- **SSD:** Active sessions, recent logs, current knowledge base, active checkpoints
- **HDD:** Archived sessions, historical patterns, long-term memory, backups

---

'''
    
    # Replace storage path placeholders with actual paths
    # Note: In code examples, f-strings are shown as-is, so we escape them
    sections = sections.replace('{KNOWLEDGE_DB}', str(KNOWLEDGE_DB))
    sections = sections.replace('{SESSION_LOGS}', str(SESSION_LOGS))
    sections = sections.replace('{CHECKPOINTS}', str(CHECKPOINTS))
    sections = sections.replace('{MEMORY_STASH}', str(MEMORY_STASH))
    sections = sections.replace('{SSD_STORAGE}', str(SSD_STORAGE))
    sections = sections.replace('{HDD_STORAGE}', str(HDD_STORAGE))
    
    # Insert before Section 19 (Cross-Reference Index)
    pattern = r'(## 19\. CROSS-REFERENCE INDEX)'
    if re.search(pattern, content):
        # Use re.escape for the replacement to avoid regex interpretation issues
        # Find the position and insert manually
        match = re.search(pattern, content)
        if match:
            insert_pos = match.start()
            content = content[:insert_pos] + sections + '\n\n' + content[insert_pos:]
        # Renumber Cross-Reference Index to Section 25
        content = content.replace('## 19. CROSS-REFERENCE INDEX', '## 25. CROSS-REFERENCE INDEX')
        
        # Update Cross-Reference Index to include new LLM sections
        index_updates = '''
- **LLM Context Management:** Section 19.1
- **State Persistence (Local VM):** Section 19.2
- **State Reconstruction:** Section 19.3
- **Tool Execution (Local VM):** Section 19.4
- **Storage Optimization:** Section 19.5
- **Effective Prompting:** Section 20
- **File System Operations (Local VM):** Section 21
- **Incremental Execution (Local VM):** Section 22
- **Self-Correction Protocol:** Section 23
- **Agent Self-Identification (Local VM):** Section 24
'''
        
        # Add to "Common Tasks" section of index
        content = content.replace(
            '- **Optimizing performance:** Section 4.1.5, 9.4',
            f'- **Optimizing performance:** Section 4.1.5, 9.4{index_updates}'
        )
    else:
        # Insert before final "Document Version" section
        pattern2 = r'(---\s+\n\*\*Document Version)'
        if re.search(pattern2, content):
            content = re.sub(
                pattern2,
                sections + r'\1',
                content
            )
        else:
            # Append at the end
            content = content.rstrip() + sections
    
    return content


def main():
    """Main execution function"""
    print("="*70)
    print("ADDING LLM OPERATIONAL SECTIONS (19-24)")
    print("="*70)
    print("Adapted for Local VM with LM Studio, SSD/HDD storage")
    
    # Read the file
    print("\n📖 Reading master prompt file...")
    content = INPUT_FILE.read_text(encoding='utf-8')
    print(f"✅ Read {len(content):,} characters")
    
    # Add sections
    print("\n📝 Adding LLM operational sections...")
    content = add_llm_sections(content)
    
    # Write the updated file
    print("\n💾 Writing updated file...")
    OUTPUT_FILE.write_text(content, encoding='utf-8')
    print(f"✅ Updated file saved: {OUTPUT_FILE.name}")
    print(f"✅ File size: {OUTPUT_FILE.stat().st_size:,} bytes")
    
    print("\n" + "="*70)
    print("SECTIONS 19-24 ADDED SUCCESSFULLY")
    print("="*70)
    print("\nNew sections added:")
    print("  - Section 19: LLM Operational Requirements (Local VM)")
    print("  - Section 20: Effective Prompting")
    print("  - Section 21: File System Interaction (Local VM)")
    print("  - Section 22: Incremental Execution (Local VM)")
    print("  - Section 23: Self-Correction Protocol")
    print("  - Section 24: Agent Self-Identification (Local VM)")


if __name__ == "__main__":
    main()

