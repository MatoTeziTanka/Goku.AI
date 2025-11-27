#!/bin/bash

set -e

DEPLOYMENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_DIR="${HOME}/.vm101-deployment"
MAIN_LOG="${LOG_DIR}/VM101-DEPLOYMENT-MASTER-${TIMESTAMP}.log"
STATUS_FILE="${LOG_DIR}/deployment-status.json"

mkdir -p "$LOG_DIR"

log_message() {
    local level=$1
    local message=$2
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[${timestamp}] [${level}] ${message}" | tee -a "$MAIN_LOG"
}

log_task_status() {
    local task_id=$1
    local status=$2
    local message=$3
    local duration=$4
    
    local entry=$(cat <<EOF
{
  "task_id": "${task_id}",
  "status": "${status}",
  "message": "${message}",
  "duration_seconds": ${duration},
  "timestamp": "$(date '+%Y-%m-%d %H:%M:%S')"
}
EOF
)
    echo "$entry" >> "${LOG_DIR}/task-${task_id}-${TIMESTAMP}.json"
}

execute_task() {
    local task_id=$1
    local task_name=$2
    local script=$3
    
    log_message "INFO" "=========================================="
    log_message "INFO" "Starting Task ${task_id}: ${task_name}"
    log_message "INFO" "=========================================="
    
    local start_time=$(date +%s)
    
    if [ ! -f "$script" ]; then
        log_message "ERROR" "Script not found: $script"
        log_task_status "$task_id" "FAILED" "Script not found" 0
        return 1
    fi
    
    if ! bash "$script" >> "$MAIN_LOG" 2>&1; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        log_message "ERROR" "Task ${task_id} failed"
        log_task_status "$task_id" "FAILED" "Script execution failed" "$duration"
        return 1
    fi
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    log_message "SUCCESS" "Task ${task_id} completed in ${duration} seconds"
    log_task_status "$task_id" "SUCCESS" "Task completed successfully" "$duration"
    
    return 0
}

print_banner() {
    cat <<'EOF'

╔════════════════════════════════════════════════════════════════════╗
║                  ZENCODER v1.0.0 DEPLOYMENT                        ║
║                   Master Execution Script                          ║
║                                                                    ║
║  This script will execute all deployment tasks in sequence         ║
║  All progress will be logged to: $MAIN_LOG                         ║
╚════════════════════════════════════════════════════════════════════╝

EOF
}

print_banner

log_message "INFO" "Starting Zencoder v1.0.0 Deployment"
log_message "INFO" "Log file: $MAIN_LOG"
log_message "INFO" "Package directory: $DEPLOYMENT_DIR"
log_message "INFO" "User: $(whoami)"
log_message "INFO" "Host: $(hostname)"
log_message "INFO" "Timestamp: $(date)"

log_message "INFO" ""
log_message "INFO" "📋 Deployment Plan:"
log_message "INFO" "  1. Task 1.1 - Execute Setup Script (30 min)"
log_message "INFO" "  2. Task 1.2 - Deploy Keys to Linux VMs (45 min)"
log_message "INFO" "  3. Task 1.3 - Test Windows Deployment (30 min)"
log_message "INFO" "  4. Task 1.4 - Verify All Services (30 min)"
log_message "INFO" "  5. Task 1.5 - Setup Basic Monitoring (30 min)"
log_message "INFO" ""

read -p "Continue with deployment? (yes/no): " confirm_deploy
if [ "$confirm_deploy" != "yes" ]; then
    log_message "WARN" "Deployment cancelled by user"
    exit 0
fi

log_message "INFO" "User confirmed deployment"

failed_tasks=()
successful_tasks=()

if execute_task "1.1" "Execute Setup Script" "${DEPLOYMENT_DIR}/TASK-1.1-EXECUTE-SETUP.sh"; then
    successful_tasks+=("1.1")
else
    failed_tasks+=("1.1")
    log_message "WARN" "Pausing for manual review. Continue? (yes/no): "
    read -p "" continue_after_failure
    if [ "$continue_after_failure" != "yes" ]; then
        log_message "ERROR" "Deployment stopped by user after Task 1.1 failure"
        exit 1
    fi
fi

if execute_task "1.2" "Deploy Keys to Linux VMs" "${DEPLOYMENT_DIR}/TASK-1.2-DEPLOY-KEYS-LINUX.sh"; then
    successful_tasks+=("1.2")
else
    failed_tasks+=("1.2")
    log_message "WARN" "Task 1.2 failed, but continuing to next tasks"
fi

if execute_task "1.3" "Test Windows Deployment" "${DEPLOYMENT_DIR}/TASK-1.3-TEST-WINDOWS.sh"; then
    successful_tasks+=("1.3")
else
    failed_tasks+=("1.3")
    log_message "WARN" "Task 1.3 failed, but continuing to next tasks"
fi

if execute_task "1.4" "Verify All Services" "${DEPLOYMENT_DIR}/TASK-1.4-VERIFY-SERVICES.sh"; then
    successful_tasks+=("1.4")
else
    failed_tasks+=("1.4")
    log_message "WARN" "Task 1.4 failed, but continuing to next tasks"
fi

if execute_task "1.5" "Setup Basic Monitoring" "${DEPLOYMENT_DIR}/TASK-1.5-SETUP-MONITORING.sh"; then
    successful_tasks+=("1.5")
else
    failed_tasks+=("1.5")
fi

log_message "INFO" ""
log_message "INFO" "=========================================="
log_message "INFO" "DEPLOYMENT SUMMARY"
log_message "INFO" "=========================================="
log_message "INFO" "Successful Tasks: ${#successful_tasks[@]}"
for task in "${successful_tasks[@]}"; do
    log_message "INFO" "  ✅ Task $task"
done

if [ ${#failed_tasks[@]} -gt 0 ]; then
    log_message "ERROR" "Failed Tasks: ${#failed_tasks[@]}"
    for task in "${failed_tasks[@]}"; do
        log_message "ERROR" "  ❌ Task $task"
    done
fi

log_message "INFO" ""
log_message "INFO" "📋 Next Steps:"
log_message "INFO" "  1. Review logs: $MAIN_LOG"
log_message "INFO" "  2. Run QC verification: ${DEPLOYMENT_DIR}/QC-VERIFY-ALL.sh"
log_message "INFO" "  3. If issues found, use rollback: ${DEPLOYMENT_DIR}/ROLLBACK.sh"
log_message "INFO" ""

if [ ${#failed_tasks[@]} -eq 0 ]; then
    log_message "SUCCESS" "✅ All deployment tasks completed successfully!"
    exit 0
else
    log_message "ERROR" "❌ Some tasks failed. Please review logs and troubleshoot."
    exit 1
fi
