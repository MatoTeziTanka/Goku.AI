import sys

files = [
    "C:/Users/sethp/Documents/Github/VM101-DEPLOYMENT-PACKAGE-v1.0.0/TASK-1.3-TEST-WINDOWS.sh",
    "C:/Users/sethp/Documents/Github/VM101-DEPLOYMENT-PACKAGE-v1.0.0/TASK-1.2-DEPLOY-KEYS-LINUX.sh"
]

for file_path in files:
    print(f"\n{'='*60}\n FILE: {file_path}\n{'='*60}\n")
    try:
        with open(file_path, encoding='utf-8', errors='replace') as f:
            print(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")
