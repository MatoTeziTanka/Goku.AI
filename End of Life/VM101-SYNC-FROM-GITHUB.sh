#!/bin/bash
# Sync Dell-Server-Roadmap from GitHub (GitHub is source of truth)

set -e

cd ~/GitHub/Dell-Server-Roadmap

echo "🔄 Syncing Dell-Server-Roadmap from GitHub"
echo "=========================================="
echo ""

# 1. Create backup branch (just in case)
echo "📦 Creating backup branch..."
BACKUP_BRANCH="backup-before-sync-$(date +%Y%m%d_%H%M%S)"
git branch "$BACKUP_BRANCH"
echo "✅ Backup branch created: $BACKUP_BRANCH"
echo ""

# 2. Stash any uncommitted changes
echo "💾 Stashing uncommitted changes..."
if git stash push -m "backup-$(date +%Y%m%d_%H%M%S)" 2>/dev/null; then
    echo "✅ Changes stashed"
else
    echo "ℹ️  No uncommitted changes to stash"
fi
echo ""

# 3. Fetch latest from GitHub
echo "📥 Fetching latest from GitHub..."
git fetch origin
echo "✅ Fetched"
echo ""

# 4. Reset to GitHub's main branch
echo "🔄 Resetting to GitHub's main branch..."
CURRENT_BRANCH=$(git branch --show-current)
git reset --hard origin/main
echo "✅ Reset to origin/main"
echo ""

# 5. Clean up any untracked files (optional - be careful!)
echo "🧹 Cleaning untracked files..."
git clean -fd
echo "✅ Cleaned"
echo ""

echo "=========================================="
echo "✅ Sync complete!"
echo ""
echo "📋 Summary:"
echo "   - Backup branch: $BACKUP_BRANCH"
echo "   - Current branch: $CURRENT_BRANCH"
echo "   - Now synced with: origin/main"
echo ""
echo "💡 If you need stashed changes:"
echo "   git stash list"
echo "   git stash pop"
echo ""
echo "💡 If you need backup branch:"
echo "   git log $BACKUP_BRANCH --oneline"
echo ""




