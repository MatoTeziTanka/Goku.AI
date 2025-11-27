<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
"""
SHENRON MCP TOOLS - Phase 1: File & Terminal Operations
Ultra Instinct Foundation

Provides SHENRON with file access and command execution across all VMs.
"""

import paramiko
import os
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple

class MCPTools:
    """MCP Tool Executor for SHENRON"""
    
    def __init__(self, log_file='C:\\GOKU-AI\\shenron\\logs\\mcp_audit.log'):
        self.ssh_connections = {}
        self.log_file = log_file
        
        # VM credentials (use SSH keys in production)
        self.vm_credentials = {
            '<VM100_IP>': {'username': 'Administrator', 'key': None},  # Windows
            '<VM150_IP>': {'username': 'wp1', 'password': 'Norelec7!'},
            '<VM101_IP>': {'username': 'admin', 'password': None},
            '192.168.12.210': {'username': 'admin', 'password': None}
        }
        
        self._ensure_log_directory()
    
    def _ensure_log_directory(self):
        """Create log directory if it doesn't exist"""
        log_dir = os.path.dirname(self.log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    
    def _log_action(self, tool: str, vm_ip: str, action: str, result: str, success: bool):
        """Audit log all MCP tool usage"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'tool': tool,
            'vm_ip': vm_ip,
            'action': action,
            'result': result[:200],  # Truncate long results
            'success': success
        }
        
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def _get_ssh_connection(self, vm_ip: str) -> paramiko.SSHClient:
        """Get or create SSH connection to VM"""
        if vm_ip not in self.ssh_connections:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            creds = self.vm_credentials.get(vm_ip)
            if not creds:
                raise ValueError(f"No credentials configured for VM {vm_ip}")
            
            try:
                if creds.get('key'):
                    ssh.connect(vm_ip, username=creds['username'], 
                               key_filename=creds['key'])
                elif creds.get('password'):
                    ssh.connect(vm_ip, username=creds['username'], 
                               password=creds['password'])
                else:
                    raise ValueError(f"No authentication method for VM {vm_ip}")
                
                self.ssh_connections[vm_ip] = ssh
            except Exception as e:
                self._log_action('ssh_connect', vm_ip, 'connect', str(e), False)
                raise
        
        return self.ssh_connections[vm_ip]
    
    # ========================================================================
    # FILE OPERATIONS
    # ========================================================================
    
    def read_file(self, vm_ip: str, file_path: str, offset: int = 0, 
                  limit: Optional[int] = None) -> Dict:
        """
        Read file from any VM
        
        Args:
            vm_ip: Target VM IP address
            file_path: Full path to file
            offset: Starting line number (0-indexed)
            limit: Maximum lines to read (None = all)
        
        Returns:
            {
                'success': bool,
                'content': str,
                'lines': int,
                'file_size': int
            }
        """
        try:
            ssh = self._get_ssh_connection(vm_ip)
            
            # Get file size first
            stdin, stdout, stderr = ssh.exec_command(f'wc -l "{file_path}"')
            total_lines = int(stdout.read().decode().split()[0])
            
            # Read file content
            if limit:
                cmd = f'sed -n "{offset+1},{offset+limit}p" "{file_path}"'
            else:
                cmd = f'tail -n +{offset+1} "{file_path}"'
            
            stdin, stdout, stderr = ssh.exec_command(cmd)
            content = stdout.read().decode()
            error = stderr.read().decode()
            
            if error:
                raise Exception(error)
            
            result = {
                'success': True,
                'content': content,
                'lines': total_lines,
                'file_size': len(content)
            }
            
            self._log_action('read_file', vm_ip, file_path, f'Read {len(content)} bytes', True)
            return result
            
        except Exception as e:
            self._log_action('read_file', vm_ip, file_path, str(e), False)
            return {
                'success': False,
                'error': str(e),
                'content': ''
            }
    
    def write_file(self, vm_ip: str, file_path: str, content: str, 
                   append: bool = False) -> Dict:
        """
        Write content to file on any VM
        
        Args:
            vm_ip: Target VM IP address
            file_path: Full path to file
            content: Content to write
            append: If True, append instead of overwrite
        
        Returns:
            {
                'success': bool,
                'bytes_written': int,
                'file_path': str
            }
        """
        try:
            ssh = self._get_ssh_connection(vm_ip)
            
            # Escape special characters in content
            safe_content = content.replace('"', '\\"').replace('$', '\\$')
            
            # Write using echo (safer than heredoc for SSH)
            operator = '>>' if append else '>'
            cmd = f'echo -e "{safe_content}" {operator} "{file_path}"'
            
            stdin, stdout, stderr = ssh.exec_command(cmd)
            error = stderr.read().decode()
            
            if error:
                raise Exception(error)
            
            result = {
                'success': True,
                'bytes_written': len(content),
                'file_path': file_path,
                'mode': 'append' if append else 'overwrite'
            }
            
            self._log_action('write_file', vm_ip, file_path, 
                           f'Wrote {len(content)} bytes', True)
            return result
            
        except Exception as e:
            self._log_action('write_file', vm_ip, file_path, str(e), False)
            return {
                'success': False,
                'error': str(e)
            }
    
    def search_files(self, vm_ip: str, pattern: str, directory: str = '/',
                     file_pattern: str = '*') -> Dict:
        """
        Search for files matching pattern
        
        Args:
            vm_ip: Target VM IP address
            pattern: Text pattern to search for (grep)
            directory: Directory to search in
            file_pattern: File name pattern (e.g., '*.py')
        
        Returns:
            {
                'success': bool,
                'matches': List[{file, line, content}],
                'total_matches': int
            }
        """
        try:
            ssh = self._get_ssh_connection(vm_ip)
            
            # Use grep to search files
            cmd = f'grep -r -n "{pattern}" {directory} --include="{file_pattern}"'
            
            stdin, stdout, stderr = ssh.exec_command(cmd)
            output = stdout.read().decode()
            
            matches = []
            for line in output.split('\n'):
                if ':' in line:
                    parts = line.split(':', 2)
                    if len(parts) >= 3:
                        matches.append({
                            'file': parts[0],
                            'line': int(parts[1]),
                            'content': parts[2].strip()
                        })
            
            result = {
                'success': True,
                'matches': matches,
                'total_matches': len(matches)
            }
            
            self._log_action('search_files', vm_ip, f'{directory}/{file_pattern}',
                           f'Found {len(matches)} matches', True)
            return result
            
        except Exception as e:
            self._log_action('search_files', vm_ip, directory, str(e), False)
            return {
                'success': False,
                'error': str(e),
                'matches': []
            }
    
    def list_directory(self, vm_ip: str, directory: str) -> Dict:
        """
        List files and directories
        
        Args:
            vm_ip: Target VM IP address
            directory: Directory path
        
        Returns:
            {
                'success': bool,
                'files': List[str],
                'directories': List[str]
            }
        """
        try:
            ssh = self._get_ssh_connection(vm_ip)
            
            # List files
            stdin, stdout, stderr = ssh.exec_command(f'ls -la "{directory}"')
            output = stdout.read().decode()
            
            files = []
            directories = []
            
            for line in output.split('\n')[1:]:  # Skip first line (total)
                if not line.strip():
                    continue
                
                parts = line.split()
                if len(parts) < 9:
                    continue
                
                name = ' '.join(parts[8:])
                if name in ['.', '..']:
                    continue
                
                if line.startswith('d'):
                    directories.append(name)
                else:
                    files.append(name)
            
            result = {
                'success': True,
                'files': files,
                'directories': directories,
                'total': len(files) + len(directories)
            }
            
            self._log_action('list_directory', vm_ip, directory,
                           f'{len(files)} files, {len(directories)} dirs', True)
            return result
            
        except Exception as e:
            self._log_action('list_directory', vm_ip, directory, str(e), False)
            return {
                'success': False,
                'error': str(e),
                'files': [],
                'directories': []
            }
    
    # ========================================================================
    # TERMINAL OPERATIONS
    # ========================================================================
    
    def run_command(self, vm_ip: str, command: str, timeout: int = 30,
                   sudo: bool = False) -> Dict:
        """
        Execute command on any VM
        
        Args:
            vm_ip: Target VM IP address
            command: Command to execute
            timeout: Execution timeout in seconds
            sudo: Run with sudo (requires passwordless sudo or password in creds)
        
        Returns:
            {
                'success': bool,
                'stdout': str,
                'stderr': str,
                'exit_code': int,
                'execution_time': float
            }
        """
        try:
            ssh = self._get_ssh_connection(vm_ip)
            
            if sudo:
                command = f'sudo {command}'
            
            start_time = datetime.now()
            stdin, stdout, stderr = ssh.exec_command(command, timeout=timeout)
            
            stdout_text = stdout.read().decode()
            stderr_text = stderr.read().decode()
            exit_code = stdout.channel.recv_exit_status()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = {
                'success': exit_code == 0,
                'stdout': stdout_text,
                'stderr': stderr_text,
                'exit_code': exit_code,
                'execution_time': execution_time,
                'command': command
            }
            
            self._log_action('run_command', vm_ip, command,
                           f'Exit: {exit_code}, Time: {execution_time}s', exit_code == 0)
            return result
            
        except Exception as e:
            self._log_action('run_command', vm_ip, command, str(e), False)
            return {
                'success': False,
                'error': str(e),
                'stdout': '',
                'stderr': str(e),
                'exit_code': -1
            }
    
    def get_system_info(self, vm_ip: str) -> Dict:
        """
        Get system information from VM
        
        Returns:
            {
                'hostname': str,
                'cpu_usage': float,
                'memory_usage': float,
                'disk_usage': float,
                'uptime': str
            }
        """
        try:
            # Get hostname
            hostname_result = self.run_command(vm_ip, 'hostname')
            hostname = hostname_result['stdout'].strip()
            
            # Get CPU usage (Linux)
            cpu_result = self.run_command(vm_ip, "top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
            cpu_usage = float(cpu_result['stdout'].strip().replace('%', ''))
            
            # Get memory usage
            mem_result = self.run_command(vm_ip, "free | grep Mem | awk '{print ($3/$2) * 100.0}'")
            memory_usage = float(mem_result['stdout'].strip())
            
            # Get disk usage
            disk_result = self.run_command(vm_ip, "df -h / | tail -1 | awk '{print $5}'")
            disk_usage = float(disk_result['stdout'].strip().replace('%', ''))
            
            # Get uptime
            uptime_result = self.run_command(vm_ip, 'uptime')
            uptime = uptime_result['stdout'].strip()
            
            return {
                'success': True,
                'hostname': hostname,
                'cpu_usage': cpu_usage,
                'memory_usage': memory_usage,
                'disk_usage': disk_usage,
                'uptime': uptime
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def close_all_connections(self):
        """Close all SSH connections"""
        for vm_ip, ssh in self.ssh_connections.items():
            try:
                ssh.close()
                self._log_action('ssh_close', vm_ip, 'close', 'Connection closed', True)
            except:
                pass
        
        self.ssh_connections = {}


# ============================================================================
# TOOL PERMISSION CHECKER
# ============================================================================

class ToolPermissions:
    """Security model for MCP tools"""
    
    # SAFE: Always allowed (read-only operations)
    SAFE_TOOLS = [
        'read_file',
        'list_directory',
        'search_files',
        'get_system_info'
    ]
    
    # MODERATE: Requires Agent Mode with 2FA
    MODERATE_TOOLS = [
        'write_file',
        'run_command'
    ]
    
    # DANGEROUS: Blocked (or require explicit approval)
    DANGEROUS_COMMANDS = [
        'rm -rf',
        'dd if=',
        'mkfs',
        'fdisk',
        '> /dev/',
        'shutdown',
        'reboot',
        'init 0',
        'systemctl stop',
        'kill -9',
        'DROP DATABASE',
        'DROP TABLE'
    ]
    
    @staticmethod
    def check_permission(tool: str, command: Optional[str] = None, 
                        agent_mode_enabled: bool = False) -> Tuple[bool, str]:
        """
        Check if tool usage is permitted
        
        Returns:
            (allowed: bool, reason: str)
        """
        # SAFE tools always allowed
        if tool in ToolPermissions.SAFE_TOOLS:
            return (True, "SAFE operation")
        
        # MODERATE tools require Agent Mode
        if tool in ToolPermissions.MODERATE_TOOLS:
            if not agent_mode_enabled:
                return (False, "Agent Mode required (enable with 2FA)")
            
            # Check for dangerous commands
            if command:
                for dangerous in ToolPermissions.DANGEROUS_COMMANDS:
                    if dangerous.lower() in command.lower():
                        return (False, f"DANGEROUS command blocked: {dangerous}")
            
            return (True, "Agent Mode enabled")
        
        # Unknown tool
        return (False, "Unknown tool")


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    # Initialize MCP tools
    mcp = MCPTools()
    
    # Test: Read file from VM150
    print("📄 Reading file from VM150...")
    result = mcp.read_file('<VM150_IP>', '/var/www/shenron.lightspeedup.com/index.html', limit=10)
    if result['success']:
        print(f"✅ Read {result['lines']} lines")
        print(result['content'][:200])
    
    # Test: List directory
    print("\n📁 Listing directory...")
    result = mcp.list_directory('<VM150_IP>', '/var/www')
    if result['success']:
        print(f"✅ Found {result['total']} items")
        print(f"Directories: {result['directories']}")
    
    # Test: Run command
    print("\n⚡ Running command...")
    result = mcp.run_command('<VM150_IP>', 'hostname')
    if result['success']:
        print(f"✅ Hostname: {result['stdout'].strip()}")
    
    # Test: System info
    print("\n📊 Getting system info...")
    result = mcp.get_system_info('<VM150_IP>')
    if result['success']:
        print(f"✅ Hostname: {result['hostname']}")
        print(f"   CPU: {result['cpu_usage']:.1f}%")
        print(f"   RAM: {result['memory_usage']:.1f}%")
        print(f"   Disk: {result['disk_usage']:.1f}%")
    
    # Close connections
    mcp.close_all_connections()
    print("\n✅ All tests complete!")

