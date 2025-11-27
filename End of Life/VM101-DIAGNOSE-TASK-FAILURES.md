<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Diagnose Task 1.2 and 1.3 Failures

**On VM101, run these commands:**

## Check Task 1.2 Logs (Linux Deployment)

```bash
# Find Task 1.2 log
ls -la ~/.vm101-deployment/TASK-1.2-*.log

# Read the log
cat ~/.vm101-deployment/TASK-1.2-*.log

# Check for specific errors
grep -i error ~/.vm101-deployment/TASK-1.2-*.log
grep -i "failed\|cannot\|unable" ~/.vm101-deployment/TASK-1.2-*.log
```

## Check Task 1.3 Logs (Windows Deployment)

```bash
# Find Task 1.3 log
ls -la ~/.vm101-deployment/TASK-1.3-*.log

# Read the log
cat ~/.vm101-deployment/TASK-1.3-*.log

# Check for specific errors
grep -i error ~/.vm101-deployment/TASK-1.3-*.log
grep -i "failed\|cannot\|unable" ~/.vm101-deployment/TASK-1.3-*.log
```

## Verify Keys Were Generated

```bash
# Check if keys exist
ls -la ~/.ssh/vm-keys/

# Should see keys like:
# vm100_key, vm120_key, vm150_key, etc.
```

## Test SSH Connectivity Manually

```bash
# Test if you can still SSH to VMs with old key
ssh -i ~/.ssh/id_rsa proxy1@<VM120_IP> "echo 'VM120 accessible'"

# Test with new key (should fail until deployed)
ssh -i ~/.ssh/vm-keys/vm120_key proxy1@<VM120_IP> "echo 'VM120 accessible'"
```

## Common Issues

1. **SSH connectivity problems** - VMs not accessible
2. **Old key still required** - Need to use old key to deploy new key
3. **Permission issues** - Can't write to authorized_keys on target VMs
4. **Network issues** - Firewall blocking SSH

## Quick Fix: Manual Deployment

If automatic deployment failed, you can manually deploy keys:

```bash
# For Linux VM (example: VM120)
cat ~/.ssh/vm-keys/vm120_key.pub | ssh -i ~/.ssh/id_rsa proxy1@<VM120_IP> "mkdir -p ~/.ssh && chmod 700 ~/.ssh && cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"

# Then test
ssh -i ~/.ssh/vm-keys/vm120_key proxy1@<VM120_IP> "echo 'Success'"
```



