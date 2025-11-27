#!/bin/bash
# Sync All GitHub Repositories to VM 101
# This script clones or updates all repositories needed on VM 101

set -e

echo "========================================="
echo "Sync All GitHub Repos to VM 101"
echo "========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# GitHub username
GITHUB_USER="sethpizzaboy"

# Base directory for repositories
REPO_BASE="$HOME/GitHub"
mkdir -p "$REPO_BASE"
cd "$REPO_BASE"

# List of repositories to sync
REPOS=(
    "sethpizzaboy/ScalpStorm"
    "sethpizzaboy/FamilyFork"
    "sethpizzaboy/Games-with-Logan"
    "sethpizzaboy/CursorAI"
    "MatoTeziTanka/Dell-Server-Roadmap"
    "sethpizzaboy/BackTrack"
    "sethpizzaboy/KeyHound"
    "sethpizzaboy/GSMG.IO"
    "sethpizzaboy/Flayer"
    "sethpizzaboy/StreamForge"
    "MatoTeziTanka/CryptoPuzzles"
)

echo -e "${BLUE}Repository Base: $REPO_BASE${NC}"
echo ""

# Function to clone or update a repository
sync_repo() {
    local repo_url="$1"
    local repo_name=$(basename "$repo_url" .git)
    local repo_path="$REPO_BASE/$repo_name"
    
    if [ -d "$repo_path" ]; then
        echo -e "${YELLOW}[UPDATE]${NC} Updating $repo_name..."
        cd "$repo_path"
        
        # Check if it's a git repository
        if [ -d .git ]; then
            # Fetch latest changes
            git fetch --all
            
            # Check current branch
            current_branch=$(git branch --show-current)
            
            # Try to pull, handle errors gracefully
            if git pull origin "$current_branch" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} $repo_name updated successfully"
            else
                echo -e "${YELLOW}⚠${NC} $repo_name: Could not pull (may have local changes or divergent branches)"
                echo -e "${YELLOW}   Current branch: $current_branch${NC}"
            fi
        else
            echo -e "${RED}✗${NC} $repo_name exists but is not a git repository"
        fi
        cd "$REPO_BASE"
    else
        echo -e "${BLUE}[CLONE]${NC} Cloning $repo_name..."
        
        # Determine URL format (SSH if key exists, HTTPS otherwise)
        if [ -f "$HOME/.ssh/id_ed25519" ] || [ -f "$HOME/.ssh/id_rsa" ]; then
            # Try SSH first
            if git clone "git@github.com:$repo_url.git" "$repo_path" 2>/dev/null; then
                echo -e "${GREEN}✓${NC} $repo_name cloned successfully (SSH)"
            else
                # Fallback to HTTPS
                echo -e "${YELLOW}   SSH failed, trying HTTPS...${NC}"
                if git clone "https://github.com/$repo_url.git" "$repo_path"; then
                    echo -e "${GREEN}✓${NC} $repo_name cloned successfully (HTTPS)"
                else
                    echo -e "${RED}✗${NC} Failed to clone $repo_name"
                fi
            fi
        else
            # Use HTTPS if no SSH key
            if git clone "https://github.com/$repo_url.git" "$repo_path"; then
                echo -e "${GREEN}✓${NC} $repo_name cloned successfully (HTTPS)"
            else
                echo -e "${RED}✗${NC} Failed to clone $repo_name"
            fi
        fi
    fi
}

# Sync all repositories
echo -e "${GREEN}Starting repository sync...${NC}"
echo ""

for repo in "${REPOS[@]}"; do
    sync_repo "$repo"
    echo ""
done

echo "========================================="
echo -e "${GREEN}Repository sync complete!${NC}"
echo "========================================="
echo ""
echo "Repositories location: $REPO_BASE"
echo ""
echo "To check repository status:"
echo "  cd $REPO_BASE"
echo "  ls -la"
echo ""

