<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 VM101 Code-Server Password Security & Change

**Issue:** Config file should be protected (sudo required)  
**Action:** Secure config file and change password

---

## 🔒 Step 1: Secure the Config File

**Make config file readable only by owner:**

```bash
# Set restrictive permissions (owner read/write only)
chmod 600 ~/.config/code-server/config.yaml

# Verify permissions
ls -la ~/.config/code-server/config.yaml
# Should show: -rw------- (600)
```

**Now only the owner (mgmt1) can read it:**
- ✅ Owner (mgmt1): read/write
- ❌ Group: no access
- ❌ Others: no access

---

## 🔑 Step 2: Change Password

**Set new password to: `<AGENT_MODE_PASSWORD>`**

```bash
# Update password in config file
sed -i "s/password:.*/password: <AGENT_MODE_PASSWORD>/" ~/.config/code-server/config.yaml

# Verify change (will require sudo now if permissions are set)
sudo cat ~/.config/code-server/config.yaml | grep password

# Restart service to apply changes
sudo systemctl restart code-server

# Check service status
sudo systemctl status code-server
```

---

## 🔒 Step 3: Secure Config Directory (Optional but Recommended)

**Also secure the config directory:**

```bash
# Set directory permissions (owner only)
chmod 700 ~/.config/code-server

# Verify
ls -ld ~/.config/code-server
# Should show: drwx------ (700)
```

---

## ✅ Complete Security Setup

**Run all commands together:**

```bash
# 1. Change password
sed -i "s/password:.*/password: <AGENT_MODE_PASSWORD>/" ~/.config/code-server/config.yaml

# 2. Secure config file
chmod 600 ~/.config/code-server/config.yaml

# 3. Secure config directory
chmod 700 ~/.config/code-server

# 4. Restart service
sudo systemctl restart code-server

# 5. Verify
echo "✅ Password changed and config secured"
echo "   New password: <AGENT_MODE_PASSWORD>"
echo "   Config file permissions: $(stat -c '%a' ~/.config/code-server/config.yaml)"
echo "   Config dir permissions: $(stat -c '%a' ~/.config/code-server)"
```

---

## 🔍 Verify Security

**Test that config is protected:**

```bash
# As regular user (should work)
cat ~/.config/code-server/config.yaml | grep password

# As another user (should fail if they exist)
sudo -u nobody cat ~/.config/code-server/config.yaml 2>&1
# Should show: Permission denied
```

**Note:** Since you're the owner (mgmt1), you can still read it. But other users cannot.

---

## 🛡️ Additional Security Recommendations

### **1. Use Strong Password**
- ✅ Your password `<AGENT_MODE_PASSWORD>` is strong (mixed case, numbers, special chars)

### **2. Consider IP Restrictions (Future)**
```bash
# Could add to systemd service:
# ExecStart=/usr/bin/code-server --bind-addr 127.0.0.1:9001 --auth password
# Then use SSH tunnel for access
```

### **3. Use HTTPS (Future)**
- Configure reverse proxy with SSL
- Or use code-server with cert

### **4. Monitor Access**
```bash
# Check access logs
sudo journalctl -u code-server -f
```

---

## 📋 Summary

**Security Changes:**
- ✅ Config file: `chmod 600` (owner read/write only)
- ✅ Config directory: `chmod 700` (owner access only)
- ✅ Password changed to: `<AGENT_MODE_PASSWORD>`

**Access:**
- URL: `http://<VM101_IP>:9001`
- Password: `<AGENT_MODE_PASSWORD>`

**Now the config file is protected - only owner can read it!** 🔐




