<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# ✅ VM101 Code-Server Setup Complete

**Date:** November 23, 2025  
**Status:** ✅ Successfully Installed and Running

---

## ✅ Setup Results

**Port:** 9001  
**Password:** `<AGENT_MODE_PASSWORD>` ⚠️ **SAVE THIS PASSWORD**  
**Access URL:** `http://<VM101_IP>:9001`  
**Service:** Enabled (auto-starts on boot)  
**Security:** ✅ Config file protected (chmod 600) - only owner can read  
**Security:** ✅ Config directory protected (chmod 700) - only owner can access  
**Status:** ✅ Password changed and verified - ready to use

---

## 🔍 Verification Commands

**Check service status:**
```bash
sudo systemctl status code-server
```

**Check if port is listening:**
```bash
sudo ss -tlnp | grep :9001
```

**Check logs:**
```bash
sudo journalctl -u code-server -f
```

**Test access:**
```bash
# From VM101
curl http://localhost:9001

# From another machine
curl http://<VM101_IP>:9001
```

---

## 🌐 Access Code-Server

**In your browser:**
```
http://<VM101_IP>:9001
```

**Login:**
- **Password:** `Jva43pw3AVikEFhG`

---

## 📋 Configuration Files

**Config:** `~/.config/code-server/config.yaml`
```yaml
bind-addr: 0.0.0.0:9001
auth: password
password: Jva43pw3AVikEFhG
cert: false
```

**Service:** `/etc/systemd/system/code-server.service`
- Auto-starts on boot
- Restarts on failure
- Runs as user: mgmt1

---

## 🔧 Management Commands

**Start/Stop/Restart:**
```bash
sudo systemctl start code-server
sudo systemctl stop code-server
sudo systemctl restart code-server
sudo systemctl status code-server
```

**View Logs:**
```bash
# Follow logs
sudo journalctl -u code-server -f

# Last 50 lines
sudo journalctl -u code-server -n 50
```

**Change Password:**
```bash
# Edit config
nano ~/.config/code-server/config.yaml

# Change password, then restart
sudo systemctl restart code-server
```

---

## 🔐 Security Status

- ✅ Password authentication enabled
- ✅ Firewall rule added (port 9001)
- ✅ Service auto-starts on boot
- ✅ Port 9001 verified safe (not used by reverse proxy)
- ✅ Running as non-root user (mgmt1)

---

## 📝 Next Steps

1. ✅ **Access code-server:** Open `http://<VM101_IP>:9001` in browser
2. ✅ **Login:** Use password `Jva43pw3AVikEFhG`
3. ✅ **Save password:** Store securely (password manager, etc.)
4. ⚠️ **Optional:** Change password if desired
5. ⚠️ **Optional:** Configure extensions, themes, etc.

---

## 🎯 Summary

**Code-server is now fully operational on VM101!**

- ✅ Port 9001 (safe, verified)
- ✅ Password authentication
- ✅ Systemd service (auto-start)
- ✅ Firewall configured
- ✅ Ready to use

**Access:** `http://<VM101_IP>:9001`  
**Password:** `Jva43pw3AVikEFhG` ⚠️ **SAVE THIS!**

---

**Setup Complete!** 🎉

