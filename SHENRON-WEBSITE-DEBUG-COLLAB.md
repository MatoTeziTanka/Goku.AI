<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 SHENRON WEBSITE DEBUG - AI COLLABORATION REQUEST

**Date:** November 7, 2025  
**Priority:** CRITICAL  
**Status:** Going in circles - need fresh perspective

---

## 🚨 THE ACTUAL PROBLEM

**User clicks "Summon Shenron" on https://shenron.lightspeedup.com and NOTHING HAPPENS.**

- ❌ No animations play
- ❌ No dragon appears
- ❌ No responses displayed
- ❌ UI doesn't update

**BUT:** The backend API on VM100 (`http://<VM100_IP>:5000`) works perfectly when tested directly via PowerShell.

---

## 🏗️ ARCHITECTURE

```
[Web Browser (HTTPS)]
         ↓
[VM150 - Ubuntu + Apache]
   • https://shenron.lightspeedup.com
   • /var/www/shenron.lightspeedup.com/
   • Files: index.html, script.js, style.css, api.php
         ↓
[api.php - PHP Proxy]
   • Forwards requests to VM100
   • Handles HTTPS → HTTP conversion
         ↓
[VM100 - Windows Server]
   • SHENRON API: http://<VM100_IP>:5000
   • LM Studio API: http://<VM100_IP>:1234
   • Python Flask backend
```

---

## 🔍 WHAT WE'VE VERIFIED

### ✅ Backend is WORKING
```powershell
# Health check: SUCCESS
Invoke-RestMethod -Uri "http://localhost:5000/health"
# Output: {"dragon_awakened":true,"service":"SHENRON v4.0","status":"operational"}

# Full query test: SUCCESS (156 seconds, all 6 AI models responded)
$body = @{ query = "What is your purpose?" } | ConvertTo-Json
Invoke-RestMethod -Method POST -Uri "http://localhost:5000/api/shenron/grant-wish" -Body $body
# Output: Full synthesized response with all 6 warriors
```

### ❌ Frontend is BROKEN
```javascript
// Browser console shows these errors:
1. "TypeError: Cannot read properties of null (reading 'classList')"
   - At resetUI() line 400
   - At summonShenron() line 109

2. "POST https://shenron.lightspeedup.com/api.php 400 (Bad Request)"

3. API response: {"error":"Missing query field in request","wish_granted":false}
```

---

## 📂 CRITICAL FILES

### 1. `/var/www/shenron.lightspeedup.com/index.html`
**Current version tag:** `v4.1.3`

**Key elements that JavaScript expects:**
- `#summon-form` - The main form
- `#wish-input` - User query textarea
- `#summon-button` - Submit button
- `#council-members` - Initial warrior display section
- `#results-section` - Results container (⚠️ **MAY BE WRONG ID**)
- `#shenron-response-box` - Main response display (⚠️ **MAY BE WRONG ID**)
- `.individual-responses` - Warrior response cards (⚠️ **MAY BE WRONG CLASS**)

### 2. `/var/www/shenron.lightspeedup.com/script.js`
**Current version tag:** `v4.1.3`

**Problems identified:**
```javascript
// Line 109 - summonShenron()
resetUI(); // ← CRASHES because elements don't exist

// Line 226 - showResults()
const resultsSection = document.getElementById('results-section'); // ← NULL?
resultsSection.classList.remove('hidden'); // ← CRASH

// Line 400 - resetUI()
document.getElementById('individual-responses').classList.add('hidden'); // ← NULL?
```

### 3. `/var/www/shenron.lightspeedup.com/api.php`
**Current behavior:**
- Receives POST from `script.js`
- Expected: `{ query: "...", fast_mode: true/false }`
- Actual error: "Missing query field in request"
- Debug data shows: `received_keys: ["action"]` instead of `["query"]`

**⚠️ MISMATCH:** JavaScript sends one format, PHP expects another!

---

## 🧪 RECENT FIXES ATTEMPTED

1. ✅ **Fixed `script.js` line 524:** Changed `question: query` → `query: query`
2. ✅ **Added null checks in `resetUI()`**
3. ✅ **Fixed Fast Mode HTTPS mixed content issue** (routes through `/api.php`)
4. ✅ **Updated version tags** to force cache refresh (`v4.1.3`)
5. ❌ **STILL BROKEN** - Same errors persist

---

## 🔧 WHAT I NEED FROM YOU

### **Option A: Full HTML/JS Audit**
Compare `index.html` element IDs against `script.js` expectations line-by-line. Create a discrepancy table:

| JavaScript Expects | HTML Actually Has | Status | Fix Required |
|-------------------|-------------------|--------|--------------|
| `#results-section` | `#shenron-response-section`? | ❌ Mismatch | Update JS or HTML |
| `#individual-responses` | `.warriors-responses`? | ❌ Wrong selector | Fix selector type |

### **Option B: API Contract Analysis**
Trace the exact request flow:
1. What does `script.js` send in the POST body?
2. What does `api.php` actually receive?
3. What does `api.php` forward to the SHENRON API?
4. What does SHENRON API expect vs. receive?

### **Option C: Start from Scratch**
Is this a case where we should just rebuild the frontend HTML/JS with known-working IDs?

---

## 📊 CURRENT FILE VERSIONS (VM150)

```bash
# Last modified times
index.html    → v4.1.3 (cache busting)
script.js     → v4.1.3 (cache busting)
style.css     → v4.1.3 (cache busting)
api.php       → Last edited during Fast Mode implementation
```

---

## 🎯 SUCCESS CRITERIA

**When fixed, this should happen:**

1. User types "What is your purpose?" in the textarea
2. User clicks "Summon Shenron"
3. **Animations play** (dragon summoning sequence)
4. **Council members fade out**
5. **Loading indicators appear**
6. **6 warrior responses stream in** (if Fast Mode)
   OR **Single synthesized response appears** (if SHENRON Mode)
7. **Results section becomes visible**

**Currently:** Step 2 → **CRASH** with `TypeError` and no visible changes.

---

## 🔥 WHY WE'RE GOING IN CIRCLES

1. We fixed the **backend API** (it works via PowerShell)
2. We fixed the **model IDs** (SHENRON queries all 6 warriors successfully)
3. We fixed the **parameter names** (`query` vs `wish`)
4. We fixed the **HTTPS mixed content** issue
5. We added **null checks** to prevent crashes

**BUT:** The website UI **still doesn't work at all**.

**Hypothesis:** There's a fundamental mismatch between what the HTML provides and what the JavaScript expects. The IDs/classes don't align, so `document.getElementById()` returns `null`, causing cascading failures.

---

## 📝 QUESTIONS FOR COLLABORATOR

1. **Should we SSH into VM150 and read the ACTUAL `index.html` to see its real structure?**
2. **Should we enable verbose debug logging in `api.php` to see the exact POST body?**
3. **Should we use browser DevTools to inspect the live DOM and compare to `script.js`?**
4. **Should we rebuild the frontend from a known-good template?**
5. **Is there a version control issue?** (Old HTML, new JS, cache problems?)

---

## 🚀 RECOMMENDED NEXT STEPS

**Phase 1: Diagnose the ID/Class Mismatch (15 minutes)**
- SSH into VM150
- Read `/var/www/shenron.lightspeedup.com/index.html`
- Extract ALL element IDs and classes
- Compare against `script.js` expectations
- Generate discrepancy report

**Phase 2: Fix the API Contract (10 minutes)**
- Add debug logging to `api.php`:
  ```php
  error_log("Received POST: " . print_r($_POST, true));
  error_log("Received RAW: " . file_get_contents('php://input'));
  ```
- Check Apache logs on VM150
- Verify what `script.js` actually sends vs. what `api.php` receives

**Phase 3: Implement Fixes (20 minutes)**
- Update `script.js` with correct element IDs
- Update `index.html` with correct IDs if needed
- Update `api.php` to parse the correct request format
- Bump version to `v4.1.4`
- Test live

**Phase 4: Verify End-to-End (10 minutes)**
- Clear browser cache completely
- Test SHENRON Mode (full orchestration)
- Test Fast Mode (direct warrior calls)
- Verify animations play
- Verify responses display

---

## 📌 TECHNICAL CONTEXT

- **VM100 (Windows Server):** Backend works perfectly
- **VM150 (Ubuntu + Apache):** Frontend broken
- **Cloudflare:** Adds caching + HTTPS layer (potential timeout issues for long responses)
- **LM Studio:** RAM usage high (72GB) but functional
- **SHENRON API v4.0:** Operational, tested via PowerShell
- **Web UI v4.1.3:** Broken, needs diagnosis

---

## 💬 COLLABORATOR INSTRUCTIONS

**Read this document fully, then provide:**

1. ✅ **Confirmation you understand the problem**
2. 🔍 **Which diagnosis phase to start with (A, B, or C)**
3. 📋 **Step-by-step commands to run**
4. 🎯 **Expected output at each step**
5. 🛠️ **Specific fixes to implement**

**Goal:** Get the website working so clicking "Summon Shenron" actually does something visible.

---

**End of collaboration request. Awaiting fresh perspective.** 🙏

