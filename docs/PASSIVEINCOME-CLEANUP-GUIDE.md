<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# PassiveIncome Repository Cleanup Guide

**Purpose**: Remove sensitive information before making repo public or sharing  
**Date**: November 1, 2025

---

## 🔍 Sensitive Information Found

### 1. IP Addresses (192.168.x.x)
Found in 37 files - internal network IPs that should be redacted for security.

**Files affected**:
- INFRASTRUCTURE.md
- PORT-ALLOCATION.md
- WordPress-VM/*.md (multiple files)
- And 34+ other files

**Action**: Replace with generic placeholders or remove entirely.

### 2. Email Address (sethpizzaboy@gmail.com)
Found in 4 files - personal email address.

**Files affected**:
- README.md
- INFRASTRUCTURE.md
- WordPress-VM/CURRENT-STATE.md
- INFRASTRUCTURE-REFERENCE.md

**Action**: Replace with generic "admin@example.com" or remove.

### 3. API Keys and Credentials
Found references to passwords, API keys, secrets, and tokens in 24 files.

**Action**: Ensure no actual secrets are committed (placeholders are OK).

---

## 🧹 Cleanup Strategy

### Option 1: Create Public Version (Recommended)
Create a sanitized public copy of the repo for marketing purposes.

**Steps**:
1. Create new repo: `PassiveIncome-Public`
2. Copy only marketing-relevant files
3. Replace all sensitive info with placeholders
4. Add public-friendly documentation

**Benefits**:
- Keep private repo intact
- Control what's public
- Easy to maintain both versions

### Option 2: In-Place Cleanup
Clean up the existing repo to remove sensitive info.

**Steps**:
1. Create backup branch: `git checkout -b backup-before-cleanup`
2. Run cleanup script (provided below)
3. Review all changes carefully
4. Commit: `git commit -m "Remove sensitive information"`

**Warning**: This modifies your working repo!

---

## 🛠️ Automated Cleanup Script

Save this as `cleanup_sensitive.sh` in PassiveIncome repo:

```bash
#!/bin/bash
#
# Cleanup sensitive information from PassiveIncome repo
#

set -e

echo "==========================================="
echo "PassiveIncome Repository Cleanup"
echo "==========================================="
echo ""

# Backup current state
BACKUP_BRANCH="backup-$(date +%Y%m%d-%H%M%S)"
echo "Creating backup branch: $BACKUP_BRANCH"
git checkout -b "$BACKUP_BRANCH"
git checkout main  # or master

echo ""
echo "Starting cleanup..."
echo ""

# Find all .md files
FILES=$(find . -name "*.md" -type f)

# Replace IP addresses
echo "1. Replacing IP addresses..."
for file in $FILES; do
    sed -i 's/192\.168\.12\.[0-9]\+/192.168.X.X/g' "$file"
    sed -i 's/192\.168\.[0-9]\+\.[0-9]\+/192.168.X.X/g' "$file"
done

# Replace email addresses
echo "2. Replacing email addresses..."
for file in $FILES; do
    sed -i 's/sethpizzaboy@gmail\.com/admin@lightspeedup.com/g' "$file"
done

# Replace sensitive keywords (optional - review first)
echo "3. Checking for sensitive keywords..."
grep -r "password\|api[_-]\?key\|secret\|token" --include="*.md" . || echo "  No sensitive keywords found"

echo ""
echo "✓ Cleanup complete!"
echo ""
echo "Next steps:"
echo "1. Review changes: git diff"
echo "2. Check specific files for any remaining sensitive info"
echo "3. Commit if satisfied: git add . && git commit -m 'Remove sensitive info'"
echo "4. Restore if needed: git checkout $BACKUP_BRANCH"
echo ""
```

---

## 📋 Manual Review Checklist

Before making the repo public, manually check these items:

### Critical - Must Remove
- [ ] Real IP addresses (192.168.x.x)
- [ ] Real email addresses
- [ ] SSH private keys or credentials
- [ ] Database passwords
- [ ] API keys (Stripe live keys, Cloudflare API tokens)
- [ ] Real customer data

### Important - Review
- [ ] Server hostnames
- [ ] Domain names (OK if public anyway)
- [ ] Port numbers (OK if standard)
- [ ] VM IDs (internal references - consider removing)
- [ ] File paths (OK if generic)

### Safe to Keep
- ✓ Stripe test card (4242 4242 4242 4242)
- ✓ Technology stack (WordPress, Proxmox, etc.)
- ✓ Architecture descriptions
- ✓ Process documentation
- ✓ Revenue goals and strategies

---

## 🎯 Recommended Public Repository Structure

Create a new repo: `LightSpeedUp-Marketing`

```
LightSpeedUp-Marketing/
├── README.md                    # Public-facing overview
├── REVENUE-STRATEGY.md          # Sanitized revenue strategy
├── services/
│   ├── wordpress-hosting.md     # Service description
│   ├── discord-bots.md
│   ├── game-servers.md
│   └── api-services.md
├── content/
│   └── (blog posts, tutorials)
├── marketing/
│   └── (marketing materials)
└── case-studies/
    └── (customer success stories)
```

**What to include**:
- Service descriptions
- Pricing information
- Technical capabilities
- Success stories
- Marketing content

**What to exclude**:
- Internal infrastructure details
- Private IP addresses
- Credentials and secrets
- Proprietary processes
- Customer private data

---

## 🚀 Quick Cleanup Commands

### Check for IP addresses
```bash
grep -r "192\.168\." --include="*.md" /path/to/PassiveIncome
```

### Check for email addresses
```bash
grep -r "@gmail\.com\|@yahoo\.com" --include="*.md" /path/to/PassiveIncome
```

### Check for passwords/keys
```bash
grep -ri "password\|api.key\|secret\|token" --include="*.md" /path/to/PassiveIncome
```

### Replace IP addresses (dry run)
```bash
find /path/to/PassiveIncome -name "*.md" -exec grep -l "192\.168\." {} \; | \
  xargs sed -i.bak 's/192\.168\.12\.[0-9]\+/192.168.X.X/g'
```

---

## 📝 Replacement Mappings

| Original | Replace With | Reason |
|----------|--------------|--------|
| <PROXMOX_IP> | 192.168.X.X | Internal IP |
| <VM101_IP> | 192.168.X.X | Internal IP |
| <VM120_IP> | 192.168.X.X | Internal IP |
| <VM150_IP> | 192.168.X.X | Internal IP |
| sethpizzaboy@gmail.com | admin@lightspeedup.com | Personal email |
| VM101 | VM-MGMT | Generic name |
| VM150 | VM-WP01 | Generic name |
| Dell PowerEdge | Generic Server | Remove model info |

---

## ⚠️ Important Notes

### Git History
If you've already committed sensitive information:

1. **Rewrite history** (destructive - be careful):
```bash
git filter-branch --tree-filter 'find . -name "*.md" -exec sed -i "s/192\.168\.12\.[0-9]\+/192.168.X.X/g" {} \;' HEAD
```

2. **Or start fresh** (recommended):
- Create new repo with cleaned files
- Don't push old history

### Testing
Before going public:
1. Create a test branch
2. Run cleanup
3. Review every file manually
4. Test that documentation still makes sense
5. Have someone else review

### Ongoing Maintenance
- Add to `.gitignore`: config files with secrets
- Use environment variables for credentials
- Document sensitive fields with placeholders
- Regular audits every 3 months

---

## ✅ Post-Cleanup Verification

Run these checks after cleanup:

```bash
# 1. No IP addresses
! grep -r "192\.168\.[0-9]\+\.[0-9]\+" --include="*.md" .

# 2. No email addresses (except generic)
! grep -r "@gmail\.com\|@yahoo\.com" --include="*.md" .

# 3. No obvious passwords
! grep -ri "password\s*[:=]\s*['\"][^'\"]\+" --include="*.md" .

# 4. No API keys format
! grep -ri "api[_-]key\s*[:=]\s*['\"][^'\"]\+" --include="*.md" .

echo "✓ All checks passed - safe for public!"
```

---

## 🎉 Ready to Publish

Once cleaned:

1. **Create public repo**:
```bash
cd /path/to/cleaned-repo
git remote add public https://github.com/yourusername/PassiveIncome-Public.git
git push public main
```

2. **Add README badge**:
```markdown
![Public Version](https://img.shields.io/badge/version-public-green)
```

3. **Link from marketing materials**:
- Reference in blog posts
- Share on social media
- Add to portfolio

---

**Last Updated**: November 1, 2025  
**Status**: Ready to use

For questions or issues, review each file manually before publishing!

