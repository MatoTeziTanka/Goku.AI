<!--
NOTE: This file has been sanitized for public GitHub.
Real values are stored in credentials.json (gitignored).
For local use, restore from credentials.json or use the original file.
-->
# 🐉 Shenron Syndicate: Complete GitHub & Local Filing System Restructure

**AI Collaboration Document**  
**Created:** November 4, 2025  
**Purpose:** Ground-up restructure of all GitHub repositories and local file organization  
**Scope:** Consolidate 14 repositories → 2 monorepos (Private + Public)  
**Status:** 🟡 Planning Phase (Thought Exercise)

---

## 📋 **EXECUTIVE SUMMARY**

### **Current State:**
- **14 repositories** across 2 GitHub accounts (MatoTeziTanka + sethpizzaboy)
- Inconsistent naming conventions (hyphens, underscores, capitalization)
- Duplicated content across repos
- Unclear project boundaries
- Sensitive data scattered
- No single source of truth
- Outdated documentation

### **Desired State:**
- **2 monorepos:** `Shenron-Syndicate-Private` + `Shenron-Syndicate` (public)
- Hierarchical structure with governance at the top
- All projects organized by type/class
- Automated public/private synchronization
- Deduplicated content
- Current, cross-linked documentation
- GitHub Wiki as public knowledge base
- Zero sensitive data exposure

### **Goals:**
1. ✅ Single source of truth for all projects
2. ✅ Clear governance hierarchy (GOVERNANCE/ folder rules all)
3. ✅ Secure separation (private vs public)
4. ✅ Automated deduplication & migration
5. ✅ Comprehensive validation (no data loss)
6. ✅ Current metadata (READMEs, descriptions, tags)
7. ✅ Death document compliance (family can find everything)

---

## 🏗️ **NEW STRUCTURE: DETAILED DESIGN**

### **Repository 1: `MatoTeziTanka/Shenron-Syndicate-Private` (PRIVATE)**

```
Shenron-Syndicate-Private/
│
├── 📋 GOVERNANCE/                          # 🔒 MASTER RULING DOCUMENTS (NEVER SYNC TO PUBLIC)
│   ├── README.md                           # Governance overview & philosophy
│   ├── DEATH-DOCUMENT.md                   # 🚨 CRITICAL: Access instructions for family/successors
│   ├── NETWORK-INFRASTRUCTURE.md           # IPs (192.168.12.x), ports, VLANs, firewall rules
│   ├── HARDWARE-INVENTORY.md               # Dell R730, HDDs, SSDs, NICs, warranties, serials
│   ├── STORAGE-ZFS.md                      # ZFS pools, datasets, quotas, snapshots
│   ├── VM-SPECIFICATIONS.md                # All VMs (specs, IPs, users, purposes)
│   ├── SSH-KEYS-BACKUP.md                  # SSH key inventory, passphrases, recovery
│   ├── SECURITY-PROTOCOLS.md               # Password policies, 2FA, encryption standards
│   ├── API-KEYS-SECRETS.md                 # Stripe, GitHub tokens, service credentials
│   ├── NAMING-CONVENTIONS.md               # File/folder/VM/project naming standards
│   ├── BACKUP-DISASTER-RECOVERY.md         # Backup schedules, restoration procedures
│   ├── DEVELOPMENT-STANDARDS.md            # Code style, git workflow, CI/CD, testing
│   ├── CONTACT-EMERGENCY.md                # Key contacts, escalation paths, emergency procedures
│   └── CHANGE-LOG.md                       # Governance document version history
│
├── 🚀 PROJECTS/                            # ALL ACTIVE PROJECTS (CATEGORIZED)
│   │
│   ├── 💰 PASSIVE-INCOME/                  # 💵 REVENUE-GENERATING PROJECTS
│   │   ├── README.md                       # Passive income strategy, revenue targets, analytics
│   │   ├── infrastructure/                 # WordPress VM150, Stripe integration, DNS
│   │   │   ├── wordpress-vm-setup.md
│   │   │   ├── stripe-configuration.md
│   │   │   ├── dns-cloudflare.md
│   │   │   └── ssl-certificates.md
│   │   ├── pricing-tiers/                  # LightSpeed, VectorEdge, NovaScale
│   │   │   ├── tier-definitions.md
│   │   │   ├── stripe-products.json
│   │   │   └── pricing-calculator.xlsx
│   │   ├── pterodactyl-game-hosting/       # Game server hosting business
│   │   │   ├── README.md
│   │   │   ├── server-templates/
│   │   │   ├── customer-onboarding.md
│   │   │   └── billing-automation.md
│   │   ├── discord-bot-monetization/       # Discord bot revenue streams
│   │   │   ├── README.md
│   │   │   ├── bot-features.md
│   │   │   ├── premium-tiers.md
│   │   │   └── deployment/
│   │   ├── marketing/                      # Marketing materials, landing pages, SEO
│   │   │   ├── landing-pages/
│   │   │   ├── seo-keywords.md
│   │   │   └── social-media-content/
│   │   └── analytics/                      # Revenue tracking, customer metrics, growth
│   │       ├── revenue-dashboard.md
│   │       ├── customer-lifetime-value.xlsx
│   │       └── conversion-rates.md
│   │
│   ├── 🎮 ACTIVE-INCOME/                   # 🏢 FREELANCE/CONTRACT WORK
│   │   ├── README.md                       # Active income tracking, hourly rates, capacity
│   │   ├── fiverr/                         # Fiverr gigs & projects
│   │   │   ├── gigs/
│   │   │   ├── reviews.md
│   │   │   └── earnings-tracker.xlsx
│   │   ├── freelancer/                     # Freelancer.com projects
│   │   │   ├── proposals/
│   │   │   ├── active-contracts/
│   │   │   └── earnings-tracker.xlsx
│   │   ├── contracts/                      # 🔒 Client contracts (encrypted)
│   │   │   ├── template-contract.docx
│   │   │   └── signed-contracts/ (encrypted)
│   │   ├── invoices/                       # Billing & payment records
│   │   │   ├── invoice-template.xlsx
│   │   │   └── sent-invoices/
│   │   └── time-tracking/                  # Time logs, project hours
│   │       ├── time-tracking-tool.md
│   │       └── monthly-summaries/
│   │
│   ├── 🧩 CRYPTO-PUZZLES/                  # 🎲 PUZZLE/GAME/CRYPTO PROJECTS
│   │   ├── README.md                       # Crypto puzzle ecosystem overview, roadmap
│   │   ├── gsmg-io/                        # GSMG.IO project (formerly GSMG)
│   │   │   ├── README.md
│   │   │   ├── frontend/
│   │   │   ├── backend/
│   │   │   ├── smart-contracts/
│   │   │   └── documentation/
│   │   ├── keyhound/                       # KeyHound project (password manager/game)
│   │   │   ├── README.md
│   │   │   ├── app/
│   │   │   ├── database-schema.md
│   │   │   └── deployment/
│   │   ├── scalpstorm/                     # ScalpStorm project (trading bot/game)
│   │   │   ├── README.md
│   │   │   ├── trading-algorithms/
│   │   │   ├── backtesting/
│   │   │   └── deployment/
│   │   ├── ai-cloakcoin/                   # AI-CloakCoin (needs better name)
│   │   │   ├── README.md
│   │   │   ├── tokenomics.md
│   │   │   ├── smart-contracts/
│   │   │   └── whitepaper.md
│   │   ├── shared-components/              # Shared code/assets across puzzle projects
│   │   │   ├── crypto-libraries/
│   │   │   ├── ui-components/
│   │   │   └── game-engines/
│   │   └── puzzle-analytics/               # Player metrics, engagement, monetization
│   │       ├── player-stats.md
│   │       └── leaderboards.md
│   │
│   ├── 🎬 MEDIA-ENTERTAINMENT/             # 📺 MEDIA & STREAMING PROJECTS
│   │   ├── README.md                       # Media projects overview, content strategy
│   │   ├── sethflix-plex/                  # Plex server & SethFlix branding (formerly SethFlix-Plex)
│   │   │   ├── README.md
│   │   │   ├── plex-server-setup.md
│   │   │   ├── content-organization.md
│   │   │   ├── branding/
│   │   │   │   ├── logos/
│   │   │   │   ├── themes/
│   │   │   │   └── style-guide.md
│   │   │   └── scripts/
│   │   │       ├── media-organizer.sh
│   │   │       └── metadata-fetcher.py
│   │   ├── streamforge/                    # Streaming tools & automation (StreamForge)
│   │   │   ├── README.md
│   │   │   ├── stream-automation/
│   │   │   ├── encoding-profiles/
│   │   │   └── obs-configs/
│   │   ├── content-library/                # Media metadata & organization
│   │   │   ├── movies/
│   │   │   ├── tv-shows/
│   │   │   ├── music/
│   │   │   └── metadata-standards.md
│   │   └── media-analytics/                # Viewing stats, popular content
│   │       ├── tautulli-config.md
│   │       └── viewing-reports/
│   │
│   ├── 👨‍👩‍👧‍👦 FAMILY-PROJECTS/                # 👪 FAMILY-RELATED PROJECTS
│   │   ├── README.md                       # Family projects overview, goals
│   │   ├── family-care-ideas/              # Care & activity ideas (formerly Family-Care-Ideas)
│   │   │   ├── README.md
│   │   │   ├── activities/
│   │   │   ├── recipes/
│   │   │   ├── care-routines/
│   │   │   └── resources/
│   │   ├── familyfork/                     # Family app/website (formerly FamilyFork)
│   │   │   ├── README.md
│   │   │   ├── frontend/
│   │   │   ├── backend/
│   │   │   ├── database/
│   │   │   └── deployment/
│   │   ├── games-with-logan/               # Logan's game projects (formerly Games-with-Logan)
│   │   │   ├── README.md
│   │   │   ├── minecraft/
│   │   │   ├── roblox/
│   │   │   ├── game-ideas/
│   │   │   └── tutorials/
│   │   ├── photos-memories/                # Family photos, timelines, memories
│   │   │   ├── photo-organization.md
│   │   │   ├── albums/
│   │   │   ├── timeline.md
│   │   │   └── backup-strategy.md
│   │   └── family-calendar/                # Shared calendar, events, reminders
│   │       ├── calendar-app.md
│   │       └── recurring-events.md
│   │
│   ├── 🔍 PERSONAL-TOOLS/                  # 🛠️ PERSONAL PRODUCTIVITY & TOOLS
│   │   ├── README.md                       # Personal tools overview
│   │   ├── backtrack/                      # BackTrack project (time tracking?)
│   │   │   ├── README.md
│   │   │   ├── app/
│   │   │   └── documentation/
│   │   ├── dashden-city/                   # DashDenCity project (dashboard app?)
│   │   │   ├── README.md
│   │   │   ├── widgets/
│   │   │   ├── data-sources/
│   │   │   └── deployment/
│   │   ├── cursorai-configs/               # CursorAI settings, prompts, workflows (if relevant)
│   │   │   ├── README.md
│   │   │   ├── .cursorrules
│   │   │   ├── custom-prompts/
│   │   │   └── ai-workflows/
│   │   ├── automation-scripts/             # Personal automation (bash, python, etc.)
│   │   │   ├── file-organizers/
│   │   │   ├── backup-scripts/
│   │   │   ├── git-helpers/
│   │   │   └── system-maintenance/
│   │   └── productivity-workflows/         # GTD, note-taking, task management
│   │       ├── obsidian-vault/ (or link)
│   │       ├── gtd-workflow.md
│   │       └── templates/
│   │
│   └── 🏗️ INFRASTRUCTURE/                  # 🖥️ DELL R730 & PROXMOX MANAGEMENT
│       ├── README.md                       # Infrastructure overview (consolidates Dell-Server-Roadmap)
│       ├── proxmox-config/                 # Proxmox VE setup, clustering, HA
│       │   ├── proxmox-installation.md
│       │   ├── cluster-setup.md
│       │   ├── backup-config.md
│       │   └── upgrade-procedures.md
│       ├── vm-templates/                   # Cloud-init templates, provisioning scripts
│       │   ├── ubuntu-22.04-template.md
│       │   ├── debian-12-template.md
│       │   ├── cloud-init-configs/
│       │   └── provisioning-scripts/
│       ├── network-config/                 # Bridge configs, VLANs, firewall rules
│       │   ├── vmbr0-management.md
│       │   ├── vmbr1-production.md
│       │   ├── vmbr2-internal.md
│       │   ├── firewall-rules.md
│       │   └── vpn-tailscale.md
│       ├── monitoring/                     # Grafana, Prometheus, alerts, dashboards
│       │   ├── grafana-setup.md
│       │   ├── prometheus-config.yml
│       │   ├── alert-rules.yml
│       │   └── dashboards/
│       ├── backup-scripts/                 # Automated backup scripts (Proxmox, VMs, ZFS)
│       │   ├── proxmox-backup-server.md
│       │   ├── zfs-snapshot-script.sh
│       │   ├── vm-backup-rotation.sh
│       │   └── off-site-backup.md
│       ├── ansible-playbooks/              # Infrastructure as Code (Ansible)
│       │   ├── vm-provisioning.yml
│       │   ├── security-hardening.yml
│       │   └── software-updates.yml
│       ├── terraform/                      # Infrastructure as Code (Terraform)
│       │   ├── proxmox-provider.tf
│       │   ├── vm-definitions.tf
│       │   └── network-config.tf
│       └── documentation/                  # How-tos, troubleshooting, runbooks
│           ├── troubleshooting-guide.md
│           ├── runbooks/
│           │   ├── vm-creation.md
│           │   ├── vm-migration.md
│           │   ├── storage-expansion.md
│           │   └── network-issues.md
│           └── best-practices.md
│
├── 📚 ARCHIVE/                             # 🗄️ HISTORICAL/COMPLETED PROJECTS
│   ├── README.md                           # Archive index, why archived, retrieval instructions
│   ├── flayer/                             # Archived: Flayer project (confirmed EOL)
│   │   ├── README.md (why archived)
│   │   └── project-files/
│   ├── old-server-configs/                 # Legacy configurations (pre-Proxmox, old VMs)
│   ├── deprecated-scripts/                 # No longer used scripts (keep for reference)
│   └── completed-projects/                 # Successfully completed one-off projects
│
├── 🗑️ EOL/                                 # ⚠️ END-OF-LIFE (PENDING DELETION AFTER VALIDATION)
│   ├── README.md                           # Scheduled for deletion date, validation checklist
│   ├── .gitkeep
│   └── (files moved here during migration, deleted after validation)
│
├── .github/                                # GITHUB AUTOMATION & WORKFLOWS
│   ├── workflows/                          # CI/CD automation
│   │   ├── sync-to-public.yml              # Auto-sync to public repo (sanitized, no secrets)
│   │   ├── backup-governance.yml           # Auto-backup GOVERNANCE/ to secure location
│   │   ├── security-scan.yml               # Secret scanning, vulnerability checks, SAST
│   │   ├── validate-links.yml              # Check all internal links weekly
│   │   └── update-wiki.yml                 # Sync docs to GitHub Wiki
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug-report.yml
│   │   ├── feature-request.yml
│   │   └── documentation-update.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS                          # Code ownership rules
│   └── dependabot.yml                      # Automated dependency updates
│
├── docs/                                   # PUBLIC-FACING DOCUMENTATION (syncs to Wiki)
│   ├── getting-started.md
│   ├── project-structure.md
│   ├── contributing.md
│   └── faq.md
│
├── scripts/                                # REPO-LEVEL UTILITY SCRIPTS
│   ├── migration/                          # Migration scripts (for this restructure)
│   │   ├── analyze-and-deduplicate.sh
│   │   ├── migrate-files.sh
│   │   ├── validate-migration.sh
│   │   └── sync-private-to-public.sh
│   ├── maintenance/                        # Ongoing maintenance scripts
│   │   ├── update-readmes.sh
│   │   ├── check-broken-links.sh
│   │   └── generate-directory-tree.sh
│   └── utilities/                          # General utility scripts
│       ├── file-organizer.sh
│       └── metadata-updater.py
│
├── README.md                               # 🌟 MASTER README (NAVIGATION HUB)
├── CONTRIBUTING.md                         # How to contribute (for collaborators)
├── LICENSE                                 # Private license (proprietary or restrictive)
├── .gitignore                              # Comprehensive ignore rules
├── .gitattributes                          # Git LFS, line endings, diff settings
└── CHANGELOG.md                            # Repository-level change log
```

---

### **Repository 2: `MatoTeziTanka/Shenron-Syndicate` (PUBLIC)**

```
Shenron-Syndicate/                          # PUBLIC-FACING VERSION (SANITIZED MIRROR)
│
├── 📋 ABOUT/                               # PUBLIC PHILOSOPHY & OVERVIEW
│   ├── README.md                           # What is Shenron Syndicate? Mission statement
│   ├── PHILOSOPHY.md                       # Project philosophy, values, goals
│   ├── CONTRIBUTING.md                     # How to contribute (for open-source contributors)
│   ├── CODE_OF_CONDUCT.md                  # Community standards & behavior expectations
│   ├── ROADMAP.md                          # Public roadmap (sanitized, no sensitive dates/features)
│   └── FAQ.md                              # Frequently asked questions
│
├── 🚀 PROJECTS/                            # PUBLIC PROJECT SHOWCASES (SANITIZED)
│   │
│   ├── passive-income/                     # Public-facing business model docs (no financials)
│   │   ├── README.md
│   │   ├── architecture-overview.md
│   │   ├── tech-stack.md
│   │   └── case-studies/ (sanitized)
│   │
│   ├── crypto-puzzles/                     # Public puzzle documentation (no private keys!)
│   │   ├── README.md
│   │   ├── gsmg-io/
│   │   ├── keyhound/
│   │   ├── scalpstorm/
│   │   └── how-to-play.md
│   │
│   ├── media-entertainment/                # Public media project info
│   │   ├── README.md
│   │   ├── sethflix-plex/
│   │   └── streamforge/
│   │
│   ├── family-projects/                    # Shareable family project ideas (no private photos)
│   │   ├── README.md
│   │   ├── family-care-ideas/
│   │   └── games-with-logan/
│   │
│   ├── personal-tools/                     # Open-source tools (if sharing)
│   │   ├── README.md
│   │   ├── automation-scripts/ (sanitized)
│   │   └── productivity-workflows/ (sanitized)
│   │
│   └── infrastructure/                     # Public infrastructure guides (no IPs/passwords)
│       ├── README.md
│       ├── proxmox-best-practices.md
│       ├── homelab-setup-guide.md
│       ├── zfs-tuning.md
│       └── monitoring-stack.md
│
├── 📖 WIKI/                                # COMPREHENSIVE DOCUMENTATION (auto-published to GitHub Wiki)
│   ├── getting-started/
│   │   ├── introduction.md
│   │   ├── prerequisites.md
│   │   └── quick-start.md
│   ├── tutorials/
│   │   ├── build-a-homelab.md
│   │   ├── setup-proxmox.md
│   │   ├── deploy-wordpress.md
│   │   └── create-puzzle-game.md
│   ├── best-practices/
│   │   ├── security.md
│   │   ├── backup-strategies.md
│   │   ├── documentation-standards.md
│   │   └── git-workflow.md
│   ├── reference/
│   │   ├── glossary.md
│   │   ├── tools-list.md
│   │   └── resources.md
│   └── faq/
│       ├── general.md
│       ├── technical.md
│       └── business.md
│
├── 🎨 BRANDING/                            # BRAND ASSETS (PUBLIC)
│   ├── README.md                           # Brand guidelines
│   ├── logos/
│   │   ├── shenron-syndicate-logo.svg
│   │   ├── shenron-syndicate-logo.png
│   │   └── variations/
│   ├── colors.md                           # Brand color palette
│   ├── typography.md                       # Font choices & usage
│   ├── style-guide.md                      # Visual style guidelines
│   └── assets/
│       ├── icons/
│       ├── banners/
│       └── social-media/
│
├── 🤝 COMMUNITY/                           # COMMUNITY RESOURCES
│   ├── README.md                           # Community overview
│   ├── discussions-archive/                # Notable discussion threads
│   ├── contributors.md                     # List of contributors & acknowledgments
│   └── events.md                           # Community events, meetups, etc.
│
├── .github/                                # GITHUB AUTOMATION & TEMPLATES
│   ├── workflows/
│   │   ├── deploy-wiki.yml                 # Auto-publish docs to GitHub Wiki
│   │   ├── pr-checks.yml                   # PR validation (linting, tests)
│   │   └── issue-triage.yml                # Auto-label issues
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug-report.yml
│   │   ├── feature-request.yml
│   │   └── documentation.yml
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml
│
├── README.md                               # 🌟 PUBLIC-FACING README (PROJECT HOMEPAGE)
├── CONTRIBUTING.md                         # Contribution guidelines for public contributors
├── CODE_OF_CONDUCT.md                      # Community code of conduct
├── LICENSE                                 # Open-source license (MIT, Apache 2.0, or GPL)
├── SECURITY.md                             # Security policy & vulnerability reporting
├── CHANGELOG.md                            # Public-facing change log
├── .gitignore
└── .gitattributes
```

---

## 🗺️ **PROJECT MIGRATION MAP**

### **Where Each Current Repo Goes:**

| # | Current Repository | Owner | New Location | Category | Status | Action |
|---|-------------------|-------|--------------|----------|--------|--------|
| 1 | **Dell-Server-Roadmap** | MatoTeziTanka | `PROJECTS/INFRASTRUCTURE/` | Infrastructure | Active | **Consolidate** (merge Dell docs into Infrastructure) |
| 2 | **CryptoPuzzles** | MatoTeziTanka | `PROJECTS/CRYPTO-PUZZLES/` | Puzzle | Active | **Rename folder** (keep CryptoPuzzles as subfolder or merge into others) |
| 3 | **GSMG.IO** | MatoTeziTanka | `PROJECTS/CRYPTO-PUZZLES/gsmg-io/` | Puzzle | Active | **Move** |
| 4 | **KeyHound** | sethpizzaboy | `PROJECTS/CRYPTO-PUZZLES/keyhound/` | Puzzle | Active | **Move** |
| 5 | **ScalpStorm** | sethpizzaboy | `PROJECTS/CRYPTO-PUZZLES/scalpstorm/` | Puzzle | Active | **Move** |
| 6 | **PassiveIncome** | MatoTeziTanka | `PROJECTS/PASSIVE-INCOME/` | Business | Active | **Consolidate** (top-level folder) |
| 7 | **pterodactyl-game-hosting** | (local?) | `PROJECTS/PASSIVE-INCOME/pterodactyl/` | Business | Active | **Move** |
| 8 | **Discord-Bot-monetization** | (local?) | `PROJECTS/PASSIVE-INCOME/discord-bot/` | Business | Active | **Move** (or merge with PassiveIncome) |
| 9 | **SethFlix-Plex** | MatoTeziTanka | `PROJECTS/MEDIA-ENTERTAINMENT/sethflix-plex/` | Media | Active | **Move + Rename** |
| 10 | **StreamForge** | sethpizzaboy | `PROJECTS/MEDIA-ENTERTAINMENT/streamforge/` | Media | Active | **Move** |
| 11 | **Family-Care-Ideas** | MatoTeziTanka | `PROJECTS/FAMILY-PROJECTS/family-care-ideas/` | Family | Active | **Move** |
| 12 | **FamilyFork** | sethpizzaboy | `PROJECTS/FAMILY-PROJECTS/familyfork/` | Family | Active | **Move** |
| 13 | **Games-with-Logan** | sethpizzaboy | `PROJECTS/FAMILY-PROJECTS/games-with-logan/` | Family | Active | **Move** |
| 14 | **BackTrack** | sethpizzaboy | `PROJECTS/PERSONAL-TOOLS/backtrack/` | Personal | Active | **Move** |
| 15 | **DashDenCity** | (local?) | `PROJECTS/PERSONAL-TOOLS/dashden-city/` | Personal | Active | **Move** |
| 16 | **CursorAI** | sethpizzaboy | `PROJECTS/PERSONAL-TOOLS/cursorai-configs/` | Personal | Review | **Audit first** (decide if relevant) |
| 17 | **Flayer** | sethpizzaboy | `ARCHIVE/flayer/` | Personal | EOL | **Archive** |
| 18 | **Fiverr** | (local?) | `PROJECTS/ACTIVE-INCOME/fiverr/` | Business | Active | **Move** |
| 19 | **FreeLancer** | (local?) | `PROJECTS/ACTIVE-INCOME/freelancer/` | Business | Active | **Move** |
| 20 | **Server-Roadmap** | (duplicate?) | Merge with `INFRASTRUCTURE/` | Infrastructure | Duplicate | **Merge + Delete** |
| 21 | **AI-CloakCoin** | (local?) | `PROJECTS/CRYPTO-PUZZLES/ai-cloakcoin/` | Puzzle | Active | **Move + Rename** (needs better name) |

---

## 🤖 **AUTOMATED MIGRATION: PHASE-BY-PHASE PLAN**

### **Phase 0: Preparation (Pre-Migration)**

**Duration:** 1-2 days  
**Goal:** Understand current state, plan migration

#### **Tasks:**
1. ✅ **Backup Everything**
   ```bash
   # Clone all repos locally
   mkdir ~/github-backup-$(date +%Y%m%d)
   cd ~/github-backup-$(date +%Y%m%d)
   for repo in Dell-Server-Roadmap CryptoPuzzles GSMG.IO KeyHound ScalpStorm PassiveIncome SethFlix-Plex StreamForge Family-Care-Ideas FamilyFork Games-with-Logan BackTrack CursorAI Flayer; do
       gh repo clone "owner/$repo" || echo "Failed: $repo"
   done
   
   # Create tarball backup
   tar -czf github-backup-$(date +%Y%m%d).tar.gz .
   ```

2. ✅ **Document Current State**
   - List all repos (done above)
   - Document repo sizes
   - Identify largest files (use `git-sizer`)
   - Note any Git LFS usage
   - Document branch strategies

3. ✅ **Create Migration Spreadsheet**
   - File inventory across all repos
   - Duplicate detection
   - Target destination mapping

---

### **Phase 1: Analysis & Deduplication**

**Duration:** 2-3 days  
**Goal:** Identify duplicates, categorize files, detect sensitive data

#### **Script 1: `analyze-repos.sh`**

```bash
#!/bin/bash
# Purpose: Analyze all repos, generate file inventory

BACKUP_DIR="$HOME/github-backup-$(date +%Y%m%d)"
OUTPUT_DIR="$HOME/migration-analysis"
mkdir -p "$OUTPUT_DIR"

echo "═══════════════════════════════════════════════"
echo "PHASE 1: REPOSITORY ANALYSIS"
echo "═══════════════════════════════════════════════"
echo ""

# File inventory
echo "Step 1: Generating file inventory..."
find "$BACKUP_DIR" -type f ! -path "*/.git/*" -exec md5sum {} \; > "$OUTPUT_DIR/file-hashes.txt"

# Duplicate detection
echo "Step 2: Detecting duplicates..."
awk '{print $1}' "$OUTPUT_DIR/file-hashes.txt" | sort | uniq -d > "$OUTPUT_DIR/duplicate-hashes.txt"

# Extract duplicate file details
while read hash; do
    grep "^$hash" "$OUTPUT_DIR/file-hashes.txt" >> "$OUTPUT_DIR/duplicate-files.txt"
done < "$OUTPUT_DIR/duplicate-hashes.txt"

# File categorization by extension
echo "Step 3: Categorizing files by type..."
find "$BACKUP_DIR" -type f ! -path "*/.git/*" | awk -F. '{print $NF}' | sort | uniq -c | sort -rn > "$OUTPUT_DIR/file-types.txt"

# Sensitive data detection (basic)
echo "Step 4: Scanning for sensitive data..."
grep -r -i -E "(password|api[_-]?key|secret|token|private[_-]?key)" "$BACKUP_DIR" --exclude-dir=.git > "$OUTPUT_DIR/potential-secrets.txt" 2>/dev/null

# Large files
echo "Step 5: Finding large files (>10MB)..."
find "$BACKUP_DIR" -type f ! -path "*/.git/*" -size +10M -exec ls -lh {} \; > "$OUTPUT_DIR/large-files.txt"

# Repo sizes
echo "Step 6: Calculating repo sizes..."
du -sh "$BACKUP_DIR"/*/ > "$OUTPUT_DIR/repo-sizes.txt"

echo ""
echo "✅ Analysis complete! Results in: $OUTPUT_DIR"
echo ""
echo "Files to review:"
echo "  - duplicate-files.txt (files duplicated across repos)"
echo "  - potential-secrets.txt (files containing sensitive keywords)"
echo "  - large-files.txt (files >10MB)"
echo "  - file-types.txt (file type distribution)"
echo "  - repo-sizes.txt (repository sizes)"
```

#### **Script 2: `categorize-files.py`**

```python
#!/usr/bin/env python3
"""
Purpose: Intelligently categorize files into new structure
Uses: File content analysis, keyword matching, repo context
"""

import os
import re
from pathlib import Path
import json

# Define categories and their keywords
CATEGORIES = {
    "GOVERNANCE": ["infrastructure", "network", "ip", "vm", "hardware", "zfs", "ssh", "security", "death", "backup"],
    "PASSIVE-INCOME": ["stripe", "payment", "pricing", "revenue", "customer", "wordpress", "monetization"],
    "ACTIVE-INCOME": ["fiverr", "freelancer", "invoice", "contract", "hourly"],
    "CRYPTO-PUZZLES": ["puzzle", "game", "crypto", "blockchain", "keyhound", "gsmg", "scalpstorm", "cloakcoin"],
    "MEDIA-ENTERTAINMENT": ["plex", "media", "movie", "tv", "streaming", "sethflix", "streamforge"],
    "FAMILY-PROJECTS": ["family", "logan", "care", "recipe", "activity"],
    "PERSONAL-TOOLS": ["backtrack", "dashboard", "automation", "productivity", "cursorai"],
    "INFRASTRUCTURE": ["proxmox", "dell", "vm", "server", "network", "ansible", "terraform", "monitoring"],
}

def analyze_file(filepath):
    """Analyze file content and return likely category"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read().lower()
        
        scores = {cat: 0 for cat in CATEGORIES}
        
        for category, keywords in CATEGORIES.items():
            for keyword in keywords:
                scores[category] += content.count(keyword)
        
        # Return category with highest score
        return max(scores, key=scores.get) if max(scores.values()) > 0 else "UNCATEGORIZED"
    except Exception as e:
        return "ERROR"

def main():
    backup_dir = Path.home() / f"github-backup-{os.popen('date +%Y%m%d').read().strip()}"
    output_file = Path.home() / "migration-analysis" / "file-categories.json"
    
    print("═══════════════════════════════════════════════")
    print("CATEGORIZING FILES")
    print("═══════════════════════════════════════════════")
    
    categorized = {}
    
    for filepath in backup_dir.rglob("*"):
        if filepath.is_file() and ".git" not in str(filepath):
            category = analyze_file(filepath)
            rel_path = str(filepath.relative_to(backup_dir))
            
            if category not in categorized:
                categorized[category] = []
            categorized[category].append(rel_path)
    
    with open(output_file, 'w') as f:
        json.dump(categorized, f, indent=2)
    
    print(f"✅ Categorization complete! Output: {output_file}")
    print(f"\nSummary:")
    for cat, files in categorized.items():
        print(f"  {cat}: {len(files)} files")

if __name__ == "__main__":
    main()
```

#### **Outputs:**
- `file-hashes.txt` - All files with MD5 hashes
- `duplicate-files.txt` - Duplicate files (same hash, different locations)
- `potential-secrets.txt` - Files containing sensitive keywords
- `large-files.txt` - Files >10MB (may need Git LFS)
- `file-categories.json` - Automatic categorization of files
- `manual-review.txt` - Files requiring manual categorization

---

### **Phase 2: Structure Creation**

**Duration:** 1 day  
**Goal:** Create new repos with proper structure

#### **Script 3: `create-new-structure.sh`**

```bash
#!/bin/bash
# Purpose: Create new repo structure on GitHub and locally

set -e

PRIVATE_REPO="MatoTeziTanka/Shenron-Syndicate-Private"
PUBLIC_REPO="MatoTeziTanka/Shenron-Syndicate"
LOCAL_PRIVATE="$HOME/Shenron-Syndicate-Private"
LOCAL_PUBLIC="$HOME/Shenron-Syndicate"

echo "═══════════════════════════════════════════════"
echo "PHASE 2: CREATING NEW STRUCTURE"
echo "═══════════════════════════════════════════════"
echo ""

# Create private repo
echo "Step 1: Creating private repository..."
gh repo create "$PRIVATE_REPO" --private --description "Shenron Syndicate: Private master repository for all projects" --confirm

# Create public repo
echo "Step 2: Creating public repository..."
gh repo create "$PUBLIC_REPO" --public --description "Shenron Syndicate: Public-facing documentation and open-source projects" --confirm

# Clone repos
echo "Step 3: Cloning repos locally..."
gh repo clone "$PRIVATE_REPO" "$LOCAL_PRIVATE"
gh repo clone "$PUBLIC_REPO" "$LOCAL_PUBLIC"

# Create private repo structure
echo "Step 4: Creating private repo folder structure..."
cd "$LOCAL_PRIVATE"

mkdir -p GOVERNANCE
mkdir -p PROJECTS/{PASSIVE-INCOME,ACTIVE-INCOME,CRYPTO-PUZZLES,MEDIA-ENTERTAINMENT,FAMILY-PROJECTS,PERSONAL-TOOLS,INFRASTRUCTURE}
mkdir -p ARCHIVE
mkdir -p EOL
mkdir -p .github/workflows
mkdir -p docs
mkdir -p scripts/{migration,maintenance,utilities}

# Create placeholder READMEs
echo "# Shenron Syndicate - Private" > README.md
echo "# Governance" > GOVERNANCE/README.md
echo "# Projects" > PROJECTS/README.md
echo "# Passive Income" > PROJECTS/PASSIVE-INCOME/README.md
echo "# Active Income" > PROJECTS/ACTIVE-INCOME/README.md
echo "# Crypto Puzzles" > PROJECTS/CRYPTO-PUZZLES/README.md
echo "# Media & Entertainment" > PROJECTS/MEDIA-ENTERTAINMENT/README.md
echo "# Family Projects" > PROJECTS/FAMILY-PROJECTS/README.md
echo "# Personal Tools" > PROJECTS/PERSONAL-TOOLS/README.md
echo "# Infrastructure" > PROJECTS/INFRASTRUCTURE/README.md
echo "# Archive" > ARCHIVE/README.md
echo "# End of Life (Pending Deletion)" > EOL/README.md

# Create public repo structure
echo "Step 5: Creating public repo folder structure..."
cd "$LOCAL_PUBLIC"

mkdir -p ABOUT
mkdir -p PROJECTS/{passive-income,crypto-puzzles,media-entertainment,family-projects,personal-tools,infrastructure}
mkdir -p WIKI/{getting-started,tutorials,best-practices,reference,faq}
mkdir -p BRANDING/{logos,assets}
mkdir -p COMMUNITY
mkdir -p .github/workflows

# Create placeholder READMEs
echo "# Shenron Syndicate" > README.md
echo "# About" > ABOUT/README.md
echo "# Projects" > PROJECTS/README.md
echo "# Wiki" > WIKI/README.md
echo "# Branding" > BRANDING/README.md
echo "# Community" > COMMUNITY/README.md

# Commit and push
echo "Step 6: Committing initial structure..."
cd "$LOCAL_PRIVATE"
git add .
git commit -m "Initial structure: Private repository"
git push origin main

cd "$LOCAL_PUBLIC"
git add .
git commit -m "Initial structure: Public repository"
git push origin main

echo ""
echo "✅ Structure created successfully!"
echo "  Private: $PRIVATE_REPO"
echo "  Public: $PUBLIC_REPO"
```

---

### **Phase 3: Migration**

**Duration:** 3-5 days  
**Goal:** Move files from old repos to new structure

#### **Script 4: `migrate-files.sh`**

```bash
#!/bin/bash
# Purpose: Migrate files from old repos to new structure
# Uses: file-categories.json from Phase 1

set -e

BACKUP_DIR="$HOME/github-backup-$(date +%Y%m%d)"
NEW_PRIVATE="$HOME/Shenron-Syndicate-Private"
CATEGORIES_FILE="$HOME/migration-analysis/file-categories.json"
LOG_FILE="$HOME/migration-analysis/migration-log.txt"

echo "═══════════════════════════════════════════════"
echo "PHASE 3: FILE MIGRATION"
echo "═══════════════════════════════════════════════"
echo ""

# Parse JSON and move files
python3 << 'EOF'
import json
import shutil
import os
from pathlib import Path

backup_dir = Path(os.environ['BACKUP_DIR'])
new_private = Path(os.environ['NEW_PRIVATE'])
categories_file = Path(os.environ['CATEGORIES_FILE'])
log_file = Path(os.environ['LOG_FILE'])

with open(categories_file, 'r') as f:
    categories = json.load(f)

with open(log_file, 'w') as log:
    for category, files in categories.items():
        if category == "UNCATEGORIZED" or category == "ERROR":
            # Move to EOL for manual review
            dest_base = new_private / "EOL"
        else:
            # Map category to folder
            if category == "GOVERNANCE":
                dest_base = new_private / "GOVERNANCE"
            elif category in ["PASSIVE-INCOME", "ACTIVE-INCOME", "CRYPTO-PUZZLES", "MEDIA-ENTERTAINMENT", "FAMILY-PROJECTS", "PERSONAL-TOOLS", "INFRASTRUCTURE"]:
                dest_base = new_private / "PROJECTS" / category
            else:
                dest_base = new_private / "EOL"
        
        for file in files:
            src = backup_dir / file
            # Reconstruct target path (preserving some structure)
            rel_path = Path(file).relative_to(Path(file).parts[0])  # Remove repo name
            dest = dest_base / rel_path
            
            dest.parent.mkdir(parents=True, exist_ok=True)
            
            try:
                shutil.copy2(src, dest)
                log.write(f"✅ {src} → {dest}\n")
                print(f"✅ Migrated: {file}")
            except Exception as e:
                log.write(f"❌ {src} → FAILED: {e}\n")
                print(f"❌ Failed: {file}")

print("\n✅ Migration complete! Check log: $LOG_FILE")
EOF

# Commit changes
cd "$NEW_PRIVATE"
git add .
git commit -m "Migration: Moved files from old repos"
git push origin main

echo ""
echo "✅ Migration complete!"
```

**Note:** This is a simplified version. In practice, you'd want:
- Manual review of each file placement
- Preserve git history for important files (using `git filter-repo`)
- Handle binary files (Git LFS)
- Update internal links

---

### **Phase 4: Validation**

**Duration:** 2-3 days  
**Goal:** Ensure no data loss, validate EOL folder

#### **Script 5: `validate-migration.sh`**

```bash
#!/bin/bash
# Purpose: Validate migration completeness

NEW_PRIVATE="$HOME/Shenron-Syndicate-Private"
EOL_DIR="$NEW_PRIVATE/EOL"
VALIDATION_REPORT="$HOME/migration-analysis/validation-report.txt"

echo "═══════════════════════════════════════════════"
echo "PHASE 4: VALIDATION"
echo "═══════════════════════════════════════════════"
echo ""

{
    echo "VALIDATION REPORT"
    echo "Generated: $(date)"
    echo ""
    
    # Check EOL folder
    echo "Step 1: Scanning EOL folder for valuable content..."
    if [ -d "$EOL_DIR" ]; then
        EOL_FILE_COUNT=$(find "$EOL_DIR" -type f ! -name "README.md" ! -name ".gitkeep" | wc -l)
        echo "  Files in EOL: $EOL_FILE_COUNT"
        
        if [ $EOL_FILE_COUNT -gt 0 ]; then
            echo ""
            echo "  ⚠️  WARNING: EOL folder contains files! Manual review required."
            echo ""
            echo "  Files in EOL:"
            find "$EOL_DIR" -type f ! -name "README.md" ! -name ".gitkeep" | while read file; do
                echo "    - $(basename "$file")"
                
                # Basic content check
                if grep -q -i -E "(important|critical|production|password|key)" "$file" 2>/dev/null; then
                    echo "      ⚠️  Contains potentially important keywords!"
                fi
            done
        else
            echo "  ✅ EOL folder is empty (ready for deletion)"
        fi
    fi
    
    echo ""
    echo "Step 2: Checking for broken internal links..."
    # Find all markdown files
    find "$NEW_PRIVATE" -name "*.md" -type f | while read mdfile; do
        # Extract links
        grep -o -E '\[.*\]\(.*\)' "$mdfile" 2>/dev/null | grep -o -E '\(.*\)' | tr -d '()' | while read link; do
            # Skip external links
            if [[ $link == http* ]]; then
                continue
            fi
            
            # Check if link target exists
            link_target="$(dirname "$mdfile")/$link"
            if [ ! -f "$link_target" ] && [ ! -d "$link_target" ]; then
                echo "  ❌ Broken link in $mdfile: $link"
            fi
        done
    done
    
    echo ""
    echo "Step 3: Verifying no sensitive data in files..."
    grep -r -i -E "(Norelec7!|192\.168\.12\.|ssh.*AAAA|password.*=)" "$NEW_PRIVATE" --exclude-dir=.git | while read match; do
        echo "  ⚠️  Potential sensitive data: $match"
    done
    
    echo ""
    echo "Step 4: Checking README completeness..."
    find "$NEW_PRIVATE" -type d | while read dir; do
        if [ ! -f "$dir/README.md" ] && [ "$(basename "$dir")" != ".git" ] && [ "$(basename "$dir")" != ".github" ]; then
            echo "  ⚠️  Missing README.md in: $dir"
        fi
    done
    
    echo ""
    echo "✅ Validation complete!"
    
} | tee "$VALIDATION_REPORT"

echo ""
echo "Report saved to: $VALIDATION_REPORT"
```

---

### **Phase 5: Sanitization & Public Sync**

**Duration:** 2-3 days  
**Goal:** Create sanitized public repo

#### **Script 6: `sync-private-to-public.sh`**

```bash
#!/bin/bash
# Purpose: Sync private repo to public (sanitized)

PRIVATE_DIR="$HOME/Shenron-Syndicate-Private"
PUBLIC_DIR="$HOME/Shenron-Syndicate"

echo "═══════════════════════════════════════════════"
echo "PHASE 5: SYNC TO PUBLIC"
echo "═══════════════════════════════════════════════"
echo ""

# Folders to NEVER sync (entirely private)
EXCLUDE_FOLDERS=(
    "GOVERNANCE"
    "EOL"
    "ARCHIVE"
)

# Sensitive patterns to strip from files
SENSITIVE_PATTERNS=(
    "Norelec7!"
    "192\.168\.12\."
    "ssh-rsa AAAA[A-Za-z0-9+/=]*"
    "ssh-ed25519 AAAA[A-Za-z0-9+/=]*"
    "password.*=.*"
    "api[_-]?key.*=.*"
)

echo "Step 1: Copying project files to public repo..."

# Copy projects (sanitized)
rsync -av --delete \
    --exclude="GOVERNANCE/" \
    --exclude="EOL/" \
    --exclude="ARCHIVE/" \
    --exclude=".git/" \
    --exclude="*.key" \
    --exclude="*.pem" \
    --exclude=".env" \
    "$PRIVATE_DIR/PROJECTS/" "$PUBLIC_DIR/PROJECTS/"

echo ""
echo "Step 2: Sanitizing files..."

# Find all text files and sanitize
find "$PUBLIC_DIR" -type f \( -name "*.md" -o -name "*.txt" -o -name "*.yml" -o -name "*.yaml" -o -name "*.json" \) | while read file; do
    for pattern in "${SENSITIVE_PATTERNS[@]}"; do
        sed -i "s/$pattern/[REDACTED]/g" "$file"
    done
    
    # Replace real IPs with documentation IPs
    sed -i 's/192\.168\.12\./192.0.2./g' "$file"
    
    # Replace real domain with example.com
    sed -i 's/lightspeedup\.com/example.com/g' "$file"
done

echo ""
echo "Step 3: Generating public README..."

cat > "$PUBLIC_DIR/README.md" << 'EOF'
# 🐉 Shenron Syndicate

**Shenron Syndicate** is a collection of projects spanning passive income businesses, crypto puzzles, media entertainment, family projects, and personal tools.

## 🚀 Projects

### 💰 Passive Income
- Infrastructure automation
- SaaS pricing tiers
- Game server hosting

### 🧩 Crypto Puzzles
- GSMG.IO
- KeyHound
- ScalpStorm

### 🎬 Media & Entertainment
- SethFlix Plex
- StreamForge

### 👨‍👩‍👧‍👦 Family Projects
- Family care ideas
- Games with Logan

### 🏗️ Infrastructure
- Proxmox homelab guides
- ZFS best practices
- Monitoring stack

## 📖 Documentation

Visit our [Wiki](https://github.com/MatoTeziTanka/Shenron-Syndicate/wiki) for comprehensive documentation.

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

See [LICENSE](LICENSE) for details.
EOF

# Commit and push
cd "$PUBLIC_DIR"
git add .
git commit -m "Sync from private repo (sanitized)"
git push origin main

echo ""
echo "✅ Public repo synced and sanitized!"
```

---

### **Phase 6: Cleanup & Archive**

**Duration:** 1 day  
**Goal:** Archive old repos, update references

#### **Script 7: `archive-old-repos.sh`**

```bash
#!/bin/bash
# Purpose: Archive old repositories (make read-only)

OLD_REPOS=(
    "MatoTeziTanka/Dell-Server-Roadmap"
    "MatoTeziTanka/CryptoPuzzles"
    "MatoTeziTanka/GSMG.IO"
    "MatoTeziTanka/Family-Care-Ideas"
    "MatoTeziTanka/PassiveIncome"
    "MatoTeziTanka/SethFlix-Plex"
    "sethpizzaboy/BackTrack"
    "sethpizzaboy/CursorAI"
    "sethpizzaboy/FamilyFork"
    "sethpizzaboy/Flayer"
    "sethpizzaboy/Games-with-Logan"
    "sethpizzaboy/KeyHound"
    "sethpizzaboy/ScalpStorm"
    "sethpizzaboy/StreamForge"
)

echo "═══════════════════════════════════════════════"
echo "PHASE 6: ARCHIVING OLD REPOS"
echo "═══════════════════════════════════════════════"
echo ""

for repo in "${OLD_REPOS[@]}"; do
    echo "Archiving: $repo"
    
    # Update description
    gh repo edit "$repo" --description "[ARCHIVED] Moved to Shenron-Syndicate-Private"
    
    # Archive repo (makes it read-only)
    gh repo archive "$repo" --yes
    
    echo "  ✅ Archived: $repo"
done

echo ""
echo "✅ All old repos archived!"
echo ""
echo "⚠️  IMPORTANT: Old repos are now read-only."
echo "   Review for 90 days before deleting."
```

---

## 🔒 **SECURITY & SANITIZATION RULES**

### **Never Sync to Public:**

1. **Entire Folders:**
   - `GOVERNANCE/` (all governance docs)
   - `EOL/` (end-of-life files)
   - `ARCHIVE/` (archived projects)

2. **File Types:**
   - `.key`, `.pem`, `.p12` (private keys)
   - `.env` (environment variables)
   - `*secrets*`, `*credentials*` (any filename with these words)

3. **Sensitive Patterns (Auto-Redact):**
   - Passwords: `password.*=.*`
   - API Keys: `api[_-]?key.*=.*`
   - SSH Keys: `ssh-(rsa|ed25519) AAAA[A-Za-z0-9+/=]*`
   - IP Addresses: `192.168.12.x` → Replace with `192.0.2.x`
   - Domains: `lightspeedup.com` → Replace with `example.com`
   - Personal Names: Redact non-public names

### **GitHub Secrets Scanning:**

Enable on both repos:
```bash
# Enable vulnerability alerts
gh api -X PUT /repos/MatoTeziTanka/Shenron-Syndicate-Private/vulnerability-alerts
gh api -X PUT /repos/MatoTeziTanka/Shenron-Syndicate/vulnerability-alerts

# Enable automated security fixes
gh api -X PUT /repos/MatoTeziTanka/Shenron-Syndicate-Private/automated-security-fixes
gh api -X PUT /repos/MatoTeziTanka/Shenron-Syndicate/automated-security-fixes
```

### **Pre-Commit Hook (Prevent Secret Commits):**

```bash
# .git/hooks/pre-commit
#!/bin/bash
# Prevent committing secrets

SECRETS_FOUND=0

# Scan staged files for secrets
git diff --cached --name-only | while read file; do
    if grep -q -E "(password|api[_-]?key|secret|192\.168\.12\.)" "$file" 2>/dev/null; then
        echo "❌ Potential secret found in: $file"
        SECRETS_FOUND=1
    fi
done

if [ $SECRETS_FOUND -eq 1 ]; then
    echo ""
    echo "⚠️  Commit blocked: Potential secrets detected!"
    echo "   Review files and remove sensitive data."
    exit 1
fi
```

---

## 📊 **EXPECTED OUTCOMES**

### **Before:**
- 14 repositories
- ~5-10 GB total (estimated)
- Duplicated content across repos
- Unclear project boundaries
- Sensitive data scattered
- Outdated documentation

### **After:**
- 2 repositories (Private + Public)
- Estimated size:
  - Private: ~8-12 GB (consolidated, deduplicated)
  - Public: ~500 MB - 1 GB (sanitized docs only)
- Zero duplication
- Clear hierarchical structure
- All sensitive data in GOVERNANCE/ (private only)
- Current, cross-linked documentation
- GitHub Wiki as public knowledge base

---

## ⏱️ **TIMELINE & EFFORT ESTIMATE**

| Phase | Duration | Effort | Can Automate? |
|-------|----------|--------|---------------|
| **Phase 0: Preparation** | 1-2 days | 4-8 hours | Partially (backup scripts) |
| **Phase 1: Analysis** | 2-3 days | 8-12 hours | Yes (90% automated) |
| **Phase 2: Structure Creation** | 1 day | 2-4 hours | Yes (100% automated) |
| **Phase 3: Migration** | 3-5 days | 12-20 hours | Partially (60% automated) |
| **Phase 4: Validation** | 2-3 days | 8-12 hours | Partially (70% automated) |
| **Phase 5: Public Sync** | 2-3 days | 8-12 hours | Partially (80% automated) |
| **Phase 6: Cleanup** | 1 day | 2-4 hours | Yes (90% automated) |
| **TOTAL** | **12-17 days** | **44-72 hours** | **~70% automated** |

**Recommendation:** Plan for **3-4 weeks** to allow for:
- Manual review of categorization
- Testing public sync
- Updating external references
- Buffer for unexpected issues

---

## ✅ **DECISION POINTS**

### **Questions to Answer Before Starting:**

1. **Git History:**
   - Do you want to preserve git history for important files?
   - If yes, use `git filter-repo` (slower but preserves history)
   - If no, simple file copy (faster, cleaner history)

2. **Large Files:**
   - Do you have binary files >100 MB?
   - If yes, set up Git LFS before migration

3. **Collaboration:**
   - Will others contribute to these repos?
   - If yes, set up branch protection, CODEOWNERS

4. **Naming:**
   - Is "Shenron Syndicate" the final name?
   - Any specific naming conventions for projects?

5. **AI-CloakCoin:**
   - What's the better name for this project?
   - Suggestions: CryptoCloak, CloakChain, PrivacyCoin, ShadowCoin

6. **CursorAI Repo:**
   - Is this repo relevant/active?
   - Should it be kept, archived, or deleted?

7. **Flayer:**
   - Confirmed EOL?
   - Any data worth extracting before archiving?

---

## 🎯 **SUCCESS CRITERIA**

Migration is complete when:

- ✅ All 14 repos consolidated into 2 monorepos
- ✅ Zero duplicate files (deduplication complete)
- ✅ All projects categorized correctly
- ✅ GOVERNANCE/ folder complete (Death Document, infrastructure, etc.)
- ✅ EOL/ folder validated (no valuable data)
- ✅ Public repo sanitized (zero sensitive data)
- ✅ All internal links work
- ✅ All README.md files present and current
- ✅ GitHub Wiki published (public repo)
- ✅ Old repos archived (read-only, not deleted yet)
- ✅ All repo metadata updated (descriptions, topics, homepages)
- ✅ Automated sync workflow working (private → public)
- ✅ Secret scanning enabled on both repos
- ✅ All external references updated (bookmarks, docs, etc.)

---

## 🚀 **NEXT STEPS (IF APPROVED)**

### **Immediate Actions:**

1. **Review this document** - Adjust structure/categorization as needed
2. **Answer decision points** - Git history? Git LFS? Naming?
3. **Backup everything** - Run Phase 0 scripts
4. **Test migration on 1 repo** - Prove the concept works
5. **Full migration** - Execute Phases 1-6
6. **Validation period** - 90 days with old repos archived (not deleted)
7. **Final cleanup** - Delete old repos after validation

### **Commands to Start:**

```bash
# 1. Backup all repos
mkdir ~/github-migration-$(date +%Y%m%d)
cd ~/github-migration-$(date +%Y%m%d)
# ... (run backup commands)

# 2. Run analysis
bash analyze-repos.sh

# 3. Review analysis results
less ~/migration-analysis/duplicate-files.txt
less ~/migration-analysis/potential-secrets.txt

# 4. If happy with analysis, proceed to structure creation
bash create-new-structure.sh

# ... (continue through phases)
```

---

## 💡 **MY FINAL RECOMMENDATION**

### **What I Think You Should Do:**

1. ✅ **Proceed with 2 Monorepos** (Private + Public)
   - This is the cleanest, most maintainable approach
   - Single source of truth for each visibility level
   - Aligns with your Death Document goal (everything in one place)

2. ✅ **Prioritize GOVERNANCE/ Folder First**
   - Most critical content for continuity
   - Create Death Document immediately
   - Document all infrastructure (IPs, VMs, ZFS, SSH keys)

3. ✅ **Use 70% Automation, 30% Manual Review**
   - Let scripts handle bulk work (deduplication, categorization)
   - Manually review categorization for accuracy
   - Manually sanitize sensitive data (don't rely 100% on regex)

4. ✅ **Preserve Git History for Critical Files**
   - Use `git filter-repo` for:
     - GOVERNANCE/ docs
     - Production code (PassiveIncome, etc.)
     - Any file with valuable commit history
   - Simple copy for:
     - Notes, drafts, temporary files
     - Duplicated content

5. ✅ **90-Day Validation Period**
   - Archive (don't delete) old repos
   - Make them read-only
   - After 90 days of using new structure, delete old repos

6. ✅ **Publish GitHub Wiki**
   - Public repo's documentation should be on Wiki
   - Easier to navigate than README files
   - Better for community contributions

7. ✅ **Set Up Automated Sync**
   - GitHub Action to sync private → public (sanitized)
   - Runs on every push to main
   - Prevents public repo from getting stale

### **Timeline:**

- **Week 1:** Backup, analysis, structure creation
- **Week 2:** Migration (50% complete)
- **Week 3:** Migration (100% complete), validation
- **Week 4:** Public sync, cleanup, testing

### **Effort:**

- **Total Hours:** 50-70 hours
- **AI Can Automate:** ~70% (35-50 hours saved)
- **Manual Work:** ~20-30 hours (review, decision-making, testing)

---

## 📄 **APPENDIX: EXAMPLE FILES**

### **Example: GOVERNANCE/DEATH-DOCUMENT.md**

```markdown
# 🚨 DEATH DOCUMENT (CRITICAL)

**Purpose:** If I'm unable to access these systems, this document tells my family/successors how to access everything.

**Last Updated:** [DATE]

---

## 🔐 MASTER CREDENTIALS

### Proxmox Host
- **IP:** <PROXMOX_IP>
- **Username:** root
- **Password:** [SECURE LOCATION]
- **SSH Key:** /path/to/key

### VM101 (Management AI)
- **IP:** <VM101_IP>
- **Username:** mgmt1
- **SSH Key:** /path/to/key

### GitHub
- **Account:** MatoTeziTanka
- **Email:** [EMAIL]
- **2FA Recovery Codes:** [SECURE LOCATION]

### Stripe
- **Account:** [EMAIL]
- **Recovery Codes:** [SECURE LOCATION]

---

## 📁 CRITICAL FILES

1. **This Repository:** Everything you need is in `GOVERNANCE/`
2. **Backups:** [BACKUP LOCATION]
3. **Passwords:** [PASSWORD MANAGER]

---

## 🆘 EMERGENCY CONTACTS

- **IT Contact:** [NAME, PHONE]
- **Legal:** [NAME, PHONE]
- **Accountant:** [NAME, PHONE]

---

## 📋 SHUTDOWN PROCEDURES

If shutting down infrastructure:
1. Stop all VMs (see VM-SPECIFICATIONS.md)
2. Export customer data (see BACKUP-DISASTER-RECOVERY.md)
3. Cancel Stripe subscriptions
4. Archive GitHub repos
```

---

## 🎉 **CONCLUSION**

This restructure will:
- ✅ Eliminate repository sprawl
- ✅ Create single source of truth
- ✅ Improve security (clear public/private separation)
- ✅ Enhance discoverability (GitHub Wiki, proper README files)
- ✅ Enable Death Document compliance
- ✅ Scale with future projects
- ✅ Reduce maintenance burden

**The juice is worth the squeeze.** 🍊

---

**Ready to proceed? Let me know and I'll help execute each phase!** 🚀

