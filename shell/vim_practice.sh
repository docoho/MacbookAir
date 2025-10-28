#!/bin/bash
# Shebang line - specifies that this script should be executed using the bash shell

# Log cleanup script for /tmp/dumas/*
# Runs on the last day of every month
# Author: Operations Team
# Date: $(date)
# These are header comments documenting the script's purpose, schedule, author, and date

# Configuration
LOG_DIR="/tmp/dumas"
# Variable declaration - sets the directory path where log files are stored

SCRIPT_LOG="/var/log/log_cleanup.log"
# Variable declaration - sets the path for this script's own log file to record its operations

RETENTION_DAYS=30
# Variable declaration - defines how many days to keep log files (files older than 30 days will be deleted)

# Function to log messages
log_message() {
    # Function definition - creates a reusable function named "log_message" that takes one parameter ($1)

    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$SCRIPT_LOG"
    # Outputs a timestamped message to both stdout and appends it to the log file
    # $(date '+%Y-%m-%d %H:%M:%S') - generates current timestamp in YYYY-MM-DD HH:MM:SS format
    # $1 - the message text passed as first argument to the function
    # tee -a - displays on screen AND appends to the log file simultaneously
}

# Function to check if today is the last day of the month
is_last_day_of_month() {
    # Function definition - determines whether the current date is the last day of the month

    local today=$(date '+%Y-%m-%d')
    # Creates a local variable storing today's date in YYYY-MM-DD format

    local tomorrow=$(date -d "$today + 1 day" '+%Y-%m-%d')
    # Creates a local variable storing tomorrow's date by adding 1 day to today

    local today_month=$(date -d "$today" '+%m')
    # Extracts the month number (01-12) from today's date

    local tomorrow_month=$(date -d "$tomorrow" '+%m')
    # Extracts the month number (01-12) from tomorrow's date

    if [ "$today_month" != "$tomorrow_month" ]; then
        # Compares today's month with tomorrow's month
        # If they're different, it means today is the last day of the current month

        return 0  # True - today is last day of month
        # Returns 0 (success/true in bash) indicating today is the last day
    else
        # If the months are the same, today is not the last day

        return 1  # False - not last day of month
        # Returns 1 (failure/false in bash) indicating today is not the last day
    fi
}

# Function to cleanup logs
cleanup_logs() {
    # Function definition - performs the actual log file cleanup operations

    log_message "Starting log cleanup in $LOG_DIR"
    # Logs a message indicating the cleanup process has started

    # Check if directory exists
    if [ ! -d "$LOG_DIR" ]; then
        # Tests if the log directory does NOT exist (-d checks for directory, ! negates the test)

        log_message "ERROR: Directory $LOG_DIR does not exist"
        # Logs an error message if the directory is missing

        exit 1
        # Exits the script with error code 1 (non-zero indicates failure)
    fi

    # Count files before cleanup
    local file_count_before=$(find "$LOG_DIR" -type f -name "*.log" 2>/dev/null | wc -l)
    # Counts the number of .log files before cleanup
    # find - searches for files matching criteria
    # -type f - only regular files
    # -name "*.log" - only files ending in .log
    # 2>/dev/null - suppresses error messages
    # wc -l - counts the number of lines (files found)

    local total_size_before=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
    # Calculates the total disk usage of the log directory before cleanup
    # du -sh - disk usage, summary in human-readable format
    # cut -f1 - extracts only the size portion (first field)

    log_message "Found $file_count_before log files, total size: $total_size_before"
    # Logs the count and size of files before cleanup

    # Remove log files older than retention period
    local deleted_count=0
    # Initializes a counter variable to track how many files are deleted

    # Find and delete log files older than RETENTION_DAYS
    while IFS= read -r -d '' file; do
        # Starts a while loop that reads null-terminated filenames from the find command
        # IFS= - prevents trimming of whitespace
        # read -r - reads raw input without interpreting backslashes
        # -d '' - uses null character as delimiter (works with -print0)

        if [ -f "$file" ]; then
            # Checks if the item is actually a regular file (safety check)

            rm -f "$file"
            # Deletes the file forcefully without prompting

            ((deleted_count++))
            # Increments the deleted file counter by 1

            log_message "Deleted: $file"
            # Logs which file was deleted
        fi
    done < <(find "$LOG_DIR" -type f -name "*.log" -mtime +$RETENTION_DAYS -print0 2>/dev/null)
    # Process substitution - feeds the output of find into the while loop
    # -mtime +$RETENTION_DAYS - finds files modified more than RETENTION_DAYS ago
    # -print0 - outputs filenames separated by null characters (handles spaces/special chars safely)

    # Also clean up any empty directories
    find "$LOG_DIR" -type d -empty -delete 2>/dev/null
    # Finds and deletes any empty subdirectories within the log directory
    # -type d - only directories
    # -empty - only empty directories
    # -delete - deletes the found items

    # Count files after cleanup
    local file_count_after=$(find "$LOG_DIR" -type f -name "*.log" 2>/dev/null | wc -l)
    # Counts the number of .log files remaining after cleanup (same method as before)

    local total_size_after=$(du -sh "$LOG_DIR" 2>/dev/null | cut -f1)
    # Calculates the total disk usage after cleanup (same method as before)

    log_message "Cleanup completed. Deleted $deleted_count files"
    # Logs a summary message showing how many files were deleted

    log_message "Remaining: $file_count_after log files, total size: $total_size_after"
    # Logs the final count and size of remaining log files
}

# Main execution
main() {
    # Function definition - the main entry point that orchestrates the script's workflow

    log_message "Log cleanup script started"
    # Logs that the script has begun execution

    # Check if today is the last day of the month
    if is_last_day_of_month; then
        # Calls the is_last_day_of_month function and checks if it returns true (0)

        log_message "Today is the last day of the month - proceeding with cleanup"
        # Logs that cleanup will proceed because it's the last day of the month

        cleanup_logs
        # Calls the cleanup_logs function to perform the actual cleanup
    else
        # If today is not the last day of the month

        log_message "Today is not the last day of the month - skipping cleanup"
        # Logs that cleanup is being skipped

        exit 0
        # Exits successfully (0 = success) without performing cleanup
    fi

    log_message "Log cleanup script completed"
    # Logs that the script has finished successfully
}

# Run main function
main "$@"
# Executes the main function, passing all script arguments ($@) to it