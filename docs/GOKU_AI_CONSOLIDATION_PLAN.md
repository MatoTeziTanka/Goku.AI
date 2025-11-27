<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# Goku.AI File Consolidation Plan

**Date:** 2025-11-27  
**Purpose:** Move all Goku.AI, Shenron, VM100/VM101 related files to `Goku.AI` repository

---

## 📋 What Will Be Moved

### Search Criteria
Files matching any of these keywords will be moved:
- Goku.AI, Goku, GOKU
- Shenron, SHENRON
- DragonBall Z, Dragon Ball
- VM100, VM101
- IPs: <VM100_IP>, <VM101_IP>
- LM Studio, LM-Studio
- Personalities
- Control node

### Files Found (Initial Search)
Based on grep results, files are located in:
- `Dell-Server-Roadmap/` - Multiple documentation files
- `ScalpStorm/` - Shenron reporter
- Root directory - Various scripts

---

## 🔧 How to Run

### Step 1: Find Files (Preview)
```python
python find_goku_files.py
```
This will:
- List all matching files
- Show keywords matched
- Save list to `GOKU_FILES_LIST.json`
- **Does NOT move anything**

### Step 2: Move Files
```python
python consolidate_goku_ai_files.py
```
This will:
- Find all matching files
- Show preview
- Ask for confirmation
- Move files to `Goku.AI` repository
- Organize by source repository
- Create consolidation log

---

## 📁 Target Structure

Files will be organized in `Goku.AI` by source repository:

```
Goku.AI/
├── Dell-Server-Roadmap/
│   ├── docs/
│   │   ├── server-infrastructure-documentation.md
│   │   ├── chat-history-transfer.md
│   │   └── vm-101-setup-guide.md
│   ├── SHENRON-v4-DEPLOYMENT-COMPLETE.md
│   ├── ETERNAL-DRAGON-SHENRON-KNOWLEDGE.md
│   └── ...
├── ScalpStorm/
│   └── ai_integration/
│       └── shenron_reporter.py
└── root/
    └── (files from root directory)
```

---

## ⚠️ Important Notes

1. **Git History:** Files moved from git repositories will lose their git history
2. **Backup:** Consider backing up before moving
3. **Review:** Review the file list before moving
4. **Organization:** Files are organized by source to maintain context

---

## ✅ After Consolidation

1. Review files in `Goku.AI` repository
2. Organize into logical structure
3. Update documentation
4. Commit to git
5. Remove from source repositories (if desired)

---

**Ready to run:** Execute `python find_goku_files.py` first to preview, then `python consolidate_goku_ai_files.py` to move.

