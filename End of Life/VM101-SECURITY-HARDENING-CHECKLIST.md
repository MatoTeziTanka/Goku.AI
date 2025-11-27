# ✅ VM101 Security Hardening Checklist

**Purpose:** Ensure VM101 control node is hardened against attacks  
**Last Updated:** November 24, 2025  
**Status:** Pre-Deployment Security Verification

---

## 🎯 Checklist Organization

This checklist is organized by security layer and priority:
- **🔴 CRITICAL:** Must be completed before production deployment
- **🟠 HIGH:** Should be completed before production deployment
- **🟡 MEDIUM:** Should be completed within 30 days of deployment
- **🟢 LOW:** Should be completed within 90 days of deployment

---

## 🔴 CRITICAL SECURITY LAYER 1: VM101 Network Isolation

- [ ] **1.1: SSH Access Restricted to Local Network**
  - [ ] UFW firewall configured
  - [ ] Rule: `sudo ufw allow from 192.168.12.0/24 to any port 22`
  - [ ] Rule: `sudo ufw deny from any to any port 22`
  - **Verification:** `ssh user@external_ip` should be refused

- [ ] **1.2: Only Local Network Can Access SSH**
  - [ ] `sudo ufw status numbered | grep 22`
  - Should only allow from 192.168.12.0/24
  - **Verification:** External SSH attempts fail

- [ ] **1.3: Code-Server Port Restricted**
  - [ ] Code-server only accessible locally (or via VPN)
  - [ ] Rule: `sudo ufw allow from 192.168.12.0/24 to any port 9001`
  - [ ] Rule: `sudo ufw deny from any to any port 9001`
  - **Verification:** `ssh user@external_ip -p 9001` should be refused

- [ ] **1.4: Outbound SSH Only to Management Network**
  - [ ] VM101 can only SSH to 192.168.12.0/24
  - [ ] No outbound SSH to external networks
  - **Verification:** `ssh user@external_vm` from VM101 should fail

- [ ] **1.5: Physical or Secure Network Isolation**
  - [ ] VM101 on isolated VM network (not accessible from internet)
  - [ ] Proxmox management network separated from data networks
  - **Verification:** Proxmox network configuration reviewed

---

## 🔴 CRITICAL SECURITY LAYER 2: SSH Key Security

- [ ] **2.1: Separate SSH Keys Per VM (NOT Shared Keys)**
  - [ ] All 7 VMs have separate ed25519 keys
  - [ ] `ls -la ~/.ssh/vm-keys/ | wc -l` should show 14 (7 private + 7 public)
  - [ ] No shared keys used across multiple VMs
  - **Verification:** `ssh-keygen -lf ~/.ssh/vm-keys/vm120_key` shows unique fingerprints

- [ ] **2.2: SSH Private Key Permissions (600)**
  - [ ] `ls -la ~/.ssh/vm-keys/vm*_key` all show `-rw-------`
  - [ ] Not world-readable
  - **Verification:** `stat ~/.ssh/vm-keys/vm120_key | grep Access` shows `(0600)`

- [ ] **2.3: SSH Directory Permissions (700)**
  - [ ] `ls -lad ~/.ssh` shows `drwx------`
  - [ ] Not accessible to other users
  - **Verification:** `stat ~/.ssh | grep Access` shows `(0700)`

- [ ] **2.4: SSH Public Keys Only in authorized_keys**
  - [ ] Only `.pub` files shared with VMs
  - [ ] Never share private keys
  - **Verification:** `cat ~/.ssh/vm-keys/vm120_key | head -c 30` starts with `-----BEGIN`

- [ ] **2.5: No Shared/Default SSH Keys Used**
  - [ ] `~/.ssh/id_rsa` backed up or removed
  - [ ] `~/.ssh/id_ed25519` backed up or removed
  - [ ] Only VM-specific keys used
  - **Verification:** `ls -la ~/.ssh/id_* 2>/dev/null` shows no default keys

- [ ] **2.6: SSH Key Backup Exists**
  - [ ] Backup directory exists: `~/.ssh/backup-YYYYMMDD_HHMMSS/`
  - [ ] Contains copies of all keys before migration
  - [ ] Backup stored securely outside VM101
  - **Verification:** `ls -la ~/.ssh/backup-*/ | head -5`

---

## 🔴 CRITICAL SECURITY LAYER 3: One-Way Trust Model

- [ ] **3.1: VM101 → Other VMs Access Enabled**
  - [ ] VM101 can SSH to all 7 VMs
  - [ ] Each VM has VM101's public key in authorized_keys
  - **Verification:** `ssh vm120-proxy "echo test"` succeeds

- [ ] **3.2: Other VMs → VM101 Access BLOCKED**
  - [ ] No VM can SSH back to VM101
  - [ ] VM101 authorized_keys does NOT contain keys from other VMs
  - **Verification:** `cat ~/.ssh/authorized_keys | wc -l` should be 0 or contain only trusted external keys

- [ ] **3.3: SSH Config Enforces One-Way Trust**
  - [ ] `~/.ssh/config` has `IdentitiesOnly yes` for all hosts
  - [ ] Each VM only has its specific key in IdentityFile
  - **Verification:** `grep -c "IdentitiesOnly yes" ~/.ssh/config` should be 7 (one per VM)

- [ ] **3.4: No Reverse Tunnel Access**
  - [ ] VMs cannot create reverse SSH tunnels back to VM101
  - [ ] SSH reverse port forwarding disabled if possible
  - **Verification:** `sshd_config` on VMs has AllowTcpForwarding restricted

---

## 🟠 HIGH PRIORITY: API Security (VM100 → VM101 Communication)

- [ ] **4.1: API Input Validation**
  - [ ] All API endpoints validate input
  - [ ] No shell metacharacters allowed without escaping
  - [ ] Command injection prevention implemented
  - **Verification:** Review `/code-server/app/api/` files

- [ ] **4.2: Rate Limiting Enabled**
  - [ ] Redis-based rate limiting implemented
  - [ ] Configuration persists across restarts
  - [ ] Default: 60 requests/minute per IP
  - **Verification:** `curl -X POST http://vm101:5000/api/deploy` > 60 times returns 429

- [ ] **4.3: Authentication for API Calls**
  - [ ] API key or token required for deployments
  - [ ] All VM100→VM101 API calls include authentication
  - [ ] No unauthenticated deployments allowed
  - **Verification:** `curl http://vm101:5000/api/deploy` without auth returns 401

- [ ] **4.4: HTTPS/TLS for API Communication**
  - [ ] API uses HTTPS (not HTTP)
  - [ ] Valid TLS certificate installed
  - [ ] TLS 1.2 or higher
  - **Verification:** `curl https://vm101:5000/api/status --insecure` succeeds

- [ ] **4.5: Logging of All API Calls**
  - [ ] Every API call logged with timestamp, IP, and action
  - [ ] Failed attempts logged
  - [ ] Logs retention: 90 days minimum
  - **Verification:** `tail ~/.ssh/api-calls.log`

---

## 🟠 HIGH PRIORITY: SSH Access Hardening

- [ ] **5.1: SSH Timeout on Inactivity**
  - [ ] SSH config has `ServerAliveInterval 60`
  - [ ] SSH config has `ServerAliveCountMax 3`
  - [ ] Hangs after 180 seconds of inactivity
  - **Verification:** SSH to VM and wait 3+ minutes → connection closes

- [ ] **5.2: SSH ConnectTimeout Set**
  - [ ] `ConnectTimeout 10` in SSH config
  - [ ] Fails fast if VM is unreachable
  - [ ] No indefinite hanging
  - **Verification:** Try SSH to offline VM → fails in ~10 seconds

- [ ] **5.3: StrictHostKeyChecking Enabled**
  - [ ] `StrictHostKeyChecking yes` in SSH config
  - [ ] Man-in-the-middle attacks prevented
  - [ ] Must accept known_hosts first time
  - **Verification:** `ssh vm120-proxy "echo test"` succeeds (after first-time acceptance)

- [ ] **5.4: SSH Key Audit Logging**
  - [ ] Deployment log exists: `~/.ssh/key-deployment.log`
  - [ ] All key additions logged with timestamp
  - [ ] Successes and failures recorded
  - **Verification:** `tail ~/.ssh/key-deployment.log | grep -c SUCCESS`

- [ ] **5.5: SSH Duplicate Key Detection**
  - [ ] Script checks if key exists before adding
  - [ ] No duplicate keys in authorized_keys
  - [ ] Each key added only once per VM
  - **Verification:** `ssh vm120-proxy "cat ~/.ssh/authorized_keys" | sort | uniq -d`

---

## 🟠 HIGH PRIORITY: Monitoring & Alerting

- [ ] **6.1: Failed SSH Attempts Monitored**
  - [ ] Failed login attempts logged
  - [ ] Alert if > 5 failed attempts in 1 minute
  - [ ] Suspicious IPs rate-limited
  - **Verification:** Check syslog: `grep "Failed password" /var/log/auth.log | tail -10`

- [ ] **6.2: Key Rotation Scheduled**
  - [ ] Automated key rotation every 90 days
  - [ ] Crontab entry: `0 2 1 */3 * /home/mgmt1/rotate-vm-keys.sh`
  - [ ] Rotation log maintained
  - **Verification:** `cat ~/.ssh/key-rotation.log`

- [ ] **6.3: Suspicious Activity Alerts**
  - [ ] Alert on multiple failed SSH attempts
  - [ ] Alert on rate limit violations
  - [ ] Alert on unexpected API calls
  - **Verification:** Monitoring system configured

- [ ] **6.4: Log Retention Policy**
  - [ ] SSH logs retained 90 days minimum
  - [ ] API logs retained 90 days minimum
  - [ ] Key deployment logs retained 1 year
  - **Verification:** `find /var/log -name "auth.log*" | head -5`

---

## 🟡 MEDIUM PRIORITY: Access Control & Least Privilege

- [ ] **7.1: Restricted Shell for SSH Keys**
  - [ ] Consider using restricted shells for VM SSH keys
  - [ ] Or use command restrictions in authorized_keys
  - **Verification:** Check if restricted shell needed for compliance

- [ ] **7.2: SSH Command Restrictions**
  - [ ] Authorized_keys entries have command restrictions
  - [ ] Each VM key can only run specific commands
  - **Verification:** `cat ~/.ssh/authorized_keys | grep "^command="`

- [ ] **7.3: SELinux/AppArmor Hardening**
  - [ ] SELinux or AppArmor profiles created for SSH
  - [ ] Confines SSH process to minimal privileges
  - **Verification:** `getenforce` (SELinux) or `aa-enabled` (AppArmor)

- [ ] **7.4: Sudo Access Limited**
  - [ ] Sudo configured only for necessary commands
  - [ ] NOPASSWD used sparingly, if at all
  - [ ] Sudo access logged
  - **Verification:** `sudo -l` shows restricted commands

- [ ] **7.5: SSH Key Password Protection (Optional)**
  - [ ] Consider password-protecting SSH keys
  - [ ] Or use SSH agent for passphrase management
  - **Verification:** `ssh-keygen -p -f ~/.ssh/vm-keys/vm120_key`

---

## 🟡 MEDIUM PRIORITY: Backup & Disaster Recovery

- [ ] **8.1: SSH Keys Backed Up**
  - [ ] All keys in ~/.ssh/vm-keys/ backed up
  - [ ] Backups encrypted if stored remotely
  - [ ] Backup location outside VM101
  - **Verification:** `test -f /backup/vm-keys.tar.gz.enc && echo "OK"`

- [ ] **8.2: Backup Tested**
  - [ ] Restore procedure tested
  - [ ] Can restore keys from backup
  - [ ] Restore succeeds in < 30 minutes
  - **Verification:** Test restore on non-production system

- [ ] **8.3: Disaster Recovery Plan**
  - [ ] Documented process for key loss scenario
  - [ ] Roles assigned for emergency response
  - [ ] Recovery time objective (RTO) defined
  - **Verification:** Disaster recovery plan document exists

---

## 🟢 LOW PRIORITY: Additional Hardening

- [ ] **9.1: SSH Harding Configuration**
  - [ ] `PermitRootLogin no` on all VMs
  - [ ] `PasswordAuthentication no` on all VMs
  - [ ] `PubkeyAuthentication yes` on all VMs
  - **Verification:** Review sshd_config on each VM

- [ ] **9.2: Two-Factor Authentication (2FA)**
  - [ ] Consider 2FA for SSH access
  - [ ] Or require 2FA for sensitive operations
  - **Verification:** SSH 2FA implementation reviewed

- [ ] **9.3: SSH Key Escrow**
  - [ ] Consider backup of keys with escrow service
  - [ ] Or hardware security module (HSM) storage
  - **Verification:** Escrow procedure documented

- [ ] **9.4: Compliance Documentation**
  - [ ] Security hardening documented
  - [ ] Compliance checklist created
  - [ ] Audit trail available
  - **Verification:** Documentation in git repo

---

## 📋 Completion Metrics

**Current Status:**

| Priority | Target | Completed | % |
|----------|--------|-----------|---|
| 🔴 CRITICAL (9 items) | 9 | ___ | ___% |
| 🟠 HIGH (13 items) | 13 | ___ | ___% |
| 🟡 MEDIUM (5 items) | 5 | ___ | ___% |
| 🟢 LOW (4 items) | 4 | ___ | ___% |
| **TOTAL** | **31 items** | **___** | **___%** |

---

## 🚀 Deployment Readiness

### Minimum Requirements (Must Complete Before Production)
- [x] All 🔴 CRITICAL items
- [x] All 🟠 HIGH Priority items for SSH
- [x] Item 6.4 (Log Retention Policy)

### Recommended (Should Complete Before Production)
- [x] All 🟠 HIGH Priority items
- [x] Most 🟡 MEDIUM Priority items

### Nice-to-Have (Can Complete After Production)
- [ ] Most 🟢 LOW Priority items
- [ ] Advanced 2FA/HSM security

---

## ✅ Pre-Deployment Sign-Off

- [ ] Security team reviewed this checklist
- [ ] All 🔴 CRITICAL items completed and verified
- [ ] All 🟠 HIGH items completed and verified (or scheduled)
- [ ] Deployment approved by: _________________ Date: _________
- [ ] Post-deployment security audit scheduled: ________________

---

**Document Version:** 1.0.0  
**Last Updated:** November 24, 2025  
**Created by:** Zencoder VM101 Security Review  
**Review Frequency:** Quarterly or before any major changes
