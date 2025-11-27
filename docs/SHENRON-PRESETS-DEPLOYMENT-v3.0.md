<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 SHENRON'S SYNDICATE - PRESETS DEPLOYMENT GUIDE v3.0

## ✅ **PROPER LM STUDIO HUB DEPLOYMENT**

**Version:** 3.0.0  
**Date:** 2025-11-07  
**Type:** PRESETS (not models)  
**Author:** MatoTezi Tanka (@matotezitanka)  
**Organization:** @lightspeedup

---

## 📦 **WHAT'S INCLUDED:**

This package contains **6 PRESETS** for Shenron's Syndicate AI Council:

```
✅ GOKU.AI    - Adaptive Warrior & Growth Catalyst (DeepSeek Coder V2 Lite)
✅ VEGETA.AI  - Technical Authority & Precision Expert (Llama 3.2 3B)
✅ PICCOLO.AI - Strategic Architect & Long-term Planning (Qwen2.5 Coder 7B)
✅ GOHAN.AI   - Guardian & Risk Analysis Expert (Mistral 7B v0.3)
✅ KRILLIN.AI - Practical Engineer & Quick Implementation (Phi-3 Mini 128K)
✅ FRIEZA.AI  - Devil's Advocate & Contrarian Analyst (Phi-3 Mini 128K v2)
```

---

## ⚠️ **IMPORTANT: PRESETS vs MODELS**

### **What are PRESETS?**
- **Small configuration files** (KB, not GB)
- Reference external base models (HuggingFace)
- Include custom settings and system prompts
- Users must download base models separately

### **What are MODELS?**
- **Large GGUF files** (GB to tens of GB)
- Full model weights uploaded to Hub
- Users download everything from YOUR Hub

**We use PRESETS because:**
1. ✅ Smaller files (4.5 KB total for all 6!)
2. ✅ Don't re-upload existing models
3. ✅ Legal and proper Hub usage
4. ✅ Users get latest quantized versions

---

## 🗑️ **STEP 1: CLEAN UP VM100 (DO THIS FIRST)**

**ON VM100:**

```powershell
cd C:\GOKU-AI
powershell -ExecutionPolicy Bypass -File delete-downloaded-models.ps1
```

**This will:**
- Delete `C:\AI-Models-Q8_0\` directory
- Delete models from LM Studio directory
- Backup your conversations
- Clean up old warrior directories

---

## 🗑️ **STEP 2: DELETE OLD WARRIORS FROM HUB (DO THIS SECOND)**

**Go to:** https://lmstudio.ai/matotezitanka

**For each of these 6 warriors:**
- goku-ai-deepseek-coder-v2-lite-instruct
- vegeta-ai-llama-3.2-3b-instruct
- piccolo-ai-qwen2.5-coder-7b-instruct
- gohan-ai-mistral-7b-instruct-v0.3
- krillin-ai-phi-3-mini-128k-instruct
- frieza-ai-phi-3-mini-128k-instruct-v2

**Delete each one:**
1. Click on the warrior name
2. Click "Settings" tab
3. Scroll to bottom
4. Click "Delete Model" or "Delete Artifact"
5. Confirm deletion

---

## 📤 **STEP 3: UPLOAD PRESETS TO HUB (DO THIS ON VM100)**

### **Transfer tarball to VM100:**

**FROM LINUX (mgmt1):**
```bash
scp /home/mgmt1/GitHub/Dell-Server-Roadmap/shenrons-syndicate-presets-v3.0.tar.gz Administrator@<VM100_IP>:C:/GOKU-AI/
```

### **Extract and publish on VM100:**

**ON VM100:**
```powershell
cd C:\GOKU-AI

# Extract presets
tar -xzf shenrons-syndicate-presets-v3.0.tar.gz

# Verify extraction
Get-ChildItem -Recurse -Filter "*.yaml"
# Should show 6 preset.yaml files

# Publish each preset (one at a time)
cd GOKU-deepseek-coder-v2-lite-instruct
lms push
cd ..

cd VEGETA-llama-3.2-3b-instruct
lms push
cd ..

cd PICCOLO-qwen2.5-coder-7b-instruct
lms push
cd ..

cd GOHAN-mistral-7b-instruct-v0.3
lms push
cd ..

cd KRILLIN-phi-3-mini-128k-instruct
lms push
cd ..

cd FRIEZA-phi-3-mini-128k-instruct-v2
lms push
cd ..
```

**Expected output for each:**
```
Artifact successfully uploaded! View it at:
  https://lmstudio.ai/matotezitanka/goku-ai-shenron-syndicate (Revision 1)
```

---

## 📥 **STEP 4: DOWNLOAD PRESETS FROM YOUR HUB**

**ON VM100:**

```powershell
cd C:\GOKU-AI

# Download all 6 presets from YOUR Hub
lms get matotezitanka/goku-ai-shenron-syndicate
lms get matotezitanka/vegeta-ai-shenron-syndicate
lms get matotezitanka/piccolo-ai-shenron-syndicate
lms get matotezitanka/gohan-ai-shenron-syndicate
lms get matotezitanka/krillin-ai-shenron-syndicate
lms get matotezitanka/frieza-ai-shenron-syndicate
```

**Expected:** Each preset downloads in < 1 second (tiny files!)

---

## 📥 **STEP 5: DOWNLOAD BASE MODELS**

### **Method: LM Studio GUI (EASIEST)**

**Open LM Studio** → Press `Ctrl+Shift+M` (Model Search)

**Download these models (in order):**

1. **VEGETA** (~3 GB)
   - Search: `llama-3.2-3b Q8_0`
   - Download: `bartowski/Llama-3.2-3B-Instruct-GGUF` (Q8_0)

2. **KRILLIN** (~5 GB)
   - Search: `phi-3-mini 128k q8`
   - Download: `microsoft/Phi-3-mini-128k-instruct-gguf` (Q8_0)
   - ⚠️ **SET CONTEXT TO 32K** (not 128K!)

3. **FRIEZA** (~same as KRILLIN)
   - Uses same model as KRILLIN
   - Load twice with different presets
   - ⚠️ **SET CONTEXT TO 32K** (not 128K!)

4. **PICCOLO** (~7 GB)
   - Search: `qwen2.5-coder-7b Q8_0`
   - Download: `bartowski/Qwen2.5-Coder-7B-Instruct-GGUF` (Q8_0)

5. **GOHAN** (~7 GB)
   - Search: `mistral-7b-instruct-v0.3 Q8_0`
   - Download: `bartowski/Mistral-7B-Instruct-v0.3-GGUF` (Q8_0)

6. **GOKU** (~16 GB)
   - Search: `deepseek-coder-v2-lite Q8_0`
   - Download: `bartowski/deepseek-coder-v2-lite-instruct-GGUF` (Q8_0)

**Total download:** ~43 GB  
**Time estimate:** 15-20 minutes (60 MB/s internet)

---

## ⚙️ **STEP 6: APPLY PRESETS TO MODELS**

**In LM Studio:**

1. Go to "My Models" tab
2. For each model:
   - Right-click → "Apply Preset"
   - Select the corresponding warrior preset
   - Example: Apply "GOKU.AI" preset to "deepseek-coder-v2-lite-instruct"

**This will:**
- Set context length
- Set temperature and sampling params
- Apply custom system prompt
- Configure the AI personality

---

## 🖥️ **STEP 7: LOAD ALL 6 MODELS**

**In LM Studio → "Local Server" tab:**

**Load in this order (smallest to largest):**

```
1. VEGETA     (Llama-3.2-3B Q8_0)         ~3 GB
2. KRILLIN    (Phi-3-mini Q8_0)           ~5 GB  ⚠️ CONTEXT: 32K
3. FRIEZA     (Phi-3-mini Q8_0)           ~5 GB  ⚠️ CONTEXT: 32K
4. PICCOLO    (Qwen2.5-Coder-7B Q8_0)     ~7 GB
5. GOHAN      (Mistral-7B Q8_0)           ~7 GB
6. GOKU       (DeepSeek-Coder-V2 Q8_0)   ~16 GB
```

**For each model:**
- Click "Load Model"
- Select the model
- Verify preset is applied
- **CRITICAL FOR KRILLIN/FRIEZA:** Set context to 32768 (32K)
- Click "Load"
- Wait for green checkmark

**Monitor RAM:** Should stay < 80 GB total

---

## ✅ **STEP 8: VERIFY & TEST**

### **Verify all 6 models loaded:**

```powershell
Invoke-RestMethod -Uri "http://localhost:1234/v1/models" | ConvertTo-Json -Depth 5
```

**Expected:** 6 models listed

---

### **Test SHENRON Health:**

```powershell
Invoke-RestMethod -Uri "http://localhost:5000/health"
```

**Expected:**
```json
{
  "status": "operational",
  "version": "4.0",
  "warriors_loaded": 6
}
```

---

### **Test Simple Query:**

```powershell
$body = @{
    wish = "What is the IP address of VM100?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/api/shenron/grant-wish" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body `
  -TimeoutSec 180
```

**Expected:** Unified response with consensus from all 6 warriors

---

### **Test Web UI:**

1. Open: https://shenron.lightspeedup.com
2. Enter: "What is Proxmox?"
3. Click: "SUMMON SHENRON"
4. Verify:
   - ✅ Warrior status: "Consulting..." → "Complete" (green)
   - ✅ SHENRON's unified response appears
   - ✅ Individual warrior responses expand

---

## 📊 **DEPLOYMENT CHECKLIST:**

```
🗑️  Step 1: Clean up VM100 (delete downloaded models)
🗑️  Step 2: Delete old warriors from Hub (web UI)
📤 Step 3: Extract & publish presets to Hub (lms push x6)
📥 Step 4: Download presets from YOUR Hub (lms get x6)
📥 Step 5: Download base models via LM Studio GUI (43 GB)
⚙️  Step 6: Apply presets to models (right-click → Apply Preset)
🖥️  Step 7: Load all 6 models in LM Studio (Local Server)
✅ Step 8: Verify & test SHENRON (API + Web UI)
```

---

## ⏱️ **TIMELINE:**

```
Step 1 (VM cleanup):           5 min
Step 2 (Hub deletion):         5 min
Step 3 (Publish presets):      5 min
Step 4 (Download presets):     1 min
Step 5 (Download base models): 15-20 min
Step 6 (Apply presets):        5 min
Step 7 (Load models):          10 min
Step 8 (Verify & test):        5 min
-------------------------------------------
TOTAL:                         50-55 min
```

---

## 📝 **NOTES:**

### **Preset vs Model Files:**
- **Presets** are in `preset.yaml` files
- **Models** were in `model.yaml` files (v2.0)
- Hub now correctly identifies these as "preset" artifacts

### **Base Model Downloads:**
- Users download from HuggingFace, not your Hub
- This is the proper LM Studio Hub way
- Smaller Hub storage, faster deployments

### **Context Length:**
- **KRILLIN & FRIEZA:** Use 32K context (not 128K!)
- **All others:** Use default context lengths
- This saves significant RAM

### **RAM Requirements:**
```
VEGETA:    4-8 GB
KRILLIN:   5-10 GB (32K context)
FRIEZA:    5-10 GB (32K context)
PICCOLO:   8-16 GB
GOHAN:     8-16 GB
GOKU:      16-32 GB
----------------------------
TOTAL:     ~46-92 GB (expect 60-70 GB)
```

---

## 🚀 **SHARING WITH OTHERS:**

When others want to use Shenron's Syndicate:

1. They visit your Hub: https://lmstudio.ai/matotezitanka
2. Download the 6 presets (tiny files)
3. Download base models from HuggingFace (via LM Studio GUI)
4. Apply presets to models
5. Load all 6 and run SHENRON

**Your presets are now shareable and legal!** ✅

---

## 📚 **FILES IN THIS PACKAGE:**

```
shenrons-syndicate-presets-v3.0.tar.gz (4.5 KB)
│
├── GOKU-deepseek-coder-v2-lite-instruct/
│   ├── manifest.json
│   └── preset.yaml
│
├── VEGETA-llama-3.2-3b-instruct/
│   ├── manifest.json
│   └── preset.yaml
│
├── PICCOLO-qwen2.5-coder-7b-instruct/
│   ├── manifest.json
│   └── preset.yaml
│
├── GOHAN-mistral-7b-instruct-v0.3/
│   ├── manifest.json
│   └── preset.yaml
│
├── KRILLIN-phi-3-mini-128k-instruct/
│   ├── manifest.json
│   └── preset.yaml
│
└── FRIEZA-phi-3-mini-128k-instruct-v2/
    ├── manifest.json
    └── preset.yaml
```

---

## 🐉 **READY TO DEPLOY!**

All presets are created, packaged, and ready for upload.

**Your next steps:**
1. Clean VM100 (delete old models)
2. Delete old warriors from Hub
3. Publish these presets
4. Download & apply
5. Test SHENRON!

⚡ **LET'S DO THIS PROPERLY!** ⚡

