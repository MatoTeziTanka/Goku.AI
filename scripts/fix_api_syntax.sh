#!/bin/bash
# Quick fix for API syntax error on VM101

echo "Fixing API syntax error..."

cd ~/GitHub/Goku.AI

# Remove HTML comments from the beginning of the API file
sed -i '1,5d' src/api/shenron_api_v5_mcp.py

# Verify the fix
if head -1 src/api/shenron_api_v5_mcp.py | grep -q '"""'; then
    echo "✅ API file fixed!"
    echo "Testing syntax..."
    python3 -m py_compile src/api/shenron_api_v5_mcp.py
    if [ $? -eq 0 ]; then
        echo "✅ Syntax is valid!"
    else
        echo "❌ Still has syntax errors"
    fi
else
    echo "❌ Fix failed - file doesn't start with docstring"
fi

