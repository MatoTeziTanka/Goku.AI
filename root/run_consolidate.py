#!/usr/bin/env python3
import subprocess
import sys

# Run the consolidation script
result = subprocess.run([sys.executable, "consolidate_goku_ai_files.py"], 
                       cwd=r"C:\Users\sethp\Documents\Github",
                       capture_output=False)

sys.exit(result.returncode)

