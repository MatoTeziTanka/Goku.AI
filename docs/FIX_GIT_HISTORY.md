# Fix Git History - Remove Secrets from Commit

## Problem
Commit `990814e` contains secrets and is blocking the push to GitHub.

## Solution: Reset and Recommit

### Step 1: Reset to commit before secrets (keeps all sanitized files)
```bash
cd C:\Users\sethp\Documents\Github\Goku.AI
git reset --soft 2c393fd
```

This will:
- Move HEAD back to commit `2c393fd` (before secrets)
- Keep ALL your sanitized files staged and ready to commit
- NOT lose any work

### Step 2: Verify files are staged
```bash
git status
```

You should see all your sanitized files listed as "Changes to be committed".

### Step 3: Create new clean commit
```bash
git commit -m "feat(repo): initial commit - Goku.AI framework v2.9.0 (sanitized)"
```

### Step 4: Verify the new history
```bash
git log --oneline -5
```

You should see:
- Your new clean commit (no `990814e`)
- Commit `2c393fd` as the base

### Step 5: Verify no secrets in new commit
```bash
git show HEAD | grep -i "sk_\|ghp_\|api_key" | head -10
```

This should return nothing (or only show placeholders like `<API_KEY>`).

### Step 6: Force push to GitHub
```bash
git push -u origin main --force
```

⚠️ **WARNING**: Force push will overwrite remote history. This is necessary to remove the secrets.

## Alternative: If Step 1 doesn't work

If `git reset --soft 2c393fd` doesn't work, try:

```bash
# Hard reset (WARNING: Make sure files are already sanitized!)
git reset --hard 2c393fd

# Re-add all files
git add .

# Commit
git commit -m "feat(repo): initial commit - Goku.AI framework v2.9.0 (sanitized)"

# Force push
git push -u origin main --force
```

## After Pushing

1. **Rotate all exposed secrets immediately:**
   - Groq API Key
   - OpenAI API Key
   - GitHub Personal Access Token
   - Azure AI Services Key
   - Stripe Test API Secret Key

2. **Verify push succeeded:**
   - Check GitHub repository
   - Verify no secrets are visible in file contents

3. **Update credentials.json:**
   - Ensure all real secrets are in `credentials.json` (gitignored)
   - Never commit real secrets again

