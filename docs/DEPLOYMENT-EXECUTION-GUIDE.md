<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🎯 DEPLOYMENT EXECUTION GUIDE - v1.0.0

**How to Execute the Zencoder v1.0.0 Deployment**

---

## ⏰ Timeline

- **Total Deployment Time:** 2-3 hours
- **Actual Execution:** ~1.5-2 hours (machine-time)
- **Your Time:** ~30 minutes (monitoring + decisions)

---

## 🚀 QUICK START (Copy & Paste)

```bash
# 1. Navigate to deployment package
cd ~/VM101-DEPLOYMENT-PACKAGE-v1.0.0/

# 2. Make all scripts executable
chmod +x *.sh

# 3. Run master deployment
./MASTER-DEPLOYMENT-EXECUTOR.sh

# 4. Answer prompts as they appear
# (Just follow the screen prompts)

# 5. After completion, verify
./QC-VERIFY-ALL.sh
```

---

## 📋 STEP-BY-STEP EXECUTION

### Step 0: Preparation

Before starting, ensure:

- [ ] Connected to VM101 via SSH
- [ ] Have deployment package extracted locally
- [ ] All target VMs are powered on and accessible
- [ ] Docker is running on VM101
- [ ] Network connectivity confirmed

**Pre-Deployment Check:**
```bash
# Check you're on VM101
hostname
# Should show: goku (or your VM101 hostname)

# Check SSH access to at least one VM
ssh vm120 "hostname"
# Should succeed without password (or you have password)

# Check Docker is running
docker ps
# Should show: "CONTAINER ID" header
```

### Step 1: Extract Package to VM101

**From Your Local Machine:**
```bash
# Copy package to VM101 (adjust path/IP as needed)
scp -r VM101-DEPLOYMENT-PACKAGE-v1.0.0/ mgmt1@<VM101_IP>:~/

# OR if already extracted, just navigate to it
ssh mgmt1@<VM101_IP>
cd ~/VM101-DEPLOYMENT-PACKAGE-v1.0.0/
```

**On VM101:**
```bash
# Navigate to package
cd ~/VM101-DEPLOYMENT-PACKAGE-v1.0.0/

# Verify files
ls -la
# Should show:
# - MASTER-DEPLOYMENT-EXECUTOR.sh
# - TASK-1.1-*.sh through TASK-1.5-*.sh
# - QC-VERIFY-ALL.sh
# - ROLLBACK.sh
# - All documentation files
```

### Step 2: Make Scripts Executable

```bash
chmod +x *.sh
```

### Step 3: Run Master Deployment

```bash
./MASTER-DEPLOYMENT-EXECUTOR.sh
```

**You'll see:**
```
╔════════════════════════════════════════════════════════════════════╗
║                  ZENCODER v1.0.0 DEPLOYMENT                        ║
║                   Master Execution Script                          ║
...
```

### Step 4: Confirm Deployment

When prompted:
```
Continue with deployment? (yes/no):
```

Type: `yes` and press Enter

### Step 5: Monitor Execution

The script will now execute all 5 tasks in sequence:

**Task 1.1 - Execute Setup Script** (~30 min)
- Generates SSH keys for all VMs
- Creates SSH config
- Creates helper scripts
- **You should see:** ✅ All setup complete messages

**Task 1.2 - Deploy Keys to Linux VMs** (~45 min)
- Deploys vm120_key to VM120
- Deploys vm150_key to VM150
- Tests connectivity
- **You may see prompts:** asking if you want to deploy to VM160/170/180
- **Answer:** `yes` or `no` based on your needs

**Task 1.3 - Test Windows Deployment** (~30 min)
- Tests Windows VM connectivity
- Attempts PowerShell key deployment
- **You may see:** ⚠️ warnings about manual RDP setup (this is OK)

**Task 1.4 - Verify All Services** (~30 min)
- Checks Docker running
- Checks code-server accessible
- Checks firewall, network, Python
- **You should see:** ✅ All services verified

**Task 1.5 - Setup Basic Monitoring** (~30 min)
- Sets up SSH logging
- Configures alert system
- Installs monitoring scripts
- **You should see:** ✅ Monitoring system ready

### Step 6: Handle Failures (If Any)

If any task fails:

```
❌ FAILED: Task 1.X - Description
Continue after failure? (yes/no):
```

**Options:**
1. **Yes** - Continue to next task (script may have partially succeeded)
2. **No** - Stop and investigate

**To investigate:**
```bash
# Check the task log
tail ~/.vm101-deployment/TASK-1.X-*.log

# Check specific errors
grep ERROR ~/.vm101-deployment/TASK-1.X-*.log

# Fix issue
# Then either:
# a) Re-run that task individually
# b) Run rollback and restart
```

### Step 7: Final Summary

After all tasks complete, you'll see:

```
==========================================
DEPLOYMENT SUMMARY
==========================================
Successful Tasks: 5
Failed Tasks: 0

✅ All deployment tasks completed successfully!
```

### Step 8: Post-Deployment Verification

Run the QC verification script:

```bash
./QC-VERIFY-ALL.sh
```

**Expected output:**
```
╔════════════════════════════════════════════════════════════════════╗
║              ZENCODER v1.0.0 QC VERIFICATION                       ║
...
✅ PASS: SSH config exists
✅ PASS: Key directory exists
...
RESULTS:
  ✅ PASS: 12
  ⚠️  WARN: 2
  ❌ FAIL: 0

✅ ALL CRITICAL CHECKS PASSED
```

### Step 9: Test SSH Access

Test new SSH aliases:

```bash
# Test VM120 (Proxy)
ssh vm120-proxy "hostname"
# Should show: proxy1-vm120 (or similar)

# Test VM150 (WordPress)
ssh vm150-wordpress "hostname"
# Should show: wordpress-vm150 (or similar)

# Test VM100 (AI Host) - may fail if not deployed
ssh vm100-goku "hostname"
# May show error (expected on Windows if not deployed)
```

### Step 10: Review Logs

Check deployment logs:

```bash
# View all deployment logs
ls -la ~/.vm101-deployment/

# View master log
tail ~/.vm101-deployment/MASTER-DEPLOYMENT-EXECUTOR-*.log

# View task logs
tail ~/.vm101-deployment/TASK-1.*.log

# View monitoring setup
cat ~/.vm101-deployment/monitoring/MONITORING-SUMMARY.txt
```

---

## ⚙️ TROUBLESHOOTING DURING EXECUTION

### Task Hangs / Timeout

If a task appears to hang:

```bash
# In another terminal, check what's happening
ssh vm120 "hostname"  # Test if VM is responsive

# If VM is unresponsive:
# 1. Wait a bit longer (task may still be running)
# 2. Check network connectivity
# 3. Power-cycle the VM if unresponsive
# 4. Press Ctrl+C to stop current task
# 5. Check logs for errors
```

### SSH Connection Failures

If SSH commands fail:

```bash
# Check if key was deployed
ssh vm120 "cat ~/.ssh/authorized_keys | grep vm120"

# Test with verbose output
ssh -vv vm120 "hostname"

# Check key file
ls -la ~/.ssh/vm-keys/
```

### Windows VM Issues

Windows deployment commonly has issues:

**Option A: Use RDP**
- Connect via RDP to Windows VM
- Manually add SSH key
- See guide in Task 1.3 output

**Option B: Use SSH with password**
- If Windows SSH is set up, will prompt for password
- Enter password when prompted

**Option C: Skip for now**
- Complete Linux VMs first
- Return to Windows later

### Services Not Running

If Docker or code-server aren't running:

```bash
# Check Docker
systemctl status docker

# Restart if needed
sudo systemctl restart docker

# Check code-server
systemctl status code-server

# Restart if needed
sudo systemctl restart code-server
```

---

## 🔄 IF YOU NEED TO ROLLBACK

If something went wrong:

```bash
# Run rollback script
./ROLLBACK.sh

# Follow prompts
# - Confirm rollback (type 'yes')
# - Confirm restoration (type 'yes')
# - Choose whether to remove vm-keys directory

# After rollback completes
# Test old SSH keys still work
ssh vm120 "hostname"  # Should work with old key
```

---

## ✅ SUCCESS CRITERIA

You're done when:

- [ ] All 5 tasks completed (or mostly completed)
- [ ] QC verification shows mostly ✅ PASS
- [ ] SSH aliases work: `ssh vm120-proxy`, `ssh vm150-wordpress`
- [ ] Services still running: Docker, code-server
- [ ] Logs clean and reviewed
- [ ] No critical ❌ FAIL items

**If any above is false:**
- Review logs
- Check troubleshooting guide
- Fix issues
- Re-run QC verification

---

## 📊 WHAT GETS CREATED

After successful deployment:

**On VM101 Local Files:**
```
~/.ssh/
├── vm-keys/
│   ├── vm100_key, vm100_key.pub
│   ├── vm120_key, vm120_key.pub
│   ├── vm150_key, vm150_key.pub
│   └── ... (one pair per VM)
└── config              # Updated with new entries

~/.vm101-deployment/    # Log files
├── TASK-*.log
├── QC-*.log
├── monitoring/
│   ├── ssh-monitor.log
│   ├── ssh-failed-attempts.log
│   ├── alerts.log
│   └── MONITORING-SUMMARY.txt
└── ... (various logs)
```

**On Each Target VM:**
```
~/.ssh/
└── authorized_keys    # Now contains just the vm-specific key
```

---

## 🎓 NEXT STEPS

After successful deployment:

1. **Keep the logs** - Save deployment logs somewhere
2. **Document your setup** - Note any special configuration
3. **Set monitoring** - Check alerts.log regularly
4. **Test periodically** - Ensure SSH still works
5. **Plan rotation** - Schedule key rotation (quarterly recommended)

---

## 📞 STILL HAVING ISSUES?

1. **Check logs first:**
   ```bash
   tail -100 ~/.vm101-deployment/TASK-1.*.log | grep ERROR
   ```

2. **Review Troubleshooting Guide:**
   ```bash
   cat TROUBLESHOOTING-GUIDE.md
   ```

3. **Check specific error:**
   ```bash
   grep -i "error\|failed\|cannot" ~/.vm101-deployment/*.log
   ```

4. **If needed, rollback:**
   ```bash
   ./ROLLBACK.sh
   ```

---

**Happy Deploying! 🚀**

For detailed troubleshooting, see `TROUBLESHOOTING-GUIDE.md`.
