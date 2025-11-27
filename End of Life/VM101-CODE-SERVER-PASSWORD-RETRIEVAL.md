# 🔐 VM101 Code-Server Password Retrieval

**Issue:** Password not working or forgotten  
**Solution:** Retrieve password from config file

---

## 🔍 Get Password from Config File

**On VM101, run:**

```bash
# View the password
cat ~/.config/code-server/config.yaml | grep password
```

**Or view the full config:**
```bash
cat ~/.config/code-server/config.yaml
```

---

## 🔧 Change Password (If Needed)

**If you want to set a new password:**

```bash
# Edit config file
nano ~/.config/code-server/config.yaml

# Change the password line:
# password: YOUR_NEW_PASSWORD

# Restart service to apply changes
sudo systemctl restart code-server
```

**Or generate a new random password:**
```bash
# Generate new password
NEW_PASSWORD=$(openssl rand -base64 12)

# Update config
sed -i "s/password:.*/password: ${NEW_PASSWORD}/" ~/.config/code-server/config.yaml

# Restart service
sudo systemctl restart code-server

# Show new password
echo "New password: ${NEW_PASSWORD}"
```

---

## ✅ Verify Service is Running

**Check status:**
```bash
sudo systemctl status code-server
```

**Check logs:**
```bash
sudo journalctl -u code-server -n 20
```

**Test access:**
```bash
curl http://localhost:9001
```

---

**Run `cat ~/.config/code-server/config.yaml | grep password` to see the current password!**




