<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# ✅ VM101 Code-Server Password Verification

**Status:** Security applied, need to verify password

---

## 🔍 Verify Password Was Changed

**Check the actual password in config:**

```bash
# View password (you're owner, so you can read it)
cat ~/.config/code-server/config.yaml | grep password
```

**Expected output:**
```
password: <AGENT_MODE_PASSWORD>
```

---

## 🔧 Fix Password (If Needed)

**If the password wasn't set correctly due to the command mix-up:**

```bash
# Fix the password properly
echo "password: <AGENT_MODE_PASSWORD>" > /tmp/password_line.txt
sed -i '/^password:/d' ~/.config/code-server/config.yaml
sed -i '/^bind-addr:/a password: <AGENT_MODE_PASSWORD>' ~/.config/code-server/config.yaml

# Or manually edit
nano ~/.config/code-server/config.yaml
# Make sure it shows:
# password: <AGENT_MODE_PASSWORD>

# Restart service
sudo systemctl restart code-server
```

**Or use a simpler approach:**

```bash
# Backup current config
cp ~/.config/code-server/config.yaml ~/.config/code-server/config.yaml.backup

# Recreate with correct password
cat > ~/.config/code-server/config.yaml << EOF
bind-addr: 0.0.0.0:9001
auth: password
password: <AGENT_MODE_PASSWORD>
cert: false
EOF

# Ensure permissions are correct
chmod 600 ~/.config/code-server/config.yaml

# Restart service
sudo systemctl restart code-server

# Verify
cat ~/.config/code-server/config.yaml
```

---

## ✅ Current Status

**What worked:**
- ✅ Config file permissions: 600 (owner read/write only)
- ✅ Config directory permissions: 700 (owner access only)
- ✅ Service is running

**What to verify:**
- ⚠️ Password in config file (check with `cat ~/.config/code-server/config.yaml | grep password`)

---

## 🧪 Test Login

**After verifying/fixing password:**

1. Open browser: `http://<VM101_IP>:9001`
2. Enter password: `<AGENT_MODE_PASSWORD>`
3. Should login successfully

---

**Run `cat ~/.config/code-server/config.yaml | grep password` to verify the password is correct!**




