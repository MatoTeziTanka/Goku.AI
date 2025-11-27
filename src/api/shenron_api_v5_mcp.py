"""
SHENRON API v5.0 - ULTRA INSTINCT
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
With MCP Tools Integration

Extends SHENRON with file operations, terminal access, and autonomous capabilities.
"""

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from datetime import datetime
# Import MCP tools - adjust path based on your structure
try:
    from src.utils.mcp_tools import MCPTools, ToolPermissions
except ImportError:
    try:
        from src.mcp_tools import MCPTools, ToolPermissions
    except ImportError:
        from mcp_tools import MCPTools, ToolPermissions

app = Flask(__name__)
CORS(app)

# Initialize MCP tools
mcp = MCPTools()

# LM Studio API endpoint
# [CONFIG] Update VM100_IP in environment or credentials.json
VM100_IP = os.getenv('VM100_IP', '192.168.12.100')
LM_STUDIO_API = f"http://{VM100_IP}:1234/v1/chat/completions"

# Warrior configurations
# [NOTE] Model names match LM Studio display names (with -instruct@q8_0 suffix)
# LM Studio will match partial names, but using full names is more reliable
WARRIORS = {
    "goku": {
        "model": "Goku-deepseek-coder-v2-lite-instruct@q8_0",  # Full name from LM Studio
        "model_short": "deepseek-coder-v2-lite",  # Fallback short name
        "emoji": "🥋", 
        "temp": 0.7
    },
    "vegeta": {
        "model": "Vegeta-llama-3.2-3b-instruct@q8_0",
        "model_short": "llama-3.2-3b",
        "emoji": "👑", 
        "temp": 0.3
    },
    "piccolo": {
        "model": "Piccolo-qwen2.5-coder-7b-instruct@q8_0",
        "model_short": "qwen2.5-coder-7b",
        "emoji": "🧠", 
        "temp": 0.5
    },
    "gohan": {
        "model": "Gohan-mistral-7b-instruct-v0.3@q8_0",
        "model_short": "mistral-7b",
        "emoji": "⚠️", 
        "temp": 0.4
    },
    "krillin": {
        "model": "Krillin-phi-3-mini-128k-instruct@q8_0",
        "model_short": "phi-3-mini-128k",
        "emoji": "🔧", 
        "temp": 0.6
    },
    "frieza": {
        "model": "Frieza-phi-3-mini-128k-instruct@q8_0",  # Same model as Krillin, different instance
        "model_short": "phi-3-mini-128k",
        "emoji": "😈", 
        "temp": 0.9
    }
}

def get_model_name(warrior: str) -> str:
    """
    Get the model name for a warrior.
    Tries full name first, falls back to short name if LM Studio doesn't match.
    """
    config = WARRIORS.get(warrior.lower())
    if not config:
        return "deepseek-coder-v2-lite"  # Default fallback
    
    # Try full name first (more reliable)
    return config.get("model", config.get("model_short", "deepseek-coder-v2-lite"))


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
        import re
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
        import re
        cmd_match = re.search(r"['\"](.+?)['\"]", query)
        if cmd_match:
            return {
                'is_mcp_request': True,
                'tool': 'run_command',
                'vm_ip': vm_ip,
                'params': {'command': cmd_match.group(1)}
            }
    
    elif any(word in query_lower for word in ['list', 'ls', 'show directory']):
        import re
        path_match = re.search(r'in ([/\\][\w/.\\-]+)', query)
        directory = path_match.group(1) if path_match else '/'
        return {
            'is_mcp_request': True,
            'tool': 'list_directory',
            'vm_ip': vm_ip,
            'params': {'directory': directory}
        }
    
    elif 'search' in query_lower or 'grep' in query_lower or 'find' in query_lower:
        import re
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
    
    tool = data.get('tool')
    vm_ip = data.get('vm_ip')
    params = data.get('params', {})
    agent_mode = data.get('agent_mode', False)
    
    # Security check
    command = params.get('command') if tool == 'run_command' else None
    allowed, reason = ToolPermissions.check_permission(tool, command, agent_mode)
    
    if not allowed:
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
            return jsonify({
                'success': False,
                'error': f'Unknown tool: {tool}'
            }), 400
        
        return jsonify(result)
    
    except Exception as e:
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
        
        # Security check
        command = params.get('command') if tool == 'run_command' else None
        allowed, reason = ToolPermissions.check_permission(tool, command, agent_mode)
        
        if not allowed:
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
                return jsonify({
                    'wish_granted': True,
                    'synthesized_answer': format_mcp_response(tool, result),
                    'mcp_tool_used': tool,
                    'vm_ip': vm_ip,
                    'raw_result': result
                })
            else:
                return jsonify({
                    'wish_granted': False,
                    'error': result.get('error', 'Tool execution failed'),
                    'mcp_tool_used': tool
                })
        
        except Exception as e:
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
        lines = result['content'].count('\n') + 1
        return f"""✅ **File Read Successfully**

📄 **File:** {result.get('file_path', 'N/A')}  
📏 **Lines:** {result['lines']}  
📦 **Size:** {result['file_size']} bytes

**Content:**
```
{result['content'][:500]}
{'...' if len(result['content']) > 500 else ''}
```

✨ *Your wish has been granted!*"""
    
    elif tool == 'run_command':
        return f"""✅ **Command Executed Successfully**

⚡ **Command:** `{result['command']}`  
⏱️ **Time:** {result['execution_time']:.2f}s  
🔢 **Exit Code:** {result['exit_code']}

**Output:**
```
{result['stdout']}
```

{'⚠️ **Errors:**\n```\n' + result['stderr'] + '\n```' if result['stderr'] else ''}

✨ *Your wish has been granted!*"""
    
    elif tool == 'list_directory':
        files_str = '\n'.join(f"📄 {f}" for f in result['files'][:10])
        dirs_str = '\n'.join(f"📁 {d}" for d in result['directories'][:10])
        
        return f"""✅ **Directory Listed Successfully**

📊 **Total:** {result['total']} items

**Directories:**
{dirs_str}

**Files:**
{files_str}

{'...' if result['total'] > 20 else ''}

✨ *Your wish has been granted!*"""
    
    elif tool == 'search_files':
        matches_str = '\n'.join(
            f"📄 {m['file']}:{m['line']} - {m['content'][:80]}"
            for m in result['matches'][:10]
        )
        
        return f"""✅ **Search Complete**

🔍 **Found:** {result['total_matches']} matches

**Results:**
{matches_str}

{'...' if result['total_matches'] > 10 else ''}

✨ *Your wish has been granted!*"""
    
    elif tool == 'get_system_info':
        return f"""✅ **System Information**

🖥️ **Hostname:** {result['hostname']}  
⚡ **CPU:** {result['cpu_usage']:.1f}%  
💾 **Memory:** {result['memory_usage']:.1f}%  
💿 **Disk:** {result['disk_usage']:.1f}%  
⏱️ **Uptime:** {result['uptime']}

✨ *Your wish has been granted!*"""
    
    return str(result)


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'operational',
        'service': 'SHENRON v5.0 - Ultra Instinct',
        'features': ['rag', 'synthesis', 'agent_mode', 'mcp_tools'],
        'dragon_awakened': True
    })


# ============================================================================
# START SERVER
# ============================================================================

if __name__ == '__main__':
    print("""
╔═══════════════════════════════════════════════════════════════╗
║  🐉⚡ SHENRON ULTRA INSTINCT - v5.0                          ║
║  MCP Tools Enabled: File, Terminal, System Access             ║
║  Port: 5000                                                    ║
║  Status: AWAKENED                                              ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    app.run(host='0.0.0.0', port=5000, debug=True)

