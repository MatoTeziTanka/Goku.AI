# 🔧 VM101 Quick Fixes

## Issue 1: API Syntax Error ✅ FIXED

**Error:** `SyntaxError: invalid syntax` at line 1  
**Cause:** HTML comments (`<!-- -->`) at the top of the Python file

**Fix:**
```bash
cd ~/GitHub/Goku.AI

# Remove the first 5 lines (HTML comments)
sed -i '1,5d' src/api/shenron_api_v5_mcp.py

# Or use the automated script
chmod +x scripts/fix_api_syntax.sh
bash scripts/fix_api_syntax.sh
```

**Verify:**
```bash
python3 -m py_compile src/api/shenron_api_v5_mcp.py
# Should return no errors
```

---

## Issue 2: Missing Verification Script

**Error:** `can't open file 'scripts/verify_infrastructure.py'`  
**Cause:** Script wasn't committed to GitHub

**Fix:** The script exists locally but needs to be committed. For now, create it manually:

```bash
cd ~/GitHub/Goku.AI/scripts

cat > verify_infrastructure.py << 'EOF'
#!/usr/bin/env python3
"""
Infrastructure Verification Script
Run this on VM101 to verify everything is ready for Goku.AI
"""

import os
import sys
import subprocess
import requests
from pathlib import Path

# Colors for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def check_python():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"  {GREEN}✅ Python {version.major}.{version.minor}.{version.micro}{RESET}")
        return True
    else:
        print(f"  {RED}❌ Python {version.major}.{version.minor} - Need 3.10+{RESET}")
        return False

def check_dependencies():
    """Check if required packages are installed."""
    print("\n📦 Checking dependencies...")
    required = ['flask', 'flask_cors', 'requests', 'paramiko', 'pydantic']
    missing = []
    
    for package in required:
        try:
            __import__(package.replace('-', '_'))
            print(f"  {GREEN}✅ {package}{RESET}")
        except ImportError:
            print(f"  {RED}❌ {package} - MISSING{RESET}")
            missing.append(package)
    
    if missing:
        print(f"\n  {YELLOW}💡 Install missing: pip3 install {' '.join(missing)}{RESET}")
        return False
    return True

def check_file_structure():
    """Check if required files exist."""
    print("\n📁 Checking file structure...")
    repo_root = Path.cwd()
    required_files = [
        'src/api/shenron_api_v5_mcp.py',
        'src/utils/mcp_tools.py',
        'src/config/settings.py',
    ]
    
    all_exist = True
    for file_path in required_files:
        full_path = repo_root / file_path
        if full_path.exists():
            print(f"  {GREEN}✅ {file_path}{RESET}")
        else:
            print(f"  {RED}❌ {file_path} - NOT FOUND{RESET}")
            all_exist = False
    
    return all_exist

def check_vm100_connectivity():
    """Check if VM100 (LM Studio) is reachable."""
    print("\n🌐 Checking VM100 connectivity...")
    
    vm100_ip = os.getenv('VM100_IP', '192.168.12.100')
    
    # Test LM Studio API
    lm_studio_url = f"http://{vm100_ip}:1234/v1/models"
    try:
        response = requests.get(lm_studio_url, timeout=5)
        if response.status_code == 200:
            models = response.json().get('data', [])
            print(f"  {GREEN}✅ LM Studio API responding{RESET}")
            print(f"  {GREEN}   Models loaded: {len(models)}{RESET}")
            return True
        else:
            print(f"  {RED}❌ LM Studio API returned status {response.status_code}{RESET}")
            return False
    except Exception as e:
        print(f"  {RED}❌ Cannot connect to LM Studio: {e}{RESET}")
        return False

def main():
    print("=" * 70)
    print("GOKU.AI INFRASTRUCTURE VERIFICATION".center(70))
    print("=" * 70)
    print()
    
    checks = [
        ("Python Version", check_python),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("VM100 Connectivity", check_vm100_connectivity),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  {RED}❌ Error during {name}: {e}{RESET}")
            results.append((name, False))
    
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY".center(70))
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"  {name:30} {status}")
    
    print()
    print(f"Results: {passed}/{total} checks passed")
    
    if passed == total:
        print(f"\n{GREEN}🎉 ALL CHECKS PASSED - Ready to start API!{RESET}")
        return 0
    else:
        print(f"\n{YELLOW}⚠️  Some checks failed - Review issues above{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
EOF

chmod +x verify_infrastructure.py
```

---

## Quick Fix Commands (Run All at Once)

```bash
cd ~/GitHub/Goku.AI

# Fix API syntax
sed -i '1,5d' src/api/shenron_api_v5_mcp.py

# Verify API syntax
python3 -m py_compile src/api/shenron_api_v5_mcp.py && echo "✅ API syntax OK"

# Set VM100 IP
export VM100_IP=192.168.12.100

# Test API import
python3 -c "import sys; sys.path.insert(0, '.'); from src.api.shenron_api_v5_mcp import app; print('✅ API imports successfully')"

# If import works, start the API
python3 src/api/shenron_api_v5_mcp.py
```

---

## Next Steps After Fixes

1. ✅ Fix API syntax (remove HTML comments)
2. ✅ Set environment variable: `export VM100_IP=192.168.12.100`
3. ✅ Install dependencies if needed: `pip3 install flask flask-cors requests paramiko pydantic`
4. ✅ Test API: `python3 src/api/shenron_api_v5_mcp.py`

The API should start on port 5000 and be accessible at `http://192.168.12.101:5000`

