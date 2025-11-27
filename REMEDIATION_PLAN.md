# Goku.AI Repository Remediation Plan

**Goal:** Transform messy legacy codebase into v2.9.0 Enterprise Standard

**Strategy:** Strangler Fig Pattern - Build perfect structure next to mess, migrate good stuff, delete rest

---

## 🛑 Phase 1: The "Musk Algorithm" (Delete & Sort)

**Ref:** Master Prompt Section 1.3

### Step 1: Safety Backup
```bash
# Create backup of entire repo
xcopy "C:\Users\sethp\Documents\Github\Goku.AI" "C:\Backups\GokuAI_Legacy_Snapshot" /E /I /H
```

### Step 2: The "Sorting Hat" Method
```bash
cd C:\Users\sethp\Documents\Github\Goku.AI
python phase1_sorting_hat.py
```

This will:
- Create `_TRASH_BIN/` folder
- Move EVERYTHING into it (except .git, .gitignore)
- Leave you with a clean slate

### Step 3: Smart Recovery (Automated)
```bash
python phase2_smart_recovery.py
```

This will:
- Automatically scan `_TRASH_BIN/` for Goku.AI files
- Use forensic analysis (filename + content scanning)
- Categorize recovered files by type
- Place them in `_RECOVERED_GOKU/` staging area

**No manual sorting needed!** The script finds the relevant files automatically.

### Step 4: Review Recovered Files
1. Open `_RECOVERED_GOKU/` folder
2. Review the categorized files:
   - `src_candidates/` → Will go to `src/`
   - `docs_candidates/` → Will go to `docs/`
   - `config_candidates/` → Will go to `config/`
   - `scripts_candidates/` → Will go to `scripts/`
3. Delete anything in `_RECOVERED_GOKU` that's not actually relevant

---

## 🏗️ Phase 3: Structural Alignment

**Ref:** Master Prompt Section 18.10 (Visual Tree)

```bash
cd C:\Users\sethp\Documents\Github\Goku.AI
python align_goku_structure.py
```

**Note:** Run this AFTER Smart Recovery so you know what files to organize.

This creates:
- Perfect v2.9.0 directory structure
- Required config files (.gitignore, README.md, etc.)
- Installation scripts (install.bat, install.sh)
- IDE configuration (.vscode/, .editorconfig)

---

## 🧹 Phase 4: The Migration

Now organize the files from `_RECOVERED_GOKU/`:

### Move Recovered Files
From `_RECOVERED_GOKU/`:

- **src_candidates/** → Move to `src/` subdirectories:
  - Core AI logic → `src/services/`
  - API endpoints → `src/api/`
  - Utilities → `src/utils/`

- **docs_candidates/** → Move to `docs/`:
  - General docs → `docs/`
  - Architecture docs → `docs/architecture/`

- **config_candidates/** → Move to `config/`

- **scripts_candidates/** → Move to `scripts/`:
  - Windows scripts → `scripts/windows/`
  - Linux scripts → `scripts/linux/`
  - General scripts → `scripts/`

### Sanitize Root
Delete any files in root that are NOT in the v2.9.0 Visual Tree:
- ✅ Keep: README.md, LICENSE, CHANGELOG.md, CONTRIBUTING.md, .gitignore
- ❌ Delete: Everything else not in the standard structure

---

## 📝 Phase 5: Git Hygiene

**Ref:** Master Prompt Section 18.0 (Conventional Commits)

### Clean Up
```bash
# Delete the staging folders (they're no longer needed)
rmdir /s /q _TRASH_BIN
rmdir /s /q _RECOVERED_GOKU
```

### Verify Changes
```bash
git status
```

### Commit
```bash
git add .
git commit -m "chore(structure): align repository with v2.9.0 engineering standards"
```

### Push
```bash
git push origin main
```

---

## ✅ Success Criteria

After completion, your repo should have:

- ✅ Perfect v2.9.0 directory structure
- ✅ All code in `src/` subdirectories
- ✅ All docs in `docs/`
- ✅ Clean root directory (only standard files)
- ✅ Installation scripts per OS
- ✅ IDE configuration files
- ✅ Proper .gitignore
- ✅ README.md with required sections

---

## 🚨 Important Notes

1. **Backup First:** Always create the safety backup before Phase 1
2. **Review Carefully:** Don't delete files you might need
3. **Test After Migration:** Ensure code still works after moving
4. **Commit Often:** Make commits after each phase

---

**Ready to begin? Start with Phase 1!**

