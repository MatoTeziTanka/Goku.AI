<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# ✅ POST-DEPLOYMENT VERIFICATION CHECKLIST

**Use this checklist to verify successful v1.0.0 deployment**

---

## 🎯 IMMEDIATE POST-DEPLOYMENT (Right After Execution)

### Deployment Completion
- [ ] Master script completed without critical errors
- [ ] All 5 tasks executed
- [ ] Deployment logs available: `~/.vm101-deployment/`

**Log Location:**
```bash
ls -la ~/.vm101-deployment/
```

### SSH Keys Generated
- [ ] Key directory exists: `~/.ssh/vm-keys/`
- [ ] At least 3 VM key pairs generated
- [ ] Private keys have 600 permissions
- [ ] Public keys readable

**Verify:**
```bash
ls -la ~/.ssh/vm-keys/
# Should show: vm100_key vm100_key.pub vm120_key vm120_key.pub vm150_key vm150_key.pub ...
find ~/.ssh/vm-keys/ -name "*_key" -exec ls -l {} \;
# Should show: -rw------- (600 permissions)
```

### SSH Config Updated
- [ ] SSH config exists: `~/.ssh/config`
- [ ] Contains new Host entries for VMs
- [ ] SSH aliases configured

**Verify:**
```bash
cat ~/.ssh/config | head -20
# Should show: Host vm100-goku, Host vm120-proxy, etc.
```

---

## 🔐 SSH KEY DEPLOYMENT VERIFICATION

### Linux VMs (VM120, VM150)
- [ ] SSH access to VM120 works
- [ ] SSH access to VM150 works
- [ ] Can execute commands: `ssh vm120-proxy "hostname"`
- [ ] Public key in authorized_keys on each VM

**Verify VM120:**
```bash
ssh vm120-proxy "cat ~/.ssh/authorized_keys | grep vm120"
# Should return the vm120_key public key
```

**Verify VM150:**
```bash
ssh vm150-wordpress "cat ~/.ssh/authorized_keys | grep vm150"
# Should return the vm150_key public key
```

### Windows VMs (VM100, VM200)
- [ ] Windows SSH deployment attempted
- [ ] Key file prepared: `~/.ssh/vm-keys/vm100_key.pub`
- [ ] If deployed: can SSH to Windows VM
- [ ] If not deployed: RDP manual setup documented

**If SSH works:**
```bash
ssh vm100-goku "hostname"
# Should return Windows hostname
```

**If using RDP fallback:**
- [ ] RDP to Windows VM confirmed working
- [ ] SSH key manually added via PowerShell/RDP

---

## 🛠️ SERVICE VERIFICATION

### Docker
- [ ] Docker daemon running
- [ ] Docker responds to commands
- [ ] Docker containers can be managed

**Verify:**
```bash
docker ps
# Should show: CONTAINER ID header (even if no containers)

docker --version
# Should show: Docker X.X.X
```

### code-server
- [ ] code-server process running
- [ ] Accessible on port 9001
- [ ] Web UI loads without errors

**Verify:**
```bash
ps aux | grep code-server
# Should show: code-server process running

curl -s http://localhost:9001 | head -5
# Should return HTML content

# Or visit in browser: http://<VM101-IP>:9001
```

### SSH Service
- [ ] SSH daemon running
- [ ] SSH config valid (no syntax errors)
- [ ] Can connect to VMs via SSH

**Verify:**
```bash
systemctl status ssh
# Should show: active (running)

ssh -G vm120-proxy | head -10
# Should show SSH config for alias
```

### Python Environment
- [ ] Python 3 available
- [ ] Virtual environment exists
- [ ] Dependencies installed if needed

**Verify:**
```bash
python3 --version
# Should show: Python 3.X.X

ls ~/ai-workspace/ai-env/
# Should show: bin, lib, include, etc.
```

---

## 📊 NETWORK & CONNECTIVITY

### VM Reachability
- [ ] VM120 responds to ping/SSH
- [ ] VM150 responds to ping/SSH
- [ ] All critical VMs accessible

**Verify:**
```bash
ping -c 1 <VM120_IP>
ping -c 1 <VM150_IP>
ssh -o ConnectTimeout=5 vm120-proxy "echo OK"
```

### Firewall
- [ ] SSH port 22 accessible
- [ ] Docker port 2375 (if needed) accessible
- [ ] code-server port 9001 accessible
- [ ] No unexpected firewall blocks

**Verify:**
```bash
sudo ufw status
# Should show ports 22, 9001 ALLOW

netstat -tlnp | grep -E "22|9001|2375"
# Should show listening ports
```

### Network Interfaces
- [ ] Primary IP configured: <VM101_IP> (or assigned)
- [ ] Secondary IP working if applicable
- [ ] DNS resolution working

**Verify:**
```bash
ip addr show
# Should show eth0 (or network interface) with IP

nslookup <VM120_IP>
# Should resolve to hostname
```

---

## 📝 LOGGING & MONITORING

### Deployment Logs
- [ ] Task 1.1 log exists and contains no critical errors
- [ ] Task 1.2 log shows key deployments
- [ ] Task 1.3 log shows Windows test results
- [ ] Task 1.4 log shows service verifications
- [ ] Task 1.5 log shows monitoring setup

**Verify:**
```bash
ls -la ~/.vm101-deployment/TASK-*.log
# Should show all 5 task logs

grep -c "SUCCESS" ~/.vm101-deployment/TASK-*.log
# Should show high number of SUCCESS entries
```

### Monitoring System
- [ ] Monitoring directory created: `~/.vm101-deployment/monitoring/`
- [ ] Alert checker script installed
- [ ] Cron job configured
- [ ] Monitoring README present

**Verify:**
```bash
ls -la ~/.vm101-deployment/monitoring/
# Should show: ssh-alert-checker.sh, README.md, MONITORING-SUMMARY.txt

crontab -l | grep monitoring
# Should show cron job for monitoring

cat ~/.vm101-deployment/monitoring/MONITORING-SUMMARY.txt
```

### SSH Logging
- [ ] SSH connections logged
- [ ] Failed attempts logged
- [ ] Monitoring system active

**Verify:**
```bash
tail -5 /var/log/auth.log | grep sshd
# Should show recent SSH activity

test -f ~/.vm101-deployment/monitoring/alerts.log && echo "Alert log exists" || echo "Alert log not yet created"
```

---

## 🔍 SECURITY VERIFICATION

### Key Security
- [ ] Old shared keys backup exists: `~/.ssh/backup-YYYYMMDD_HHMMSS/`
- [ ] New per-VM keys isolated in `~/.ssh/vm-keys/`
- [ ] Key permissions correct (600 for private, 644 for public)
- [ ] No unauthorized keys in `~/.ssh/`

**Verify:**
```bash
ls -la ~/.ssh/backup-*/
# Should show backup of old configuration

ls -la ~/.ssh/vm-keys/
# Should show all vm_key pairs with correct permissions

ls -la ~/.ssh/ | grep -v "vm-keys\|config\|authorized\|known"
# Should not show suspicious files
```

### SSH Configuration Security
- [ ] SSH config has IdentitiesOnly=yes (prevents key enumeration)
- [ ] StrictHostKeyChecking=yes (prevents MITM)
- [ ] Known hosts updated for VMs

**Verify:**
```bash
grep "IdentitiesOnly" ~/.ssh/config
# Should show: yes

grep "StrictHostKeyChecking" ~/.ssh/config
# Should show: yes

cat ~/.ssh/known_hosts | wc -l
# Should show non-zero count
```

### Access Control
- [ ] Only mgmt1 user has SSH key access
- [ ] Root cannot use these keys
- [ ] Keys properly restricted in authorized_keys

**Verify:**
```bash
whoami
# Should show: mgmt1

sudo cat ~/.ssh/vm-keys/vm120_key 2>&1 | grep -q "denied" && echo "✅ Restricted" || echo "❌ May be accessible to sudo"
```

---

## 🧪 FUNCTIONAL TESTING

### SSH Alias Testing
- [ ] ssh vm120-proxy works
- [ ] ssh vm150-wordpress works
- [ ] ssh vm100-goku responds or shows expected error
- [ ] Can run commands via aliases

**Test:**
```bash
ssh vm120-proxy "hostname"
# Should return: proxy1-hostname

ssh vm150-wordpress "hostname"
# Should return: wordpress-hostname

ssh vm100-goku "hostname"
# Should work or show auth error (both expected)
```

### Deployment Helper Scripts
- [ ] test-vm-keys.sh exists and is executable
- [ ] add-vm-keys.sh exists and is executable
- [ ] remove-old-shared-keys.sh exists and is executable

**Test:**
```bash
chmod +x ~/add-vm-keys.sh ~/test-vm-keys.sh ~/remove-old-shared-keys.sh

# Run test script
~/test-vm-keys.sh
# Should show connection test results
```

### Orchestration Scripts
- [ ] Docker commands work: `docker ps`
- [ ] Code-server accessible via port 9001
- [ ] Python virtual environment activates
- [ ] Git repositories cloned (if applicable)

**Test:**
```bash
docker ps
code-server --version
python3 --version
ls -la ~/GitHub/ 2>/dev/null && echo "✅ Repos present" || echo "No GitHub clones found"
```

---

## 📋 PERFORMANCE CHECKS

### System Resource Usage
- [ ] CPU usage normal (< 50% idle)
- [ ] Memory usage reasonable (< 80% used)
- [ ] Disk space adequate (> 20% free)
- [ ] No zombie processes

**Check:**
```bash
top -b -n 1 | head -20
# Should show reasonable CPU/Memory usage

df -h
# Should show > 20% free space on main partition

ps aux | grep defunct | grep -v grep
# Should show no zombie processes
```

### Network Performance
- [ ] SSH latency acceptable (< 100ms)
- [ ] No packet loss to VMs
- [ ] Network interfaces operational

**Check:**
```bash
ping -c 5 <VM120_IP> | tail -2
# Should show 0% packet loss, reasonable latency

mtr -c 10 <VM150_IP> 2>&1 | tail -5
# Should show good connectivity
```

---

## 🎓 DOCUMENTATION REVIEW

### Deployment Documentation
- [ ] Release Notes reviewed: `VM101-v1.0.0-RELEASE-NOTES.md`
- [ ] Execution Guide reviewed: `DEPLOYMENT-EXECUTION-GUIDE.md`
- [ ] This checklist completed: `POST-DEPLOYMENT-CHECKLIST.md`
- [ ] Troubleshooting Guide available: `TROUBLESHOOTING-GUIDE.md`

**Review:**
```bash
head -50 VM101-v1.0.0-RELEASE-NOTES.md
head -50 DEPLOYMENT-EXECUTION-GUIDE.md
head -50 TROUBLESHOOTING-GUIDE.md
```

### Deployment Logs Documentation
- [ ] All task logs reviewed for errors
- [ ] Monitoring summary reviewed
- [ ] QC results understood
- [ ] Any warnings documented

**Review:**
```bash
grep -i "error\|failed\|critical" ~/.vm101-deployment/TASK-*.log
# Should show minimal errors

cat ~/.vm101-deployment/monitoring/MONITORING-SUMMARY.txt
```

---

## 🚨 ISSUES FOUND / REMEDIATION

If any checks failed, document here:

| Check | Status | Issue | Remediation |
|:------|:-------|:------|:------------|
| Example | ❌ | SSH to VM120 failed | Check VM120 network, restart SSH |
| | | | |
| | | | |

---

## ✅ FINAL APPROVAL

### Deployment Status
- [ ] All critical checks passed
- [ ] All service checks passed
- [ ] All security checks passed
- [ ] All functional tests passed

### Ready for Production?
- [ ] Yes, deployment successful ✅
- [ ] Partial success, issues documented
- [ ] Needs rollback and retry

### Sign-Off
- **Deployment Date:** ________________
- **Verified By:** ________________
- **Status:** ✅ Approved / ⚠️ Conditional / ❌ Failed

### Notes
```
[Deployment notes, issues found, resolutions, etc.]



```

---

## 🔄 NEXT ACTIONS

- [ ] Document any issues encountered
- [ ] Save all logs for future reference
- [ ] Schedule monitoring review (weekly)
- [ ] Plan key rotation (quarterly)
- [ ] Update infrastructure documentation
- [ ] Notify team of successful deployment
- [ ] Archive deployment package

---

**Deployment v1.0.0 Verification Complete** ✅

*Print this checklist and keep on file for audit purposes.*
