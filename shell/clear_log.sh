#!/bin/bash
# Log cleanup script for /tmp/dumas/* 
# Runs on the last day of every month
# Author: Operations Team
# Date: $(date)

# Configuration
LOG_DIR="/tmp/dumas"
SCRIPT_LOG="/var/log/log_cleanup.log"
RETENTION_DAYS=30

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$SCRIPT_LOG"
}

# Function to check if today is the last day of the month
is_last_day_of_month() {
    local today=$(date '+%Y-%m-%d')
    local tomorrow=$(date -d "$today + 1 day" '+%Y-%m-%d')
    local today_month=$(date -d "$today" '+%m')
    local tomorrow_month=$(date -d "$tomorrow" '+%m')
    
    if [ "$today_month" != "$tomorrow_month" ]; then
        return 0  # True - today is last day of month
    else
        return 1  # False - not last day of month
    fi
}

# Function to cleanup logs
cleanup_logs() {
    log_message "Starting log cleanup in $LOG_DIR"
    
    # Check if directory exists
    if [ ! -d "$LOG_DIR" ]; then
        log_message "ERROR: Directory $LOG_DIR does not exist"
        exit 1
    fi
    
    # Count files before cleanup
    local file_count_before=$(find "$LOG_DIR" -type f -name "*.log" 2>/dev/null | wc -l)
    local total_size_before=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
    
    log_message "Found $file_count_before log files, total size: $total_size_before"
    
    # Remove log files older than retention period
    local deleted_count=0
    
    # Find and delete log files older than RETENTION_DAYS
    while IFS= read -r -d '' file; do
        if [ -f "$file" ]; then
            rm -f "$file"
            ((deleted_count++))
            log_message "Deleted: $file"
        fi
    done < <(find "$LOG_DIR" -type f -name "*.log" -mtime +$RETENTION_DAYS -print0 2>/dev/null)
    
    # Also clean up any empty directories
    find "$LOG_DIR" -type d -empty -delete 2>/dev/null
    
    # Count files after cleanup
    local file_count_after=$(find "$LOG_DIR" -type f -name "*.log" 2>/dev/null | wc -l)
    local total_size_after=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
    
    log_message "Cleanup completed. Deleted $deleted_count files"
    log_message "Remaining: $file_count_after log files, total size: $total_size_after"
}

# Main execution
main() {
    log_message "Log cleanup script started"
    
    # Check if today is the last day of the month
    if is_last_day_of_month; then
        log_message "Today is the last day of the month - proceeding with cleanup"
        cleanup_logs
    else
        log_message "Today is not the last day of the month - skipping cleanup"
        exit 0
    fi
    
    log_message "Log cleanup script completed"
}

# Run main function
main "$@"