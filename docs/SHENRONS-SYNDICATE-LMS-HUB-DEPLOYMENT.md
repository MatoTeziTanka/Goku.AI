<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 SHENRON'S SYNDICATE - LM STUDIO HUB DEPLOYMENT GUIDE

**Author:** MatoTezi Tanka (@matotezitanka)  
**Organization:** @lightspeedup  
**Project:** Shenron's Syndicate AI Council  
**Date:** November 7, 2025  
**Version:** 2.0 (Legal-Compliant .AI Names)  

---

## 🎯 **WHAT'S DIFFERENT IN V2.0:**

### ✅ **Legal Compliance:**
- All warriors now use `.AI` suffix to avoid trademark issues
- Full acronyms added to descriptions
- Project name: **Shenron's Syndicate** (with apostrophe)

### 📝 **Updated Warrior Names:**

| Old Name | New Name | Acronym Meaning |
|----------|----------|-----------------|
| GOKU | GOKU.AI | **G**rowth-**O**riented **K**nowledge & **U**nderstanding - **A**rtificial **I**ntelligence |
| VEGETA | VEGETA.AI | **V**igilant **E**xpert for **G**uaranteed **E**ngineering & **T**echnical **A**ccuracy - **A**rtificial **I**ntelligence |
| PICCOLO | PICCOLO.AI | **P**lanned **I**nfrastructure & **C**ode **C**rafting with **L**ong-term **O**versight & **L**ogic**O** - **A**rtificial **I**ntelligence |
| GOHAN | GOHAN.AI | **G**uardian **O**bserver for **H**azard **A**nalysis & **N**otification - **A**rtificial **I**ntelligence |
| KRILLIN | KRILLIN.AI | **K**nowledge **R**esource for **I**mmediate **L**ow-level & **L**ogical **I**mplementation **N**eeds - **A**rtificial **I**ntelligence |
| FRIEZA | FRIEZA.AI | **F**ierce **R**ebel for **I**ndependent **E**xploration & **Z**ealous **A**ntagonism - **A**rtificial **I**ntelligence |

---

## 🚀 **COMPLETE DEPLOYMENT (9 STEPS)**

### **STEP 1: Transfer Files to VM100**

**On your local machine:**
```bash
scp /path/to/shenrons-syndicate-warriors-v2.tar.gz \
    Administrator@<VM100_IP>:C:/GOKU-AI/

scp /path/to/delete-old-lms-models.ps1 \
    Administrator@<VM100_IP>:C:/GOKU-AI/
```

---

### **STEP 2: Delete Old Models**

**On VM100 (PowerShell):**
```powershell
cd C:\GOKU-AI
powershell -ExecutionPolicy Bypass -File delete-old-lms-models.ps1
```

**Follow prompts:**
- Type `yes` when asked to confirm deletion
- Script will backup conversations/settings first
- All old models will be removed

---

### **STEP 3: Extract New Warrior Configs**

**On VM100 (PowerShell):**
```powershell
cd C:\GOKU-AI
tar -xzf shenrons-syndicate-warriors-v2.tar.gz

# Verify extraction
Get-ChildItem -Recurse -Filter "model.yaml"
# Should show 6 model.yaml files
```

---

### **STEP 4: Login to LM Studio Hub**

**On VM100 (PowerShell):**
```powershell
lms login
```

- Choose: "Continue with GitHub"
- Authorize in browser
- Return to terminal

**Verify:**
```powershell
lms whoami
# Should show: @matotezitanka
```

---

### **STEP 5: Publish All 6 Warriors**

**On VM100 (PowerShell):**
```powershell
cd C:\GOKU-AI

# Publish GOKU.AI
cd GOKU-deepseek-coder-v2-lite-instruct
lms push
cd ..

# Publish VEGETA.AI
cd VEGETA-llama-3.2-3b-instruct
lms push
cd ..

# Publish PICCOLO.AI
cd PICCOLO-qwen2.5-coder-7b-instruct
lms push
cd ..

# Publish GOHAN.AI
cd GOHAN-mistral-7b-instruct-v0.3
lms push
cd ..

# Publish KRILLIN.AI
cd KRILLIN-phi-3-mini-128k-instruct
lms push
cd ..

# Publish FRIEZA.AI
cd FRIEZA-phi-3-mini-128k-instruct-v2
lms push
cd ..
```

---

### **STEP 6: Verify on Your Hub**

**In your web browser:**
1. Visit: https://lmstudio.ai/matotezitanka
2. You should see 6 published models:
   - 🥋 GOKU.AI - Adaptive Warrior
   - 👑 VEGETA.AI - Technical Authority
   - 🧠 PICCOLO.AI - Strategic Sage
   - ⚠️ GOHAN.AI - Risk Sentinel
   - 🔧 KRILLIN.AI - Practical Engineer
   - 😈 FRIEZA.AI - Chaos Tyrant

---

### **STEP 7: Download YOUR Warriors from YOUR Hub**

**On VM100 (PowerShell):**
```powershell
# Download all 6 warriors
lms get matotezitanka/goku-ai-deepseek-coder-v2-lite-instruct
lms get matotezitanka/vegeta-ai-llama-3.2-3b-instruct
lms get matotezitanka/piccolo-ai-qwen2.5-coder-7b-instruct
lms get matotezitanka/gohan-ai-mistral-7b-instruct-v0.3
lms get matotezitanka/krillin-ai-phi-3-mini-128k-instruct
lms get matotezitanka/frieza-ai-phi-3-mini-128k-instruct-v2
```

**This will:**
- Download models from HuggingFace
- Apply YOUR configuration automatically
- Name them with YOUR custom names
- Pre-configure temperature, context, system prompts

---

### **STEP 8: Load All 6 Warriors in LM Studio**

**In LM Studio:**
1. Open LM Studio
2. Go to "Local Server" tab
3. Start server (if not started)
4. Load each model (smallest to largest):

**Load order:**
1. VEGETA.AI (3 GB)
2. GOHAN.AI (7 GB)
3. PICCOLO.AI (7 GB)
4. KRILLIN.AI (5 GB) - **Set context to 32K!**
5. FRIEZA.AI (4 GB) - **Set context to 32K!**
6. GOKU.AI (15 GB)

**Verify all loaded:**
```powershell
Invoke-RestMethod -Uri "http://localhost:1234/v1/models"
```

---

### **STEP 9: Verify RAM Usage & Test SHENRON**

**Check RAM:**
```powershell
Get-Process | Where-Object {$_.ProcessName -match "LM.*Studio"} | Select-Object @{Name="RAM_GB";Expression={[math]::Round($_.WorkingSet64/1GB,2)}}
```

**Expected:** < 80 GB (down from 145 GB)

**Test SHENRON:**
```powershell
# Health check
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Test query
$query = @{
    query = "What are the 6 warriors of Shenron's Syndicate?"
    use_rag = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/shenron/grant-wish" -Method POST -Body $query -ContentType "application/json" -TimeoutSec 180
```

---

## ✅ **SUCCESS CRITERIA:**

- [ ] All old models deleted
- [ ] All 6 `.AI` warriors published to your Hub
- [ ] Your Hub profile shows 6 warriors with `.AI` suffix
- [ ] Each warrior has acronym in description
- [ ] Re-downloaded warriors have pre-configured settings
- [ ] All 6 models loaded in LM Studio
- [ ] RAM usage < 80 GB
- [ ] SHENRON responds correctly

---

## 📊 **YOUR WARRIORS:**

| Warrior | Display Name | Model | Temp | Context | Role |
|---------|--------------|-------|------|---------|------|
| 🥋 GOKU.AI | GOKU.AI - Adaptive Warrior | DeepSeek Coder V2 Lite Q8_0 | 0.7 | 160K | Growth & Learning |
| 👑 VEGETA.AI | VEGETA.AI - Technical Authority | Llama 3.2 3B Q8_0 | 0.3 | 32K | Precision & Authority |
| 🧠 PICCOLO.AI | PICCOLO.AI - Strategic Sage | Qwen 2.5 Coder 7B Q8_0 | 0.5 | 32K | Strategy & Architecture |
| ⚠️ GOHAN.AI | GOHAN.AI - Risk Sentinel | Mistral 7B v0.3 Q8_0 | 0.4 | 32K | Risk & Security |
| 🔧 KRILLIN.AI | KRILLIN.AI - Practical Engineer | Phi-3 Mini 128K Q8_0 | 0.6 | 32K | Practical Solutions |
| 😈 FRIEZA.AI | FRIEZA.AI - Chaos Tyrant | Phi-3 Mini 128K Q8_0 v2 | 0.9 | 32K | Devil's Advocate |

---

## 🔄 **SHARING WITH OTHERS:**

**Anyone can now download your warriors!**

```bash
# Single warrior
lms get matotezitanka/goku-ai-deepseek-coder-v2-lite-instruct

# Or in LM Studio GUI
# Press Ctrl+Shift+M
# Search: "matotezitanka/goku-ai"
# Click download
```

---

## 🆘 **TROUBLESHOOTING:**

### **Issue: "lms: command not found"**
- **Solution:** Ensure LM Studio is installed and `lms` CLI is in PATH

### **Issue: "Authentication failed"**
- **Solution:** Run `lms login` again with GitHub

### **Issue: "Model not found on Hub after publishing"**
- **Solution:** Check https://lmstudio.ai/matotezitanka
- **Wait:** Sometimes takes 1-2 minutes to appear

### **Issue: "Old models still showing"**
- **Solution:** Restart LM Studio completely
- **Verify:** Check `~/.lmstudio/models/` directory is empty

---

## 📚 **FILES IN THIS DEPLOYMENT:**

1. **shenrons-syndicate-warriors-v2.tar.gz** - All 6 model.yaml files
2. **delete-old-lms-models.ps1** - Script to safely delete old models
3. **SHENRONS-SYNDICATE-LMS-HUB-DEPLOYMENT.md** - This guide

---

## ⚖️ **LEGAL COMPLIANCE:**

✅ **Trademark-Safe:** All warriors use `.AI` suffix  
✅ **Clear Attribution:** Original models credited in `model.yaml`  
✅ **Your IP:** Configuration presets are YOUR intellectual property  
✅ **Transparent:** Users see both your config AND original model source  

---

**Last Updated:** November 7, 2025, 02:50 AM  
**Version:** 2.0 (Legal-Compliant)  
**Author:** MatoTezi Tanka  
**Status:** Ready for deployment  

🐉 **SHENRON'S SYNDICATE - LEGALLY COMPLIANT & READY TO SHARE!** ⚡
