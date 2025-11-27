<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
#!/bin/bash
# VM101 SSH Access Test Script
# Tests SSH connectivity to all VMs in the infrastructure

echo "========================================="
echo "VM101 SSH Access Test"
echo "========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test results
PASSED=0
FAILED=0
RESULTS=()

# Function to test SSH access
test_ssh() {
    local vm_name=$1
    local user=$2
    local host=$3
    local port=${4:-22}
    
    echo -n "Testing $vm_name ($user@$host:$port)... "
    
    # Test SSH connection with timeout
    if timeout 5 ssh -o ConnectTimeout=3 -o BatchMode=yes -o StrictHostKeyChecking=no -p $port $user@$host "hostname && whoami" 2>/dev/null; then
        echo -e "${GREEN}✅ PASSED${NC}"
        ((PASSED++))
        RESULTS+=("✅ $vm_name ($user@$host:$port) - PASSED")
        return 0
    else
        echo -e "${RED}❌ FAILED${NC}"
        ((FAILED++))
        RESULTS+=("❌ $vm_name ($user@$host:$port) - FAILED")
        return 1
    fi
}

# Test all VMs
echo "Testing SSH access to all VMs..."
echo ""

# VM100 - Windows Server 2025
test_ssh "VM100 (Windows)" "Administrator" "<VM100_IP>" "22"

# VM120 - Reverse Proxy
test_ssh "VM120 (Reverse Proxy)" "proxy1" "<VM120_IP>" "22"

# VM150 - WordPress/Web Server
test_ssh "VM150 (WordPress)" "wp1" "<VM150_IP>" "22"

# VM160 - Database
test_ssh "VM160 (Database)" "dbs1" "<VM160_IP>" "22"

# VM170 - Game Servers
test_ssh "VM170 (Game Servers)" "gsh1" "<VM170_IP>" "22"

# VM180 - API Services
test_ssh "VM180 (API Services)" "apis1" "<VM180_IP>" "22"

# VM200 - Plex (Windows)
test_ssh "VM200 (Plex - Windows)" "Administrator" "<VM200_IP>" "22"

# VM203 - Desktop
test_ssh "VM203 (Desktop)" "mgmt1" "192.168.12.203" "22" 2>/dev/null || echo -e "${YELLOW}⚠️  VM203 - Not tested (user unknown)${NC}"

echo ""
echo "========================================="
echo "SSH Test Results Summary"
echo "========================================="
echo ""
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo ""

echo "Detailed Results:"
for result in "${RESULTS[@]}"; do
    echo "  $result"
done

echo ""
echo "========================================="

# Save results to file
{
    echo "=== SSH Access Test Results ==="
    echo "Date: $(date)"
    echo ""
    echo "Summary:"
    echo "  Passed: $PASSED"
    echo "  Failed: $FAILED"
    echo ""
    echo "Detailed Results:"
    for result in "${RESULTS[@]}"; do
        echo "  $result"
    done
} > ~/vm101-ssh-test-results.txt

echo "Results saved to: ~/vm101-ssh-test-results.txt"




