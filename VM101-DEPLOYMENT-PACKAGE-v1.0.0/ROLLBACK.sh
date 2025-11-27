#!/bin/bash

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
ROLLBACK_LOG="${HOME}/.vm101-deployment/ROLLBACK-${TIMESTAMP}.log"

mkdir -p "${HOME}/.vm101-deployment"

log_msg() {
    local level=$1
    local msg=$2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg" | tee -a "$ROLLBACK_LOG"
}

print_header() {
    cat <<'EOF'

╔════════════════════════════════════════════════════════════════════╗
║         ZENCODER v1.0.0 DEPLOYMENT ROLLBACK                        ║
║                                                                    ║
║  This script will rollback SSH key migration if needed             ║
║  WARNING: This will restore backed-up SSH configuration            ║
╚════════════════════════════════════════════════════════════════════╝

EOF
}

print_header

log_msg "WARN" "=========================================="
log_msg "WARN" "ROLLBACK PROCEDURE INITIATED"
log_msg "WARN" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "This will rollback to previous SSH configuration"
log_msg "INFO" "Backed-up files location: ${HOME}/.ssh/backup-*"
log_msg "INFO" ""

read -p "⚠️  Are you sure you want to rollback? Type 'yes' to confirm: " confirm

if [ "$confirm" != "yes" ]; then
    log_msg "INFO" "Rollback cancelled by user"
    exit 0
fi

log_msg "WARN" "User confirmed rollback"

find_backup() {
    log_msg "INFO" "Looking for backup directories..."
    
    local backups=$(find "${HOME}/.ssh" -maxdepth 1 -type d -name "backup-*" 2>/dev/null | sort -r | head -1)
    
    if [ -z "$backups" ]; then
        log_msg "ERROR" "No backup directories found"
        log_msg "INFO" "Checked: ${HOME}/.ssh/backup-*"
        return 1
    fi
    
    echo "$backups"
    return 0
}

BACKUP_DIR=$(find_backup)

if [ -z "$BACKUP_DIR" ]; then
    log_msg "ERROR" "Cannot find backup directory"
    exit 1
fi

log_msg "INFO" "Found backup directory: $BACKUP_DIR"

if [ ! -f "$BACKUP_DIR/config" ]; then
    log_msg "WARN" "SSH config backup not found in $BACKUP_DIR"
    log_msg "INFO" "Files in backup directory:"
    ls -la "$BACKUP_DIR" >> "$ROLLBACK_LOG"
fi

read -p "Restore from $BACKUP_DIR ? (yes/no): " confirm_restore

if [ "$confirm_restore" != "yes" ]; then
    log_msg "INFO" "Rollback cancelled by user at restore step"
    exit 0
fi

log_msg "INFO" ""
log_msg "INFO" "RESTORING SSH CONFIGURATION"
log_msg "INFO" "============================="
log_msg "INFO" ""

restore_ssh_config() {
    if [ -f "$BACKUP_DIR/config" ]; then
        log_msg "INFO" "Restoring SSH config..."
        cp "$BACKUP_DIR/config" "${HOME}/.ssh/config"
        chmod 600 "${HOME}/.ssh/config"
        log_msg "INFO" "✅ SSH config restored"
    else
        log_msg "WARN" "No SSH config backup found"
    fi
}

restore_ssh_keys() {
    log_msg "INFO" "Restoring SSH keys..."
    
    if [ -f "$BACKUP_DIR/id_rsa" ]; then
        cp "$BACKUP_DIR/id_rsa" "${HOME}/.ssh/id_rsa"
        chmod 600 "${HOME}/.ssh/id_rsa"
        log_msg "INFO" "✅ id_rsa restored"
    fi
    
    if [ -f "$BACKUP_DIR/id_rsa.pub" ]; then
        cp "$BACKUP_DIR/id_rsa.pub" "${HOME}/.ssh/id_rsa.pub"
        chmod 644 "${HOME}/.ssh/id_rsa.pub"
        log_msg "INFO" "✅ id_rsa.pub restored"
    fi
    
    if [ -f "$BACKUP_DIR/id_ed25519" ]; then
        cp "$BACKUP_DIR/id_ed25519" "${HOME}/.ssh/id_ed25519"
        chmod 600 "${HOME}/.ssh/id_ed25519"
        log_msg "INFO" "✅ id_ed25519 restored"
    fi
    
    if [ -f "$BACKUP_DIR/id_ed25519.pub" ]; then
        cp "$BACKUP_DIR/id_ed25519.pub" "${HOME}/.ssh/id_ed25519.pub"
        chmod 644 "${HOME}/.ssh/id_ed25519.pub"
        log_msg "INFO" "✅ id_ed25519.pub restored"
    fi
}

backup_current_config() {
    log_msg "INFO" "Backing up current configuration..."
    
    local current_backup="${HOME}/.ssh/backup-pre-rollback-${TIMESTAMP}"
    mkdir -p "$current_backup"
    
    if [ -d "${HOME}/.ssh/vm-keys" ]; then
        cp -r "${HOME}/.ssh/vm-keys" "$current_backup/"
        log_msg "INFO" "✅ Backed up current vm-keys"
    fi
    
    if [ -f "${HOME}/.ssh/config" ]; then
        cp "${HOME}/.ssh/config" "$current_backup/"
        log_msg "INFO" "✅ Backed up current SSH config"
    fi
    
    log_msg "INFO" "Pre-rollback backup saved to: $current_backup"
}

backup_current_config
log_msg "INFO" ""

restore_ssh_config
log_msg "INFO" ""

restore_ssh_keys
log_msg "INFO" ""

log_msg "INFO" "Verifying restoration..."

if [ -f "${HOME}/.ssh/config" ]; then
    log_msg "INFO" "✅ SSH config file present"
else
    log_msg "ERROR" "❌ SSH config file not found after restoration"
fi

if [ -f "${HOME}/.ssh/id_rsa" ]; then
    log_msg "INFO" "✅ SSH private key present"
else
    log_msg "WARN" "⚠️  SSH private key not found (may be expected)"
fi

log_msg "INFO" ""
log_msg "INFO" "=========================================="
log_msg "INFO" "ROLLBACK CLEANUP"
log_msg "INFO" "=========================================="
log_msg "INFO" ""

read -p "Remove VM-specific keys directory (vm-keys)? (yes/no): " remove_vm_keys

if [ "$remove_vm_keys" = "yes" ]; then
    if [ -d "${HOME}/.ssh/vm-keys" ]; then
        log_msg "INFO" "Removing vm-keys directory..."
        rm -rf "${HOME}/.ssh/vm-keys"
        log_msg "INFO" "✅ vm-keys directory removed"
    fi
else
    log_msg "INFO" "Keeping vm-keys directory for reference"
fi

log_msg "INFO" ""
log_msg "INFO" "=========================================="
log_msg "INFO" "ROLLBACK COMPLETE"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "Restoration Summary:"
log_msg "INFO" "  - SSH configuration restored from backup"
log_msg "INFO" "  - SSH keys restored from backup"
log_msg "INFO" "  - Current config backed up for recovery"
log_msg "INFO" ""
log_msg "INFO" "Next Steps:"
log_msg "INFO" "  1. Test SSH connectivity: ssh <known-host>"
log_msg "INFO" "  2. Verify services still running: systemctl status docker"
log_msg "INFO" "  3. Review rollback log: $ROLLBACK_LOG"
log_msg "INFO" ""
log_msg "INFO" "If you need to restore from rollback:"
log_msg "INFO" "  Backup directory: ${HOME}/.ssh/backup-pre-rollback-${TIMESTAMP}"
log_msg "INFO" ""
log_msg "SUCCESS" "✅ Rollback completed successfully"

echo ""
echo "Rollback log saved to: $ROLLBACK_LOG"
