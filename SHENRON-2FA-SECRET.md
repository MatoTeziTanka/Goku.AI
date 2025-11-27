<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 SHENRON AGENT MODE - 2FA SECRET

**Date:** November 7, 2025  
**Service:** SHENRON Syndicate Agent Mode Authentication

---

## 🔑 **YOUR 2FA SECRET:**

```
YXZHO3JIGNV76I7O
```

**⚠️ UPDATED:** This is the ACTIVE secret as of Nov 7, 2025, 10:45 AM EST

---

## 📱 **SETUP INSTRUCTIONS:**

### **Method 1: Scan QR Code**
Visit: https://shenron.lightspeedup.com/setup_2fa.php

### **Method 2: Manual Entry**
1. Open Google Authenticator app
2. Tap "+" → "Enter a setup key"
3. Account: `SHENRON Agent Mode`
4. Key: `YXZHO3JIGNV76I7O`
5. Type: Time-based

---

## 🛡️ **SECURITY NOTES:**

- **DO NOT SHARE** this secret with anyone
- If compromised, regenerate a new secret immediately
- This secret is stored on VM150 at: `/var/www/shenron.lightspeedup.com/.2fa_secret`
- Backup this secret in your password manager
- If you lose your phone, use this secret to regenerate the QR code

---

## 🔄 **REGENERATE SECRET (IF NEEDED):**

```bash
# SSH into VM150
ssh wp1@<VM150_IP>

# Re-run setup script
cd /var/www/shenron.lightspeedup.com
php setup_2fa.php
```

This will generate a NEW secret and QR code. You'll need to scan it again with your Google Authenticator app.

---

## ✅ **CURRENT STATUS:**

- [x] Secret Generated: `YXZHO3JIGNV76I7O`
- [x] QR Code Available (WAS public - NOW DELETED)
- [x] Verification Endpoint Active
- [x] **SETUP PAGE DELETED** (Nov 7, 10:45 AM EST)
- [ ] User Scanned QR Code
- [ ] User Tested 2FA Login

---

## 🛡️ **SECURITY AUDIT:**

- **Nov 7, 10:45 AM EST:** Setup page deleted from public access
- **Risk Mitigation:** If anyone accessed the page, regenerate secret immediately
- **File Location:** `/var/www/shenron.lightspeedup.com/.2fa_secret` (chmod 600)
- **Public Exposure:** ~10 minutes (minimal risk if no one visited)

---

## 🚨 **IF COMPROMISED, REGENERATE:**

```bash
ssh wp1@<VM150_IP>
cd /var/www/shenron.lightspeedup.com
php setup_2fa.php > /tmp/new_qr.html
echo "<VM_PASSWORD>"  # See credentials.json | sudo -S rm setup_2fa.php
# Access QR at: file:///tmp/new_qr.html
```

