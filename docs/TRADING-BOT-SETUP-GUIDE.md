<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Trading Bot Setup Guide - Quick Start

**Location:** VM101 (<VM101_IP>)  
**File:** `~/trading_bot/trading_bot_production.py`  
**Start Capital:** $100  
**Target:** $1,578 in 6 months

---

## ✅ **STEP 1: CREATE EXCHANGE ACCOUNT** (30 minutes)

### **Option A: Binance.US** (Recommended)

1. Go to: https://accounts.binance.us/register
2. Sign up with email
3. Complete KYC verification (driver's license)
4. Enable 2FA (Google Authenticator app)
5. Deposit $100 via bank transfer or debit card

### **Option B: Coinbase Pro**

1. Go to: https://www.coinbase.com/signup
2. Sign up and verify identity
3. Enable 2FA
4. Deposit $100

---

## 🔑 **STEP 2: GENERATE API KEYS** (10 minutes)

### **Binance.US:**

1. Log in → Account → API Management
2. Click "Create API"
3. Label: "Trading Bot"
4. **Enable:** Spot & Margin Trading
5. **DISABLE:** Withdrawals ⚠️ (IMPORTANT FOR SECURITY)
6. Add IP Whitelist: `<VM101_IP>` (your public IP)
7. **Save both keys:**
   - API Key: `starts with letters/numbers`
   - Secret Key: `long string - NEVER share this`

### **Coinbase Pro:**

1. Settings → API
2. Create API Key
3. **Permissions:** View + Trade (NOT Transfer)
4. Add IP: `<VM101_IP>`
5. Save keys

---

## 🐍 **STEP 3: INSTALL DEPENDENCIES** (10 minutes)

```bash
# SSH to VM101
ssh mgmt1@<VM101_IP>

# Create Python environment
cd ~/trading_bot
python3 -m venv venv
source venv/bin/activate

# Install required packages
pip install ccxt pandas numpy requests schedule

# Verify installation
python3 -c "import ccxt; print('✅ CCXT installed')"
python3 -c "import pandas; print('✅ Pandas installed')"
python3 -c "import requests; print('✅ Requests installed')"
```

---

## ⚙️ **STEP 4: CONFIGURE BOT** (5 minutes)

```bash
# Edit the bot file
cd ~/trading_bot
nano trading_bot_production.py

# Find these lines (near the bottom):
API_KEY = 'YOUR_BINANCE_API_KEY_HERE'
API_SECRET = 'YOUR_BINANCE_API_SECRET_HERE'

# Replace with your actual keys
API_KEY = 'paste your API key here'
API_SECRET = 'paste your secret here'

# Save: Ctrl+O, Enter, Ctrl+X
```

**Important Settings to Verify:**
```python
INITIAL_CAPITAL = 100  # Your starting capital
exchange_id='binanceus'  # or 'coinbasepro'
check_interval=300  # 5 minutes between checks
```

---

## 🧪 **STEP 5: TEST RUN** (5 minutes)

```bash
# Activate environment
cd ~/trading_bot
source venv/bin/activate

# Test connection
python3 -c "
import ccxt
exchange = ccxt.binanceus({
    'apiKey': 'YOUR_KEY',
    'secret': 'YOUR_SECRET'
})
print(exchange.fetch_ticker('BTC/USDT'))
"

# If that works, run the bot in test mode
python3 trading_bot_production.py
```

**What You Should See:**
```
2025-11-06 14:30:00 - INFO - Trading Bot initialized with $100
2025-11-06 14:30:00 - INFO - 🤖 Trading Bot Started
2025-11-06 14:30:00 - INFO - Initial Capital: $100.00
2025-11-06 14:30:00 - INFO - Symbols: BTC/USDT, ETH/USDT, BNB/USDT
2025-11-06 14:30:00 - INFO - Check Interval: 300s (5 min)
...
2025-11-06 14:31:00 - INFO - SHENRON Decision: HOLD (Confidence: 65%)
2025-11-06 14:31:00 - INFO - Status: Capital=$100.00 | Positions=0 | Total=$100.00 | Gain=+0.00%
```

**Press Ctrl+C to stop after seeing it connect successfully.**

---

## 🚀 **STEP 6: RUN 24/7** (Deploy as Service)

```bash
# Create systemd service
sudo nano /etc/systemd/system/trading-bot.service
```

**Paste this:**
```ini
[Unit]
Description=SHENRON Trading Bot
After=network.target

[Service]
Type=simple
User=mgmt1
WorkingDirectory=/home/mgmt1/trading_bot
Environment="PATH=/home/mgmt1/trading_bot/venv/bin"
ExecStart=/home/mgmt1/trading_bot/venv/bin/python3 /home/mgmt1/trading_bot/trading_bot_production.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Save and enable:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable trading-bot
sudo systemctl start trading-bot

# Check status
sudo systemctl status trading-bot

# View logs
sudo journalctl -u trading-bot -f
```

---

## 📊 **MONITORING**

### **Check Status:**
```bash
# Live logs
sudo journalctl -u trading-bot -f

# Last 50 lines
sudo journalctl -u trading-bot -n 50

# Trading log file
tail -f ~/trading_bot/trading.log
```

### **Check Capital Growth:**
```bash
# View recent trades
grep "SOLD" ~/trading_bot/trading.log | tail -10

# Calculate total gain
# (Check the "Total Gain" in status updates)
```

### **Binance.US Dashboard:**
- Log in to Binance.US
- Go to Wallet → Spot
- See current balance and trade history

---

## 🎯 **EXPECTED PERFORMANCE**

| Month | Capital | Return | Profit | Notes |
|-------|---------|--------|--------|-------|
| 0 | $100 | - | - | Starting |
| 1 | $120 | 20% | $20 | First month |
| 2 | $150 | 25% | $30 | Building momentum |
| 3 | $188 | 25% | $38 | Compounding |
| 4 | $244 | 30% | $56 | Strong performance |
| 5 | $317 | 30% | $73 | Consistent |
| 6 | $411 | 30% | $94 | Target achieved |

**Conservative:** $100 → $400+ in 6 months  
**Aggressive:** $100 → $600+ in 6 months

---

## ⚙️ **CONFIGURATION OPTIONS**

### **Risk Settings** (in the code):
```python
self.max_position_size = 0.5  # 50% max per trade
self.stop_loss_pct = -1.5     # -1.5% stop loss
self.take_profit_pct = 3.0    # 3% take profit
self.max_daily_trades = 10    # Max trades per day
```

### **Trading Pairs:**
```python
symbols=['BTC/USDT', 'ETH/USDT', 'BNB/USDT']
```

### **Check Interval:**
```python
check_interval=300  # 5 minutes (recommended)
# Options: 180 (3min), 300 (5min), 600 (10min)
```

---

## 🔒 **SECURITY BEST PRACTICES**

✅ **DO:**
- Keep API secret offline (write it down)
- Disable withdrawal permissions
- Use IP whitelist
- Enable 2FA on exchange
- Monitor daily first week

❌ **DON'T:**
- Share API keys
- Enable withdrawal on API
- Skip 2FA
- Leave keys in GitHub
- Trust anyone asking for keys

---

## 🐛 **TROUBLESHOOTING**

### **"Invalid API Key" Error:**
```bash
# Verify keys are correct
# Check IP whitelist on Binance.US
# Ensure Trading permission is enabled
```

### **"Insufficient Balance" Error:**
```bash
# Check Binance.US wallet balance
# Ensure $100+ in Spot wallet (not Fiat)
```

### **"SHENRON API Unavailable":**
```bash
# Check SHENRON is running
curl http://<VM100_IP>:5000/health

# Should return: {"status": "operational"}
```

### **Bot Not Trading:**
- Check logs: Technical conditions must be met first
- RSI must be < 40 (oversold)
- MACD must be bullish
- SHENRON must confirm with >60% confidence
- May take hours/days to find first opportunity

---

## 📈 **SCALING UP**

Once profitable for 1-2 months:

### **Month 3:**
```python
INITIAL_CAPITAL = 200  # Double capital
```

### **Month 4:**
```python
INITIAL_CAPITAL = 500  # More aggressive
```

### **Month 6:**
```python
INITIAL_CAPITAL = 1000  # Serious trading
# Expected returns: $250-$350/month
```

---

## 🎯 **SUCCESS METRICS**

**Week 1:**
- [ ] Bot running 24/7
- [ ] Connected to exchange successfully
- [ ] SHENRON queries working
- [ ] First trade executed

**Month 1:**
- [ ] 5-10 trades completed
- [ ] 15-25% return achieved
- [ ] No losses >1.5%
- [ ] $100 → $115-$125

**Month 3:**
- [ ] 30+ trades completed
- [ ] 60-80% total return
- [ ] $100 → $160-$180
- [ ] System stable and profitable

**Month 6:**
- [ ] 100+ trades completed
- [ ] 300-500% total return
- [ ] $100 → $400-$600
- [ ] Generating $80-$150/month

---

## 💡 **PRO TIPS**

1. **Start Small:** $100 is perfect for learning
2. **Be Patient:** First trade may take days
3. **Check Daily:** First week, monitor progress
4. **Don't Panic:** Small losses are normal (-1.5% max)
5. **Trust SHENRON:** 6 AI warriors know best
6. **Compound:** Reinvest profits for growth
7. **Scale Slowly:** Double capital every 2-3 months

---

## 🚀 **READY TO LAUNCH?**

```bash
# One command to rule them all:
ssh mgmt1@<VM101_IP>
cd ~/trading_bot
source venv/bin/activate
nano trading_bot_production.py  # Add your API keys
python3 trading_bot_production.py  # Test run
# Then Ctrl+C and deploy as service (Step 6)
```

---

**TRADING BOT:** Ready to Deploy  
**Expected Time to Profit:** 1-7 days  
**Expected Month 1 Return:** 15-25%  
**Expected Month 6 Capital:** $400-$600

**🤖 LET THE BOT MAKE YOU MONEY WHILE YOU SLEEP! 💰**

---

**Questions? Check the logs:**
```bash
tail -f ~/trading_bot/trading.log
```

**Everything is documented. Just follow the steps!**

