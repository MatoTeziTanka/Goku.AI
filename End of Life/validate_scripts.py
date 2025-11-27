#!/usr/bin/env python
import re

files = {
    "TASK-1.2-DEPLOY-KEYS-LINUX.sh": "C:/Users/sethp/Documents/Github/VM101-DEPLOYMENT-PACKAGE-v1.0.0/TASK-1.2-DEPLOY-KEYS-LINUX.sh",
    "TASK-1.3-TEST-WINDOWS.sh": "C:/Users/sethp/Documents/Github/VM101-DEPLOYMENT-PACKAGE-v1.0.0/TASK-1.3-TEST-WINDOWS.sh"
}

for filename, filepath in files.items():
    print(f"\n{'='*60}\nValidating: {filename}\n{'='*60}\n")
    
    with open(filepath, 'rb') as f:
        content = f.read().decode('utf-8', errors='replace')
    
    lines = content.split('\n')
    
    print(f"Total lines: {len(lines)}")
    
    if filename == "TASK-1.2-DEPLOY-KEYS-LINUX.sh":
        if 'load_vm_config()' in content:
            matches = [i+1 for i, line in enumerate(lines) if 'load_vm_config' in line]
            print(f"\nload_vm_config references at lines: {matches[:5]}")
        else:
            print("\n❌ ISSUE: load_vm_config() function NOT FOUND - but it's called in deploy_from_config()")
    
    if 'CONFIG_FILE=' in content:
        for i, line in enumerate(lines):
            if 'CONFIG_FILE=' in line:
                print(f"\nCONFIG_FILE set at line {i+1}: {line.strip()}")
                break
    else:
        print("\n❌ ISSUE: CONFIG_FILE variable not defined")
    
    if filename == "TASK-1.3-TEST-WINDOWS.sh":
        hardcoded = [i+1 for i, line in enumerate(lines) if re.search(r'192\.168\.12\.\d+', line) and 'test_windows_vm' not in line]
        if hardcoded:
            print(f"\nHardcoded IPs found at lines: {hardcoded[:5]}")
    
    has_set_e = any('-e' in line and 'set' in line for line in lines[:5])
    print(f"\n✅ Error handling (set -e): {has_set_e}")
