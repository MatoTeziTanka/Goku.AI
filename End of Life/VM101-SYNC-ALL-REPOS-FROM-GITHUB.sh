#!/bin/bash
# Sync ALL GitHub Repositories on VM101 from GitHub
# GitHub is the source of truth - sync all repos

set -e

REPO_BASE="$HOME/GitHub"
cd "$REPO_BASE"

echo "🔄 Syncing ALL Repositories from GitHub"
echo "========================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

# Function to sync a single repo
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
    
    # Check status
    ahead=$(git rev-list --count origin/$current_branch..HEAD 2>/dev/null || echo "0")
    behind=$(git rev-list --count HEAD..origin/$current_branch 2>/dev/null || echo "0")
    uncommitted=$(git status --porcelain | wc -l)
    
    # Create backup if there are local changes
    if [ "$ahead" -gt 0 ] || [ "$uncommitted" -gt 0 ]; then
        echo -e "  📦 Creating backup..."
        git branch "backup-$(date +%Y%m%d)" 2>/dev/null || true
        
        if [ "$uncommitted" -gt 0 ]; then
            git stash push -m "backup-$(date +%Y%m%d)" 2>/dev/null || true
        fi
    fi
    
    # Fetch latest
    echo -e "  📥 Fetching from GitHub..."
    if ! git fetch origin 2>/dev/null; then
        echo -e "${RED}  ✗ Fetch failed (check network/auth)${NC}"
        cd ..
        return
    fi
    
    # Sync
    if [ "$behind" -gt 0 ]; then
        echo -e "  🔄 Syncing (behind by $behind commits)..."
        if git reset --hard origin/$current_branch 2>/dev/null; then
            echo -e "${GREEN}  ✅ Synced${NC}"
        else
            echo -e "${RED}  ✗ Sync failed${NC}"
        fi
    elif [ "$ahead" -gt 0 ]; then
        echo -e "${YELLOW}  ⚠️  Ahead by $ahead commits (local changes)${NC}"
        echo -e "${YELLOW}  💡 Review backup branch if needed${NC}"
    else
        echo -e "${GREEN}  ✅ Already up to date${NC}"
    fi
    
    # Clean untracked files
    git clean -fd 2>/dev/null || true
    
    cd ..
    echo ""
}

# Sync all repos
echo -e "${GREEN}Starting sync of all repositories...${NC}"
echo ""

for repo_dir in */; do
    sync_repo "$repo_dir"
done

echo "========================================"
echo -e "${GREEN}✅ All repositories synced!${NC}"
echo ""
echo "📋 Summary:"
echo "  - Repositories location: $REPO_BASE"
echo "  - Backup branches created: backup-$(date +%Y%m%d)"
echo ""
echo "💡 To check backup branches:"
echo "  git branch | grep backup"
echo ""
echo "💡 To restore from backup:"
echo "  git checkout backup-YYYYMMDD"
echo ""




