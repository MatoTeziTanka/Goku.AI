#!/bin/bash
# Quick analysis of massive git diff - exclude node_modules

cd ~/GitHub/Dell-Server-Roadmap

echo "📊 Quick Git Diff Analysis (Excluding node_modules)"
echo "====================================================="
echo ""

echo "=== Actual Code Files Changed ==="
code_files=$(git diff origin/main..HEAD --name-only | grep -v node_modules | grep -v '\.map$' | grep -E '\.(py|js|ts|tsx|sh|md|yaml|yml|json)$' | wc -l)
echo "Code files: $code_files"
echo ""

echo "=== Sample Code Files ==="
git diff origin/main..HEAD --name-only | grep -v node_modules | grep -v '\.map$' | grep -E '\.(py|js|ts|tsx|sh|md|yaml|yml|json)$' | head -20
echo ""

echo "=== Local Commits (Code Only) ==="
git log origin/main..HEAD --oneline -- ':!frontend/node_modules' ':!**/node_modules' ':!shenron-env' | head -10
echo ""

echo "=== Changes by Directory (Excluding node_modules) ==="
git diff origin/main..HEAD --name-only | grep -v node_modules | grep -v '\.map$' | cut -d'/' -f1 | sort | uniq -c | sort -rn | head -10
echo ""

echo "=== Recommendation ==="
if [ "$code_files" -lt 50 ]; then
    echo "✅ Only $code_files code files changed"
    echo "✅ Safe to sync from GitHub - most changes are node_modules/build artifacts"
    echo ""
    echo "💡 Recommended:"
    echo "   git fetch origin"
    echo "   git reset --hard origin/main"
else
    echo "⚠️  $code_files code files changed - review before syncing"
    echo ""
    echo "💡 Review changes:"
    echo "   git log origin/main..HEAD --oneline -- ':!frontend/node_modules'"
fi




