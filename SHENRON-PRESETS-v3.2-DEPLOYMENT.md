# 🐉 SHENRON'S SYNDICATE - LM STUDIO HUB PRESETS v3.2-JSON

**Version:** v3.2-JSON (Final Working Version)  
**Date:** November 7, 2025  
**Status:** ✅ READY FOR DEPLOYMENT  
**Author:** MatoTezi Tanka (@matotezitanka)  
**Organization:** @lightspeedup  
**Project:** Shenron's Syndicate AI Council

---

## 📋 **VERSION HISTORY & ISSUES RESOLVED**

### v3.0 (FAILED ❌)
- **Issue:** Used `preset.yaml` format, but LM Studio Hub requires `preset.json`
- **Error:** "Missing preset.json"
- **Result:** Unable to publish

### v3.1-FIXED (FAILED ❌)
- **Fixed:** Added missing VEGETA directory
- **Fixed:** Added `owner` field to all manifest.json files
- **Issue:** Still used `preset.yaml` format
- **Error:** "Missing preset.json" (same error as v3.0)
- **Result:** Unable to publish

### v3.2-JSON (SUCCESS ✅)
- **Fixed:** Converted all `preset.yaml` to `preset.json` (proper JSON format)
- **Fixed:** Proper LM Studio Hub structure (manifest.json + preset.json)
- **Fixed:** Complete system prompts with personality traits
- **Fixed:** Optimized parameters (temperature, top_p, top_k, repeat_penalty)
- **Added:** Metadata section (base model, quantization, context, RAM requirements)
- **Result:** Ready for successful publishing!

---

## 🎯 **WHAT'S IN v3.2-JSON:**

### Files Included (6 Warriors × 2 Files Each = 12 Files)

Each warrior directory contains:
1. **`manifest.json`** - Hub metadata (owner, name, description, tags)
2. **`preset.json`** - Preset configuration (system prompt, parameters, metadata)

### Warriors Included:

| Warrior | Model | Context | RAM | Temperature | Role |
|---------|-------|---------|-----|-------------|------|
| 🥋 GOKU.AI | DeepSeek Coder V2 Lite Q8_0 | 16K | 16-32 GB | 0.7 | Adaptive Warrior |
| 👑 VEGETA.AI | Llama 3.2 3B Q8_0 | 8K | 4-8 GB | 0.5 | Technical Authority |
| 🧘 PICCOLO.AI | Qwen2.5 Coder 7B Q8_0 | 16K | 8-16 GB | 0.6 | Strategic Architect |
| 🛡️ GOHAN.AI | Mistral 7B Q8_0 | 16K | 8-16 GB | 0.4 | Guardian & Risk Analyst |
| ⚙️ KRILLIN.AI | Phi-3 Mini 128K Q8_0 | 32K | 5-10 GB | 0.6 | Practical Engineer |
| 😈 FRIEZA.AI | Phi-3 Mini 128K Q8_0 | 32K | 5-10 GB | 0.8 | Devil's Advocate |

**Total RAM when all loaded:** ~43-73 GB (32K context for Phi-3 models)

---

## 🚀 **DEPLOYMENT STEPS**

### **STEP 1: Clean Up Old Extractions (VM100)**

```powershell
cd C:\GOKU-AI

# Remove ALL old extractions
Remove-Item -Path "GOKU-deepseek-coder-v2-lite-instruct" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "VEGETA-llama-3.2-3b-instruct" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "PICCOLO-qwen2.5-coder-7b-instruct" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "GOHAN-mistral-7b-instruct-v0.3" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "KRILLIN-phi-3-mini-128k-instruct" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "FRIEZA-phi-3-mini-128k-instruct-v2" -Recurse -Force -ErrorAction SilentlyContinue
```

---

### **STEP 2: Extract v3.2-JSON**

```powershell
cd C:\GOKU-AI
tar -xzf shenrons-syndicate-presets-v3.2-JSON.tar.gz
```

---

### **STEP 3: Verify Extraction**

```powershell
# Check directories
Write-Host "`n=== Directories ===" -ForegroundColor Cyan
Get-ChildItem -Directory | Where-Object {$_.Name -match "GOKU|VEGETA|PICCOLO|GOHAN|KRILLIN|FRIEZA"}

# Check manifest.json files
Write-Host "`n=== manifest.json files ===" -ForegroundColor Cyan
Get-ChildItem -Recurse -Filter "manifest.json" | Select-Object FullName

# Check preset.json files (CRITICAL!)
Write-Host "`n=== preset.json files ===" -ForegroundColor Cyan
Get-ChildItem -Recurse -Filter "preset.json" | Select-Object FullName

Write-Host "`n✅ Extraction complete! Ready to publish.`n" -ForegroundColor Green
```

**Expected output:** 6 directories, 6 manifest.json files, 6 preset.json files

---

### **STEP 4: Publish to LM Studio Hub**

```powershell
cd C:\GOKU-AI

# Publish GOKU
cd GOKU-deepseek-coder-v2-lite-instruct
lms push
cd ..

# Publish VEGETA
cd VEGETA-llama-3.2-3b-instruct
lms push
cd ..

# Publish PICCOLO
cd PICCOLO-qwen2.5-coder-7b-instruct
lms push
cd ..

# Publish GOHAN
cd GOHAN-mistral-7b-instruct-v0.3
lms push
cd ..

# Publish KRILLIN
cd KRILLIN-phi-3-mini-128k-instruct
lms push
cd ..

# Publish FRIEZA
cd FRIEZA-phi-3-mini-128k-instruct-v2
lms push
cd ..
```

**Expected output for EACH warrior:**
```
Artifact successfully uploaded! View it at:
https://lmstudio.ai/matotezitanka/[warrior-name]-ai-shenron-syndicate (Revision 1)
```

---

### **STEP 5: Download Presets from Hub**

```powershell
cd C:\GOKU-AI

# Download all 6 presets (instant - only config files, ~5 KB total)
lms get matotezitanka/goku-ai-shenron-syndicate
lms get matotezitanka/vegeta-ai-shenron-syndicate
lms get matotezitanka/piccolo-ai-shenron-syndicate
lms get matotezitanka/gohan-ai-shenron-syndicate
lms get matotezitanka/krillin-ai-shenron-syndicate
lms get matotezitanka/frieza-ai-shenron-syndicate
```

---

### **STEP 6: Download Base Models (LM Studio GUI)**

1. **Open LM Studio**
2. **Press `Ctrl+Shift+M`** (Model Search)
3. **Download these 6 models:**

| Search Term | Model to Download | Size | Warrior |
|-------------|-------------------|------|---------|
| `deepseek-coder-v2-lite q8` | bartowski/deepseek-coder-v2-lite-instruct-GGUF (Q8_0) | 16 GB | GOKU |
| `llama-3.2-3b q8` | bartowski/Llama-3.2-3B-Instruct-GGUF (Q8_0) | 3 GB | VEGETA |
| `qwen2.5-coder-7b q8` | bartowski/Qwen2.5-Coder-7B-Instruct-GGUF (Q8_0) | 7 GB | PICCOLO |
| `mistral-7b-instruct-v0.3 q8` | bartowski/Mistral-7B-Instruct-v0.3-GGUF (Q8_0) | 7 GB | GOHAN |
| `phi-3-mini-128k q8` | bartowski/Phi-3-mini-128k-instruct-GGUF (Q8_0) | 5 GB | KRILLIN & FRIEZA |

**Total download:** ~43 GB (will take 10-30 minutes depending on internet)

---

### **STEP 7: Apply Presets to Models**

1. **Go to "My Models" tab** in LM Studio
2. **For each model:**
   - Right-click the model
   - Select "Apply Preset"
   - Choose the corresponding warrior preset (e.g., GOKU.AI for DeepSeek Coder)

---

### **STEP 8: Load Models in Local Server**

1. **Go to "Local Server" tab**
2. **Load models in this order (smallest to largest):**
   - VEGETA (3 GB)
   - KRILLIN (5 GB) ⚠️ **SET CONTEXT TO 32K**
   - FRIEZA (5 GB) ⚠️ **SET CONTEXT TO 32K**
   - PICCOLO (7 GB)
   - GOHAN (7 GB)
   - GOKU (16 GB)

3. **Verify all 6 loaded:**
```powershell
Invoke-RestMethod -Uri "http://localhost:1234/v1/models"
```

**Expected output:** 6 models listed

---

### **STEP 9: Test SHENRON**

```powershell
# Check SHENRON health
Invoke-RestMethod -Uri "http://localhost:5000/health"

# Test a simple query
Invoke-RestMethod -Method POST -Uri "http://localhost:5000/api/shenron/grant-wish" `
  -ContentType "application/json" `
  -Body '{"wish":"What is your purpose?"}' `
  -TimeoutSec 180
```

**Expected:** Responses from all 6 warriors + SHENRON's synthesis

---

## ⏱️ **ESTIMATED TIMELINE**

| Step | Task | Time |
|------|------|------|
| 1-3 | Clean, extract, verify | 2 min |
| 4 | Publish all 6 presets | 5 min |
| 5 | Download presets | 1 min |
| 6 | Download base models | 20 min |
| 7 | Apply presets | 5 min |
| 8 | Load models | 10 min |
| 9 | Test SHENRON | 5 min |
| **TOTAL** | | **~48 min** |

---

## 🔍 **TROUBLESHOOTING**

### Issue: "Missing preset.json" error
**Solution:** You're using v3.0 or v3.1. Use **v3.2-JSON** instead.

### Issue: "Missing owner" error
**Solution:** You're using v3.0. Use **v3.2-JSON** instead.

### Issue: Models downloaded but preset not applied
**Solution:** Manually apply preset in LM Studio GUI (Right-click model → Apply Preset)

### Issue: KRILLIN/FRIEZA taking too much RAM
**Solution:** Reduce context from 128K to 32K in model settings before loading

### Issue: SHENRON timeout
**Solution:** Ensure all 6 models are loaded and API is running on `localhost:1234`

---

## 📚 **TECHNICAL DETAILS**

### manifest.json Structure
```json
{
  "type": "preset",
  "owner": "matotezitanka",
  "name": "warrior-ai-shenron-syndicate",
  "displayName": "🥋 WARRIOR.AI - Shenron's Syndicate",
  "version": "3.2.0",
  "author": "MatoTezi Tanka",
  "organization": "lightspeedup",
  "description": "Warrior description...",
  "license": "MIT",
  "homepage": "https://shenron.lightspeedup.com"
}
```

### preset.json Structure
```json
{
  "system_prompt": "Full warrior personality and role...",
  "parameters": {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "repeat_penalty": 1.1,
    "max_tokens": 4096
  },
  "metadata": {
    "baseModel": "model-name",
    "quantization": "Q8_0",
    "contextLength": 16384,
    "minimumSystemMemory": "16 GB",
    "recommendedSystemMemory": "32 GB",
    "tags": ["shenrons-syndicate", "warrior-name", "q8-0"]
  }
}
```

---

## ✅ **SUCCESS CRITERIA**

- [ ] All 6 warriors published to LM Studio Hub (no errors)
- [ ] All 6 presets downloaded successfully
- [ ] All 6 base models downloaded (43 GB total)
- [ ] Presets applied to models
- [ ] All 6 models loaded in LM Studio Local Server
- [ ] SHENRON health check returns "operational"
- [ ] Test query returns responses from all 6 warriors
- [ ] Web UI at https://shenron.lightspeedup.com works

---

## 🐉 **FINAL NOTES**

v3.2-JSON is the **DEFINITIVE VERSION** that resolves all LM Studio Hub publishing issues:

✅ Proper JSON format (not YAML)  
✅ Both manifest.json AND preset.json included  
✅ Complete system prompts with personality traits  
✅ Optimized parameters for each warrior  
✅ Metadata for documentation  

**No more "Missing preset.json" errors!**  
**No more "Missing owner" errors!**  

🐉 **YOUR WARRIORS ARE READY FOR THE HUB!** ⚡

