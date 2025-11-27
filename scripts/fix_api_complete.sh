#!/bin/bash
# Complete fix for API file on VM101
# This script ensures the API file is correct

cd ~/GitHub/Goku.AI

echo "Fixing API file..."

# Backup original
cp src/api/shenron_api_v5_mcp.py src/api/shenron_api_v5_mcp.py.backup

# Check if file starts with HTML comments and remove them
if head -1 src/api/shenron_api_v5_mcp.py | grep -q '^<!--'; then
    echo "Removing HTML comments..."
    sed -i '1,5d' src/api/shenron_api_v5_mcp.py
fi

# Verify syntax
echo "Checking syntax..."
python3 -m py_compile src/api/shenron_api_v5_mcp.py 2>&1

if [ $? -eq 0 ]; then
    echo "✅ Syntax is valid!"
    rm src/api/shenron_api_v5_mcp.py.backup
    exit 0
else
    echo "❌ Syntax error detected. Restoring from git..."
    git checkout src/api/shenron_api_v5_mcp.py
    python3 -m py_compile src/api/shenron_api_v5_mcp.py
    if [ $? -eq 0 ]; then
        echo "✅ File restored and syntax is valid!"
        exit 0
    else
        echo "❌ Still has errors. Check the file manually."
        exit 1
    fi
fi

