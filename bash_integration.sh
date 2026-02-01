#!/bin/bash
# Bash Integration for Dynamic Prompt Reminder
# Works with default macOS Terminal app

# Configuration
REMINDER_CACHE="$HOME/.cache/prompt-reminder/current_reminder.txt"
CONDA_ENV_PYTHON="/opt/miniconda3/envs/prompt-reminder/bin/python"
REMINDER_SCRIPT="$(dirname "${BASH_SOURCE[0]}")/prompt_reminder.py"

# Colors
REMINDER_COLOR='\033[38;5;240m'  # Gray
RESET_COLOR='\033[0m'

# Function to read current reminder
get_current_reminder() {
    if [[ -f "$REMINDER_CACHE" ]]; then
        cat "$REMINDER_CACHE" 2>/dev/null
    else
        echo ""
    fi
}

# Function to display reminder before prompt
display_reminder() {
    local reminder=$(get_current_reminder)
    if [[ -n "$reminder" ]]; then
        echo -e "${REMINDER_COLOR}💡 ${reminder}${RESET_COLOR}"
    fi
}

# Add to PROMPT_COMMAND to run before each prompt
if [[ -z "$PROMPT_COMMAND" ]]; then
    PROMPT_COMMAND="display_reminder"
else
    PROMPT_COMMAND="display_reminder; $PROMPT_COMMAND"
fi

# Start the daemon
start_reminder_daemon() {
    "$CONDA_ENV_PYTHON" "$REMINDER_SCRIPT" start 2>/dev/null
}

# Stop daemon on exit
stop_reminder_daemon() {
    "$CONDA_ENV_PYTHON" "$REMINDER_SCRIPT" stop 2>/dev/null
}

# Auto-start daemon
start_reminder_daemon

# Register cleanup
trap stop_reminder_daemon EXIT

# Aliases for manual control
alias reminder-start="$CONDA_ENV_PYTHON $REMINDER_SCRIPT start"
alias reminder-stop="$CONDA_ENV_PYTHON $REMINDER_SCRIPT stop"
alias reminder-get="$CONDA_ENV_PYTHON $REMINDER_SCRIPT get"

echo "✨ Dynamic reminders enabled for Bash!"
