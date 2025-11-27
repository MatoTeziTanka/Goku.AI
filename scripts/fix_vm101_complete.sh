#!/bin/bash
# Complete fix script for VM101
# Fixes API syntax, imports, and sets up environment

set -e

cd ~/GitHub/Goku.AI

echo "======================================================================"
echo "COMPLETE VM101 FIX SCRIPT"
echo "======================================================================"
echo

# 1. Restore API file from git (clean version)
echo "1. Restoring API file from git..."
git checkout src/api/shenron_api_v5_mcp.py
echo "   ✅ API file restored"

# 2. Verify syntax
echo
echo "2. Verifying syntax..."
python3 -m py_compile src/api/shenron_api_v5_mcp.py
if [ $? -eq 0 ]; then
    echo "   ✅ Syntax is valid"
else
    echo "   ❌ Syntax error - manual fix required"
    exit 1
fi

# 3. Set environment variable
echo
echo "3. Setting environment variables..."
export VM100_IP=192.168.12.100
echo "   ✅ VM100_IP=192.168.12.100"
echo "   💡 Add to ~/.bashrc: echo 'export VM100_IP=192.168.12.100' >> ~/.bashrc"

# 4. Create virtual environment for dependencies
echo
echo "4. Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ✅ Virtual environment already exists"
fi

# 5. Install dependencies
echo
echo "5. Installing dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install flask flask-cors requests paramiko pydantic
echo "   ✅ Dependencies installed"

# 6. Check file structure
echo
echo "6. Checking file structure..."
if [ -f "src/mcp_tools.py" ]; then
    echo "   ✅ Found src/mcp_tools.py"
elif [ -f "src/utils/mcp_tools.py" ]; then
    echo "   ✅ Found src/utils/mcp_tools.py"
else
    echo "   ⚠️  mcp_tools.py not found - may need to create symlink or adjust import"
fi

# 7. Test import
echo
echo "7. Testing API import..."
python3 -c "
import sys
sys.path.insert(0, '.')
try:
    from src.api.shenron_api_v5_mcp import app, WARRIORS
    print('   ✅ API imports successfully')
    print(f'   ✅ Warriors configured: {len(WARRIORS)}')
except Exception as e:
    print(f'   ❌ Import failed: {e}')
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    echo
    echo "======================================================================"
    echo "✅ ALL FIXES COMPLETE!"
    echo "======================================================================"
    echo
    echo "Next steps:"
    echo "  1. Activate venv: source venv/bin/activate"
    echo "  2. Set VM100_IP: export VM100_IP=192.168.12.100"
    echo "  3. Start API: python3 src/api/shenron_api_v5_mcp.py"
    echo
else
    echo
    echo "======================================================================"
    echo "⚠️  SOME ISSUES REMAIN"
    echo "======================================================================"
    echo "Please review errors above"
fi

