<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
"""
SHENRON API v5.0 - ULTRA INSTINCT
With MCP Tools Integration

Extends SHENRON with file operations, terminal access, and autonomous capabilities.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime
from mcp_tools import MCPTools, ToolPermissions
import re
import logging

app = Flask(__name__)
CORS(app)

# ============================================================================
# SECURITY LOGGING & AUDIT
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

def audit_log(event_type, details):
    logging.info(f"[AUDIT] {event_type}: {details}")

# ============================================================================
# Initialize MCP tools
# ============================================================================

mcp = MCPTools()

# LM Studio API endpoint
LM_STUDIO_API = "http://localhost:1234/v1/chat/completions"

# Warrior configurations
WARRIORS = {
    "goku": {"model": "deepseek-coder-v2-lite", "emoji": "🥋", "temp": 0.7},
    "vegeta": {"model": "llama-3.2-3b", "emoji": "👑", "temp": 0.3},
    "piccolo": {"model": "qwen2.5-coder-7b", "emoji": "🧠", "temp": 0.5},
    "gohan": {"model": "mistral-7b", "emoji": "⚠️", "temp": 0.4},
    "krillin": {"model": "phi-3-mini-128k", "emoji": "🔧", "temp": 0.6},
    "frieza": {"model": "phi-3-mini-128k:2", "emoji": "😈", "temp": 0.9}
}


# ============================================================================
# HELPER: Parse MCP Tool Requests
# ============================================================================

def parse_mcp_request(query: str) -> dict:
    """
    Parse user query to detect MCP tool requests
    
    Examples:
        "read file /var/www/index.html on VM150"
        "execute 'df -h' on <VM150_IP>"
        "list files in /home on VM150"
        "search for 'error' in /var/log on VM150"
    
    Returns:
        {
            'is_mcp_request': bool,
            'tool': str,
            'vm_ip': str,
            'params': dict
        }
    """
    query_lower = query.lower()
    
    # Extract VM IP or alias
    vm_mapping = {
        'vm100': '<VM100_IP>',
        'vm150': '<VM150_IP>',
        'vm101': '<VM101_IP>',
        'vm210': '192.168.12.210'
    }
    
    vm_ip = None
    for alias, ip in vm_mapping.items():
        if alias in query_lower or ip in query:
            vm_ip = ip
            break
    
    if not vm_ip:
        return {'is_mcp_request': False}
    
    # Detect tool based on keywords
    if any(word in query_lower for word in ['read file', 'read', 'show file', 'cat']):
        # Extract file path
        path_match = re.search(r'[/\\][\w/.\\-]+', query)
        if path_match:
            return {
                'is_mcp_request': True,
                'tool': 'read_file',
                'vm_ip': vm_ip,
                'params': {'file_path': path_match.group()}
            }
    
    elif any(word in query_lower for word in ['execute', 'run command', 'run', 'exec']):
        # Extract command (between quotes)
        cmd_match = re.search(r"['\"](.+?)['\"]", query)
        if cmd_match:
            return {
                'is_mcp_request': True,
                'tool': 'run_command',
                'vm_ip': vm_ip,
                'params': {'command': cmd_match.group(1)}
            }
    
    elif any(word in query_lower for word in ['list', 'ls', 'show directory']):
        path_match = re.search(r'in ([/\\][\w/.\\-]+)', query)
        directory = path_match.group(1) if path_match else '/'
        return {
            'is_mcp_request': True,
            'tool': 'list_directory',
            'vm_ip': vm_ip,
            'params': {'directory': directory}
        }
    
    elif 'search' in query_lower or 'grep' in query_lower or 'find' in query_lower:
        pattern_match = re.search(r"for ['\"](.+?)['\"]", query)
        path_match = re.search(r'in ([/\\][\w/.\\-]+)', query)
        
        if pattern_match:
            return {
                'is_mcp_request': True,
                'tool': 'search_files',
                'vm_ip': vm_ip,
                'params': {
                    'pattern': pattern_match.group(1),
                    'directory': path_match.group(1) if path_match else '/'
                }
            }
    
    elif 'system info' in query_lower or 'status' in query_lower or 'health' in query_lower:
        return {
            'is_mcp_request': True,
            'tool': 'get_system_info',
            'vm_ip': vm_ip,
            'params': {}
        }
    
    return {'is_mcp_request': False}


# ============================================================================
# SECURITY: Command Validation & Sudo Controls
# ============================================================================

FORBIDDEN_COMMANDS = [
    'rm', 'shutdown', 'reboot', 'mkfs', 'dd', 'init', 'poweroff', 'halt'
]

def validate_command(command: str) -> (bool, str):
    """
    Validates shell command to prevent dangerous operations.
    Returns (allowed, reason)
    """
    for forbidden in FORBIDDEN_COMMANDS:
        # Use word boundaries to match whole words only
        if re.search(r'\b' + re.escape(forbidden) + r'\b', command):
            return False, f"Command '{forbidden}' is forbidden for security reasons."
    # Disallow potentially dangerous shell metacharacters unless explicitly permitted
    if re.search(r'[;&|`$><]', command):
        return False, "Command contains forbidden shell metacharacters (&, ;, |, $, >, <, `)."
    # Length check
    if len(command) > 128:
        return False, "Command is too long."
    return True, ""

def validate_file_path(file_path: str) -> (bool, str):
    """
    Basic file path validation to prevent traversal, etc.
    Returns (allowed, reason)
    """
    # Disallow parent traversal and other risky patterns
    if '..' in file_path or file_path.startswith('/etc/') or file_path.startswith('/root') or file_path.startswith('/dev/'):
        return False, "Access to sensitive directories is not allowed."
    # Length check
    if len(file_path) > 256:
        return False, "File path is too long."
    return True, ""

def require_agent_mode_sudo(data):
    """
    Returns True if sudo is requested, but agent_mode is not true
    """
    params = data.get('params', {})
    if data.get('tool') == 'run_command' and params.get('sudo', False):
        if not data.get('agent_mode', False):
            return True
    return False

# ============================================================================
# ROUTE: Execute MCP Tool
# ============================================================================

@app.route('/api/shenron/execute-tool', methods=['POST'])
def execute_tool():
    """
    Execute MCP tool directly (requires Agent Mode)
    
    Request:
    {
        "tool": "read_file",
        "vm_ip": "<VM150_IP>",
        "params": {"file_path": "/var/www/index.html"},
        "agent_mode": true
    }
    """
    data = request.json

    audit_log('tool_attempt', {
        'ip': request.remote_addr,
        'tool': data.get('tool'),
        'vm_ip': data.get('vm_ip'),
        'params': data.get('params', {}),
        'agent_mode': data.get('agent_mode', False)
    })

    tool = data.get('tool')
    vm_ip = data.get('vm_ip')
    params = data.get('params', {})
    agent_mode = data.get('agent_mode', False)

    # SECURITY: Sudo must require agent_mode
    if require_agent_mode_sudo(data):
        audit_log('sudo_denied', {
            'ip': request.remote_addr,
            'tool': tool,
            'vm_ip': vm_ip,
            'command': params.get('command')
        })
        return jsonify({
            'success': False,
            'error': 'Sudo operations require Agent Mode and 2FA.'
        }), 403

    # Security check
    command = params.get('command') if tool == 'run_command' else None
    allowed, reason = ToolPermissions.check_permission(tool, command, agent_mode)

    # Additional command validation for run_command
    if tool == 'run_command' and command:
        cmd_valid, cmd_reason = validate_command(command)
        if not cmd_valid:
            audit_log('command_blocked', {
                'ip': request.remote_addr,
                'tool': tool,
                'vm_ip': vm_ip,
                'command': command,
                'reason': cmd_reason
            })
            return jsonify({
                'success': False,
                'error': f'Permission denied: {cmd_reason}'
            }), 403

    # File path validation for read_file, write_file
    if tool in ['read_file', 'write_file']:
        file_path = params.get('file_path')
        if file_path:
            path_valid, path_reason = validate_file_path(file_path)
            if not path_valid:
                audit_log('path_blocked', {
                    'ip': request.remote_addr,
                    'tool': tool,
                    'vm_ip': vm_ip,
                    'file_path': file_path,
                    'reason': path_reason
                })
                return jsonify({
                    'success': False,
                    'error': f'Permission denied: {path_reason}'
                }), 403

    if not allowed:
        audit_log('permission_denied', {
            'ip': request.remote_addr,
            'tool': tool,
            'vm_ip': vm_ip,
            'reason': reason
        })
        return jsonify({
            'success': False,
            'error': f'Permission denied: {reason}'
        }), 403

    # Execute tool
    try:
        if tool == 'read_file':
            result = mcp.read_file(vm_ip, params['file_path'], 
                                  params.get('offset', 0), params.get('limit'))
        
        elif tool == 'write_file':
            result = mcp.write_file(vm_ip, params['file_path'], 
                                   params['content'], params.get('append', False))
        
        elif tool == 'run_command':
            result = mcp.run_command(vm_ip, params['command'], 
                                    params.get('timeout', 30), params.get('sudo', False))
        
        elif tool == 'list_directory':
            result = mcp.list_directory(vm_ip, params['directory'])
        
        elif tool == 'search_files':
            result = mcp.search_files(vm_ip, params['pattern'], 
                                     params.get('directory', '/'))
        
        elif tool == 'get_system_info':
            result = mcp.get_system_info(vm_ip)
        
        else:
            audit_log('unknown_tool', {
                'ip': request.remote_addr,
                'tool': tool,
                'vm_ip': vm_ip
            })
            return jsonify({
                'success': False,
                'error': f'Unknown tool: {tool}'
            }), 400
        
        audit_log('tool_success', {
            'ip': request.remote_addr,
            'tool': tool,
            'vm_ip': vm_ip,
            'result': 'success'
        })
        return jsonify(result)
    
    except Exception as e:
        audit_log('tool_failure', {
            'ip': request.remote_addr,
            'tool': tool,
            'vm_ip': vm_ip,
            'error': str(e)
        })
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


# ============================================================================
# ROUTE: Grant Wish (Enhanced with MCP)
# ============================================================================

@app.route('/api/shenron/grant-wish', methods=['POST'])
def grant_wish():
    """
    Main SHENRON endpoint - now with MCP tool detection
    
    If query is an MCP request → Execute tool directly
    If query is a question → Query 6 warriors + synthesize
    """
    data = request.json
    query = data.get('query', '')
    agent_mode = data.get('agent_mode', False)
    
    if not query:
        return jsonify({
            'wish_granted': False,
            'error': 'No query provided'
        }), 400
    
    # Check if this is an MCP tool request
    mcp_request = parse_mcp_request(query)
    
    if mcp_request['is_mcp_request']:
        # Execute MCP tool
        tool = mcp_request['tool']
        vm_ip = mcp_request['vm_ip']
        params = mcp_request['params']

        audit_log('wish_attempt', {
            'ip': request.remote_addr,
            'tool': tool,
            'vm_ip': vm_ip,
            'params': params,
            'agent_mode': agent_mode
        })
        
        # Security check
        command = params.get('command') if tool == 'run_command' else None
        allowed, reason = ToolPermissions.check_permission(tool, command, agent_mode)

        # Additional command validation for run_command
        if tool == 'run_command' and command:
            cmd_valid, cmd_reason = validate_command(command)
            if not cmd_valid:
                audit_log('wish_command_blocked', {
                    'ip': request.remote_addr,
                    'tool': tool,
                    'vm_ip': vm_ip,
                    'command': command,
                    'reason': cmd_reason
                })
                return jsonify({
                    'wish_granted': False,
                    'error': f'🔐 {cmd_reason}',
                    'hint': 'Enable Agent Mode with 2FA to execute commands'
                })

        # File path validation for read_file, write_file
        if tool in ['read_file', 'write_file']:
            file_path = params.get('file_path')
            if file_path:
                path_valid, path_reason = validate_file_path(file_path)
                if not path_valid:
                    audit_log('wish_path_blocked', {
                        'ip': request.remote_addr,
                        'tool': tool,
                        'vm_ip': vm_ip,
                        'file_path': file_path,
                        'reason': path_reason
                    })
                    return jsonify({
                        'wish_granted': False,
                        'error': f'🔐 {path_reason}',
                        'hint': 'Access denied to sensitive file path'
                    })

        # Sudo must require agent_mode
        if tool == 'run_command' and params.get('sudo', False) and not agent_mode:
            audit_log('wish_sudo_denied', {
                'ip': request.remote_addr,
                'tool': tool,
                'vm_ip': vm_ip,
                'command': command
            })
            return jsonify({
                'wish_granted': False,
                'error': '🔐 Sudo operations require Agent Mode and 2FA.',
                'hint': 'Enable Agent Mode with 2FA to execute sudo commands'
            })

        if not allowed:
            audit_log('wish_permission_denied', {
                'ip': request.remote_addr,
                'tool': tool,
                'vm_ip': vm_ip,
                'reason': reason
            })
            return jsonify({
                'wish_granted': False,
                'error': f'🔐 {reason}',
                'hint': 'Enable Agent Mode with 2FA to execute commands'
            })
        
        # Execute tool
        try:
            if tool == 'read_file':
                result = mcp.read_file(vm_ip, **params)
            elif tool == 'run_command':
                result = mcp.run_command(vm_ip, **params)
            elif tool == 'list_directory':
                result = mcp.list_directory(vm_ip, **params)
            elif tool == 'search_files':
                result = mcp.search_files(vm_ip, **params)
            elif tool == 'get_system_info':
                result = mcp.get_system_info(vm_ip)
            
            # Format response
            if result['success']:
                audit_log('wish_success', {
                    'ip': request.remote_addr,
                    'tool': tool,
                    'vm_ip': vm_ip
                })
                return jsonify({
                    'wish_granted': True,
                    'synthesized_answer': format_mcp_response(tool, result),
                    'mcp_tool_used': tool,
                    'vm_ip': vm_ip,
                    'raw_result': result
                })
            else:
                audit_log('wish_tool_failed', {
                    'ip': request.remote_addr,
                    'tool': tool,
                    'vm_ip': vm_ip,
                    'error': result.get('error', 'Tool execution failed')
                })
                return jsonify({
                    'wish_granted': False,
                    'error': result.get('error', 'Tool execution failed'),
                    'mcp_tool_used': tool
                })
        
        except Exception as e:
            audit_log('wish_exception', {
                'ip': request.remote_addr,
                'tool': tool,
                'vm_ip': vm_ip,
                'error': str(e)
            })
            return jsonify({
                'wish_granted': False,
                'error': str(e)
            })
    
    else:
        # Standard SHENRON query (existing logic)
        # Query 6 warriors, synthesize response, etc.
        # (Keep existing code here)
        
        return jsonify({
            'wish_granted': False,
            'error': 'Standard SHENRON logic not yet migrated in this example',
            'hint': 'Use MCP tool syntax like: "read file /path/to/file on VM150"'
        })


def format_mcp_response(tool: str, result: dict) -> str:
    """Format MCP tool result into user-friendly response"""
    
    if tool == 'read_file':
        lines = result.get('content', '').count('\n') + 1
        return f"""✅ **File Read Successfully**

📄 **File:** {result.get('file_path', 'N/A')}  
📏 **Lines:** {result.get('lines', lines)}  
📦 **Size:** {result.get('file_size', 'N/A')} bytes

**Content:**