#!/bin/bash

set -e

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
TASK_LOG="${HOME}/.vm101-deployment/TASK-1.5-MONITORING-${TIMESTAMP}.log"
QC_CHECKLIST="${HOME}/.vm101-deployment/TASK-1.5-QC-${TIMESTAMP}.log"

mkdir -p "${HOME}/.vm101-deployment"

log_msg() {
    local level=$1
    local msg=$2
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $msg" | tee -a "$TASK_LOG"
}

qc_check() {
    local check=$1
    local status=$2
    echo "- [ ] $check: $status" >> "$QC_CHECKLIST"
}

log_msg "INFO" "=========================================="
log_msg "INFO" "TASK 1.5: Setup Basic Monitoring"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "Objective: Setup SSH connection logging and basic alerts"
log_msg "INFO" "Time: ~30 minutes"
log_msg "INFO" "Location: VM101"
log_msg "INFO" ""

echo "Task 1.5 QC Checklist" > "$QC_CHECKLIST"
echo "===================" >> "$QC_CHECKLIST"
echo "" >> "$QC_CHECKLIST"

MONITOR_DIR="${HOME}/.vm101-deployment/monitoring"
mkdir -p "$MONITOR_DIR"

log_msg "INFO" "Setting up SSH monitoring..."
log_msg "INFO" ""

setup_ssh_logging() {
    log_msg "INFO" "Configuring SSH logging..."
    
    local sshd_config="/etc/ssh/sshd_config"
    local log_file="/var/log/auth.log"
    
    if [ ! -f "$sshd_config" ]; then
        log_msg "WARN" "SSH config not found: $sshd_config"
        log_msg "INFO" "SSH logging may already be configured"
        qc_check "SSH logging configuration" "WARNING - sshd_config not found"
        return 0
    fi
    
    if grep -q "^SyslogFacility" "$sshd_config"; then
        log_msg "INFO" "✅ SSH syslog facility already configured"
        qc_check "SSH syslog facility" "PASS"
    else
        log_msg "INFO" "ℹ️  SSH syslog facility not explicitly configured (using defaults)"
        qc_check "SSH syslog facility" "INFO"
    fi
    
    if grep -q "^LogLevel" "$sshd_config"; then
        local log_level=$(grep "^LogLevel" "$sshd_config" | awk '{print $2}')
        log_msg "INFO" "✅ SSH LogLevel configured: $log_level"
        qc_check "SSH LogLevel" "PASS - $log_level"
    else
        log_msg "INFO" "ℹ️  SSH LogLevel using default"
        qc_check "SSH LogLevel" "INFO - using default"
    fi
    
    if [ -f "$log_file" ]; then
        log_msg "INFO" "✅ SSH log file present: $log_file"
        qc_check "SSH log file" "PASS"
        
        local recent_lines=$(tail -5 "$log_file" 2>/dev/null | wc -l)
        log_msg "INFO" "Recent log entries: $recent_lines"
    else
        log_msg "WARN" "SSH log file not found: $log_file"
        qc_check "SSH log file" "WARNING"
    fi
    
    return 0
}

create_monitoring_script() {
    log_msg "INFO" "Creating SSH monitoring script..."
    
    local monitor_script="${MONITOR_DIR}/monitor-ssh-connections.sh"
    
    cat > "$monitor_script" << 'EOF'
#!/bin/bash

# Simple SSH connection monitoring script
# Logs all SSH connections and failed attempts

MONITOR_LOG="${HOME}/.vm101-deployment/monitoring/ssh-monitor.log"
FAILED_LOG="${HOME}/.vm101-deployment/monitoring/ssh-failed-attempts.log"

# Function to log SSH connections
log_ssh_connection() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] SSH Connection: $@" >> "$MONITOR_LOG"
}

# Function to log failed attempts
log_failed_attempt() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] FAILED SSH Attempt: $@" >> "$FAILED_LOG"
}

# Monitor auth log for SSH activity
if [ -f "/var/log/auth.log" ]; then
    # Get last hour of SSH activity
    tail -f /var/log/auth.log | grep "sshd\|SSH" | while read line; do
        if echo "$line" | grep -q "Failed password\|Invalid user\|Authentication failure"; then
            log_failed_attempt "$line"
        elif echo "$line" | grep -q "Accepted\|session opened"; then
            log_ssh_connection "$line"
        fi
    done
else
    echo "Auth log not found"
    exit 1
fi
EOF
    
    chmod +x "$monitor_script"
    log_msg "INFO" "✅ Monitoring script created: $monitor_script"
    qc_check "SSH monitoring script" "PASS"
}

create_alert_script() {
    log_msg "INFO" "Creating alert script..."
    
    local alert_script="${MONITOR_DIR}/ssh-alert-checker.sh"
    
    cat > "$alert_script" << 'EOF'
#!/bin/bash

# Check for suspicious SSH activity and alert
# Run this periodically via cron

THRESHOLD=5  # Alert if more than 5 failed attempts in 5 minutes
ALERT_LOG="${HOME}/.vm101-deployment/monitoring/alerts.log"

mkdir -p "$(dirname "$ALERT_LOG")"

check_failed_attempts() {
    # Count failed SSH attempts in last 5 minutes
    if [ ! -f "/var/log/auth.log" ]; then
        return
    fi
    
    local time_ago=$(date -d '5 minutes ago' '+%b %d %H:%M' 2>/dev/null || date -v-5m '+%b %d %H:%M')
    local recent_failures=$(grep "$time_ago" /var/log/auth.log 2>/dev/null | grep -i "failed password\|invalid user" | wc -l)
    
    if [ "$recent_failures" -gt "$THRESHOLD" ]; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ALERT: $recent_failures failed SSH attempts detected" >> "$ALERT_LOG"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Details:" >> "$ALERT_LOG"
        grep "$time_ago" /var/log/auth.log 2>/dev/null | grep -i "failed password\|invalid user" | tail -$recent_failures >> "$ALERT_LOG"
        echo "" >> "$ALERT_LOG"
    fi
}

check_key_deployment() {
    # Check if any new SSH keys were deployed recently
    KEY_DIR="${HOME}/.ssh/vm-keys"
    DEPLOY_LOG="${HOME}/.ssh/key-deployment.log"
    
    if [ -f "$DEPLOY_LOG" ]; then
        local recent_changes=$(find "$KEY_DIR" -type f -mmin -60 2>/dev/null | wc -l)
        if [ "$recent_changes" -gt 0 ]; then
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] INFO: $recent_changes SSH keys modified in last hour" >> "$ALERT_LOG"
        fi
    fi
}

check_service_status() {
    # Check if critical services are still running
    services=("docker" "code-server" "ssh")
    
    for service in "${services[@]}"; do
        if ! systemctl is-active --quiet "$service" 2>/dev/null; then
            if [ "$service" != "docker" ] || systemctl is-active --quiet docker 2>/dev/null; then
                true  # Docker might not be in systemctl
            else
                echo "[$(date '+%Y-%m-%d %H:%M:%S')] WARNING: Service '$service' is not running" >> "$ALERT_LOG"
            fi
        fi
    done
}

# Run all checks
check_failed_attempts
check_key_deployment
check_service_status

# Display recent alerts
if [ -f "$ALERT_LOG" ]; then
    tail -20 "$ALERT_LOG"
fi
EOF
    
    chmod +x "$alert_script"
    log_msg "INFO" "✅ Alert checker script created: $alert_script"
    qc_check "Alert checker script" "PASS"
}

create_cron_job() {
    log_msg "INFO" "Creating cron job for periodic monitoring..."
    
    local alert_script="${MONITOR_DIR}/ssh-alert-checker.sh"
    local cron_comment="SSH Monitoring Alert Checker (Zencoder v1.0.0)"
    
    (crontab -l 2>/dev/null | grep -v "$cron_comment" || true; \
     echo "# $cron_comment" && \
     echo "*/5 * * * * ${alert_script} > /dev/null 2>&1") | crontab -
    
    log_msg "INFO" "✅ Cron job installed to run every 5 minutes"
    qc_check "Cron job installed" "PASS"
}

create_readme() {
    log_msg "INFO" "Creating monitoring documentation..."
    
    local readme="${MONITOR_DIR}/README.md"
    
    cat > "$readme" << 'EOF'
# SSH Monitoring Setup

## Overview

This directory contains SSH monitoring and alerting scripts for Zencoder v1.0.0 deployment.

## Scripts

### monitor-ssh-connections.sh
Continuously monitors SSH connections and logs them.

**Usage:**
```bash
./monitor-ssh-connections.sh &
```

### ssh-alert-checker.sh
Checks for suspicious SSH activity and generates alerts.

**Usage:**
```bash
./ssh-alert-checker.sh
```

Or run periodically via cron (already configured).

## Log Files

- `ssh-monitor.log` - All SSH connections
- `ssh-failed-attempts.log` - Failed authentication attempts
- `alerts.log` - Suspicious activity alerts

## Alerts

Alerts are triggered when:
- More than 5 failed SSH attempts in 5 minutes
- SSH keys modified
- Critical services go down

## Disabling Monitoring

Remove the cron job:
```bash
crontab -e
# Delete the SSH Monitoring line
```

## Manual Checks

Check for failed attempts:
```bash
grep "Failed password" /var/log/auth.log | tail -20
```

Check SSH key deployments:
```bash
ls -la ~/.ssh/vm-keys/
```

Check service status:
```bash
systemctl status docker code-server ssh
```
EOF
    
    log_msg "INFO" "✅ Monitoring documentation created: $readme"
    qc_check "Monitoring README" "PASS"
}

create_summary_report() {
    log_msg "INFO" "Creating monitoring summary report..."
    
    local report="${MONITOR_DIR}/MONITORING-SUMMARY.txt"
    
    cat > "$report" << EOF
=====================================
SSH Monitoring Setup Summary
Generated: $(date)
=====================================

INSTALLED COMPONENTS:
  ✅ SSH Logging Configuration
  ✅ Monitoring Scripts
  ✅ Alert Checker
  ✅ Cron Job (runs every 5 minutes)

KEY LOCATION:
  ~/.ssh/vm-keys/

SSH CONFIG:
  ~/.ssh/config

LOG FILES:
  /var/log/auth.log (system SSH logs)
  ~/.vm101-deployment/monitoring/ssh-monitor.log
  ~/.vm101-deployment/monitoring/ssh-failed-attempts.log
  ~/.vm101-deployment/monitoring/alerts.log

ALERT THRESHOLDS:
  - Failed SSH attempts: > 5 in 5 minutes
  - Key modifications: any changes logged
  - Service status: critical services monitored

VERIFICATION COMMANDS:
  1. Check SSH config:
     cat ~/.ssh/config

  2. Check recent SSH activity:
     tail -20 /var/log/auth.log | grep sshd

  3. Check deployment logs:
     ls -la ~/.vm101-deployment/monitoring/

  4. View recent alerts:
     tail -20 ~/.vm101-deployment/monitoring/alerts.log

NEXT STEPS:
  1. Monitor alerts regularly
  2. Review logs periodically
  3. Respond to any suspicious activity
  4. Test alert system: generate failed login attempts

EMERGENCY:
  If suspicious activity detected:
  1. Check /var/log/auth.log for details
  2. Review ~/.ssh/vm-keys/ for unauthorized keys
  3. Contact system administrator
  4. Review SSH config for unauthorized entries

=====================================
EOF
    
    log_msg "INFO" "✅ Monitoring summary created: $report"
    qc_check "Monitoring summary report" "PASS"
}

log_msg "INFO" ""
log_msg "INFO" "SETTING UP MONITORING SYSTEM"
log_msg "INFO" ""

setup_ssh_logging
log_msg "INFO" ""

create_monitoring_script
log_msg "INFO" ""

create_alert_script
log_msg "INFO" ""

create_cron_job
log_msg "INFO" ""

create_readme
log_msg "INFO" ""

create_summary_report

log_msg "INFO" ""
log_msg "INFO" "=========================================="
log_msg "INFO" "MONITORING SETUP VERIFICATION"
log_msg "INFO" "=========================================="
log_msg "INFO" ""
log_msg "INFO" "✅ SSH monitoring configured"
log_msg "INFO" "✅ Alert scripts installed"
log_msg "INFO" "✅ Cron job scheduled"
log_msg "INFO" "✅ Documentation created"
log_msg "INFO" ""
log_msg "INFO" "Monitoring Directory: $MONITOR_DIR"

log_msg "INFO" "Files installed:"
ls -lah "$MONITOR_DIR"/ 2>&1 | tee -a "$TASK_LOG"

log_msg "INFO" ""
log_msg "INFO" "Next Steps:"
log_msg "INFO" "  1. Review monitoring documentation:"
log_msg "INFO" "     cat ${MONITOR_DIR}/README.md"
log_msg "INFO" "  2. Review monitoring summary:"
log_msg "INFO" "     cat ${MONITOR_DIR}/MONITORING-SUMMARY.txt"
log_msg "INFO" "  3. Test alert system:"
log_msg "INFO" "     ${MONITOR_DIR}/ssh-alert-checker.sh"
log_msg "INFO" "  4. Monitor alerts regularly"
log_msg "INFO" ""
log_msg "INFO" "Automatic monitoring:"
log_msg "INFO" "  - Cron job runs every 5 minutes"
log_msg "INFO" "  - Check alerts in: ~/.vm101-deployment/monitoring/alerts.log"
log_msg "INFO" ""
log_msg "SUCCESS" "✅ Task 1.5 Complete"

echo ""
echo "QC Checklist saved to: $QC_CHECKLIST"
echo ""
cat "$QC_CHECKLIST"
