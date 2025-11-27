# Sensitive Files Removal Action Plan

**Generated:** 2025-11-27  
**Purpose:** Safe removal of sensitive files before making repos public

---

## 🚨 Critical Files (MUST Remove)

### BitPhoenix
- `Marketing-Automation/social-media-automation/credentials/api_credentials.json` - **CRITICAL**
- `backend/src/secrets_manager.py` - **CRITICAL** (may contain secrets)
- `deployment/k8s/secrets.yaml` - **CRITICAL**

### FamilyFork
- `backend/.env` - **CRITICAL** (actual environment file with secrets)
- `frontend/.env` - **CRITICAL** (actual environment file with secrets)

### PassiveIncome
- `WordPress-VM/Setup-Guides/STRIPE-API-KEYS-LIVE.txt` - **CRITICAL** (live API keys!)

### ScalpStorm
- `V1_EOL/docker.env` - **CRITICAL** (environment file)

### Dell-Server-Roadmap
- `SHENRON-2FA-SECRET.md` - **CRITICAL**
- `docs/vm-access-credentials.md` - **CRITICAL**
- `BINANCE-API-KEYS-SECURE-SETUP.md` - **CRITICAL**

---

## ⚠️ Warning Files (Review Needed)

### BitPhoenix
- `backend/src/recovery_engine.py.backup` - Backup file, may contain secrets

### Dell-Server-Roadmap
- `Marketing-Automation/get-linkedin-token.py` - May contain tokens
- `Marketing-Automation/config/content_config.json` - Review for secrets
- `Marketing-Automation/config/marketing_config.json` - Review for secrets

---

## ✅ False Positives (Safe to Keep)

These files are safe and can remain:
- `.env.example` - Example file, no actual secrets
- `.vscode/extensions.json` - IDE config, safe
- `.vscode/launch.json` - Debug config, usually safe
- `tsconfig.json`, `jsconfig.json` - Config files, safe
- `node_modules/` - Should be in .gitignore but not sensitive
- `__pycache__/` - Should be in .gitignore but not sensitive

---

## 🔧 Removal Commands

### For Each Repository:

```bash
# Navigate to repository
cd C:/Users/sethp/Documents/Github/<REPO_NAME>

# Remove file from git (keeps file on disk)
git rm --cached <FILE_PATH>

# Add to .gitignore (if not already there)
echo "<FILE_PATTERN>" >> .gitignore

# Commit the removal
git commit -m "Remove sensitive files before making public"
```

### Example for FamilyFork:

```bash
cd C:/Users/sethp/Documents/Github/FamilyFork
git rm --cached backend/.env
git rm --cached frontend/.env
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
git commit -m "Remove .env files before making public"
```

---

## 🧹 Cleaning Git History (If Files Were Already Committed)

If sensitive files were already committed and pushed, you need to clean history:

### Option 1: git-filter-repo (Recommended)

```bash
# Install git-filter-repo first
pip install git-filter-repo

# Remove file from entire history
cd <REPO>
git filter-repo --path <FILE_PATH> --invert-paths

# Force push (WARNING: This rewrites history)
git push origin --force --all
```

### Option 2: BFG Repo-Cleaner

```bash
# Download BFG
# https://rtyley.github.io/bfg-repo-cleaner/

# Remove file
java -jar bfg.jar --delete-files <FILE_NAME> <REPO_PATH>

# Clean up
cd <REPO>
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

---

## ✅ Verification Checklist

Before making repos public:

- [ ] All `.env` files removed from git
- [ ] All `credentials.json` files removed
- [ ] All API key files removed
- [ ] All secret files removed
- [ ] `.gitignore` updated with proper patterns
- [ ] Changes committed
- [ ] Git history cleaned (if files were in history)
- [ ] Tested that sensitive files are not accessible
- [ ] Verified `.gitignore` is working

---

## 📋 Repository-by-Repository Actions

### BitPhoenix
```bash
cd BitPhoenix
git rm --cached Marketing-Automation/social-media-automation/credentials/api_credentials.json
git rm --cached backend/src/secrets_manager.py
git rm --cached deployment/k8s/secrets.yaml
git rm --cached backend/src/recovery_engine.py.backup
echo "**/api_credentials.json" >> .gitignore
echo "**/secrets.yaml" >> .gitignore
echo "*.backup" >> .gitignore
git commit -m "Remove sensitive files"
```

### FamilyFork
```bash
cd FamilyFork
git rm --cached backend/.env
git rm --cached frontend/.env
echo ".env" >> .gitignore
echo ".env.local" >> .gitignore
git commit -m "Remove .env files"
```

### PassiveIncome
```bash
cd PassiveIncome
git rm --cached WordPress-VM/Setup-Guides/STRIPE-API-KEYS-LIVE.txt
git rm --cached WordPress-VM/Marketing-Content/Credentials/CREDENTIALS-REGISTRY.md
echo "**/*API*KEY*.txt" >> .gitignore
echo "**/CREDENTIALS*.md" >> .gitignore
git commit -m "Remove API keys and credentials"
```

### ScalpStorm
```bash
cd ScalpStorm
git rm --cached V1_EOL/docker.env
git rm --cached V1_EOL/API_CREDENTIAL_SECURITY_ANALYSIS.md
echo "*.env" >> .gitignore
git commit -m "Remove sensitive files"
```

### Dell-Server-Roadmap
```bash
cd Dell-Server-Roadmap
git rm --cached SHENRON-2FA-SECRET.md
git rm --cached docs/vm-access-credentials.md
git rm --cached BINANCE-API-KEYS-SECURE-SETUP.md
git rm --cached Marketing-Automation/get-linkedin-token.py
echo "**/*SECRET*.md" >> .gitignore
echo "**/*CREDENTIAL*.md" >> .gitignore
echo "**/*API*KEY*.md" >> .gitignore
git commit -m "Remove sensitive documentation"
```

---

## 🛡️ Security Best Practices

1. **Never commit:**
   - `.env` files
   - API keys
   - Passwords
   - Private keys
   - Certificates
   - Database credentials

2. **Always use:**
   - `.env.example` (with placeholder values)
   - Environment variables
   - Secret management services
   - `.gitignore` for sensitive patterns

3. **Before making public:**
   - Run security audit
   - Review all tracked files
   - Clean git history if needed
   - Test that secrets are not accessible

---

**Generated:** 2025-11-27  
**Next Steps:** Run `remove_sensitive_files_safely.py` or follow manual commands above

