#!/usr/bin/env python
import re

filepath = "C:/Users/sethp/Documents/Github/VM101-DEPLOYMENT-PACKAGE-v1.0.0/TASK-1.2-DEPLOY-KEYS-LINUX.sh"

with open(filepath, 'rb') as f:
    content = f.read().decode('utf-8', errors='replace')

lines = content.split('\n')

print("="*60)
print("SEARCHING FOR load_vm_config FUNCTION DEFINITION")
print("="*60)

function_found = False
for i, line in enumerate(lines):
    if re.match(r'^\s*load_vm_config\s*\(\s*\)', line):
        print(f"FOUND at line {i+1}: {line.strip()}")
        function_found = True
        for j in range(i, min(i+20, len(lines))):
            print(f"  {lines[j]}")

if not function_found:
    print("NOT FOUND - Function load_vm_config() is NOT defined in this file!")
    print("\nSearching for references to load_vm_config:")
    for i, line in enumerate(lines):
        if 'load_vm_config' in line:
            print(f"  Line {i+1}: {line.strip()}")

print("\n" + "="*60)
print("CHECKING CONFIG_FILE")
print("="*60)

for i, line in enumerate(lines):
    if 'CONFIG_FILE=' in line:
        print(f"Line {i+1}: {line.strip()}")
