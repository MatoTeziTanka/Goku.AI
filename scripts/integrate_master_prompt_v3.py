#!/usr/bin/env python3
"""
Integrate Master Prompt v3.0.0 into SHENRON API
This script modifies shenron_api_v5_mcp.py to load and use the Master Prompt
"""

from pathlib import Path
import re

# Paths
REPO_ROOT = Path(__file__).parent.parent
API_FILE = REPO_ROOT / "src" / "api" / "shenron_api_v5_mcp.py"
MASTER_PROMPT_FILE = REPO_ROOT.parent / "MASTER_PROMPT_PRODUCTION.md"

def integrate_master_prompt():
    """Integrate Master Prompt into API file."""
    
    print("=" * 70)
    print("INTEGRATING MASTER PROMPT v3.0.0 INTO API".center(70))
    print("=" * 70)
    print()
    
    # 1. Check files exist
    if not API_FILE.exists():
        print(f"❌ API file not found: {API_FILE}")
        return False
    
    if not MASTER_PROMPT_FILE.exists():
        print(f"❌ Master Prompt not found: {MASTER_PROMPT_FILE}")
        print(f"   Expected location: {MASTER_PROMPT_FILE}")
        return False
    
    print(f"✅ Found API file: {API_FILE.name}")
    print(f"✅ Found Master Prompt: {MASTER_PROMPT_FILE.name}")
    print()
    
    # 2. Read current API file
    content = API_FILE.read_text(encoding='utf-8')
    
    # 3. Add Master Prompt loading at the top (after imports)
    master_prompt_loader = '''
# ============================================================================
# MASTER PROMPT v3.0.0 INTEGRATION
# ============================================================================

from pathlib import Path as PathLib

# Load Master Prompt as system context
MASTER_PROMPT_PATH = PathLib(__file__).parent.parent.parent.parent / "MASTER_PROMPT_PRODUCTION.md"
if MASTER_PROMPT_PATH.exists():
    MASTER_PROMPT = MASTER_PROMPT_PATH.read_text(encoding='utf-8')
else:
    # Fallback: try relative to repo root
    MASTER_PROMPT_PATH = PathLib(__file__).parent.parent.parent.parent.parent / "MASTER_PROMPT_PRODUCTION.md"
    if MASTER_PROMPT_PATH.exists():
        MASTER_PROMPT = MASTER_PROMPT_PATH.read_text(encoding='utf-8')
    else:
        MASTER_PROMPT = "# Master Prompt v3.0.0 - Not found, using fallback"
        print("⚠️  WARNING: Master Prompt not found, using fallback")

# Operational Modes (from Master Prompt v3.0.0)
OPERATIONAL_MODES = {
    "architect": "ARCHITECT MODE: Pure system design. No code. Focus on data flow, security boundaries (VM100 vs VM101), and scalability.",
    "coder": "CODER MODE (Goku/Vegeta): Strict v3.0.0 adherence. 100% test coverage. No prose, just logic. High performance.",
    "debug": "DEBUG MODE (Shenron): Root cause analysis. Log analysis. No new features, just fixes. Chain of Thought required.",
    "strategy": "STRATEGY MODE (Frieza): Business logic. Monetization. KPI tracking. Growth hacking.",
    "teaching": "TEACHING MODE (Gohan): Explain concepts using the Adaptive Explanations ladder (Expert -> Elementary)."
}

def get_system_message(mode: str = "coder") -> str:
    """Get system message with Master Prompt and operational mode."""
    mode_text = OPERATIONAL_MODES.get(mode.lower(), OPERATIONAL_MODES["coder"])
    return f"{MASTER_PROMPT}\\n\\n{mode_text}"

'''
    
    # Check if already integrated
    if "MASTER_PROMPT_PATH" in content:
        print("⚠️  Master Prompt already integrated (or similar code exists)")
        print("   Skipping integration to avoid duplicates")
        return True
    
    # Find insertion point (after imports, before app initialization)
    import_pattern = r"(from mcp_tools import.*?\n)"
    match = re.search(import_pattern, content, re.DOTALL)
    
    if match:
        insert_pos = match.end()
        new_content = content[:insert_pos] + master_prompt_loader + content[insert_pos:]
    else:
        # Fallback: insert after last import
        lines = content.split('\n')
        last_import = 0
        for i, line in enumerate(lines):
            if line.startswith('import ') or line.startswith('from '):
                last_import = i
        insert_pos = last_import + 1
        lines.insert(insert_pos, master_prompt_loader)
        new_content = '\n'.join(lines)
    
    # 4. Update warrior query function to use Master Prompt
    warrior_query_pattern = r'(payload = \{[^}]+"messages":\s*\[)'
    
    def add_master_prompt_to_payload(match):
        return match.group(1) + '''
            {
                "role": "system",
                "content": get_system_message("coder")
            },'''
    
    new_content = re.sub(warrior_query_pattern, add_master_prompt_to_payload, new_content, flags=re.DOTALL)
    
    # 5. Write updated file
    backup_file = API_FILE.with_suffix('.py.backup')
    API_FILE.rename(backup_file)
    print(f"📦 Created backup: {backup_file.name}")
    
    API_FILE.write_text(new_content, encoding='utf-8')
    print(f"✅ Updated: {API_FILE.name}")
    print()
    
    # 6. Verify syntax
    try:
        compile(new_content, str(API_FILE), 'exec')
        print("✅ Syntax check passed")
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        print("   Restoring backup...")
        backup_file.rename(API_FILE)
        return False
    
    print()
    print("=" * 70)
    print("✅ MASTER PROMPT INTEGRATION COMPLETE".center(70))
    print("=" * 70)
    print()
    print("Next steps:")
    print("  1. Test the API: python3 src/api/shenron_api_v5_mcp.py")
    print("  2. Verify Master Prompt is loaded in system messages")
    print()
    
    return True

if __name__ == "__main__":
    success = integrate_master_prompt()
    exit(0 if success else 1)

