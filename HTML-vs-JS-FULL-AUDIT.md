<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🔍 SHENRON WEBSITE - HTML vs JavaScript AUDIT

**Date:** November 7, 2025  
**Audited:** index.html v4.1.5 vs script.js v4.1.3  
**VM150:** `/var/www/shenron.lightspeedup.com/`

---

## ❌ **CRITICAL BUGS FOUND**

### **Bug #1: Missing Element IDs**
| JavaScript Expects | HTML Has | Status |
|-------------------|----------|--------|
| `#wish-input` | ❌ Does NOT exist | MISSING |
| `#results-section` | ❌ Does NOT exist | MISSING |
| `#shenron-response-box` | ❌ Does NOT exist | MISSING |
| `#user-location` | ❌ Does NOT exist | MISSING |
| `#agent-mode-password` | ❌ Does NOT exist | MISSING |
| `#agent-log-section` | ❌ Does NOT exist | MISSING |
| `#agent-log` | ❌ Does NOT exist | MISSING |
| `#approve-btn` | ❌ Does NOT exist | MISSING |
| `#deny-btn` | ❌ Does NOT exist | MISSING |
| `#agentMode` | ❌ Does NOT exist | MISSING |

### **Bug #2: Element ID Mismatches**
| JavaScript Expects | HTML Actually Has |
|-------------------|-------------------|
| `#wish-input` | `#question` ✅ |
| `#results-section` | `.shenron-response-section` ❌ (it's a CLASS!) |
| `#shenron-response-box` | `#shenron-synthesis` ✅ |

### **Bug #3: Conflicting Element Selectors**
```javascript
// Line ~16: script.js tries BOTH IDs
const textarea = document.getElementById('wish-input') || document.getElementById('question');
// ✅ This works because of fallback to 'question'
```

```javascript
// Line ~226: script.js (showResults function)
document.getElementById('council-members').classList.add('hidden');
document.getElementById('results-section').classList.remove('hidden');
// ❌ 'results-section' does NOT exist as an ID!
// HTML has: <div class="shenron-response-section hidden">
```

```javascript
// Line ~231: script.js
document.getElementById('shenron-response-box').innerHTML = `...`
// ❌ 'shenron-response-box' does NOT exist!
// HTML has: <div id="shenron-synthesis">
```

### **Bug #4: Class vs ID Confusion**
```javascript
// Line ~366: script.js (resetUI function)
const resultsSection = document.getElementById('results-section');
// ❌ HTML has this as a CLASS, not an ID:
// <div class="shenron-response-section hidden">
```

---

## ✅ **ELEMENTS THAT EXIST (Correct)**

| ID | Purpose | Status |
|----|---------|--------|
| `#question` | User input textarea | ✅ OK |
| `#summon-btn` | Summon button | ✅ OK (class `.summon-btn`) |
| `#fast-mode-checkbox` | Fast mode toggle | ✅ OK |
| `#current-time` | Clock display | ✅ OK |
| `#api-status` | API status indicator | ✅ OK |
| `#progress-section` | Progress bar container | ✅ OK |
| `#progress-fill` | Progress bar fill | ✅ OK |
| `#progress-text` | Progress message | ✅ OK |
| `#council-members` | Warrior cards container | ✅ OK |
| `#shenron-synthesis` | Main response box | ✅ OK |
| `#warriors-responses` | Individual warrior responses | ✅ OK |
| `#expand-warriors-btn` | Expand/collapse button | ✅ OK |
| `#consensus-badge` | Consensus display | ✅ OK |
| `#status-goku` | GOKU status bar | ✅ OK |
| `#status-vegeta` | VEGETA status bar | ✅ OK |
| `#status-piccolo` | PICCOLO status bar | ✅ OK |
| `#status-gohan` | GOHAN status bar | ✅ OK |
| `#status-krillin` | KRILLIN status bar | ✅ OK (not in grep output but implied) |
| `#status-frieza` | FRIEZA status bar | ✅ OK |
| `#agentModeToggle` | Agent mode checkbox | ✅ OK |
| `#agentModeInfo` | Agent mode description | ✅ OK |
| `#agentModeStatus` | Agent mode status | ✅ OK |
| `#agentExecutionLog` | Agent command log | ✅ OK |
| `#logContent` | Log content area | ✅ OK |

---

## 🛠️ **REQUIRED FIXES**

### **Fix #1: Update script.js Line ~226 (showResults function)**
```javascript
// ❌ BROKEN CODE:
document.getElementById('council-members').classList.add('hidden');
document.getElementById('results-section').classList.remove('hidden');

// ✅ FIXED CODE:
document.getElementById('council-members').classList.add('hidden');
document.querySelector('.shenron-response-section').classList.remove('hidden');
```

### **Fix #2: Update script.js Line ~231 (showResults function)**
```javascript
// ❌ BROKEN CODE:
document.getElementById('shenron-response-box').innerHTML = `...`

// ✅ FIXED CODE:
document.getElementById('shenron-synthesis').innerHTML = `...`
```

### **Fix #3: Update script.js Line ~366 (resetUI function)**
```javascript
// ❌ BROKEN CODE:
const resultsSection = document.getElementById('results-section');
if (resultsSection) resultsSection.classList.add('hidden');

// ✅ FIXED CODE:
const resultsSection = document.querySelector('.shenron-response-section');
if (resultsSection) resultsSection.classList.add('hidden');
```

### **Fix #4: Add Missing Elements to HTML (IF NEEDED)**
**Question:** Does the website need these features?
- Agent Mode password input (`#agent-mode-password`)
- Agent log section (`#agent-log-section`, `#agent-log`)
- Approve/Deny buttons (`#approve-btn`, `#deny-btn`)
- User location display (`#user-location`)

**If YES:** Add to `index.html`  
**If NO:** Remove from `script.js`

---

## 📊 **PRIORITY MATRIX**

| Bug | Impact | Fix Complexity | Priority |
|-----|--------|---------------|----------|
| `#results-section` mismatch | 🔴 **CRITICAL** | Easy | **P0** |
| `#shenron-response-box` mismatch | 🔴 **CRITICAL** | Easy | **P0** |
| `#wish-input` fallback works | 🟡 Minor | Easy | P2 |
| Missing agent mode elements | 🟡 Minor | Medium | P3 |
| Missing location element | 🟢 Low | Easy | P4 |

---

## 🚀 **IMMEDIATE ACTION PLAN**

### **Step 1: Fix the 3 Critical Bugs** (5 minutes)
```bash
ssh wp1@<VM150_IP> 'cd /var/www/shenron.lightspeedup.com && cp script.js script.js.backup'
```

Then apply these 3 fixes to `script.js`:
1. Line ~226: `getElementById('results-section')` → `querySelector('.shenron-response-section')`
2. Line ~231: `getElementById('shenron-response-box')` → `getElementById('shenron-synthesis')`
3. Line ~366: `getElementById('results-section')` → `querySelector('.shenron-response-section')`

### **Step 2: Bump Version** (1 minute)
Update `index.html`:
```html
<script src="script.js?v=4.1.4"></script>
```

### **Step 3: Test** (2 minutes)
1. Clear browser cache
2. Visit https://shenron.lightspeedup.com
3. Click "Summon Shenron"
4. **Expected:** Animations play, dragon appears, results display

---

## 📝 **EXACT LINE NUMBERS TO FIX**

**File:** `/var/www/shenron.lightspeedup.com/script.js`

```bash
# Find exact line numbers
ssh wp1@<VM150_IP> "grep -n \"getElementById('results-section')\" /var/www/shenron.lightspeedup.com/script.js"
ssh wp1@<VM150_IP> "grep -n \"getElementById('shenron-response-box')\" /var/www/shenron.lightspeedup.com/script.js"
```

**Expected output:**
- Line ~226: Inside `showResults()` function
- Line ~231: Inside `showResults()` function
- Line ~366: Inside `resetUI()` function

---

## ✅ **POST-FIX VERIFICATION**

After applying fixes, verify:
```bash
# 1. Check syntax
ssh wp1@<VM150_IP> "node -c /var/www/shenron.lightspeedup.com/script.js"

# 2. Search for remaining issues
ssh wp1@<VM150_IP> "grep -E 'results-section|shenron-response-box|wish-input' /var/www/shenron.lightspeedup.com/script.js"

# 3. Verify version bump
ssh wp1@<VM150_IP> "grep 'script.js?v=' /var/www/shenron.lightspeedup.com/index.html"
```

---

## 🎯 **ROOT CAUSE ANALYSIS**

**Why did this happen?**
1. **Inconsistent naming conventions** between HTML and JS development
2. **No automated testing** to catch ID/class mismatches
3. **Manual edits** without cross-referencing both files
4. **Version drift** between HTML v4.1.5 and JS v4.1.3

**Prevention:**
1. Create a `CODING-STANDARDS.md` with element naming rules
2. Use a linter to catch missing element references
3. Implement automated E2E tests (Playwright/Cypress)
4. Keep HTML and JS version numbers in sync

---

**End of audit. Fixes ready to implement.** 🛠️
