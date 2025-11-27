# 🔄 VM101 GitHub Repository Sync Guide

**Issue:** VM101 has repos but they're not synced with GitHub (GitHub is more up to date)  
**Solution:** Sync all repositories to match GitHub

---

## 🔍 Step 1: Check Current Repository Status

**On VM101, check what repos you have and their status:**

```bash
# List all repos
cd ~/GitHub
ls -la

# Check status of each repo
for repo in */; do
    echo "=== $repo ==="
    cd "$repo"
    if [ -d .git ]; then
        echo "Branch: $(git branch --show-current)"
        echo "Status: $(git status --short | head -5)"
        echo "Behind: $(git rev-list --count HEAD..origin/$(git branch --show-current) 2>/dev/null || echo 'unknown')"
        echo "Ahead: $(git rev-list --count origin/$(git branch --show-current)..HEAD 2>/dev/null || echo 'unknown')"
    else
        echo "Not a git repository"
    fi
    cd ..
    echo ""
done
```

**Or check a specific repo:**
```bash
cd ~/GitHub/Dell-Server-Roadmap
git status
git fetch
git log HEAD..origin/main --oneline  # Shows commits on GitHub not in local
```

---

## 🔄 Step 2: Sync All Repositories

### **Option 1: Use Existing Sync Script**

**The sync script is in Dell-Server-Roadmap:**

```bash
# Run the sync script
cd ~/GitHub/Dell-Server-Roadmap/scripts
chmod +x sync-all-repos-to-vm101.sh
./sync-all-repos-to-vm101.sh
```

**This script will:**
- Update existing repos (git pull)
- Clone missing repos
- Handle SSH/HTTPS authentication

### **Option 2: Manual Sync (More Control)**

**Sync each repo individually:**

```bash
cd ~/GitHub

# For each repo, update it
for repo in */; do
    echo "Syncing $repo..."
    cd "$repo"
    if [ -d .git ]; then
        git fetch --all
        current_branch=$(git branch --show-current)
        git pull origin "$current_branch"
    fi
    cd ..
done
```

### **Option 3: Improved Sync Script (Handles All Repos)**

**Create an improved sync script that handles all repos:**

```bash
cat > ~/sync-all-repos.sh << 'EOF'
#!/bin/bash
# Sync All GitHub Repositories on VM101

set -e

REPO_BASE="$HOME/GitHub"
cd "$REPO_BASE"

echo "🔄 Syncing all repositories..."
echo ""

# Get all directories
for repo_dir in */; do
    repo_name="${repo_dir%/}"
    echo "=== $repo_name ==="
    
    cd "$repo_dir"
    
    if [ -d .git ]; then
        # Get current branch
        current_branch=$(git branch --show-current 2>/dev/null || echo "main")
        
        # Fetch latest
        echo "  Fetching from GitHub..."
        git fetch --all --prune
        
        # Check if behind
        behind=$(git rev-list --count HEAD..origin/$current_branch 2>/dev/null || echo "0")
        ahead=$(git rev-list --count origin/$current_branch..HEAD 2>/dev/null || echo "0")
        
        if [ "$behind" -gt 0 ]; then
            echo "  ⚠️  Behind by $behind commits"
            echo "  Pulling latest changes..."
            git pull origin "$current_branch"
            echo "  ✅ Updated"
        elif [ "$ahead" -gt 0 ]; then
            echo "  ⚠️  Ahead by $ahead commits (local changes)"
            echo "  ⚠️  Skipping (has local commits)"
        else
            echo "  ✅ Up to date"
        fi
    else
        echo "  ⚠️  Not a git repository"
    fi
    
    cd ..
    echo ""
done

echo "✅ Sync complete!"
EOF

chmod +x ~/sync-all-repos.sh
./sync-all-repos.sh
```

---

## 🔍 Step 3: Check for Missing Repos

**Compare what's on VM101 vs what should be there:**

```bash
# List repos on VM101
cd ~/GitHub
ls -1 > /tmp/vm101_repos.txt

# Expected repos (from sync script)
cat > /tmp/expected_repos.txt << 'EOF'
ScalpStorm
FamilyFork
Games-with-Logan
CursorAI
Dell-Server-Roadmap
BackTrack
KeyHound
GSMG.IO
Flayer
StreamForge
CryptoPuzzles
BackTrack
CryptoPuzzles
CursorAI
Dino-Cloud
Family-Care-Ideas
FamilyFork
Flayer
GSMG.IO
Games-with-Logan
InfraScan-Systems-Inc
KeyHound
PassiveIncome
ScalpStorm
ScalpStorm_V2
SethFlix-Plex
StreamForge
project-repo-template
unknown
EOF

# Compare
echo "Missing repos:"
comm -23 <(sort /tmp/expected_repos.txt) <(sort /tmp/vm101_repos.txt)
```

---

## 🛠️ Step 4: Handle Divergent Branches

**If a repo has local changes that conflict with GitHub:**

```bash
cd ~/GitHub/REPO_NAME

# Check status
git status

# Option 1: Stash local changes and pull
git stash
git pull origin main
git stash pop  # Reapply local changes

# Option 2: Create backup branch and reset
git branch backup-$(date +%Y%m%d)
git fetch origin
git reset --hard origin/main

# Option 3: Merge (if you want to keep both)
git pull origin main --no-rebase
```

---

## 📋 Complete Sync Script

**Create this comprehensive sync script:**

```bash
cat > ~/sync-github-repos.sh << 'SCRIPT_EOF'
#!/bin/bash
# Comprehensive GitHub Repository Sync for VM101

set -e

REPO_BASE="$HOME/GitHub"
cd "$REPO_BASE"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "🔄 GitHub Repository Sync"
echo "=========================="
echo ""

# Function to sync a repo
sync_repo() {
    local repo_dir="$1"
    local repo_name="${repo_dir%/}"
    
    echo -e "${BLUE}=== $repo_name ===${NC}"
    
    if [ ! -d "$repo_dir" ]; then
        echo -e "${RED}  ✗ Directory not found${NC}"
        return
    fi
    
    cd "$repo_dir"
    
    if [ ! -d .git ]; then
        echo -e "${YELLOW}  ⚠️  Not a git repository${NC}"
        cd ..
        return
    fi
    
    # Get current branch
    current_branch=$(git branch --show-current 2>/dev/null || echo "main")
    echo -e "  Branch: ${BLUE}$current_branch${NC}"
    
    # Fetch latest
    echo -e "  Fetching from GitHub..."
    if ! git fetch --all --prune 2>/dev/null; then
        echo -e "${RED}  ✗ Fetch failed (check network/auth)${NC}"
        cd ..
        return
    fi
    
    # Check status
    behind=$(git rev-list --count HEAD..origin/$current_branch 2>/dev/null || echo "0")
    ahead=$(git rev-list --count origin/$current_branch..HEAD 2>/dev/null || echo "0")
    uncommitted=$(git status --porcelain | wc -l)
    
    if [ "$uncommitted" -gt 0 ]; then
        echo -e "${YELLOW}  ⚠️  Has uncommitted changes ($uncommitted files)${NC}"
    fi
    
    if [ "$behind" -gt 0 ]; then
        echo -e "${YELLOW}  ⚠️  Behind by $behind commits${NC}"
        echo -e "  Pulling latest changes..."
        if git pull origin "$current_branch" 2>/dev/null; then
            echo -e "${GREEN}  ✅ Updated successfully${NC}"
        else
            echo -e "${RED}  ✗ Pull failed (may have conflicts)${NC}"
            echo -e "${YELLOW}  Run manually: cd $repo_dir && git pull${NC}"
        fi
    elif [ "$ahead" -gt 0 ]; then
        echo -e "${YELLOW}  ⚠️  Ahead by $ahead commits (local commits not on GitHub)${NC}"
    else
        echo -e "${GREEN}  ✅ Up to date${NC}"
    fi
    
    cd ..
    echo ""
}

# Sync all repos
for repo_dir in */; do
    sync_repo "$repo_dir"
done

echo "=========================="
echo -e "${GREEN}✅ Sync complete!${NC}"
echo ""
echo "To check individual repo status:"
echo "  cd ~/GitHub/REPO_NAME"
echo "  git status"
SCRIPT_EOF

chmod +x ~/sync-github-repos.sh
./sync-github-repos.sh
```

---

## 🔐 Step 5: Verify GitHub Authentication

**Check if you can authenticate with GitHub:**

```bash
# Test SSH connection
ssh -T git@github.com

# Test HTTPS (will prompt for credentials)
git ls-remote https://github.com/sethpizzaboy/ScalpStorm.git
```

**If SSH fails, you may need to:**
1. Add SSH key to GitHub
2. Or use HTTPS with personal access token

---

## 📊 Step 6: Generate Sync Report

**Create a report of all repo statuses:**

```bash
cat > ~/repo-status-report.sh << 'EOF'
#!/bin/bash
# Generate repository status report

REPO_BASE="$HOME/GitHub"
cd "$REPO_BASE"

echo "📊 Repository Status Report"
echo "============================"
echo "Generated: $(date)"
echo ""

for repo_dir in */; do
    repo_name="${repo_dir%/}"
    cd "$repo_dir"
    
    if [ -d .git ]; then
        branch=$(git branch --show-current 2>/dev/null || echo "unknown")
        git fetch --all --prune 2>/dev/null
        behind=$(git rev-list --count HEAD..origin/$branch 2>/dev/null || echo "0")
        ahead=$(git rev-list --count origin/$branch..HEAD 2>/dev/null || echo "0")
        uncommitted=$(git status --porcelain | wc -l)
        
        status="✅"
        if [ "$behind" -gt 0 ]; then
            status="⚠️  BEHIND"
        elif [ "$ahead" -gt 0 ]; then
            status="⚠️  AHEAD"
        elif [ "$uncommitted" -gt 0 ]; then
            status="⚠️  UNCOMMITTED"
        fi
        
        echo "$status | $repo_name | Branch: $branch | Behind: $behind | Ahead: $ahead | Uncommitted: $uncommitted"
    else
        echo "❌ | $repo_name | Not a git repository"
    fi
    
    cd ..
done

echo ""
echo "============================"
EOF

chmod +x ~/repo-status-report.sh
./repo-status-report.sh
```

---

## 🚀 Quick Sync Command

**One-liner to sync all repos:**

```bash
cd ~/GitHub && for repo in */; do (cd "$repo" && [ -d .git ] && git fetch --all && git pull origin $(git branch --show-current)) || true; done
```

---

## 📋 Summary

**To sync all repos with GitHub:**

1. **Check status:** Run `~/repo-status-report.sh` (create it first)
2. **Sync all:** Run `~/sync-github-repos.sh` (create it first)
3. **Or use existing:** Run `~/GitHub/Dell-Server-Roadmap/scripts/sync-all-repos-to-vm101.sh`

**The sync will:**
- ✅ Fetch latest from GitHub
- ✅ Pull changes for repos that are behind
- ✅ Skip repos with local uncommitted changes
- ✅ Show status for each repo

**After syncing, all repos should match GitHub!** 🔄




