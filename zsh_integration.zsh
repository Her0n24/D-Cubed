# Zsh Integration for Dynamic Prompt Reminder
# Universal support for multiple terminals

# Configuration
REMINDER_CACHE="$HOME/.cache/prompt-reminder/current_reminder.txt"
CONDA_ENV_PYTHON="/opt/miniconda3/envs/prompt-reminder/bin/python"
REMINDER_SCRIPT="$(dirname "${(%):-%x}")/prompt_reminder.py"

# Color for display
REMINDER_COLOR=$'\e[38;5;240m'
RESET_COLOR=$'\e[0m'

# Function to read current reminder
get_current_reminder() {
    if [[ -f "$REMINDER_CACHE" ]]; then
        cat "$REMINDER_CACHE" 2>/dev/null
    else
        echo "💡 Loading reminders..."
    fi
}

# Detect terminal type
detect_terminal() {
    if [[ -n "$ITERM_SESSION_ID" ]]; then
        echo "iterm2"
    elif [[ -n "$TMUX" ]]; then
        echo "tmux"
    elif [[ "$TERM_PROGRAM" == "vscode" ]]; then
        echo "vscode"
    elif [[ "$TERM_PROGRAM" == "Apple_Terminal" ]]; then
        echo "terminal_app"
    else
        echo "generic"
    fi
}

TERMINAL_TYPE=$(detect_terminal)

# iTerm2: Use status bar with user variables
update_iterm2_status() {
    local reminder=$(get_current_reminder)
    printf "\033]1337;SetUserVar=reminder=%s\a" "$(echo -n "$reminder" | base64)"
}

# tmux: Use status bar
update_tmux_status() {
    local reminder=$(get_current_reminder)
    # Truncate for tmux status bar
    if (( ${#reminder} > 80 )); then
        reminder="${reminder:0:77}..."
    fi
    tmux set-option -g status-right "#[fg=colour240]${reminder}#[default]" 2>/dev/null
}

# Generic: Show before prompt
show_prompt_reminder() {
    local reminder=$(get_current_reminder)
    if [[ -n "$reminder" ]]; then
        echo "${REMINDER_COLOR}💡 ${reminder}${RESET_COLOR}"
    fi
}

# Set up integration based on terminal type
case "$TERMINAL_TYPE" in
    iterm2)
        # iTerm2 status bar integration
        autoload -U add-zsh-hook
        precmd_update_reminder() {
            update_iterm2_status
        }
        add-zsh-hook precmd precmd_update_reminder
        
        # Initial update
        update_iterm2_status
        
        # Start continuous updater in background
        (
            while true; do
                sleep 5
                if [[ -f "$REMINDER_CACHE" ]]; then
                    reminder=$(cat "$REMINDER_CACHE" 2>/dev/null)
                    printf "\033]1337;SetUserVar=reminder=%s\a" "$(echo -n "$reminder" | base64)"
                fi
            done
        ) &
        
        # Store PID for cleanup
        ITERM_UPDATER_PID=$!
        
        echo "✨ iTerm2 status bar integration enabled!"
        echo "📋 Setup: iTerm2 → Preferences → Profiles → Session → Configure Status Bar"
        echo "   → Add 'Interpolated String' with value: \\\(user.reminder)"
        ;;
        
    tmux)
        # tmux status bar integration
        autoload -U add-zsh-hook
        precmd_update_reminder() {
            update_tmux_status
        }
        add-zsh-hook precmd precmd_update_reminder
        
        # Update periodically
        TMOUT=5
        TRAPALRM() {
            update_tmux_status
        }
        
        echo "✨ tmux status bar integration enabled!"
        ;;
        
    *)
        # Generic terminal - show before prompt
        autoload -U add-zsh-hook
        precmd_show_reminder() {
            show_prompt_reminder
        }
        add-zsh-hook precmd precmd_show_reminder
        
        echo "✨ Prompt reminders enabled!"
        ;;
esac

# Start the daemon when shell starts
start_reminder_daemon() {
    "$CONDA_ENV_PYTHON" "$REMINDER_SCRIPT" start 2>/dev/null
}

# Stop daemon when shell exits
stop_reminder_daemon() {
    "$CONDA_ENV_PYTHON" "$REMINDER_SCRIPT" stop 2>/dev/null
    # Kill iTerm updater if it exists
    if [[ -n "$ITERM_UPDATER_PID" ]]; then
        kill $ITERM_UPDATER_PID 2>/dev/null
    fi
}

# Auto-start daemon
start_reminder_daemon

# Register cleanup on shell exit
trap stop_reminder_daemon EXIT

# Provide manual control commands
alias reminder-start="$CONDA_ENV_PYTHON $REMINDER_SCRIPT start"
alias reminder-stop="$CONDA_ENV_PYTHON $REMINDER_SCRIPT stop"
alias reminder-get="$CONDA_ENV_PYTHON $REMINDER_SCRIPT get"
