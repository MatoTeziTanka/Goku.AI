#!/bin/bash
# Complete v3.0.0 Integration Script
# Run this on VM101 to complete all integration steps

set -e

cd ~/GitHub/Goku.AI

echo "======================================================================"
echo "COMPLETE v3.0.0 INTEGRATION"
echo "======================================================================"
echo

# Step 1: Integrate Master Prompt
echo "Step 1: Integrating Master Prompt into API..."
python3 scripts/integrate_master_prompt_v3.py
if [ $? -ne 0 ]; then
    echo "❌ Master Prompt integration failed"
    exit 1
fi
echo

# Step 2: Create Warrior State Machines
echo "Step 2: Creating Warrior State Machines..."
python3 scripts/create_warrior_states.py
if [ $? -ne 0 ]; then
    echo "❌ State machine creation failed"
    exit 1
fi
echo

# Step 3: Complete Ports Registry
echo "Step 3: Completing Ports Registry..."
chmod +x scripts/complete_ports_registry.sh
bash scripts/complete_ports_registry.sh
echo

# Step 4: Verify integration
echo "Step 4: Verifying integration..."
echo "Checking files..."

if grep -q "MASTER_PROMPT" src/api/shenron_api_v5_mcp.py; then
    echo "  ✅ Master Prompt integrated in API"
else
    echo "  ❌ Master Prompt not found in API"
fi

if [ -f "src/services/warrior_states.py" ]; then
    echo "  ✅ Warrior state machines created"
else
    echo "  ❌ Warrior state machines not found"
fi

if [ -f "docs/infrastructure/PORTS_REGISTRY.md" ]; then
    echo "  ✅ Ports Registry updated"
else
    echo "  ❌ Ports Registry not found"
fi

echo
echo "======================================================================"
echo "INTEGRATION COMPLETE"
echo "======================================================================"
echo
echo "Next steps:"
echo "  1. Test API: python3 src/api/shenron_api_v5_mcp.py"
echo "  2. Verify Master Prompt is loaded"
echo "  3. Test state machines: python3 -c 'from src.services.warrior_states import get_state_manager; print(get_state_manager())'"
echo

