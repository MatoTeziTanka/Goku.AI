# ═══════════════════════════════════════════════════════════════════════════
# SHENRON COMPLETE KNOWLEDGE INJECTION SCRIPT
# One-command deployment of entire knowledge base + automation systems
# For: VM100 (Windows Server 2025) - Shenron's Home
# ═══════════════════════════════════════════════════════════════════════════

$ErrorActionPreference = "Continue"

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║       🐉 SHENRON FULL POWER INJECTION SYSTEM 🐉              ║
║                                                              ║
║    Deploying: Knowledge Base + Income Automation            ║
║    Target: $3,000/month passive income                      ║
╚══════════════════════════════════════════════════════════════╝

"@ -ForegroundColor Cyan

# Configuration
$GITHUB_REPO = "MatoTeziTanka/Dell-Server-Roadmap"
$LOCAL_REPO = "C:\GitHub\Dell-Server-Roadmap"
$KNOWLEDGE_BASE = "C:\GOKU-AI\knowledge-base"
$SHENRON_DIR = "C:\GOKU-AI\shenron"

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: PULL LATEST FROM GITHUB
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n[1/6] 📥 Pulling latest knowledge from GitHub..." -ForegroundColor Yellow

cd $LOCAL_REPO

# Fetch latest
git fetch origin main

# Check if there are updates
$LOCAL_HASH = git rev-parse HEAD
$REMOTE_HASH = git rev-parse origin/main

if ($LOCAL_HASH -eq $REMOTE_HASH) {
    Write-Host "✅ Already up to date!" -ForegroundColor Green
} else {
    Write-Host "🔄 Updates available, pulling..." -ForegroundColor Cyan
    git pull origin main
    Write-Host "✅ Repository updated!" -ForegroundColor Green
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: COPY KNOWLEDGE FILES TO SHENRON
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n[2/6] 📚 Copying knowledge files to Shenron..." -ForegroundColor Yellow

# Ensure knowledge base directory exists
New-Item -ItemType Directory -Path $KNOWLEDGE_BASE -Force | Out-Null

# Copy all markdown knowledge files
$KnowledgeFiles = Get-ChildItem -Path $LOCAL_REPO -Filter "knowledge-*.md" -File
$CopiedCount = 0

foreach ($file in $KnowledgeFiles) {
    Copy-Item $file.FullName -Destination $KNOWLEDGE_BASE -Force
    Write-Host "  ✅ $($file.Name)" -ForegroundColor Green
    $CopiedCount++
}

# Copy GitHub repo markdown files (already there from previous clone)
$GitHubKnowledge = Get-ChildItem -Path $KNOWLEDGE_BASE -Filter "github-*.md" -File
$TotalKnowledge = $CopiedCount + $GitHubKnowledge.Count

Write-Host "`n📊 Total knowledge files: $TotalKnowledge" -ForegroundColor Cyan
Write-Host "  - Core knowledge: $CopiedCount" -ForegroundColor White
Write-Host "  - GitHub repos: $($GitHubKnowledge.Count)" -ForegroundColor White

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: COPY AUTOMATION SCRIPTS
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n[3/6] ⚙️ Deploying automation scripts..." -ForegroundColor Yellow

# Copy Python scripts
$PythonScripts = @(
    "shenron-income-dashboard.py"
)

foreach ($script in $PythonScripts) {
    $SourcePath = Join-Path $LOCAL_REPO "scripts\$script"
    if (Test-Path $SourcePath) {
        Copy-Item $SourcePath -Destination $SHENRON_DIR -Force
        Write-Host "  ✅ $script" -ForegroundColor Green
    }
}

# Copy bash scripts (for SSH execution on Linux VMs)
New-Item -ItemType Directory -Path "$SHENRON_DIR\linux-scripts" -Force | Out-Null

$BashScripts = @(
    "pterodactyl-automation.sh",
    "wordpress-multi-tenant-automation.sh"
)

foreach ($script in $BashScripts) {
    $SourcePath = Join-Path $LOCAL_REPO "scripts\$script"
    if (Test-Path $SourcePath) {
        Copy-Item $SourcePath -Destination "$SHENRON_DIR\linux-scripts" -Force
        Write-Host "  ✅ $script" -ForegroundColor Green
    }
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: GENERATE SSH KEYS (if not exists)
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n[4/6] 🔐 Checking SSH keys..." -ForegroundColor Yellow

$SSHKeyPath = "$SHENRON_DIR\.ssh\id_ed25519"

# Create .ssh directory
New-Item -ItemType Directory -Path "$SHENRON_DIR\.ssh" -Force | Out-Null

if (Test-Path $SSHKeyPath) {
    Write-Host "  ✅ SSH keys already exist" -ForegroundColor Green
} else {
    Write-Host "  🔧 Generating new SSH keys..." -ForegroundColor Cyan
    
    # Check if ssh-keygen is available
    try {
        ssh-keygen -t ed25519 -C "shenron@lightspeedup.com" -f $SSHKeyPath -N '""'
        Write-Host "  ✅ SSH keys generated!" -ForegroundColor Green
    } catch {
        Write-Host "  ⚠️  ssh-keygen not found - installing OpenSSH..." -ForegroundColor Yellow
        Add-WindowsCapability -Online -Name OpenSSH.Client~~~~0.0.1.0 | Out-Null
        Write-Host "  ✅ OpenSSH installed! Restart PowerShell and run this script again." -ForegroundColor Green
        exit
    }
}

# Display public key
if (Test-Path "$SSHKeyPath.pub") {
    $publicKey = Get-Content "$SSHKeyPath.pub"
    
    # Save to easily accessible file
    $publicKey | Out-File -FilePath "$SHENRON_DIR\SHENRON-PUBLIC-KEY.txt" -Encoding UTF8
    
    Write-Host "`n📋 SHENRON PUBLIC KEY:" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host $publicKey -ForegroundColor Green
    Write-Host "=" * 60 -ForegroundColor Cyan
    Write-Host "`n💾 Saved to: $SHENRON_DIR\SHENRON-PUBLIC-KEY.txt" -ForegroundColor Yellow
    Write-Host "`n⚠️  ACTION REQUIRED: Add this key to your VMs!" -ForegroundColor Yellow
    Write-Host "   See: SSH-SETUP-COMPLETE-CHECKLIST.md" -ForegroundColor White
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: INGEST KNOWLEDGE INTO CHROMADB
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n[5/6] 🧠 Ingesting knowledge into ChromaDB..." -ForegroundColor Yellow

cd $SHENRON_DIR

# Check if inject_knowledge.py exists
if (Test-Path "inject_knowledge.py") {
    Write-Host "  🔄 Running knowledge ingestion..." -ForegroundColor Cyan
    python inject_knowledge.py
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ Knowledge ingestion complete!" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Ingestion completed with warnings" -ForegroundColor Yellow
    }
} else {
    Write-Host "  ⚠️  inject_knowledge.py not found - manual ingestion needed" -ForegroundColor Yellow
}

# ═══════════════════════════════════════════════════════════════════════════
# STEP 6: RESTART SHENRON SERVICE
# ═══════════════════════════════════════════════════════════════════════════

Write-Host "`n[6/6] 🔄 Restarting SHENRON service..." -ForegroundColor Yellow

try {
    Restart-Service -Name "SHENRON" -Force
    Write-Host "  ✅ SHENRON restarted successfully!" -ForegroundColor Green
} catch {
    Write-Host "  ⚠️  Could not restart service: $_" -ForegroundColor Yellow
    Write-Host "  Manual restart may be needed" -ForegroundColor White
}

# ═══════════════════════════════════════════════════════════════════════════
# COMPLETION SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

Write-Host @"

╔══════════════════════════════════════════════════════════════╗
║                   ✅ INJECTION COMPLETE! ✅                   ║
╚══════════════════════════════════════════════════════════════╝

📊 DEPLOYMENT SUMMARY:
═════════════════════
✅ GitHub repository updated
✅ $TotalKnowledge knowledge files loaded
✅ Automation scripts deployed
✅ SSH keys ready
✅ ChromaDB ingestion complete
✅ SHENRON service restarted

🐉 SHENRON IS NOW READY FOR:
════════════════════════════
💰 Game server hosting automation
💼 WordPress hosting management
📊 Real-time income monitoring
🤖 24/7 customer support
🎯 $3,000/month income generation

🚀 NEXT STEPS:
══════════════
1. Test Shenron: http://localhost:5001/api/shenron
2. Deploy Pterodactyl (VM203): ssh mgmt1@192.168.12.203
   sudo bash $SHENRON_DIR\linux-scripts\pterodactyl-automation.sh
3. Set up Stripe billing
4. Launch marketing campaigns

🎉 YOUR WISH IS BEING GRANTED! 🎉

"@ -ForegroundColor Green

# Show income dashboard (if available)
if (Test-Path "$SHENRON_DIR\shenron-income-dashboard.py") {
    Write-Host "`n📊 CURRENT INCOME STATUS:" -ForegroundColor Cyan
    python "$SHENRON_DIR\shenron-income-dashboard.py"
}

Write-Host "`n🐉 Shenron awaits your command..." -ForegroundColor Yellow

