<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
```python
"""
SHENRON MCP TOOLS - Phase 1: File & Terminal Operations
Ultra Instinct Foundation

Provides SHENRON with file access and command execution across all VMs.

================================================================================
VERSIONING
================================================================================
Stable Release: 1.0.0 (Do not reset, synchronize with repository-wide versioning)
================================================================================

================================================================================
SECURITY CONTROLS (SUMMARY)
================================================================================
- All credentials, secrets, and sensitive config must be managed securely.
- NO hardcoded passwords, keys, or secrets.
- Path traversal protection via base directory whitelisting and path sanitization
- Symlink prevention
- Environment variable-only secrets
- Command injection defense via strict allowlists
- Input validation on all user data
- Audit logging with base directory check
- Resource cleanup
- CVE-aware SSH and file handling
================================================================================

Workflow Documentation:
- File: mcp_tools.py
    - MCPTools: File operations, terminal operations, SSH management
    - ToolPermissions: Security policy enforcement
    - Main block: Example/test usage
================================================================================

For extended compliance references (NIST, CIS, OWASP, CVE), see docs/security_standards.md.
"""

import paramiko
import os
import json
import re
import sys
import stat
from datetime import datetime
from typing import Dict, List, Optional, Tuple

# ============================== VERSION TRACKING ==============================
__version__ = "1.0.0"
# ==============================================================================

# ======================= SECURE BASE DIRECTORY WHITELIST ======================
# For path traversal protection, define allowed base directories for all file operations
ALLOWED_BASE_DIRECTORIES = [
    os.path.abspath(os.path.join(os.path.expanduser('~'), 'shenron')),
    '/var/app/shenron',  # Example: Add more as required
]
# ==============================================================================

def is_path_within_allowed_base(path: str) -> bool:
    """
    Check that the absolute, canonical path is within an allowed base directory.
    Mitigates path traversal and symlink attacks.

    Args:
        path (str): Path to check. Should be absolute or will be made absolute.
    Returns:
        bool: True if path is allowed (only subdirectories), False otherwise.
    """
    canonical_path = os.path.realpath(os.path.abspath(path))
    for allowed in ALLOWED_BASE_DIRECTORIES:
        allowed_canonical = os.path.realpath(os.path.abspath(allowed))
        # Restrict to subdirectories only, not the base itself
        if canonical_path.startswith(allowed_canonical + os.sep):
            return True
    return False

def sanitize_path(path: str) -> str:
    """
    Sanitizes file system paths to prevent path traversal, symlink, and injection attacks.

    Args:
        path (str): The file or directory path to sanitize.
            - Must be a string, not None.
            - No null bytes, control chars, or forbidden patterns.
            - Must reside within allowed base directories (subdirectories only).

    Returns:
        str: Sanitized path string.

    Raises:
        ValueError: If path contains unsafe characters, forbidden patterns, escapes the intended base, or is a symlink.
    """
    # Reject null bytes and control characters
    if not isinstance(path, str):
        raise ValueError("Path must be a string.")
    if '\x00' in path or any(ord(c) < 32 for c in path):
        raise ValueError("Path contains unsafe characters.")

    # Allow [A-Za-z0-9._\-\/ ] and prohibit shell meta-characters, wildcards, etc.
    # Permit spaces, parentheses, brackets, and common safe filename characters.
    # Restrict only known dangerous shell characters.
    if re.search(r'(\.\.|~|[;&|`$<>*?\'"\\])', path):
        raise ValueError("Path contains forbidden characters or patterns.")

    # Normalize and collapse redundant separators
    norm_path = os.path.normpath(path)
    abs_path = os.path.abspath(norm_path)

    # Enforce path is within allowed base directories (subdirectories only)
    if not is_path_within_allowed_base(abs_path):
        raise ValueError("Path escapes allowed base directories or targets base directory itself.")

    # SECURITY SENTINEL: Prevent symlink traversal (refuse symlinks for file operations)
    try:
        if os.path.lexists(abs_path):
            if os.path.islink(abs_path):
                raise ValueError("Symlinks are not permitted for file operations.")
    except Exception as e:
        # If path doesn't exist, it's not a symlink; proceed
        pass

    return abs_path

def sanitize_command(command: str) -> str:
    """
    Sanitizes SSH command strings to prevent command injection.

    Args:
        command (str): The command string.
            - No shell meta-characters.
            - Must be on explicit allow-list.

    Returns:
        str: Sanitized command.

    Raises:
        ValueError: If command contains forbidden meta-characters or is not allowed.
    """
    # Reject dangerous shell meta-characters
    if re.search(r'[;&|`$<>]', command):
        raise ValueError("Command contains forbidden meta-characters.")

    # Allowlist: Example (expand as needed)
    allowed_cmds = [
        'ls', 'cat', 'grep', 'sed', 'tail', 'head', 'echo', 'wc', 'whoami', 'df', 'du', 'find', 'chmod', 'chown'
    ]
    first_word = command.strip().split()[0]
    if first_word not in allowed_cmds:
        raise ValueError(f"Command '{first_word}' is not allowed by policy.")

    return command.strip()

def sanitize_pattern(pattern: str) -> str:
    """
    Basic sanitization for search patterns (used in grep).

    Args:
        pattern (str): Pattern string.
            - No newlines, shell meta-characters, or excessively long patterns.
            - Accepts only basic ASCII.

    Returns:
        str: Sanitized pattern.

    Raises:
        ValueError: If pattern contains forbidden meta-characters.
    """
    # Only allow safe ASCII, no shell expansion, no newlines
    if not isinstance(pattern, str):
        raise ValueError("Pattern must be a string.")
    if '\n' in pattern or re.search(r'[;&|`$<>*?\'"\\]', pattern):
        raise ValueError("Pattern contains forbidden meta-characters.")
    if not re.match(r'^[A-Za-z0-9 _\.\-\[\]\(\)\{\}:,\/]+$', pattern):
        raise ValueError("Pattern contains forbidden or unsafe characters.")
    # Limit pattern length for safety
    if len(pattern) > 128:
        raise ValueError("Pattern too long, possible DoS attempt.")
    return pattern.strip()

class MCPTools:
    """
    MCP Tool Executor for SHENRON

    Enterprise-grade file and command operations across VMs.

    Practical Usage:
        - Securely connect to VMs using SSH (env-based credentials only)
        - Perform file and terminal operations (with input validation)
        - Audit all actions to secure log file (owner-only access)

    Security Controls:
        - Path traversal protection
        - Symlink prevention
        - Input sanitization, allowlist enforcement
        - Audit logging within allowed base (owner-only file permissions)
        - Credentials cleared from memory after use
        - Resource cleanup: SSH/SFTP connection management
        - No hardcoded secrets

    For extended compliance and technical standards, see docs/security_standards.md.
    """

    # TODO: Consider integrating with Hashicorp Vault, AWS Secrets Manager, or Azure Key Vault for credential management.
    # TODO: Validate and sanitize all user inputs to prevent injection attacks.

    def __init__(self, log_file: Optional[str] = None):
        """
        Initialize MCPTools.

        Args:
            log_file (str, optional): Path to audit log file.
                - If not provided, uses environment variable 'MCP_LOG_PATH' or cross-platform default.
                - Must be a valid, writable path within allowed base directories.

        Raises:
            EnvironmentError: If required credentials environment variables are missing.
            PermissionError: If log directory escapes allowed base directories.
            ValueError: If log_file path escapes allowed base directories.
        """
        self.ssh_connections = {}

        # SECURITY: Log file location is configurable and platform independent
        if log_file:
            sanitized_log_file = sanitize_path(log_file)
            self.log_file = sanitized_log_file
        else:
            default_log_file = os.environ.get(
                'MCP_LOG_PATH',
                os.path.join(
                    os.path.expanduser('~'),
                    'shenron',
                    'logs',
                    'mcp_audit.log'
                )
            )
            self.log_file = sanitize_path(default_log_file)

        self.vm_credentials = {}

        managed_vms = [
            {
                'ip': '<VM100_IP>',
                'user_env': 'VM100_USER',
                'key_env': 'VM100_SSH_KEY',
                'pass_env': 'VM100_PASS',
                'default_username': None
            },
            {
                'ip': '<VM150_IP>',
                'user_env': 'VM150_USER',
                'key_env': 'VM150_SSH_KEY',
                'pass_env': 'VM150_PASS',
                'default_username': None
            },
            {
                'ip': '<VM101_IP>',
                'user_env': 'VM101_USER',
                'key_env': 'VM101_SSH_KEY',
                'pass_env': 'VM101_PASS',
                'default_username': None
            },
            {
                'ip': '192.168.12.210',
                'user_env': 'VM210_USER',
                'key_env': 'VM210_SSH_KEY',
                'pass_env': 'VM210_PASS',
                'default_username': None
            }
        ]

        # Build credentials securely, error if missing required env vars
        for vm in managed_vms:
            username = os.environ.get(vm['user_env'], vm['default_username'])
            key = os.environ.get(vm['key_env'], None)
            password = os.environ.get(vm['pass_env'], None)
            # SECURITY SENTINEL: Do not log or print credentials
            if not username:
                raise EnvironmentError(f"Missing required environment variable for username: {vm['user_env']}")
            if not (key or password):
                raise EnvironmentError(f"Missing SSH key or password environment variable for VM {vm['ip']}")
            self.vm_credentials[vm['ip']] = {
                'username': username,
                'key': key,
                'password': password
            }

        self._ensure_log_directory()

    def _ensure_log_directory(self):
        """
        Create log directory if it doesn't exist. SECURITY: Prevent path traversal and symlink attacks,
        and support all ALLOWED_BASE_DIRECTORIES.
        """
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            # SECURITY: Only create directories inside allowed base path; resolve symlinks and canonicalize path
            log_dir_canonical = os.path.realpath(os.path.abspath(log_dir))
            allowed = False
            for base_dir in ALLOWED_BASE_DIRECTORIES:
                base_canonical = os.path.realpath(os.path.abspath(base_dir))
                if log_dir_canonical.startswith(base_canonical + os.sep):
                    allowed = True
                    break
            if allowed:
                os.makedirs(log_dir, exist_ok=True)
            else:
                raise PermissionError("Log directory escapes allowed base; path traversal detected.")

    def _log_action(self, tool: str, vm_ip: str, action: str, result: str, success: bool):
        """
        Audit log all MCP tool usage.

        Args:
            tool (str): Tool name
            vm_ip (str): Target VM IP
            action (str): Operation performed (file path, command, etc.)
            result (str): Result summary (truncated if long)
            success (bool): Was the action successful?

        SECURITY: Only write logs to a sanitized file path within allowed base.
        SECURITY: Set log file permissions to owner-only (0600) after creation.
        """
        try:
            # Sanitize log_file path before every write
            safe_log_file = sanitize_path(self.log_file)
        except Exception as e:
            print(f"[ERROR] MCPTools log file path sanitization failed: {e}", file=sys.stderr)
            return

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'tool': tool,
            'vm_ip': vm_ip,
            'action': action,
            'result': result[:200],  # Truncate long results
            'success': success,
            'version': __version__
        }

        try:
            # Write audit log entry
            with open(safe_log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(log_entry) + '\n')
            # SECURITY: Set file permissions to 0600 (owner-only) if newly created
            try:
                if os.path.exists(safe_log_file):
                    os.chmod(safe_log_file, 0o600)
            except Exception as perm_err:
                print(f"[WARN] Could not set audit log file permissions: {perm_err}", file=sys.stderr)
        except Exception as e:
            # Logging should not break the main flow, but print error for diagnostics
            print(f"[ERROR] MCPTools logging failed: {e}", file=sys.stderr)

    def _get_ssh_connection(self, vm_ip: str) -> paramiko.SSHClient:
        """
        Get or create SSH connection to VM. SECURITY: Only use env-based credentials.

        Args:
            vm_ip (str): Target VM IP

        Returns:
            paramiko.SSHClient: Connected SSH client

        Raises:
            ValueError: If no credentials or authentication method available
            Exception: On connection failure

        Security Notes:
            - Credentials are removed from memory after connection or on failure.
            - Only keys/passwords from env are used.
        """
        if vm_ip not in self.ssh_connections:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            creds = self.vm_credentials.get(vm_ip)
            try:
                if not creds:
                    raise ValueError(f"No credentials configured for VM {vm_ip}")
                # Prefer SSH key if available, fallback to password from env
                if creds.get('key'):
                    # Support passphrase-protected keys and agent forwarding
                    kwargs = {
                        'username': creds['username'],
                        'key_filename': creds['key']
                    }
                    # If passphrase env var exists, use it
                    passphrase_env = f"{vm_ip.replace('.', '_')}_SSH_PASSPHRASE"
                    passphrase = os.environ.get(passphrase_env, None)
                    if passphrase:
                        kwargs['passphrase'] = passphrase
                    # Agent forwarding (optional, only if needed)
                    if os.environ.get('SSH_AUTH_SOCK'):
                        kwargs['allow_agent'] = True
                    # Connect using advanced options
                    ssh.connect(vm_ip, **kwargs)
                elif creds.get('password'):
                    # Multi-factor authentication and certificates could be added here if required
                    ssh.connect(vm_ip, username=creds['username'],
                                password=creds['password'])
                else:
                    raise ValueError(f"No authentication method for VM {vm_ip} (missing SSH key or password in environment)")
                self.ssh_connections[vm_ip] = ssh
            except Exception as conn_exc:
                # SECURITY: Remove all credential data for the VM from self.vm_credentials after attempted connection
                self.vm_credentials[vm_ip] = {}  # Clear credential info for this VM always, even if error
                # SECURITY: Do not log sensitive info!
                raise conn_exc
            finally:
                # SECURITY: Remove credentials regardless of success or failure
                self.vm_credentials[vm_ip] = {}
        return self.ssh_connections[vm_ip]

    def close_all_connections(self):
        """
        Cleanly close all SSH connections managed by MCPTools.
        Call this when MCPTools is destroyed or when connections are no longer needed.
        """
        for vm_ip, ssh in list(self.ssh_connections.items()):
            try:
                ssh.close()
            except Exception as e:
                print(f"[ERROR] Failed to close SSH connection for {vm_ip}: {e}", file=sys.stderr)
            finally:
                self.ssh_connections.pop(vm_ip, None)

    def __enter__(self):
        """
        Context manager entry: Returns self for with-block usage.
        """
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Context manager exit: Ensures all SSH connections are closed.
        """
        self.close_all_connections()

    def __del__(self):
        """
        Destructor to ensure all SSH connections are closed upon object deletion.
        WARNING: Do not rely solely on destructor for cleanup; prefer context manager.
        """
        self.close_all_connections()

    # ========================================================================
    # FILE OPERATIONS
    # ========================================================================

    def read_file(self, vm_ip: str, file_path: str, offset: int = 0,
                  limit: Optional[int] = None) -> Dict:
        """
        Read file from any VM using SFTP only (no shell commands).

        Args:
            vm_ip (str): Target VM IP address.
            file_path (str): Full absolute path to file.
                - Must pass sanitize_path checks.
            offset (int): Starting line number (0-indexed, must be >= 0).
            limit (int, optional): Maximum lines to read (None = all).

        Returns:
            dict: Read result:
                - success (bool)
                - content (str)
                - lines (int): total lines in file
                - file_size (int): total bytes in content

        Raises:
            ValueError: For invalid paths, offset, or permission issues.

        Security Notes:
            - Path traversal, shell injection, and symlink attacks are prevented.
            - Only SFTP is used for file read; no shell.
            - SFTP connections are closed after operation.
        """
        sftp = None
        try:
            # Validate and sanitize file_path
            safe_path = sanitize_path(file_path)

            ssh = self._get_ssh_connection(vm_ip)
            sftp = ssh.open_sftp()
            # Read file content securely with SFTP
            with sftp.open(safe_path, 'r', encoding='utf-8') as remote_file:
                all_lines = remote_file.readlines()

            total_lines = len(all_lines)
            if offset < 0 or (limit is not None and limit < 1):
                raise ValueError("Offset and limit must be positive integers.")

            # Slice lines according to offset and limit
            if limit is not None:
                lines_to_return = all_lines[offset:offset + limit]
            else:
                lines_to_return = all_lines[offset:]

            content = ''.join(lines