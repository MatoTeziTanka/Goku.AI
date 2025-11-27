# 🐉 SHENRON POWER MODES - USER GUIDE

**Version:** 5.0 - Ultra Instinct  
**Website:** https://shenron.lightspeedup.com

---

## 🚀 **QUICK START**

### **Step 1: Enable Agent Mode**
1. Open https://shenron.lightspeedup.com
2. Scroll to "🤖 AGENT MODE - ULTRA INSTINCT" tile
3. Click the checkbox
4. Enter your **6-digit Google Authenticator code**
5. Wait for "✅ Enabled (59min remaining)" confirmation

### **Step 2: Select Power Mode**
After Agent Mode is enabled, you'll see **4 power options**:

- **🧠 AUTO SELECT** - Let SHENRON choose (RECOMMENDED)
- **⚡ LIGHTNING MODE** - Fast & simple (5-10s)
- **🔥 COUNCIL MODE** - Balanced & accurate (20-40s)
- **🐉 ULTRA INSTINCT** - Maximum power (60-180s)

### **Step 3: Ask Your Question**
Type your query in the text box. If you selected AUTO mode, watch as SHENRON automatically detects the best power level!

### **Step 4: Summon Shenron**
Click "⚡ SUMMON SHENRON ⚡" and watch the warriors respond!

---

## ⚡ **WHEN TO USE EACH MODE**

### **🧠 AUTO SELECT (Recommended)**
Let SHENRON analyze your query and automatically choose the best mode.

**Perfect for:** Everything! The AI is smart enough to detect what you need.

---

### **⚡ LIGHTNING MODE**
**Power:** 1,000  
**Speed:** 5-10 seconds  
**Accuracy:** 85-90%  
**Warriors:** 1 (Goku)

**Use for:**
- Quick definitions: "What is Docker?"
- Simple status checks: "Is my server running?"
- Fast facts: "What's the command to restart Apache?"
- Basic questions: "How do I check disk space?"

**Example Queries:**
```
"What is Kubernetes?"
"Quick server status"
"Show me disk usage"
"What's my IP address?"
```

---

### **🔥 COUNCIL MODE (Default)**
**Power:** 9,000  
**Speed:** 20-40 seconds  
**Accuracy:** 95-99%  
**Warriors:** 6 (All)

**Use for:**
- Technical questions
- Configuration help
- Architecture decisions
- Code reviews
- Troubleshooting

**Example Queries:**
```
"How do I configure Nginx as a reverse proxy?"
"What's the best way to backup my database?"
"Should I use Docker Compose or Kubernetes?"
"How can I improve my website performance?"
```

---

### **🐉 ULTRA INSTINCT MODE**
**Power:** OVER 9000!  
**Speed:** 60-180 seconds  
**Accuracy:** 99.99999999%  
**Warriors:** 6 (Multi-pass with debate)

**Use for:**
- Critical production decisions
- Complex multi-step operations
- Complete system analysis
- Mission-critical code changes
- When you need absolute certainty

**Example Queries:**
```
"Analyze my entire infrastructure and recommend optimizations"
"Review all my code for security vulnerabilities"
"Design a complete CI/CD pipeline for my project"
"What's the absolute best way to scale my application?"
"Diagnose why my server is slow and fix everything"
```

**What makes Ultra Instinct special:**
- If warriors disagree, they conduct a **debate round**
- Uses **multi-pass consensus** for maximum accuracy
- Can execute **multiple operations** autonomously
- Provides **confidence scores** for critical decisions

---

## 🧠 **HOW AUTO-DETECTION WORKS**

When you type a query in AUTO mode, SHENRON analyzes:

### **Triggers LIGHTNING MODE:**
- Contains: "quick", "fast", "what is", "simple", "status", "check"
- Word count < 10 words
- **Examples:**
  - "What is Docker?" → ⚡ LIGHTNING
  - "Quick status check" → ⚡ LIGHTNING

### **Triggers ULTRA INSTINCT MODE:**
- Contains: "optimize entire", "analyze all", "fix everything"
- Contains: "diagnose and fix", "maximum accuracy", "best possible"
- Word count > 50 words
- Multiple chained operations ("do X and then Y")
- **Examples:**
  - "Optimize my entire infrastructure" → 🐉 ULTRA
  - "Analyze all my code and fix all bugs" → 🐉 ULTRA

### **Defaults to COUNCIL MODE:**
- Everything else gets balanced Council Mode
- **Examples:**
  - "How do I configure Nginx?" → 🔥 COUNCIL
  - "What's the best Docker image for Node.js?" → 🔥 COUNCIL

---

## 💡 **PRO TIPS**

### **Tip 1: Trust AUTO Mode**
The AI is really good at detecting what you need. Start with AUTO and only switch to manual if you have a specific reason.

### **Tip 2: Be Specific with Ultra Instinct**
When using Ultra Instinct, be as detailed as possible. The more context you provide, the better the multi-pass analysis will be.

**Bad:** "Optimize my server"  
**Good:** "Analyze my entire VM100 server infrastructure (CPU, RAM, disk, network) and recommend specific optimizations with exact commands"

### **Tip 3: Use Lightning for Documentation**
If you're just looking something up, Lightning Mode is perfect:
- "What is X?"
- "Show me the syntax for Y"
- "Quick reminder on Z"

### **Tip 4: Watch the Console**
Open your browser's Developer Console (F12) to see:
- Which power mode was selected
- Why AUTO mode chose that mode
- Real-time warrior status updates
- API response details

### **Tip 5: Agent Mode Session**
Agent Mode stays enabled for **1 hour** after 2FA verification. The countdown shows remaining time. After expiration, you'll need to re-authenticate.

---

## 🎨 **READING THE UI**

### **AUTO-DETECTED MODE Box:**
When you type a query in AUTO mode, you'll see:

```
🧠 AUTO-DETECTED:
🔥 COUNCIL MODE
Power: 9,000 • 6 Warriors • Time: 20-40s • Accuracy: 95-99%
```

This shows you what SHENRON will use. You can override by selecting a different mode.

### **Power Level Indicators:**
- **1,000** = Lightning Mode (fast)
- **9,000** = Council Mode (balanced)
- **OVER 9000!** = Ultra Instinct Mode (maximum)

### **Warrior Status:**
- **Ready** = Warrior waiting
- **Consulting...** = Warrior thinking
- **Complete** ✅ = Warrior finished (turns green)

---

## 🔐 **SECURITY NOTES**

- **2FA Required:** You need your Google Authenticator app
- **1-Hour Session:** Re-authenticate after timeout
- **No Storage:** 2FA code is never stored, only verified
- **Rate Limited:** 5 attempts per minute max

---

## 🐛 **TROUBLESHOOTING**

### **Problem: Agent Mode won't enable**
- ✅ Check your 2FA code is exactly 6 digits
- ✅ Make sure the code is current (they expire every 30 seconds)
- ✅ Try refreshing the page

### **Problem: Power Mode selection not visible**
- ✅ You must enable Agent Mode first (with 2FA)
- ✅ The selection appears right below the Agent Mode checkbox

### **Problem: AUTO mode not detecting properly**
- ✅ Make sure you're typing in the query box
- ✅ AUTO detection happens as you type (real-time)
- ✅ Check the "AUTO-DETECTED" box to see what it chose

### **Problem: Query taking too long**
- ✅ Check if you accidentally selected Ultra Instinct (60-180s)
- ✅ Look at warrior tiles - they should turn green as they complete
- ✅ If stuck > 3 minutes, refresh the page

---

## 📊 **POWER MODE COMPARISON**

| Feature | ⚡ LIGHTNING | 🔥 COUNCIL | 🐉 ULTRA INSTINCT |
|---------|-------------|-----------|------------------|
| **Speed** | 5-10s | 20-40s | 60-180s |
| **Accuracy** | 85-90% | 95-99% | 99.99999999% |
| **Warriors** | 1 | 6 | 6 (multi-pass) |
| **RAG Search** | ❌ | ✅ | ✅ Deep |
| **Synthesis** | ❌ | ✅ | ✅ Multi-pass |
| **Debate Mode** | ❌ | ❌ | ✅ |
| **MCP Tools** | ❌ | ✅ Basic | ✅ Full |
| **Best For** | Quick facts | Most queries | Critical ops |
| **Cost** | Cheapest | Medium | Expensive |

---

## 🎯 **REAL-WORLD EXAMPLES**

### **Example 1: Morning Server Check**
**Query:** "Quick server status check"  
**AUTO Detects:** ⚡ LIGHTNING MODE  
**Result:** 7 seconds, one warrior, basic status ✅

### **Example 2: Configuration Help**
**Query:** "How do I set up SSL certificates with Nginx?"  
**AUTO Detects:** 🔥 COUNCIL MODE  
**Result:** 28 seconds, all 6 warriors agree, detailed steps ✅

### **Example 3: Production Decision**
**Query:** "Analyze my entire infrastructure and recommend if I should migrate to Kubernetes or stick with Docker Compose"  
**AUTO Detects:** 🐉 ULTRA INSTINCT MODE  
**Result:** 94 seconds, 2 passes, warriors debated pros/cons, unanimous final recommendation ✅

---

## 🚀 **ADVANCED: MANUAL MODE SELECTION**

If you want to **force** a specific mode regardless of query:

1. Select the radio button for your desired mode
2. The AUTO-DETECTED box will disappear
3. That mode will be used no matter what you type
4. Useful for testing or when you know exactly what you need

**Use Case:** You're testing Ultra Instinct performance, so you manually select it even for simple queries.

---

## 📞 **SUPPORT**

If you encounter issues:
1. Check the browser console (F12) for error messages
2. Verify Agent Mode is enabled and 2FA verified
3. Make sure the API status light is **green** (top right)
4. Try refreshing the page
5. If all else fails, disable and re-enable Agent Mode

---

## 🎉 **ENJOY YOUR ULTRA INSTINCT POWERS!**

You now have access to:
- ⚡ Lightning-fast responses when you need them
- 🔥 Balanced consensus for daily use
- 🐉 Maximum accuracy for critical decisions
- 🧠 Smart AUTO mode that picks the best option

**May the Dragon Balls be with you!** 🔮✨

---

**Version:** 5.0  
**Last Updated:** November 7, 2025  
**Website:** https://shenron.lightspeedup.com

