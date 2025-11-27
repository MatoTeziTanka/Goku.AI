# 🎬 LM STUDIO - COMPLETE GUIDE & REFERENCE

**Last Updated:** November 7, 2025  
**Version:** LM Studio v0.3.20+  
**Purpose:** Comprehensive guide for all LM Studio features, best practices, and troubleshooting

---

## 📋 **TABLE OF CONTENTS**

1. [LM Studio Hub Integration](#lm-studio-hub-integration)
2. [Model Import Methods](#model-import-methods)
3. [Directory Structure](#directory-structure)
4. [Publishing & Sharing](#publishing--sharing)
5. [CLI Usage (lms)](#cli-usage-lms)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## 🌐 **LM STUDIO HUB INTEGRATION**

### **Account Information:**
- **Username:** @matotezitanka
- **Organization:** @lightspeedup
- **Profile:** https://lmstudio.ai/matotezitanka
- **Org Settings:** https://lmstudio.ai/lightspeedup/settings/general
- **Authentication:** Continue with GitHub (same credentials as GitHub account)
- **Joined:** November 2025

### **Hub Features:**
1. **Publish Presets:**
   - Create presets in chat sidebar
   - Right-click → "Publish..."
   - Follow on-screen instructions
   
2. **CLI Publishing:**
   - Navigate to project directory
   - Run: `lms push`
   
3. **Model Sharing:**
   - Publish models to LM Studio Hub
   - Share with organization or publicly
   
4. **Collaboration:**
   - Organization members can access shared resources
   - Version control for presets and configurations

### **Requirements:**
- LM Studio v0.3.20 or later
- Valid LM Studio Hub account
- GitHub authentication (recommended)

---

## 📥 **MODEL IMPORT METHODS**

LM Studio supports **4 primary methods** for importing models:

### **Method 1: Import from URL (Recommended for HuggingFace)**

**How it works:**
1. Copy HuggingFace model URL
2. Drag URL into LM Studio window
3. LM Studio downloads and imports automatically

**Example URLs:**
- `https://huggingface.co/microsoft/Phi-3-mini-128k-instruct-gguf`
- `https://huggingface.co/Qwen/Qwen2.5-Coder-7B-Instruct-GGUF`
- `https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.3-GGUF`

**Advantages:**
- ✅ Fastest method (no manual download)
- ✅ Automatic authentication handling
- ✅ Direct integration with HuggingFace
- ✅ Automatic directory structure creation

**Requirements:**
- LM Studio v0.3.20 or later
- Active internet connection

---

### **Method 2: In-App Downloader (Ctrl+Shift+M)**

**Steps:**
1. Press `Ctrl+Shift+M` (Windows) or `⌘+Shift+M` (Mac)
2. Search for model by name (e.g., "Phi-3-mini-128k")
3. Select quantization (e.g., Q8_0, Q4_K_M)
4. Click download
5. Model imports automatically

**Advantages:**
- ✅ Built-in search functionality
- ✅ Preview model details before download
- ✅ Automatic import after download
- ✅ No authentication setup required

---

### **Method 3: Drag-and-Drop Local Files**

**Steps:**
1. Download `.gguf` file manually
2. Open LM Studio
3. Drag `.gguf` file into LM Studio window
4. LM Studio imports automatically

**Advantages:**
- ✅ Works offline (after initial download)
- ✅ Good for custom/private models
- ✅ Simple and intuitive

**Note:** LM Studio will copy file to its own directory structure.

---

### **Method 4: CLI Import**

**Command:**
```bash
lms import <path/to/model.gguf>
```

**Example:**
```bash
lms import C:\AI-Models-Quantized\GOKU\DeepSeek-Coder-V2-Lite-Instruct-Q8_0.gguf
```

**Advantages:**
- ✅ Scriptable/automatable
- ✅ Batch import multiple models
- ✅ Interactive prompts for metadata

**Requirements:**
- `lms` CLI installed
- Model file in GGUF format

---

### **Method 5: CLI Download from HuggingFace**

**Command:**
```bash
lms get <publisher>/<model>@<quantization>
```

**Examples:**
```bash
# Download specific quantization
lms get qwen/qwen2.5-coder-32b-instruct-gguf@Q4_K_M

# Download latest version (auto-select quantization)
lms get microsoft/Phi-3-mini-128k-instruct-gguf
```

**Advantages:**
- ✅ Fastest download (optimized)
- ✅ Automatic import
- ✅ Version control (specify exact quant)

---

## 📂 **DIRECTORY STRUCTURE**

### **LM Studio Models Directory:**

**Location:**
- **Windows:** `C:\Users\<Username>\.lmstudio\models\`
- **Mac:** `~/.lmstudio/models/`
- **Linux:** `~/.lmstudio/models/`

**Structure:**
```
~/.lmstudio/models/
└── publisher/
    └── model-name/
        └── model-file.gguf
```

**Example:**
```
C:\Users\Administrator\.lmstudio\models\
├── deepseek-ai/
│   └── deepseek-coder-v2-lite-instruct/
│       └── DeepSeek-Coder-V2-Lite-Instruct-Q8_0.gguf
├── microsoft/
│   └── Phi-3-mini-128k-instruct-gguf/
│       └── phi-3-mini-128k-instruct-Q8_0.gguf
├── Qwen/
│   └── Qwen2.5-Coder-7B-Instruct-GGUF/
│       └── Qwen2.5-Coder-7B-Instruct-Q8_0.gguf
└── mistralai/
    └── Mistral-7B-Instruct-v0.3-GGUF/
        └── Mistral-7B-Instruct-v0.3-Q8_0.gguf
```

### **🚨 CRITICAL: Why This Matters**

**Manual downloads MUST follow this structure:**
- If you download a model to a custom location (e.g., `C:\AI-Models-Quantized\`)
- LM Studio will NOT see it unless you:
  1. Move it to `~/.lmstudio/models/publisher/model-name/`
  2. OR drag-and-drop into LM Studio (auto-copies)
  3. OR use `lms import` (auto-copies)

**Common Mistake:**
- ❌ Download to `C:\AI-Models\model.gguf`
- ❌ Try to import in LM Studio → Can't find file
- ✅ Use drag-and-drop or move to correct directory

---

## 🚀 **PUBLISHING & SHARING**

### **Publish Presets (GUI):**

**Steps:**
1. Create a preset in chat sidebar
2. Give it a descriptive name
3. Right-click preset
4. Select "Publish..."
5. Follow on-screen instructions:
   - Choose visibility (public/private/organization)
   - Add description
   - Set tags
   - Publish

**Use Cases:**
- Share prompt templates with team
- Publish reusable configurations
- Version control for presets

---

### **Publish via CLI:**

**Steps:**
1. Navigate to project directory
2. Ensure project has valid `lmstudio.json` config
3. Run:
   ```bash
   lms push
   ```
4. Follow prompts

**Example `lmstudio.json`:**
```json
{
  "name": "shenron-council-preset",
  "version": "1.0.0",
  "description": "SHENRON Syndicate AI Council Configuration",
  "preset": {
    "temperature": 0.7,
    "max_tokens": 2048,
    "system_prompt": "You are GOKU, the Adaptive Warrior..."
  }
}
```

---

## 💻 **CLI USAGE (lms)**

### **Installation:**

LM Studio CLI (`lms`) is included with LM Studio installation.

**Verify installation:**
```bash
lms --version
```

---

### **Common Commands:**

| Command | Description | Example |
|---------|-------------|---------|
| `lms get <repo>` | Download model from HuggingFace | `lms get qwen/qwen2.5-coder-7b-gguf` |
| `lms get <repo>@<quant>` | Download specific quantization | `lms get microsoft/Phi-3@Q8_0` |
| `lms import <path>` | Import local model | `lms import ./model.gguf` |
| `lms push` | Publish project to Hub | `lms push` |
| `lms list` | List installed models | `lms list` |
| `lms whoami` | Show current user | `lms whoami` |
| `lms login` | Authenticate to Hub | `lms login` |

---

### **Advanced Usage:**

**Batch Download:**
```bash
# Download multiple models
lms get qwen/qwen2.5-coder-7b-gguf@Q8_0
lms get microsoft/Phi-3-mini-128k-instruct-gguf@Q8_0
lms get mistralai/Mistral-7B-Instruct-v0.3-gguf@Q8_0
```

**Scripted Import:**
```powershell
# PowerShell script to import all models
Get-ChildItem C:\AI-Models-Quantized\*\*.gguf | ForEach-Object {
    lms import $_.FullName
}
```

---

## ✅ **BEST PRACTICES**

### **1. Use Import from URL for HuggingFace Models**
- Fastest method
- Automatic authentication
- No manual directory management

### **2. Always Use Quantized Models (Q8_0 or Q4_K_M)**
- **Q8_0:** 50% size reduction, 95-99% accuracy
- **Q4_K_M:** 75% size reduction, 90-95% accuracy
- **FP16:** Full size, 100% accuracy (only for GPUs)

### **3. Organize Models by Publisher**
- Follows LM Studio's expected structure
- Makes updates easier
- Simplifies version management

### **4. Set Context Length Appropriately**
- **128K context:** Requires ~10 GB RAM per model
- **32K context:** Requires ~4 GB RAM per model
- **8K context:** Requires ~2 GB RAM per model
- **Rule:** Use smallest context that meets your needs

### **5. Load Models Smallest to Largest**
- Prevents RAM exhaustion
- Easier to diagnose issues
- Safer for system stability

**Example Load Order:**
1. Llama-3.2-3B (3 GB)
2. Mistral-7B (7 GB)
3. Qwen2.5-Coder-7B (7 GB)
4. Phi-3-mini (5 GB)
5. DeepSeek-Coder-V2-Lite (15 GB)

### **6. Monitor RAM Usage**
```powershell
# Windows
Get-Process | Where-Object {$_.ProcessName -match "LM.*Studio"} | Select-Object @{Name="RAM_GB";Expression={[math]::Round($_.WorkingSet64/1GB,2)}}

# Linux/Mac
ps aux | grep "LM Studio" | awk '{print $6/1024/1024 " GB"}'
```

### **7. Regular Backups**
- Backup `~/.lmstudio/` directory
- Especially before major updates
- Include models and configurations

---

## 🔧 **TROUBLESHOOTING**

### **Issue 1: "Cannot import model" or "File not found"**

**Cause:** Model not in LM Studio's expected directory structure.

**Solution:**
1. Check file location: `C:\AI-Models-Quantized\...`
2. Move to: `C:\Users\<User>\.lmstudio\models\publisher\model-name\`
3. OR use drag-and-drop into LM Studio
4. OR use `lms import <path>`

---

### **Issue 2: "Model loads but crashes"**

**Cause:** Insufficient RAM or incorrect context length.

**Solution:**
1. Check RAM usage: `Get-Process | Where-Object {$_.ProcessName -match "LM.*Studio"}`
2. Reduce context length (128K → 32K)
3. Unload other models to free RAM
4. Use more quantized model (Q8_0 → Q4_K_M)

---

### **Issue 3: "401 Unauthorized" when downloading**

**Cause:** HuggingFace authentication required for private/gated models.

**Solution:**
1. Use LM Studio's in-app downloader (Ctrl+Shift+M)
   - Handles auth automatically
2. OR authenticate via CLI:
   ```bash
   huggingface-cli login
   # Enter token from: https://huggingface.co/settings/tokens
   ```
3. OR use "Import from URL" (drag URL into LM Studio)

---

### **Issue 4: "Model not showing in 'My Models'"**

**Cause:** LM Studio hasn't refreshed or model not in correct directory.

**Solution:**
1. Restart LM Studio completely
2. Check directory: `~/.lmstudio/models/publisher/model-name/`
3. Verify `.gguf` file exists and is complete
4. Re-import: drag-and-drop into LM Studio

---

### **Issue 5: "Slow download speeds"**

**Cause:** Default HuggingFace download method is slow.

**Solution:**
1. Install `hf_xet` for faster downloads:
   ```bash
   pip install hf_xet
   ```
2. Use LM Studio's in-app downloader (optimized)
3. Use `lms get` command (optimized)

---

### **Issue 6: "Model loads but responses are gibberish"**

**Cause:** Corrupted download or wrong model format.

**Solution:**
1. Verify file integrity (check file size matches expected)
2. Re-download model
3. Use `lms import` instead of manual copy
4. Check model is GGUF format (not safetensors or pytorch)

---

## 📊 **REFERENCE: MODEL SIZE vs RAM**

| Model Size | Quantization | Approx. RAM (32K context) | Approx. RAM (128K context) |
|------------|--------------|--------------------------|----------------------------|
| 3B params  | Q8_0         | ~3 GB                    | ~6 GB                      |
| 3B params  | Q4_K_M       | ~2 GB                    | ~4 GB                      |
| 7B params  | Q8_0         | ~7 GB                    | ~12 GB                     |
| 7B params  | Q4_K_M       | ~4 GB                    | ~8 GB                      |
| 16B params | Q8_0         | ~15 GB                   | ~25 GB                     |
| 16B params | Q4_K_M       | ~9 GB                    | ~15 GB                     |
| 72B params | Q8_0         | ~70 GB                   | ~120 GB                    |
| 72B params | Q4_K_M       | ~40 GB                   | ~70 GB                     |

**Formula:**
```
RAM (GB) ≈ (Model Params × Quant Bits / 8) × (1 + Context Length / 10000)
```

---

## 🔗 **USEFUL LINKS**

- **LM Studio Hub:** https://lmstudio.ai
- **LM Studio Docs:** https://lmstudio.ai/docs
- **LM Studio CLI Docs:** https://lmstudio.ai/docs/cli
- **HuggingFace Models:** https://huggingface.co/models?library=gguf
- **GGUF Format Spec:** https://github.com/ggerganov/ggml/blob/master/docs/gguf.md
- **LM Studio Discord:** https://discord.gg/lmstudio

---

## 📝 **CHANGELOG**

| Date | Version | Changes |
|------|---------|---------|
| 2025-11-07 | 1.0.0 | Initial guide created |
| 2025-11-07 | 1.0.0 | Added Import from URL method |
| 2025-11-07 | 1.0.0 | Documented directory structure |
| 2025-11-07 | 1.0.0 | Added LM Studio Hub integration |
| 2025-11-07 | 1.0.0 | Added troubleshooting section |

---

**Last Updated:** November 7, 2025, 03:15 AM  
**Maintained By:** MatoTeziTanka  
**For Project:** SHENRON Syndicate AI Council  

🎬 **MASTER LM STUDIO - UNLOCK THE POWER OF LOCAL AI!** 🐉

