<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔐 Binance.US API Keys - Secure Setup for SHENRON & Trading Bot

**Date:** November 6, 2025  
**Purpose:** Securely store and inject Binance.US API keys for SHENRON and Trading Bot

---

## ⚠️ SECURITY NOTICE

**API keys give access to your trading account!**

- ✅ **DO**: Enable trading permissions only
- ❌ **DON'T**: Enable withdrawal permissions
- ✅ **DO**: Whitelist specific IPs
- ❌ **DON'T**: Share keys publicly or commit to public repos
- ✅ **DO**: Use 2FA on Binance.US account
- ❌ **DON'T**: Store keys in plaintext unless secured

---

## 📍 **WHERE TO STORE KEYS**

### **Option 1: Separate Private File (Recommended)**

Create a file that's NOT committed to GitHub:

```bash
# On Linux (VM101)
mkdir -p ~/secure-credentials
chmod 700 ~/secure-credentials
nano ~/secure-credentials/binance-api-keys.json
```

**File content:**
```json
{
  "binance_us": {
    "api_key": "YOUR_BINANCE_API_KEY_HERE",
    "api_secret": "YOUR_BINANCE_API_SECRET_HERE",
    "testnet": false,
    "ip_whitelist": ["<VM101_IP>", "YOUR_PUBLIC_IP"],
    "permissions": ["SPOT_TRADING"],
    "created_date": "2025-11-06",
    "notes": "For SHENRON Trading Bot - NO WITHDRAWAL ENABLED"
  }
}
```

**Secure the file:**
```bash
chmod 600 ~/secure-credentials/binance-api-keys.json
```

---

### **Option 2: Add to Existing API Credentials File**

```bash
# Edit existing file
nano /home/mgmt1/GitHub/Dell-Server-Roadmap/Marketing-Automation/social-media-automation/credentials/api_credentials.json
```

**Add this section:**
```json
{
  "reddit": { ... existing ... },
  "twitter": { ... existing ... },
  "binance_us": {
    "api_key": "YOUR_BINANCE_API_KEY",
    "api_secret": "YOUR_BINANCE_API_SECRET",
    "testnet": false
  }
}
```

**This file is already secured and NOT in public GitHub.**

---

## 🔑 **HOW TO GET BINANCE.US API KEYS**

### **Step 1: Log in to Binance.US**
```
URL: https://www.binance.us
```

### **Step 2: Go to API Management**
```
Account → API Management
```

### **Step 3: Create API Key**
1. Click **"Create API"**
2. **Label**: "SHENRON Trading Bot"
3. **Enable**:
   - ✅ Spot & Margin Trading
4. **DISABLE**:
   - ❌ Withdrawals (CRITICAL FOR SECURITY)
   - ❌ Futures Trading (unless needed)
   - ❌ Internal Transfer
5. **IP Whitelist** (Recommended):
   - Add: `<VM101_IP>` (VM101 - Trading Bot)
   - Add: `<VM100_IP>` (VM100 - SHENRON)
   - Add: Your public IP (for testing)

### **Step 4: Save Keys**
After creating, you'll see:
- **API Key**: `xxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Secret Key**: `yyyyyyyyyyyyyyyyyyyyyyyyyy`

**⚠️ SAVE THE SECRET KEY NOW - You won't see it again!**

---

## 💉 **INJECT INTO TRADING BOT**

### **Method 1: Direct Edit (Quick)**

```bash
# SSH to VM101
ssh mgmt1@<VM101_IP>

# Edit trading bot
cd ~/trading_bot
nano trading_bot_production.py

# Find these lines (near bottom):
# API_KEY = 'YOUR_BINANCE_API_KEY_HERE'
# API_SECRET = 'YOUR_BINANCE_API_SECRET_HERE'

# Replace with your actual keys
# Save: Ctrl+O, Enter, Ctrl+X
```

---

### **Method 2: From Credentials File (Secure)**

**Update trading bot to read from credentials file:**

```bash
# Edit bot to add import at top
nano ~/trading_bot/trading_bot_production.py
```

**Add after imports:**
```python
import json
from pathlib import Path

# Load credentials from secure file
def load_binance_credentials():
    # Try multiple credential file locations
    cred_locations = [
        Path.home() / "secure-credentials" / "binance-api-keys.json",
        Path.home() / "GitHub" / "Dell-Server-Roadmap" / "Marketing-Automation" / 
        "social-media-automation" / "credentials" / "api_credentials.json"
    ]
    
    for cred_file in cred_locations:
        if cred_file.exists():
            with open(cred_file, 'r') as f:
                creds = json.load(f)
                if 'binance_us' in creds:
                    return creds['binance_us']['api_key'], creds['binance_us']['api_secret']
    
    raise FileNotFoundError("Binance.US credentials not found in any expected location")

# Load keys
API_KEY, API_SECRET = load_binance_credentials()
```

---

## 💉 **INJECT INTO SHENRON (VM100)**

### **Transfer Keys to VM100:**

**Option A: Manual Entry (Most Secure)**

```powershell
# On VM100 PowerShell
cd C:\GOKU-AI\shenron

# Create credentials directory
New-Item -ItemType Directory -Path "C:\GOKU-AI\credentials" -Force

# Create credentials file
$creds = @{
    binance_us = @{
        api_key = "YOUR_BINANCE_API_KEY"
        api_secret = "YOUR_BINANCE_API_SECRET"
        testnet = $false
    }
} | ConvertTo-Json -Depth 3

$creds | Out-File -FilePath "C:\GOKU-AI\credentials\binance-api-keys.json" -Encoding UTF8

# Secure the file (restrict access)
icacls "C:\GOKU-AI\credentials\binance-api-keys.json" /inheritance:r /grant:r "${env:USERNAME}:(F)"
```

---

**Option B: SCP Transfer from VM101**

```bash
# On VM101
scp ~/secure-credentials/binance-api-keys.json Administrator@<VM100_IP>:C:/GOKU-AI/credentials/
```

---

### **Update SHENRON to Use Keys:**

**Add to SHENRON knowledge base:**

```bash
# On VM101
cat > /tmp/knowledge-binance-api-integration.md << 'EOF'
# Binance.US API Integration for SHENRON

## API Credentials Location
**File:** `C:\GOKU-AI\credentials\binance-api-keys.json`

## Usage
When SHENRON needs to execute trades via the Quest Manager or Agent Mode:

1. Load credentials from secure file
2. Initialize CCXT with `ccxt.binanceus()`
3. Enable rate limiting
4. Execute trades with AI confirmation
5. Log all trades to database

## Security
- API keys have NO withdrawal permissions
- IP whitelist enabled
- 2FA required on Binance.US account
- Keys stored locally only (not in GitHub)

## Integration with Trading Bot
SHENRON can query the trading bot on VM101 via:
- **URL:** http://<VM101_IP>:8080/api/trade
- **Method:** POST
- **Auth:** Internal network only
EOF

# Transfer to VM100
scp /tmp/knowledge-binance-api-integration.md Administrator@<VM100_IP>:C:/GOKU-AI/knowledge-base/
```

---

### **Inject Knowledge:**

```powershell
# On VM100
cd C:\GOKU-AI\shenron
C:\GOKU-AI\venv\Scripts\python.exe inject_knowledge.py
```

---

## 🧪 **TEST THE INTEGRATION**

### **Test Trading Bot Connection:**

```bash
# On VM101
cd ~/trading_bot
source venv/bin/activate

python3 -c "
import ccxt
import json

# Load credentials
with open('~/secure-credentials/binance-api-keys.json', 'r') as f:
    creds = json.load(f)

# Test connection
exchange = ccxt.binanceus({
    'apiKey': creds['binance_us']['api_key'],
    'secret': creds['binance_us']['api_secret'],
    'enableRateLimit': True
})

# Fetch balance
balance = exchange.fetch_balance()
print('✅ Connection successful!')
print(f'USD Balance: \${balance[\"USDT\"][\"free\"]:.2f}')
"
```

**Expected output:**
```
✅ Connection successful!
USD Balance: $100.00
```

---

### **Test SHENRON Can Access:**

```powershell
# On VM100
cd C:\GOKU-AI\shenron

# Test credential loading
C:\GOKU-AI\venv\Scripts\python.exe -c "
import json
with open('C:/GOKU-AI/credentials/binance-api-keys.json', 'r') as f:
    creds = json.load(f)
    print('✅ Credentials loaded successfully')
    print(f'API Key (first 10 chars): {creds[\"binance_us\"][\"api_key\"][:10]}...')
"
```

---

## 📁 **FILE STRUCTURE**

```
# On VM101 (Linux)
/home/mgmt1/
├── secure-credentials/
│   └── binance-api-keys.json  (chmod 600)
├── trading_bot/
│   └── trading_bot_production.py  (loads from secure file)
└── GitHub/
    └── Dell-Server-Roadmap/
        └── Marketing-Automation/
            └── social-media-automation/
                └── credentials/
                    └── api_credentials.json  (alternative location)

# On VM100 (Windows)
C:\GOKU-AI\
├── credentials\
│   └── binance-api-keys.json  (restricted access)
├── knowledge-base\
│   └── knowledge-binance-api-integration.md
└── shenron\
    └── (reads from credentials\ directory)
```

---

## 🔒 **SECURITY CHECKLIST**

Before using API keys in production:

- [ ] 2FA enabled on Binance.US account
- [ ] API key has **NO withdrawal** permissions
- [ ] IP whitelist configured
- [ ] Only **Spot Trading** permission enabled
- [ ] Keys stored in chmod 600 file (Linux) or restricted access (Windows)
- [ ] Keys NOT committed to public GitHub
- [ ] Test connection successful
- [ ] Backup of keys stored offline (encrypted)
- [ ] Recovery plan documented

---

## 🚨 **IF KEYS ARE COMPROMISED**

1. **Immediately log in to Binance.US**
2. **Go to API Management**
3. **Delete the compromised API key**
4. **Check recent trade history for unauthorized activity**
5. **Generate new API keys**
6. **Update all systems with new keys**
7. **Review security practices**

---

## 📝 **NEXT STEPS**

Once keys are set up:

1. **Test trading bot:** `python3 trading_bot_production.py` (test mode)
2. **Verify SHENRON knowledge:** Query about Binance.US integration
3. **Run first Quest Manager attempt:** See if it can strategize trades
4. **Monitor logs:** Ensure no errors
5. **Deploy as service:** 24/7 operation

---

## ❓ **WHERE ARE YOUR KEYS?**

**You mentioned they're already in GitHub. Please confirm the location:**

Option A: In a private repo?
Option B: In the Dell-Server-Roadmap repo (but I haven't found them yet)?
Option C: In ScalpStorm repo?
Option D: In another location?

**Once you tell me where they are, I can:**
1. Read them securely
2. Inject them into the trading bot on VM101
3. Add them to SHENRON's credentials on VM100
4. Test the integration
5. Deploy for production use

---

**Ready to inject the keys and start trading!** 🚀💰

Just tell me where the keys are, and I'll handle the rest securely.

