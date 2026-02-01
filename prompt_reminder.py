#!/usr/bin/env python3
"""
Dynamic Terminal Prompt Reminder Daemon
Continuously updates reminder cache file every 5 seconds
"""

import random
import psutil
import os
import time
import signal
import sys
from pathlib import Path

# Reminders database
USEFUL_COMMANDS = [
    "💡 Tip: Use 'Ctrl+R' to search command history",
    "💡 Tip: Use 'cd -' to go back to previous directory",
    "💡 Tip: Use '!!' to repeat last command",
    "💡 Tip: Use 'history | grep <term>' to search history",
    "💡 Tip: Use 'Ctrl+L' to clear screen (same as 'clear')",
    "💡 Tip: Use 'Ctrl+U' to clear line before cursor",
    "💡 Tip: Use 'Ctrl+A' to jump to line start",
    "💡 Tip: Use 'Ctrl+E' to jump to line end",
    "💡 Tip: Use 'ls -lah' for detailed file listing",
    "💡 Tip: Use 'tail -f file.log' to follow log files",
]

TERMINAL_SHORTCUTS = [
    # Navigation shortcuts
    "⌨️  Shortcut: Ctrl+A - Jump to beginning of line",
    "⌨️  Shortcut: Ctrl+E - Jump to end of line",
    "⌨️  Shortcut: Ctrl+B / Left Arrow - Move back one character",
    "⌨️  Shortcut: Ctrl+F / Right Arrow - Move forward one character",
    "⌨️  Shortcut: Alt+B - Move back one word",
    "⌨️  Shortcut: Alt+F - Move forward one word",
    
    # Editing shortcuts
    "⌨️  Shortcut: Ctrl+K - Delete from cursor to end of line",
    "⌨️  Shortcut: Ctrl+U - Delete from cursor to beginning of line",
    "⌨️  Shortcut: Ctrl+W - Delete word before cursor",
    "⌨️  Shortcut: Alt+D - Delete word after cursor",
    "⌨️  Shortcut: Ctrl+Y - Paste last deleted text",
    "⌨️  Shortcut: Ctrl+T - Swap last two characters",
    "⌨️  Shortcut: Alt+T - Swap last two words",
    "⌨️  Shortcut: Ctrl+_ - Undo last change",
    
    # History shortcuts
    "⌨️  Shortcut: Ctrl+R - Reverse search command history",
    "⌨️  Shortcut: Ctrl+S - Forward search (after Ctrl+R)",
    "⌨️  Shortcut: Ctrl+P / Up Arrow - Previous command in history",
    "⌨️  Shortcut: Ctrl+N / Down Arrow - Next command in history",
    "⌨️  Shortcut: Alt+. - Insert last argument of previous command",
    "⌨️  Shortcut: !$ - Refer to last argument of previous command",
    "⌨️  Shortcut: !* - Refer to all arguments of previous command",
    "⌨️  Shortcut: !command - Run most recent command starting with 'command'",
    "⌨️  Shortcut: !123 - Run command number 123 from history",
    "⌨️  Shortcut: !! - Repeat last command",
    "⌨️  Shortcut: sudo !! - Run last command with sudo",
    
    # Screen control
    "⌨️  Shortcut: Ctrl+L - Clear screen (keep current line)",
    "⌨️  Shortcut: Ctrl+S - Stop output to screen",
    "⌨️  Shortcut: Ctrl+Q - Resume output to screen",
    "⌨️  Shortcut: Ctrl+C - Interrupt/kill current command",
    "⌨️  Shortcut: Ctrl+Z - Suspend current command (use 'fg' to resume)",
    "⌨️  Shortcut: Ctrl+D - Exit shell or close connection",
]

TERMINAL_TRICKS = [
    # Command substitution
    "🎯 Trick: Use $(command) for command substitution, e.g., echo $(date)",
    "🎯 Trick: Use {a,b,c} for brace expansion, e.g., touch file{1,2,3}.txt",
    "🎯 Trick: Use {1..10} for ranges, e.g., echo {1..10}",
    "🎯 Trick: Use && to chain commands (run if previous succeeds)",
    "🎯 Trick: Use || to run command only if previous fails",
    "🎯 Trick: Use ; to run commands sequentially regardless of success",
    
    # Navigation tricks
    "🎯 Trick: 'cd -' returns to previous directory",
    "🎯 Trick: 'cd ~username' goes to another user's home directory",
    "🎯 Trick: Use 'pushd' and 'popd' to maintain directory stack",
    "🎯 Trick: Use 'dirs -v' to see directory stack with numbers",
    
    # File operations
    "🎯 Trick: Use '>' to redirect output, '>>' to append",
    "🎯 Trick: Use '2>' to redirect errors, '&>' to redirect both",
    "🎯 Trick: Use '<' to redirect input from file",
    "🎯 Trick: Use '|' to pipe output to another command",
    "🎯 Trick: Use 'tee' to write to file AND display output",
    "🎯 Trick: Use '/dev/null' as black hole for unwanted output",
    
    # Variables and aliases
    "🎯 Trick: Set variable: VAR=value, use: $VAR or ${VAR}",
    "🎯 Trick: Export for subprocesses: export VAR=value",
    "🎯 Trick: Create alias: alias ll='ls -lah'",
    "🎯 Trick: See all aliases: alias",
    "🎯 Trick: Remove alias: unalias name",
    
    # Process management
    "🎯 Trick: Add '&' at end to run command in background",
    "🎯 Trick: Use 'jobs' to see background jobs, 'fg %1' to bring to front",
    "🎯 Trick: Use 'disown' to detach job from terminal",
    "🎯 Trick: Use 'nohup command &' to run immune to hangups",
    
    # History tricks
    "🎯 Trick: Use 'history -c' to clear history",
    "🎯 Trick: Prefix command with space to exclude from history",
    "🎯 Trick: Set HISTCONTROL=ignoredups to ignore duplicates",
    "🎯 Trick: Use Ctrl+R then Ctrl+R to cycle through matches",
    
    # Quick edits
    "🎯 Trick: Use '^old^new' to replace in last command and run",
    "🎯 Trick: Use 'fc' to edit last command in $EDITOR",
    "🎯 Trick: Use ':s/old/new/' in !! for substitution",
    
    # Useful patterns
    "🎯 Trick: Use !! for last command, e.g., sudo !!",
    "🎯 Trick: Use !$ for last argument, e.g., cat !$",
    "🎯 Trick: Use !* for all arguments, e.g., git add !*",
    "🎯 Trick: Use mkdir -p path/to/deep/dir to create nested dirs",
    "🎯 Trick: Use touch {a,b,c}.txt to create multiple files",
    "🎯 Trick: Use !! | less to page through last command's output",
    
    # Wildcards
    "🎯 Trick: Use * for any characters, ? for single character",
    "🎯 Trick: Use [abc] to match a, b, or c",
    "🎯 Trick: Use [0-9] for digit range, [a-z] for letters",
    "🎯 Trick: Use {*.txt,*.md} to match multiple patterns",
    
    # Performance
    "🎯 Trick: Use 'time command' to measure execution time",
    "🎯 Trick: Use 'watch -n 2 command' to run command every 2 seconds",
    "🎯 Trick: Use 'yes | command' to auto-answer prompts with yes",
    
    # macOS specific
    "🎯 Trick (macOS): Use 'open .' to open current directory in Finder",
    "🎯 Trick (macOS): Use 'pbcopy < file' to copy file to clipboard",
    "🎯 Trick (macOS): Use 'pbpaste > file' to paste clipboard to file",
    "🎯 Trick (macOS): Use 'caffeinate' to prevent Mac from sleeping",
]

LINUX_TIPS = [
    # File operations
    "🐧 Linux: 'df -h' - Check disk space in human-readable format",
    "🐧 Linux: 'du -sh *' - See folder sizes in current directory",
    "🐧 Linux: 'find . -name \"*.py\"' - Find files by name pattern",
    "🐧 Linux: 'find . -type f -size +100M' - Find files larger than 100MB",
    "🐧 Linux: 'find . -mtime -7' - Find files modified in last 7 days",
    "🐧 Linux: 'chmod +x script.sh' - Make file executable",
    "🐧 Linux: 'chmod 644 file.txt' - Set read/write for owner, read for others",
    "🐧 Linux: 'chown user:group file' - Change file ownership",
    "🐧 Linux: 'ln -s /path/to/file linkname' - Create symbolic link",
    "🐧 Linux: 'rsync -avz source/ dest/' - Sync files with progress",
    
    # Text processing
    "🐧 Linux: 'grep -r \"pattern\" .' - Search recursively in files",
    "🐧 Linux: 'grep -i \"text\" file' - Case-insensitive search",
    "🐧 Linux: 'grep -v \"exclude\" file' - Show lines NOT matching pattern",
    "🐧 Linux: 'sed 's/old/new/g' file' - Replace text in file",
    "🐧 Linux: 'awk '{print $1}' file' - Print first column",
    "🐧 Linux: 'cut -d',' -f1,3 file.csv' - Extract CSV columns",
    "🐧 Linux: 'sort file | uniq -c' - Count unique lines",
    "🐧 Linux: 'wc -l file' - Count lines in file",
    "🐧 Linux: 'head -n 20 file' - Show first 20 lines",
    "🐧 Linux: 'tail -f file.log' - Follow log file in real-time",
    
    # Process management
    "🐧 Linux: 'top' or 'htop' - Monitor system processes",
    "🐧 Linux: 'ps aux | grep process' - Find running processes",
    "🐧 Linux: 'kill -9 PID' - Force kill a process",
    "🐧 Linux: 'killall process_name' - Kill all processes by name",
    "🐧 Linux: 'bg' and 'fg' - Background/foreground jobs",
    "🐧 Linux: 'nohup command &' - Run command immune to hangups",
    "🐧 Linux: 'jobs' - List background jobs",
    
    # Network
    "🐧 Linux: 'curl -O url' - Download file from URL",
    "🐧 Linux: 'wget url' - Download files",
    "🐧 Linux: 'ping -c 4 google.com' - Test network connectivity",
    "🐧 Linux: 'netstat -tuln' - Show listening ports",
    "🐧 Linux: 'ss -tuln' - Modern alternative to netstat",
    "🐧 Linux: 'ifconfig' or 'ip addr' - Show network interfaces",
    "🐧 Linux: 'scp file user@host:/path' - Secure copy to remote",
    "🐧 Linux: 'ssh user@host' - Connect to remote server",
    
    # System info
    "🐧 Linux: 'uname -a' - Show system information",
    "🐧 Linux: 'uptime' - Show system uptime and load",
    "🐧 Linux: 'free -h' - Show memory usage",
    "🐧 Linux: 'lsblk' - List block devices (disks)",
    "🐧 Linux: 'lscpu' - Display CPU information",
    "🐧 Linux: 'env' - Show environment variables",
    "🐧 Linux: 'which command' - Show command path",
    "🐧 Linux: 'whereis command' - Locate binary, source, manual",
    
    # Archives
    "🐧 Linux: 'tar -xzvf file.tar.gz' - Extract .tar.gz",
    "🐧 Linux: 'tar -czvf archive.tar.gz folder/' - Create .tar.gz",
    "🐧 Linux: 'unzip file.zip' - Extract zip file",
    "🐧 Linux: 'zip -r archive.zip folder/' - Create zip",
    
    # Permissions & Users
    "🐧 Linux: 'sudo command' - Run command as superuser",
    "🐧 Linux: 'sudo su' - Switch to root user",
    "🐧 Linux: 'whoami' - Display current username",
    "🐧 Linux: 'id' - Show user and group IDs",
    "🐧 Linux: 'passwd' - Change password",
    
    # Useful combos
    "🐧 Linux: 'command 2>&1 | tee log.txt' - Save output to file AND display",
    "🐧 Linux: 'command > /dev/null 2>&1' - Suppress all output",
    "🐧 Linux: 'watch -n 2 command' - Run command every 2 seconds",
    "🐧 Linux: 'xargs' - Build command from standard input",
    "🐧 Linux: 'yes | command' - Auto-answer yes to prompts",
]

GITHUB_COPILOT_TIPS = [
    "🤖 Copilot: Use '@workspace' to ask about your codebase",
    "🤖 Copilot: Use '#file' to reference specific files",
    "🤖 Copilot: Type '/' for slash commands",
    "🤖 Copilot: Use 'gh' CLI for GitHub operations",
    "🤖 Copilot: Break complex tasks into smaller steps",
    "🤖 Copilot: Ask for explanations of unfamiliar code",
]

GIT_COMMANDS = [
    # Basic operations
    "🌿 Git: 'git status' - Show working tree status",
    "🌿 Git: 'git add -A' - Stage all changes",
    "🌿 Git: 'git add -p' - Stage changes interactively",
    "🌿 Git: 'git commit -m \"message\"' - Commit with message",
    "🌿 Git: 'git commit --amend' - Modify last commit",
    "🌿 Git: 'git commit --amend --no-edit' - Add to last commit, keep message",
    
    # Viewing history
    "🌿 Git: 'git log --oneline' - Compact commit history",
    "🌿 Git: 'git log --graph --oneline --all' - Visual branch history",
    "🌿 Git: 'git log -p' - Show changes in each commit",
    "🌿 Git: 'git log --author=\"name\"' - Filter commits by author",
    "🌿 Git: 'git show commit_hash' - Show specific commit details",
    "🌿 Git: 'git blame file' - See who changed each line",
    
    # Branches
    "🌿 Git: 'git branch' - List local branches",
    "🌿 Git: 'git branch -a' - List all branches (including remote)",
    "🌿 Git: 'git branch new-branch' - Create new branch",
    "🌿 Git: 'git checkout branch' - Switch to branch",
    "🌿 Git: 'git checkout -b new-branch' - Create and switch to new branch",
    "🌿 Git: 'git branch -d branch' - Delete merged branch",
    "🌿 Git: 'git branch -D branch' - Force delete branch",
    "🌿 Git: 'git merge branch' - Merge branch into current",
    
    # Remote operations
    "🌿 Git: 'git remote -v' - Show remote repositories",
    "🌿 Git: 'git fetch' - Download remote changes (don't merge)",
    "🌿 Git: 'git pull' - Fetch and merge remote changes",
    "🌿 Git: 'git push' - Push commits to remote",
    "🌿 Git: 'git push -u origin branch' - Push and set upstream",
    "🌿 Git: 'git push --force-with-lease' - Safer force push",
    
    # Undoing changes
    "🌿 Git: 'git diff' - Show unstaged changes",
    "🌿 Git: 'git diff --staged' - Show staged changes",
    "🌿 Git: 'git restore file' - Discard changes in file",
    "🌿 Git: 'git restore --staged file' - Unstage file",
    "🌿 Git: 'git reset HEAD~1' - Undo last commit (keep changes)",
    "🌿 Git: 'git reset --hard HEAD~1' - Undo last commit (delete changes)",
    "🌿 Git: 'git revert commit_hash' - Create new commit undoing changes",
    
    # Stashing
    "🌿 Git: 'git stash' - Save changes temporarily",
    "🌿 Git: 'git stash pop' - Apply and remove latest stash",
    "🌿 Git: 'git stash list' - List all stashes",
    "🌿 Git: 'git stash apply stash@{0}' - Apply specific stash",
    "🌿 Git: 'git stash drop' - Delete latest stash",
    
    # Advanced
    "🌿 Git: 'git rebase main' - Rebase current branch on main",
    "🌿 Git: 'git rebase -i HEAD~3' - Interactive rebase last 3 commits",
    "🌿 Git: 'git cherry-pick commit_hash' - Apply specific commit",
    "🌿 Git: 'git clean -fd' - Remove untracked files and directories",
    "🌿 Git: 'git reflog' - Show history of HEAD changes",
    "🌿 Git: 'git bisect start' - Binary search for bug introduction",
]

def get_cpu_info():
    """Get current CPU usage and temperature if available"""
    cpu_percent = psutil.cpu_percent(interval=0.1)
    cpu_emoji = "🔥" if cpu_percent > 80 else "⚡" if cpu_percent > 50 else "💻"
    return f"{cpu_emoji} CPU: {cpu_percent}%"

def get_memory_info():
    """Get current memory usage"""
    mem = psutil.virtual_memory()
    mem_emoji = "🔴" if mem.percent > 80 else "🟡" if mem.percent > 50 else "🟢"
    return f"{mem_emoji} RAM: {mem.percent}%"

def get_disk_info():
    """Get disk usage for home directory"""
    try:
        disk = psutil.disk_usage(os.path.expanduser('~'))
        disk_emoji = "💾"
        return f"{disk_emoji} Disk: {disk.percent}%"
    except:
        return None

def detect_context():
    """Detect current working context for smart suggestions"""
    context = {
        'is_git_repo': False,
        'is_python_project': False,
        'is_node_project': False,
        'is_docker_project': False,
        'recent_commands': [],
        'last_command_type': None
    }
    
    # Check current directory context
    cwd = os.getcwd()
    
    # Git repository?
    if os.path.isdir(os.path.join(cwd, '.git')):
        context['is_git_repo'] = True
    
    # Python project?
    python_indicators = ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile']
    if any(os.path.isfile(os.path.join(cwd, f)) for f in python_indicators):
        context['is_python_project'] = True
    
    # Node project?
    if os.path.isfile(os.path.join(cwd, 'package.json')):
        context['is_node_project'] = True
    
    # Docker project?
    docker_indicators = ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
    if any(os.path.isfile(os.path.join(cwd, f)) for f in docker_indicators):
        context['is_docker_project'] = True
    
    # Parse recent command history
    try:
        shell = os.environ.get('SHELL', '')
        history_file = None
        
        if 'zsh' in shell:
            history_file = os.path.expanduser('~/.zsh_history')
        elif 'bash' in shell:
            history_file = os.path.expanduser('~/.bash_history')
        
        if history_file and os.path.isfile(history_file):
            with open(history_file, 'rb') as f:
                # Get last 20 commands
                lines = f.readlines()[-20:]
                for line in lines:
                    try:
                        cmd = line.decode('utf-8', errors='ignore').strip()
                        # Clean zsh history format
                        if ':' in cmd and ';' in cmd:
                            cmd = cmd.split(';', 1)[1].strip()
                        if cmd:
                            context['recent_commands'].append(cmd)
                    except:
                        pass
            
            # Determine last command type
            if context['recent_commands']:
                last_cmd = context['recent_commands'][-1].lower()
                if last_cmd.startswith('git'):
                    context['last_command_type'] = 'git'
                elif last_cmd.startswith(('docker', 'docker-compose')):
                    context['last_command_type'] = 'docker'
                elif last_cmd.startswith(('python', 'pip', 'conda')):
                    context['last_command_type'] = 'python'
                elif last_cmd.startswith(('npm', 'yarn', 'node')):
                    context['last_command_type'] = 'node'
    except:
        pass
    
    return context

def get_weighted_reminder(context):
    """Get reminder with intelligent weighting based on context"""
    # Start with equal weights
    weights = {
        'git': 1.0,
        'linux': 1.0,
        'shortcuts': 1.0,
        'tricks': 1.0,
        'copilot': 1.0,
        'useful': 1.0,
    }
    
    # Adjust weights based on context
    if context['is_git_repo']:
        weights['git'] *= 3.0  # 3x more likely to show git tips
    
    if context['last_command_type'] == 'git':
        weights['git'] *= 2.0  # 2x boost if just used git
    
    if context['last_command_type'] == 'docker':
        weights['linux'] *= 1.5  # Docker users need linux commands
    
    # Build weighted list
    weighted_reminders = []
    weighted_reminders.extend(GIT_COMMANDS * int(weights['git']))
    weighted_reminders.extend(LINUX_TIPS * int(weights['linux']))
    weighted_reminders.extend(TERMINAL_SHORTCUTS * int(weights['shortcuts']))
    weighted_reminders.extend(TERMINAL_TRICKS * int(weights['tricks']))
    weighted_reminders.extend(GITHUB_COPILOT_TIPS * int(weights['copilot']))
    weighted_reminders.extend(USEFUL_COMMANDS * int(weights['useful']))
    
    return random.choice(weighted_reminders)

def get_random_reminder():
    """Get a random reminder from all categories with context awareness"""
    try:
        # Detect context for smart suggestions
        context = detect_context()
        
        # Get weighted reminder based on context
        return get_weighted_reminder(context)
    except Exception as e:
        # Fallback to simple random if context detection fails
        all_reminders = (
            USEFUL_COMMANDS + 
            TERMINAL_SHORTCUTS +
            TERMINAL_TRICKS +
            LINUX_TIPS + 
            GITHUB_COPILOT_TIPS + 
            GIT_COMMANDS
        )
        return random.choice(all_reminders)

# Cache file location
CACHE_DIR = Path.home() / '.cache' / 'prompt-reminder'
CACHE_FILE = CACHE_DIR / 'current_reminder.txt'
PID_FILE = CACHE_DIR / 'daemon.pid'

def setup_cache():
    """Create cache directory if it doesn't exist"""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

def update_reminder():
    """Update the reminder cache file"""
    reminder = get_random_reminder()
    with open(CACHE_FILE, 'w') as f:
        f.write(reminder)

def daemon_loop():
    """Main daemon loop - updates reminder every 5 seconds"""
    setup_cache()
    
    # Write PID file
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    print(f"Daemon started with PID {os.getpid()}")
    print(f"Cache file: {CACHE_FILE}")
    
    def signal_handler(sig, frame):
        print("\nDaemon stopping...")
        PID_FILE.unlink(missing_ok=True)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    try:
        while True:
            update_reminder()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nDaemon stopped")
        PID_FILE.unlink(missing_ok=True)

def start_daemon():
    """Start the daemon in background"""
    setup_cache()
    
    # Check if daemon is already running
    if PID_FILE.exists():
        try:
            with open(PID_FILE, 'r') as f:
                pid = int(f.read().strip())
            # Check if process is running
            os.kill(pid, 0)
            print(f"Daemon already running with PID {pid}")
            return
        except (ProcessLookupError, ValueError):
            # Process not running, remove stale PID file
            PID_FILE.unlink()
    
    # Fork to background
    pid = os.fork()
    if pid > 0:
        print(f"Daemon started with PID {pid}")
        print(f"Cache file: {CACHE_FILE}")
        sys.exit(0)
    
    # Decouple from parent
    os.setsid()
    os.chdir('/')
    
    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    daemon_loop()

def stop_daemon():
    """Stop the running daemon"""
    if not PID_FILE.exists():
        print("Daemon is not running")
        return
    
    try:
        with open(PID_FILE, 'r') as f:
            pid = int(f.read().strip())
        os.kill(pid, signal.SIGTERM)
        print(f"Stopped daemon with PID {pid}")
        PID_FILE.unlink(missing_ok=True)
    except (ProcessLookupError, ValueError):
        print("Daemon is not running")
        PID_FILE.unlink(missing_ok=True)

def get_reminder():
    """Get current reminder from cache file"""
    setup_cache()
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r') as f:
            return f.read().strip()
    return "💡 Tip: Press Tab for suggestions"

def main():
    """Main function"""
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'daemon':
            daemon_loop()
        elif cmd == 'start':
            start_daemon()
        elif cmd == 'stop':
            stop_daemon()
        elif cmd == 'get':
            print(get_reminder())
        else:
            print(f"Unknown command: {cmd}")
            print("Usage: prompt_reminder.py [daemon|start|stop|get]")
    else:
        # Default: just print a reminder
        print(get_reminder())

if __name__ == "__main__":
    main()
