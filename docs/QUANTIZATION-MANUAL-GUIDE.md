<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔴 TASK 3: MODEL QUANTIZATION - MANUAL GUIDE

**Goal:** 145 GB → 73 GB RAM (2x customer capacity)  
**Time:** 2-3 hours (mostly download time)  
**Method:** Replace full-precision models with INT8 quantized versions

---

## ⚡ **QUICK START (AUTOMATED)**

### **Option A: Run Automated Script (Recommended)**

1. **Transfer script to VM100:**
   ```bash
   scp /tmp/quantize-models-complete.ps1 Administrator@<VM100_IP>:C:/GOKU-AI/quantize-models.ps1
   ```

2. **Run on VM100:**
   ```powershell
   cd C:\GOKU-AI
   powershell -ExecutionPolicy Bypass -File quantize-models.ps1
   ```

3. **Follow prompts:**
   - Script downloads all 6 models automatically
   - Backs up current models
   - Provides instructions for LM Studio import
   - Verifies RAM usage
   - Tests SHENRON

---

## 📥 **MANUAL DOWNLOAD (If Automated Fails)**

### **Direct Download Links:**

Download INT8 (Q8_0) quantized models from HuggingFace:

#### **1. GOKU (deepseek-coder-v2-lite-instruct) - 13 GB**
- **Repo:** https://huggingface.co/bartowski/deepseek-coder-v2-lite-instruct-GGUF
- **File:** `deepseek-coder-v2-lite-instruct-Q8_0.gguf`
- **Download:** Click "Files and versions" → Download Q8_0.gguf file
- **Save to:** `C:\AI-Models-Quantized\GOKU\`

#### **2. VEGETA (llama-3.2-3b-instruct) - 2 GB**
- **Repo:** https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF
- **File:** `Llama-3.2-3B-Instruct-Q8_0.gguf`
- **Download:** Click "Files and versions" → Download Q8_0.gguf file
- **Save to:** `C:\AI-Models-Quantized\VEGETA\`

#### **3. PICCOLO (qwen2.5-coder-7b-instruct) - 4 GB**
- **Repo:** https://huggingface.co/bartowski/Qwen2.5-Coder-7B-Instruct-GGUF
- **File:** `Qwen2.5-Coder-7B-Instruct-Q8_0.gguf`
- **Download:** Click "Files and versions" → Download Q8_0.gguf file
- **Save to:** `C:\AI-Models-Quantized\PICCOLO\`

#### **4. GOHAN (mistral-7b-instruct-v0.3) - 4 GB**
- **Repo:** https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.3-GGUF
- **File:** `Mistral-7B-Instruct-v0.3-Q8_0.gguf`
- **Download:** Click "Files and versions" → Download Q8_0.gguf file
- **Save to:** `C:\AI-Models-Quantized\GOHAN\`

#### **5. KRILLIN (phi-3-mini-128k-instruct) - 5 GB**
- **Repo:** https://huggingface.co/bartowski/Phi-3-mini-128k-instruct-GGUF
- **File:** `Phi-3-mini-128k-instruct-Q8_0.gguf`
- **Download:** Click "Files and versions" → Download Q8_0.gguf file
- **Save to:** `C:\AI-Models-Quantized\KRILLIN\`

#### **6. FRIEZA (phi-3-mini-128k-instruct) - 4 GB**
- **Repo:** https://huggingface.co/bartowski/Phi-3-mini-128k-instruct-GGUF
- **File:** `Phi-3-mini-128k-instruct-Q8_0.gguf` (same as KRILLIN)
- **Download:** Copy from KRILLIN or download again
- **Save to:** `C:\AI-Models-Quantized\FRIEZA\`

**TOTAL DOWNLOAD SIZE:** ~32 GB (compressed), ~73 GB (in RAM)

---

## 🔧 **LM STUDIO IMPORT INSTRUCTIONS**

### **Step 1: Open LM Studio**
```powershell
# On VM100:
Start "C:\Users\Administrator\AppData\Local\Programs\LM Studio\LM Studio.exe"
```

### **Step 2: Unload Current Models (If Loaded)**
1. In LM Studio, go to **"Local Server"** tab
2. If models are loaded, click **"Stop Server"**
3. Go to **"My Models"** tab

### **Step 3: Import Quantized Models**
For each warrior (do in this order - smallest to largest):

1. **VEGETA** (2 GB):
   - Click **"Import Model"** or **"+"**
   - Browse to: `C:\AI-Models-Quantized\VEGETA\*.gguf`
   - Select the Q8_0.gguf file
   - Click **"Import"**
   - Rename to: `llama-3.2-3b-instruct` (match original name)

2. **GOHAN** (4 GB):
   - Import: `C:\AI-Models-Quantized\GOHAN\*.gguf`
   - Rename to: `mistral-7b-instruct-v0.3`

3. **PICCOLO** (4 GB):
   - Import: `C:\AI-Models-Quantized\PICCOLO\*.gguf`
   - Rename to: `qwen2.5-coder-7b-instruct`

4. **FRIEZA** (4 GB):
   - Import: `C:\AI-Models-Quantized\FRIEZA\*.gguf`
   - Rename to: `phi-3-mini-128k-instruct:2`

5. **KRILLIN** (5 GB):
   - Import: `C:\AI-Models-Quantized\KRILLIN\*.gguf`
   - Rename to: `phi-3-mini-128k-instruct`

6. **GOKU** (13 GB):
   - Import: `C:\AI-Models-Quantized\GOKU\*.gguf`
   - Rename to: `deepseek-coder-v2-lite-instruct`

### **Step 4: Load All 6 Models**
1. Go to **"Local Server"** tab
2. Click **"Start Server"** (if not already started)
3. Go to **"My Models"** tab
4. For each model, click **"Load"** button
5. Load in order: VEGETA → GOHAN → PICCOLO → FRIEZA → KRILLIN → GOKU

**CRITICAL:** Load FRIEZA with **32K context** (not 128K)
- When loading FRIEZA, set context length to **32768** (not 128000)
- 128K context requires too much RAM!

### **Step 5: Verify All Models Loaded**
```powershell
# On VM100 (PowerShell):
Invoke-RestMethod -Uri "http://localhost:1234/v1/models"
```

**Expected Output:** 6 models listed

---

## ✅ **VERIFICATION & TESTING**

### **Check RAM Usage:**
```powershell
# On VM100 (PowerShell):
Get-Process | Where-Object {$_.ProcessName -match "LM.*Studio"} | Select-Object ProcessName, @{Name="RAM_GB";Expression={[math]::Round($_.WorkingSet64 / 1GB, 2)}}
```

**Expected:** RAM_GB < 80 GB (down from 145 GB)

**Performance Comparison:**
```
OLD (Full Precision): ~145 GB
NEW (INT8 Quantized): ~73 GB
REDUCTION: ~72 GB (50%)
```

### **Test SHENRON API:**
```powershell
# Restart SHENRON service:
Restart-Service -Name "SHENRON" -Force
Start-Sleep -Seconds 30

# Check health:
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Test query:
$body = @{query = "What is 2+2?"} | ConvertTo-Json
Invoke-RestMethod -Uri "http://localhost:5000/api/shenron/grant-wish" `
                   -Method POST `
                   -Body $body `
                   -ContentType "application/json" `
                   -TimeoutSec 120
```

**Expected:**
- All 6 warriors respond
- Response quality similar to before
- Query time: 10-30 seconds (with parallel fix)

### **Test Accuracy:**
Submit these queries and compare to previous responses:

1. **Simple:** "What is 2+2?"
2. **RAG:** "Explain the Dell R730 server configuration"
3. **Practical:** "How do I troubleshoot Apache 500 errors?"
4. **Trading:** "What are the best technical indicators for day trading?"

**Expected:** >95% accuracy retained (minimal degradation)

---

## 📊 **SUCCESS CRITERIA**

- ✅ All 6 models quantized to INT8
- ✅ RAM usage: <80 GB (down from 145 GB)
- ✅ All warriors respond correctly
- ✅ SHENRON synthesizes correctly
- ✅ Accuracy: >95% of original
- ✅ No errors in logs
- ✅ Query time: <30 seconds

---

## 🔄 **ROLLBACK (If Needed)**

If quantization causes issues:

```powershell
# On VM100:
# 1. Stop SHENRON
Stop-Service -Name "SHENRON" -Force

# 2. Close LM Studio

# 3. Restore original models from backup
$BACKUP_DIR = Get-ChildItem "C:\AI-Models-Original-Backup-*" | Sort-Object -Descending | Select-Object -First 1
Copy-Item -Path $BACKUP_DIR.FullName -Destination "$env:USERPROFILE\.cache\lm-studio\models" -Recurse -Force

# 4. Restart LM Studio and reload original models

# 5. Restart SHENRON
Start-Service -Name "SHENRON"

# 6. Verify
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

**Result:** Back to 145 GB RAM but with full precision

---

## 📋 **POST-QUANTIZATION CHECKLIST**

- [ ] All 6 models downloaded
- [ ] All 6 models imported into LM Studio
- [ ] All 6 models renamed to match originals
- [ ] All 6 models loaded (verify via API)
- [ ] FRIEZA loaded with 32K context (not 128K)
- [ ] RAM usage verified (<80 GB)
- [ ] SHENRON service restarted
- [ ] SHENRON API operational
- [ ] Test query successful
- [ ] Accuracy verified (>95%)
- [ ] Web UI tested
- [ ] Documentation updated
- [ ] GitHub committed

---

## 📚 **DOCUMENTATION TO UPDATE**

After successful quantization:

1. **VM100-BEAST-MODE-UPGRADE.md:**
   - Update model RAM sizes (145 GB → 73 GB)
   - Add quantization details

2. **ETERNAL-DRAGON-SHENRON-KNOWLEDGE.md:**
   - Update current hardware config
   - Add INT8 quantization info

3. **SHENRON-CURRENT-STATUS-2025-11-06.md:**
   - Update performance metrics
   - Update RAM usage

4. **README.md:**
   - Update system status
   - Add quantization complete

5. **Create MODEL-QUANTIZATION-COMPLETE.md:**
   - Document completion of Task 3
   - Include before/after comparison
   - Include test results

6. **Update HELP-ME-07-NOV-2025.md:**
   - Strikethrough Task 3
   - Update "Last Updated" timestamp
   - Update "CURRENT STATUS" section

---

## ⏱️ **ESTIMATED TIME**

| Step | Time | Description |
|------|------|-------------|
| Download models | 1-2 hours | Depends on internet speed |
| Import to LM Studio | 15 minutes | Manual clicking |
| Load models | 10 minutes | RAM allocation |
| Verify & test | 15 minutes | API checks, queries |
| Documentation | 15 minutes | Update docs, commit |
| **TOTAL** | **2-3 hours** | Mostly waiting for downloads |

---

## 🎯 **EXPECTED BENEFITS**

### **Immediate:**
- 50% RAM reduction (145 GB → 73 GB)
- 2x customer capacity (5 → 10-15 customers)
- More stable system (more headroom)
- Lower hosting costs (less RAM pressure)

### **Long-term:**
- Room for additional AI models
- Can add more features (Quest Manager, Trading Bot)
- Better performance under load
- Easier to scale

---

**Status:** Ready for execution  
**Method:** Automated script + manual LM Studio steps  
**Time:** 2-3 hours  
**Confidence:** 95% (INT8 is proven technology)

🐉 **READY TO QUANTIZE! LET'S GET 2X CAPACITY!** ⚡

