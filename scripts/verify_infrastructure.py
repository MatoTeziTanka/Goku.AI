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
        'docs/infrastructure/PORTS_REGISTRY.md'
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
    
    # Get VM100 IP from environment or prompt
    vm100_ip = os.getenv('VM100_IP') or os.getenv('SHENRON_URL', '').replace('http://', '').replace(':1234', '')
    
    if not vm100_ip:
        print(f"  {YELLOW}⚠️  VM100_IP not set in environment{RESET}")
        print(f"  {YELLOW}   Set it: export VM100_IP=<your_vm100_ip>{RESET}")
        return False
    
    # Test ping
    try:
        result = subprocess.run(
            ['ping', '-c', '1', vm100_ip] if sys.platform != 'win32' else ['ping', '-n', '1', vm100_ip],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            print(f"  {GREEN}✅ VM100 ({vm100_ip}) is reachable{RESET}")
        else:
            print(f"  {RED}❌ VM100 ({vm100_ip}) - PING FAILED{RESET}")
            return False
    except Exception as e:
        print(f"  {YELLOW}⚠️  Could not test ping: {e}{RESET}")
    
    # Test LM Studio API
    lm_studio_url = f"http://{vm100_ip}:1234/v1/models"
    try:
        response = requests.get(lm_studio_url, timeout=5)
        if response.status_code == 200:
            models = response.json().get('data', [])
            print(f"  {GREEN}✅ LM Studio API responding{RESET}")
            print(f"  {GREEN}   Models loaded: {len(models)}{RESET}")
            if models:
                print(f"  {GREEN}   Available: {', '.join([m.get('id', 'unknown')[:20] for m in models[:3]])}...{RESET}")
            return True
        else:
            print(f"  {RED}❌ LM Studio API returned status {response.status_code}{RESET}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"  {RED}❌ Cannot connect to LM Studio at {lm_studio_url}{RESET}")
        print(f"  {YELLOW}   Make sure LM Studio server is running on VM100{RESET}")
        return False
    except Exception as e:
        print(f"  {RED}❌ Error: {e}{RESET}")
        return False

def check_environment_variables():
    """Check if critical environment variables are set."""
    print("\n🔐 Checking environment variables...")
    
    critical_vars = {
        'SHENRON_URL': 'http://<VM100_IP>:1234',
        'VM100_IP': '<VM100_IP>'
    }
    
    optional_vars = [
        'BINANCE_API_KEY',
        'BINANCE_API_SECRET',
        'VM150_PASSWORD'
    ]
    
    all_set = True
    for var in critical_vars:
        value = os.getenv(var)
        if value and '<' not in value:
            print(f"  {GREEN}✅ {var}{RESET}")
        else:
            print(f"  {YELLOW}⚠️  {var} - Not set or placeholder{RESET}")
            print(f"     Expected: {critical_vars[var]}")
            all_set = False
    
    for var in optional_vars:
        value = os.getenv(var)
        if value:
            print(f"  {GREEN}✅ {var} (set){RESET}")
        else:
            print(f"  {YELLOW}⚠️  {var} - Not set (optional){RESET}")
    
    return all_set

def check_api_import():
    """Check if API can be imported."""
    print("\n🔌 Checking API import...")
    try:
        sys.path.insert(0, str(Path.cwd()))
        from src.api.shenron_api_v5_mcp import app, WARRIORS
        print(f"  {GREEN}✅ API imports successfully{RESET}")
        print(f"  {GREEN}   Warriors configured: {len(WARRIORS)}{RESET}")
        for warrior, config in WARRIORS.items():
            print(f"     - {warrior}: {config.get('model', 'unknown')}")
        return True
    except Exception as e:
        print(f"  {RED}❌ API import failed: {e}{RESET}")
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
        ("Environment Variables", check_environment_variables),
        ("API Import", check_api_import),
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
        print(f"\nNext step: python3 src/api/shenron_api_v5_mcp.py")
        return 0
    else:
        print(f"\n{YELLOW}⚠️  Some checks failed - Review issues above{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

