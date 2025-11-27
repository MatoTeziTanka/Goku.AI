<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔧 TROUBLESHOOTING GUIDE

**Solutions to common issues during and after v1.0.0 deployment**

---

## 🚀 QUICK DIAGNOSTICS

### Check Deployment Status
```bash
# View deployment summary
tail -50 ~/.vm101-deployment/MASTER-DEPLOYMENT-EXECUTOR-*.log | grep -E "SUMMARY|SUCCESS|FAILED"

# Check all task statuses
for f in ~/.vm101-deployment/TASK-*.log; do
    echo "=== $(basename $f) ==="
    tail -3 "$f" | grep -E "SUCCESS|FAILED|ERROR"
done

# Count errors
grep -c ERROR ~/.vm101-deployment/*.log || echo "No errors"
```

### Quick SSH Test
```bash
# Test SSH config validity
ssh -G vm120-proxy | head -5

# Test SSH connection
ssh -vvv vm120-proxy "hostname" 2>&1 | head -20

# Check key permissions
ls -la ~/.ssh/vm-keys/vm120_key
# Should show: -rw------- (600)
```

### Service Status Check
```bash
# Check critical services
systemctl status docker
systemctl status code-server
systemctl status ssh

# Check if ports are listening
netstat -tlnp | grep -E "22|9001|2375"
```

---

## ❌ COMMON ISSUES & SOLUTIONS

### Issue 1: SSH Connection Refused

**Symptom:**
```
Permission denied (publickey).
```

**Cause:**
- Key not added to target VM's authorized_keys
- Wrong key being used
- Permissions incorrect

**Solution:**

**Step 1: Verify key was deployed**
```bash
ssh vm120 "cat ~/.ssh/authorized_keys"
# Should show your vm120_key content
```

**Step 2: If not there, deploy manually**
```bash
# Get the public key
cat ~/.ssh/vm-keys/vm120_key.pub

# SSH with password (if available)
ssh proxy1@<VM120_IP>

# On the VM, add the key
cat >> ~/.ssh/authorized_keys << 'EOF'
[PASTE_YOUR_PUBLIC_KEY_HERE]
EOF

chmod 600 ~/.ssh/authorized_keys
exit
```

**Step 3: Test connection**
```bash
ssh vm120-proxy "hostname"
# Should work now
```

---

### Issue 2: SSH Connection Timeout

**Symptom:**
```
ssh: connect to host <VM120_IP> port 22: Connection timed out
```

**Cause:**
- VM not running or unreachable
- Network connectivity issue
- Firewall blocking SSH
- SSH service not running on target VM

**Solution:**

**Step 1: Check VM is running**
```bash
ping <VM120_IP>
# If no response: VM is down or unreachable
# Power on VM and wait for boot
```

**Step 2: Check network path**
```bash
traceroute <VM120_IP>
# Should show path to VM
```

**Step 3: Check SSH service on target VM**
```bash
# Try SSH with more verbose output
ssh -vv vm120 "echo test"
# Look for error messages

# If you can access VM via RDP/console:
# - Linux: systemctl status ssh
# - Windows: Get-Service sshd (check if Running)
```

**Step 4: Check local firewall**
```bash
sudo ufw status
# Check if port 22 is ALLOW

# If blocked, allow it:
sudo ufw allow 22/tcp
```

---

### Issue 3: Docker Not Running

**Symptom:**
```
Cannot connect to Docker daemon at unix:///var/run/docker.sock
```

**Cause:**
- Docker service stopped
- Docker socket not accessible
- Docker not installed

**Solution:**

```bash
# Check Docker status
systemctl status docker

# If not running, start it
sudo systemctl start docker

# Enable auto-start
sudo systemctl enable docker

# Verify it's running
docker ps

# If Docker daemon crashed, check logs
journalctl -u docker | tail -30
```

---

### Issue 4: code-server Not Accessible

**Symptom:**
```
Cannot reach http://localhost:9001
Connection refused
```

**Cause:**
- code-server service not running
- Port 9001 in use by another process
- Firewall blocking port

**Solution:**

```bash
# Check if running
systemctl status code-server

# If not running, start it
sudo systemctl start code-server

# Check port
netstat -tlnp | grep 9001
# Should show: code-server listening on :9001

# If port in use by something else
sudo lsof -i :9001
# Kill the process using that port

# Try accessing again
curl http://localhost:9001
```

---

### Issue 5: Keys Already Exist Error

**Symptom:**
```
✅ Key for VM120 already exists, skipping...
```

**Cause:**
- Key already generated from previous run
- Script designed to avoid overwriting

**Solution:**

**Option A: Use existing keys (Recommended)**
```bash
# Keys already exist, just deploy them
~/add-vm-keys.sh
~/test-vm-keys.sh
```

**Option B: Regenerate keys**
```bash
# BACKUP first!
cp -r ~/.ssh/vm-keys ~/.ssh/vm-keys.backup

# Remove old keys
rm ~/.ssh/vm-keys/vm120_key*

# Re-run setup
chmod +x ~/VM101-SEPARATE-KEYS-SETUP.sh
~/VM101-SEPARATE-KEYS-SETUP.sh

# Deploy new keys
~/add-vm-keys.sh
```

---

### Issue 6: SSH Config Not Applied

**Symptom:**
```
Host key not found in known_hosts
```

**Cause:**
- SSH config not loaded
- SSH trying different keys

**Solution:**

```bash
# Verify SSH config exists
cat ~/.ssh/config | head -20
# Should show Host entries

# Verify SSH is using config
ssh -G vm120-proxy | grep -i identityfile
# Should show: ~/.ssh/vm-keys/vm120_key

# Force SSH to use specific key
ssh -i ~/.ssh/vm-keys/vm120_key proxy1@<VM120_IP>

# If that works, SSH config issue
# Verify config syntax
ssh -T -v vm120-proxy 2>&1 | grep -i "config"
```

---

### Issue 7: Windows SSH Not Working

**Symptom:**
```
ssh vm100-goku
Permission denied (publickey).
```

**Cause:**
- Windows SSH Server not running
- PowerShell key deployment failed
- Key format incompatible

**Solution:**

**Option A: Use RDP to add key manually**
1. Connect to Windows VM via RDP
2. Open PowerShell as Administrator
3. Run:
```powershell
$key = Get-Content "$env:USERPROFILE\.ssh\vm-keys\vm100_key.pub"
$sshDir = "C:\Users\Administrator\.ssh"
if (!(Test-Path $sshDir)) {
    New-Item -ItemType Directory -Path $sshDir -Force | Out-Null
}
Add-Content -Path "$sshDir\authorized_keys" -Value $key
icacls "$sshDir\authorized_keys" /inheritance:r /grant "Administrator:F"
```

**Option B: Check Windows SSH Service**
1. Connect via RDP
2. Open Services (services.msc)
3. Look for "OpenSSH SSH Server"
4. If not running, right-click → Start
5. Set to "Automatic" for auto-start

**Option C: Use RDP as fallback**
- Keep RDP configured as backup
- SSH is optional for Windows VMs

---

### Issue 8: Failed SSH Attempts Too High

**Symptom:**
```
[ALERT] 5 failed SSH attempts detected
```

**Cause:**
- Brute force attempt
- Wrong password being tried
- Monitoring system working correctly (expected on first run)

**Solution:**

```bash
# Check what triggered alert
cat ~/.vm101-deployment/monitoring/alerts.log

# View failed attempts
tail -20 /var/log/auth.log | grep "Failed password"

# If brute force detected:
# 1. Add firewall rule to limit SSH
sudo ufw limit 22/tcp

# 2. Check for compromised credentials
ssh vm120 "w"  # See who's logged in

# 3. Change SSH port (optional)
# Edit /etc/ssh/sshd_config
# Change: Port 22 → Port 2222
# Restart SSH: sudo systemctl restart ssh
```

---

### Issue 9: Monitoring Not Working

**Symptom:**
```
Alert log not being updated
Cron job not running
```

**Cause:**
- Cron job not installed
- Monitoring script has syntax error
- Permissions incorrect

**Solution:**

```bash
# Check cron job
crontab -l | grep monitoring
# Should show monitoring cron entry

# If missing, reinstall
# Re-run Task 1.5
~/VM101-DEPLOYMENT-PACKAGE-v1.0.0/TASK-1.5-SETUP-MONITORING.sh

# Check monitoring script
ls -la ~/.vm101-deployment/monitoring/
# Should show: ssh-alert-checker.sh (with execute permission)

# Test monitoring script manually
~/.vm101-deployment/monitoring/ssh-alert-checker.sh

# Check for script errors
bash -n ~/.vm101-deployment/monitoring/ssh-alert-checker.sh
# Should show no syntax errors
```

---

### Issue 10: Need to Rollback

**Symptom:**
```
Something went wrong, need to revert
```

**Solution:**

**Step 1: Run rollback script**
```bash
./ROLLBACK.sh

# Answer prompts:
# Continue with rollback? (yes/no): yes
# Restore from /path/backup? (yes/no): yes
# Remove vm-keys directory? (yes/no): yes
```

**Step 2: Verify rollback**
```bash
# Test old SSH keys still work
ssh vm120 "hostname"
# Should work with old key

# Verify old SSH config
cat ~/.ssh/config | head -5
```

**Step 3: After rollback**
- SSH should work with original keys
- Services should still be running
- Can re-run deployment when ready

---

## 🔍 DIAGNOSTIC COMMANDS

### View All Deployment Logs
```bash
# Search for errors across all logs
grep -r ERROR ~/.vm101-deployment/ | head -20

# Search for warnings
grep -r WARN ~/.vm101-deployment/ | head -20

# Get summary
echo "=== ERRORS ===" && grep -c ERROR ~/.vm101-deployment/*.log || echo 0
echo "=== WARNINGS ===" && grep -c WARN ~/.vm101-deployment/*.log || echo 0
echo "=== SUCCESS ===" && grep -c SUCCESS ~/.vm101-deployment/*.log || echo 0
```

### Check SSH Key Integrity
```bash
# Verify key files exist
ls -la ~/.ssh/vm-keys/

# Check key fingerprints
ssh-keygen -l -f ~/.ssh/vm-keys/vm120_key.pub

# Test key works
ssh-keygen -y -f ~/.ssh/vm-keys/vm120_key > /dev/null
# No error = key is valid
```

### Monitor Real-Time SSH Activity
```bash
# Watch SSH logs in real-time
tail -f /var/log/auth.log | grep sshd

# Count SSH connections
grep "Accepted" /var/log/auth.log | wc -l

# List failed attempts
grep "Failed password" /var/log/auth.log | tail -10
```

### System Health Check
```bash
# Full system status
echo "=== UPTIME ===" && uptime
echo "=== DISK ===" && df -h /
echo "=== MEMORY ===" && free -h
echo "=== LOAD ===" && cat /proc/loadavg
echo "=== TOP PROCESSES ===" && ps aux --sort=-%cpu | head -5
```

---

## 🆘 GETTING MORE HELP

### Collect Diagnostics Package
```bash
# Create diagnostics archive
mkdir -p ~/diagnostics-${TIMESTAMP}

# Copy key logs
cp ~/.vm101-deployment/*.log ~/diagnostics-${TIMESTAMP}/
cp /var/log/auth.log ~/diagnostics-${TIMESTAMP}/auth.log.backup
cp ~/.ssh/config ~/diagnostics-${TIMESTAMP}/ssh-config.backup

# Copy service status
systemctl status docker > ~/diagnostics-${TIMESTAMP}/docker-status.txt 2>&1
systemctl status code-server > ~/diagnostics-${TIMESTAMP}/code-server-status.txt 2>&1
netstat -tlnp > ~/diagnostics-${TIMESTAMP}/netstat.txt 2>&1

# Create archive
tar -czf diagnostics-${TIMESTAMP}.tar.gz ~/diagnostics-${TIMESTAMP}/

# Share/review
echo "Diagnostics package: ~/diagnostics-${TIMESTAMP}.tar.gz"
```

### Check Zencoder Documentation
1. Review `VM101-v1.0.0-RELEASE-NOTES.md`
2. Check `DEPLOYMENT-EXECUTION-GUIDE.md`
3. Review `POST-DEPLOYMENT-CHECKLIST.md`
4. Verify logs in `~/.vm101-deployment/`

### Manual Verification Steps
```bash
# 1. SSH config is valid
ssh -T -v vm120-proxy 2>&1 | head -10

# 2. Key permissions are correct
find ~/.ssh/vm-keys -name "*_key" -exec ls -la {} \;

# 3. Services are running
systemctl status docker code-server ssh

# 4. Network is accessible
ping -c 3 <VM120_IP>

# 5. Monitoring is active
ps aux | grep monitoring
```

---

## 📞 SUPPORT RESOURCES

- **Release Notes:** `VM101-v1.0.0-RELEASE-NOTES.md`
- **Execution Guide:** `DEPLOYMENT-EXECUTION-GUIDE.md`
- **Verification Checklist:** `POST-DEPLOYMENT-CHECKLIST.md`
- **Deployment Logs:** `~/.vm101-deployment/`
- **System Logs:** `/var/log/auth.log`, `/var/log/syslog`
- **Monitoring Logs:** `~/.vm101-deployment/monitoring/`

---

**Still stuck? Rollback and try again!** 

```bash
./ROLLBACK.sh  # Safe to run anytime
```
