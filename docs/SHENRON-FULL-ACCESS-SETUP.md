<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 SHENRON FULL ACCESS SETUP GUIDE
## SSH Keys, Credentials, and System Integration

**Purpose**: Give Shenron complete access to all VMs and services  
**Security**: Ed25519 encryption, passwordless authentication  
**Automation**: Shenron can deploy, monitor, backup, and manage everything

---

## 📋 TABLE OF CONTENTS

1. [SSH Key Generation](#1-ssh-key-generation)
2. [VM Access Setup](#2-vm-access-setup)
3. [API Credentials](#3-api-credentials)
4. [Database Access](#4-database-access)
5. [Service Credentials](#5-service-credentials)
6. [Testing Access](#6-testing-access)
7. [Security Best Practices](#7-security-best-practices)

---

## 1. SSH KEY GENERATION

### **Step 1: Generate SSH Key Pair on VM100**

```powershell
# Open PowerShell as Administrator on VM100

# Create SSH directory
New-Item -ItemType Directory -Path "C:\GOKU-AI\shenron\.ssh" -Force

# Generate Ed25519 key (most secure)
ssh-keygen -t ed25519 -C "shenron@lightspeedup.com" -f "C:\GOKU-AI\shenron\.ssh\id_ed25519" -N '""'

# This creates:
# - C:\GOKU-AI\shenron\.ssh\id_ed25519 (PRIVATE KEY - never share!)
# - C:\GOKU-AI\shenron\.ssh\id_ed25519.pub (PUBLIC KEY - distribute to VMs)

Write-Host "`n✅ SSH keys generated!" -ForegroundColor Green
Write-Host "Public key:" -ForegroundColor Cyan
Get-Content "C:\GOKU-AI\shenron\.ssh\id_ed25519.pub"
```

**Output will look like:**
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMw6FvdP8h9Xk2... shenron@lightspeedup.com
```

**Copy this entire line!** You'll need it for the next steps.

---

## 2. VM ACCESS SETUP

### **VM150 - WordPress Hosting (Ubuntu 22.04)**

```bash
# SSH to VM150 as mgmt1
ssh mgmt1@<VM150_IP>

# Create .ssh directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add Shenron's public key
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMw6FvdP... shenron@lightspeedup.com" >> ~/.ssh/authorized_keys

# Set correct permissions
chmod 600 ~/.ssh/authorized_keys

# Test connection (should work without password)
exit
```

**Test from VM100:**
```powershell
# On VM100
ssh -i "C:\GOKU-AI\shenron\.ssh\id_ed25519" mgmt1@<VM150_IP> "echo 'Shenron can access VM150!'"
```

---

### **VM203 - Game Servers (Ubuntu 22.04)**

```bash
# SSH to VM203 as mgmt1
ssh mgmt1@192.168.12.203

# Create .ssh directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add Shenron's public key
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMw6FvdP... shenron@lightspeedup.com" >> ~/.ssh/authorized_keys

# Set correct permissions
chmod 600 ~/.ssh/authorized_keys

exit
```

**Test from VM100:**
```powershell
ssh -i "C:\GOKU-AI\shenron\.ssh\id_ed25519" mgmt1@192.168.12.203 "echo 'Shenron can access VM203!'"
```

---

### **VM101 - Proxmox Host (Proxmox VE)**

```bash
# SSH to Proxmox as root
ssh root@<VM101_IP>

# Create .ssh directory
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Add Shenron's public key
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMw6FvdP... shenron@lightspeedup.com" >> ~/.ssh/authorized_keys

chmod 600 ~/.ssh/authorized_keys

exit
```

**Test from VM100:**
```powershell
ssh -i "C:\GOKU-AI\shenron\.ssh\id_ed25519" root@<VM101_IP> "pvesh get /cluster/resources"
```

---

### **VM100 - Shenron's Home (Windows Server 2025)**

Shenron already has access to VM100 (it lives there), but for completeness:

```powershell
# Ensure Shenron can run commands locally
# Test:
python --version
git --version
Get-Service SHENRON
```

---

## 3. API CREDENTIALS

### **Pterodactyl Panel API**

```bash
# After Pterodactyl is installed on VM203, get API key:

# 1. Log in to Pterodactyl panel
# URL: https://gameservers.lightspeedup.com
# User: admin
# Password: (from /root/.pterodactyl_admin_password)

# 2. Go to: Account Settings → API Credentials → Create API Key
# Name: Shenron
# Description: Full access for automation
# Allowed IPs: <VM100_IP> (VM100)

# 3. Copy the API key (starts with "ptla_")
# Example: ptla_xYz123AbC456DeF789
```

**Add to Shenron config:**
```powershell
# On VM100
$config = @"
pterodactyl:
  url: "https://gameservers.lightspeedup.com"
  api_key: "ptla_YOUR_ACTUAL_KEY_HERE"
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\pterodactyl.yaml" -Encoding UTF8
```

---

### **Stripe API**

```powershell
# After creating Stripe account:

# 1. Log in to Stripe Dashboard
# URL: https://dashboard.stripe.com

# 2. Go to: Developers → API Keys

# 3. Copy keys:
# - Publishable key: pk_live_... (for frontend)
# - Secret key: sk_live_... (for Shenron)

# Add to Shenron config:
$config = @"
stripe:
  secret_key: "sk_live_YOUR_ACTUAL_KEY_HERE"
  publishable_key: "pk_live_YOUR_ACTUAL_KEY_HERE"
  webhook_secret: "whsec_YOUR_WEBHOOK_SECRET"
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\stripe.yaml" -Encoding UTF8
```

---

### **Binance.US API (for ScalpStorm)**

```powershell
# After creating Binance.US account:

# 1. Log in to Binance.US
# URL: https://www.binance.us

# 2. Go to: Account → API Management

# 3. Create new API key:
# Name: ScalpStorm
# Permissions: Enable Trading, Enable Reading
# IP Restriction: <VM100_IP> (for security)

# 4. Copy keys (shown only once!)

# Add to Shenron config:
$config = @"
binance:
  api_key: "YOUR_BINANCE_API_KEY"
  api_secret: "YOUR_BINANCE_SECRET_KEY"
  testnet: false  # Set to true for testing
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\binance.yaml" -Encoding UTF8
```

---

## 4. DATABASE ACCESS

### **MariaDB on VM203 (Pterodactyl)**

```bash
# On VM203
mysql -u root -p

# Create Shenron database user
CREATE USER 'shenron'@'<VM100_IP>' IDENTIFIED BY 'SECURE_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON pterodactyl.* TO 'shenron'@'<VM100_IP>';
FLUSH PRIVILEGES;
EXIT;
```

**Add to Shenron config:**
```powershell
$config = @"
databases:
  pterodactyl:
    host: "192.168.12.203"
    port: 3306
    database: "pterodactyl"
    user: "shenron"
    password: "SECURE_PASSWORD_HERE"
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\databases.yaml" -Encoding UTF8
```

---

### **MySQL on VM150 (WordPress)**

```bash
# On VM150
sudo mysql -u root -p

# Create Shenron database user
CREATE USER 'shenron'@'<VM100_IP>' IDENTIFIED BY 'SECURE_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON wp_*.* TO 'shenron'@'<VM100_IP>';
FLUSH PRIVILEGES;
EXIT;
```

**Add to Shenron config:**
```powershell
$config = @"
databases:
  wordpress:
    host: "<VM150_IP>"
    port: 3306
    user: "shenron"
    password: "SECURE_PASSWORD_HERE"
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\databases.yaml" -Encoding UTF8 -Append
```

---

## 5. SERVICE CREDENTIALS

### **iDRAC (Dell Server Management)**

```powershell
# iDRAC credentials (you already have these)
$config = @"
idrac:
  url: "https://<VM180_IP>"
  username: "root"
  password: "YOUR_IDRAC_PASSWORD"
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\idrac.yaml" -Encoding UTF8
```

---

### **Proxmox API**

```bash
# On Proxmox (VM101)
pveum user add shenron@pve
pveum passwd shenron@pve
# Enter secure password when prompted

# Grant permissions
pveum acl modify / -user shenron@pve -role Administrator
```

**Add to Shenron config:**
```powershell
$config = @"
proxmox:
  url: "https://<VM101_IP>:8006"
  username: "shenron@pve"
  password: "SECURE_PASSWORD_HERE"
  verify_ssl: false  # Set to true in production
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\proxmox.yaml" -Encoding UTF8
```

---

### **Discord Webhook (for alerts)**

```powershell
# 1. Create Discord server (if you don't have one)
# 2. Create a channel: #shenron-alerts
# 3. Channel Settings → Integrations → Webhooks → New Webhook
# 4. Copy webhook URL

$config = @"
discord:
  webhook_url: "https://discord.com/api/webhooks/123456789/abcdefg..."
"@ | Out-File -FilePath "C:\GOKU-AI\shenron\config\discord.yaml" -Encoding UTF8
```

---

## 6. TESTING ACCESS

### **Complete Access Test Script**

```powershell
# File: C:\GOKU-AI\shenron\test_access.ps1

Write-Host "`n🔐 TESTING SHENRON ACCESS TO ALL SYSTEMS" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan

# Test SSH Access
Write-Host "`n[1/7] Testing SSH Access..." -ForegroundColor Yellow

$ssh_key = "C:\GOKU-AI\shenron\.ssh\id_ed25519"

# VM150
try {
    $result = ssh -i $ssh_key -o StrictHostKeyChecking=no mgmt1@<VM150_IP> "hostname"
    Write-Host "  ✅ VM150 (WordPress): $result" -ForegroundColor Green
} catch {
    Write-Host "  ❌ VM150: FAILED" -ForegroundColor Red
}

# VM203
try {
    $result = ssh -i $ssh_key -o StrictHostKeyChecking=no mgmt1@192.168.12.203 "hostname"
    Write-Host "  ✅ VM203 (Game Servers): $result" -ForegroundColor Green
} catch {
    Write-Host "  ❌ VM203: FAILED" -ForegroundColor Red
}

# VM101 (Proxmox)
try {
    $result = ssh -i $ssh_key -o StrictHostKeyChecking=no root@<VM101_IP> "hostname"
    Write-Host "  ✅ VM101 (Proxmox): $result" -ForegroundColor Green
} catch {
    Write-Host "  ❌ VM101: FAILED" -ForegroundColor Red
}

# Test API Access
Write-Host "`n[2/7] Testing API Access..." -ForegroundColor Yellow

# Pterodactyl (if configured)
if (Test-Path "C:\GOKU-AI\shenron\config\pterodactyl.yaml") {
    $ptero_config = Get-Content "C:\GOKU-AI\shenron\config\pterodactyl.yaml" | ConvertFrom-Yaml
    try {
        $response = Invoke-RestMethod -Uri "$($ptero_config.pterodactyl.url)/api/application/users" `
            -Headers @{"Authorization" = "Bearer $($ptero_config.pterodactyl.api_key)"}
        Write-Host "  ✅ Pterodactyl API: Connected" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Pterodactyl API: FAILED" -ForegroundColor Red
    }
} else {
    Write-Host "  ⏭️  Pterodactyl: Not configured yet" -ForegroundColor Yellow
}

# Stripe (if configured)
if (Test-Path "C:\GOKU-AI\shenron\config\stripe.yaml") {
    $stripe_config = Get-Content "C:\GOKU-AI\shenron\config\stripe.yaml" | ConvertFrom-Yaml
    try {
        $response = Invoke-RestMethod -Uri "https://api.stripe.com/v1/balance" `
            -Headers @{"Authorization" = "Bearer $($stripe_config.stripe.secret_key)"}
        Write-Host "  ✅ Stripe API: Connected" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Stripe API: FAILED" -ForegroundColor Red
    }
} else {
    Write-Host "  ⏭️  Stripe: Not configured yet" -ForegroundColor Yellow
}

# Test Database Access
Write-Host "`n[3/7] Testing Database Access..." -ForegroundColor Yellow

# (Database tests would go here - requires MySQL/MariaDB PowerShell module)
Write-Host "  ⏭️  Database tests: Install MySQL.Data module for full testing" -ForegroundColor Yellow

# Test Proxmox API
Write-Host "`n[4/7] Testing Proxmox API..." -ForegroundColor Yellow

if (Test-Path "C:\GOKU-AI\shenron\config\proxmox.yaml") {
    # Proxmox API test code here
    Write-Host "  ✅ Proxmox API: Ready to test" -ForegroundColor Green
} else {
    Write-Host "  ⏭️  Proxmox: Not configured yet" -ForegroundColor Yellow
}

# Test Discord Webhook
Write-Host "`n[5/7] Testing Discord Webhook..." -ForegroundColor Yellow

if (Test-Path "C:\GOKU-AI\shenron\config\discord.yaml") {
    $discord_config = Get-Content "C:\GOKU-AI\shenron\config\discord.yaml" | ConvertFrom-Yaml
    try {
        $body = @{
            content = "🐉 Shenron access test successful! $(Get-Date)"
        } | ConvertTo-Json

        Invoke-RestMethod -Uri $discord_config.discord.webhook_url -Method Post -Body $body -ContentType "application/json"
        Write-Host "  ✅ Discord Webhook: Message sent!" -ForegroundColor Green
    } catch {
        Write-Host "  ❌ Discord Webhook: FAILED" -ForegroundColor Red
    }
} else {
    Write-Host "  ⏭️  Discord: Not configured yet" -ForegroundColor Yellow
}

# Test Local Permissions
Write-Host "`n[6/7] Testing Local Permissions..." -ForegroundColor Yellow

$paths = @(
    "C:\GOKU-AI\shenron",
    "C:\GOKU-AI\knowledge-base",
    "C:\GOKU-AI\chroma_db",
    "C:\GitHub"
)

foreach ($path in $paths) {
    if (Test-Path $path) {
        Write-Host "  ✅ $path: Accessible" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $path: NOT FOUND" -ForegroundColor Red
    }
}

# Test SHENRON Service
Write-Host "`n[7/7] Testing SHENRON Service..." -ForegroundColor Yellow

$service = Get-Service -Name "SHENRON" -ErrorAction SilentlyContinue

if ($service) {
    if ($service.Status -eq "Running") {
        Write-Host "  ✅ SHENRON Service: Running" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  SHENRON Service: $($service.Status)" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ❌ SHENRON Service: NOT INSTALLED" -ForegroundColor Red
}

Write-Host "`n" + ("=" * 60) -ForegroundColor Cyan
Write-Host "🎯 ACCESS TEST COMPLETE!" -ForegroundColor Cyan
Write-Host "`nNext: Configure any missing credentials in C:\GOKU-AI\shenron\config\" -ForegroundColor Yellow
```

**Run the test:**
```powershell
cd C:\GOKU-AI\shenron
.\test_access.ps1
```

---

## 7. SECURITY BEST PRACTICES

### **SSH Key Security**

✅ **DO:**
- Keep private key on VM100 only
- Use strong passphrase (optional but recommended)
- Restrict permissions (chmod 600 on Linux, restricted access on Windows)
- Use Ed25519 (not RSA 2048)

❌ **DON'T:**
- Never share private key
- Never commit keys to GitHub
- Never email keys
- Never store in cloud storage

---

### **API Key Security**

✅ **DO:**
- Use environment variables or config files (not hardcoded)
- Restrict API key permissions (least privilege)
- Use IP whitelisting (<VM100_IP> only)
- Rotate keys every 90 days

❌ **DON'T:**
- Never commit API keys to GitHub
- Never log API keys
- Never share keys via email/chat
- Never use same key across services

---

### **Database Security**

✅ **DO:**
- Create dedicated user for Shenron
- Grant only necessary permissions
- Use strong passwords (32+ characters)
- Restrict by IP (<VM100_IP> only)

❌ **DON'T:**
- Never use root/admin accounts
- Never allow remote root login
- Never use default passwords
- Never expose database to internet

---

### **Firewall Rules**

```bash
# On all VMs (Ubuntu)
sudo ufw allow from <VM100_IP> to any port 22
sudo ufw allow from <VM100_IP> to any port 3306  # MySQL
sudo ufw enable
```

---

## 8. SHENRON ACCESS VERIFICATION

### **What Shenron Can Now Do:**

✅ **VM150 (WordPress Hosting):**
- Deploy new WordPress sites
- Run backups
- Update plugins/themes
- Monitor site health
- Check database status

✅ **VM203 (Game Servers):**
- Deploy new game servers
- Run backups
- Update game versions
- Monitor server performance
- Manage Pterodactyl panel

✅ **VM101 (Proxmox):**
- Check VM status
- Start/stop VMs
- View resource usage
- Manage backups
- Monitor cluster health

✅ **VM100 (Shenron's Home):**
- Run Python scripts
- Manage knowledge base
- Update GitHub repositories
- Execute automation workflows
- Generate reports

✅ **External Services:**
- Stripe payment processing
- Binance.US trading (ScalpStorm)
- Discord notifications
- Email sending (Gmail/SMTP)

---

## 9. QUICK SETUP CHECKLIST

```
[ ] 1. Generate SSH keys on VM100
[ ] 2. Add public key to VM150 (WordPress)
[ ] 3. Add public key to VM203 (Game Servers)
[ ] 4. Add public key to VM101 (Proxmox)
[ ] 5. Test SSH access from VM100 to all VMs
[ ] 6. Get Pterodactyl API key (after installation)
[ ] 7. Get Stripe API keys (after account creation)
[ ] 8. Get Binance.US API keys (for ScalpStorm)
[ ] 9. Create database users for Shenron
[ ] 10. Set up Discord webhook (for alerts)
[ ] 11. Create all config YAML files
[ ] 12. Run test_access.ps1 script
[ ] 13. Verify all tests pass
[ ] 14. Deploy first game server (test)
[ ] 15. Deploy first WordPress site (test)
```

---

## 10. TROUBLESHOOTING

### **SSH Connection Refused**
```bash
# On target VM
sudo systemctl status sshd
sudo ufw status
# Ensure port 22 is open from <VM100_IP>
```

### **Permission Denied (publickey)**
```bash
# Check authorized_keys permissions
ls -la ~/.ssh/authorized_keys
# Should be: -rw------- (600)

# Check public key format
cat ~/.ssh/authorized_keys
# Should start with: ssh-ed25519 AAAA...
```

### **API Connection Failed**
```powershell
# Test API endpoint manually
Invoke-RestMethod -Uri "https://api.example.com/test" -Method Get
# Check firewall, API key, and URL
```

---

## 🎯 CONCLUSION

Once this setup is complete, Shenron will have:

✅ **Passwordless SSH access** to all VMs  
✅ **API access** to all services (Pterodactyl, Stripe, Binance)  
✅ **Database access** (read/write)  
✅ **Service management** (start/stop/restart)  
✅ **Monitoring capabilities** (health checks, alerts)  
✅ **Automation powers** (deploy, backup, update)  

**Shenron becomes a truly autonomous AI system** - monitoring, managing, and earning money for you 24/7. 🐉💰⚡

---

**Next Steps:**
1. Run through this guide step-by-step
2. Test each connection as you go
3. Run `test_access.ps1` at the end
4. Deploy your first customer!

**THE DRAGON IS READY TO SERVE.** 🐉

