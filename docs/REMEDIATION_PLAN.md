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

### Step 3: Manual Review
1. Open `_TRASH_BIN/`
2. **Drag back** only files 100% relevant to Goku.AI:
   - Core AI agent code
   - Configuration files
   - Essential documentation
3. **Delete** everything else (or archive off-repo)

---

## 🏗️ Phase 2: Structural Alignment

**Ref:** Master Prompt Section 18.10 (Visual Tree)

```bash
cd C:\Users\sethp\Documents\Github\Goku.AI
python align_goku_structure.py
```

This creates:
- Perfect v2.9.0 directory structure
- Required config files (.gitignore, README.md, etc.)
- Installation scripts (install.bat, install.sh)
- IDE configuration (.vscode/, .editorconfig)

---

## 🧹 Phase 3: The Migration

Now organize the files you moved back:

### Move Code
- **Core AI logic** → `src/services/`
- **API endpoints** → `src/api/`
- **Utilities** → `src/utils/`
- **Scripts** → `scripts/` (or `scripts/windows/`, `scripts/linux/`)

### Move Documentation
- **All .md files** → `docs/`
- **Architecture docs** → `docs/architecture/`

### Sanitize Root
Delete any files in root that are NOT in the v2.9.0 Visual Tree:
- ✅ Keep: README.md, LICENSE, CHANGELOG.md, CONTRIBUTING.md, .gitignore
- ❌ Delete: Everything else not in the standard structure

---

## 📝 Phase 4: Git Hygiene

**Ref:** Master Prompt Section 18.0 (Conventional Commits)

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

