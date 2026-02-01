# Terminal Learning Assistant 🎓

A context-aware terminal reminder system that helps developers learn commands, shortcuts, and best practices through intelligent, automated suggestions.

## 🌟 Key Features

### 1. **Context-Aware Intelligence**
The system analyzes your environment and adapts suggestions:
- **Git Repository Detection**: 3x more Git tips when working in a git repo
- **Project Type Detection**: Recognizes Python, Node.js, Docker projects
- **Command History Analysis**: Learns from your recent commands
- **Last Command Awareness**: Shows relevant tips based on what you just did

### 2. **Comprehensive Knowledge Base (200+ Tips)**
- ⌨️  **35+ Terminal Shortcuts** - Ctrl+R, Alt+B, editing shortcuts
- 🎯 **60+ Terminal Tricks** - Pipes, redirects, brace expansion, aliases
- 🐧 **65+ Linux Commands** - File operations, text processing, networking, archives
- 🌿 **55+ Git Commands** - From basics to advanced (rebase, cherry-pick, bisect)
- 🤖 **GitHub Copilot Tips** - Maximize your AI assistant

### 3. **Non-Intrusive Display**
- **iTerm2 Status Bar Integration** - Fixed position, never scrolls with output
- **Auto-updates every 5 seconds** - Continuous learning while you work
- **Clean, professional UI** - Follows terminal UI best practices

## 🎯 How It Works

1. **Background Daemon** - Python service updates suggestions every 5 seconds
2. **Context Detection** - Analyzes current directory, git status, command history
3. **Intelligent Weighting** - Prioritizes relevant tips based on your context
4. **Shell Integration** - Seamless Zsh integration with iTerm2

## 📊 Smart Context Detection

### Directory Context
```python
# Detects:
- Git repositories (.git folder)
- Python projects (requirements.txt, setup.py, pyproject.toml)  
- Node.js projects (package.json)
- Docker projects (Dockerfile, docker-compose.yml)
```

### Command History Analysis
```python
# Reads last 20 commands from:
- ~/.zsh_history
- ~/.bash_history

# Determines command patterns:
- Frequent git usage → more Git tips
- Docker commands → more Linux/container tips
- Python commands → Python-related suggestions
```

### Intelligent Weighting
```python
# Example: In a Git repository
- Git tips: 3x weight (most likely)
- Linux tips: 1x weight  
- Shortcuts: 1x weight
- If last command was 'git status':
  - Git tips: 6x weight (3x * 2x boost)
```

## 🖥️ Supported Platforms

### Operating Systems
- ✅ **macOS** - Native support
- ✅ **Linux** - Ubuntu, Debian, Fedora, Arch, etc.
- ✅ **BSD** - FreeBSD, OpenBSD
- ✅ **Windows** - Via WSL (Windows Subsystem for Linux)

### Terminal Emulators
- ✅ **iTerm2** (macOS) - Status bar integration
- ✅ **tmux** - Status line integration (any platform)
- ✅ **Terminal.app** (macOS) - Prompt display
- ✅ **VS Code Terminal** - Prompt display
- ✅ **GNOME Terminal** (Linux) - Prompt display
- ✅ **Konsole** (KDE) - Prompt display
- ✅ **Alacritty** - Prompt display
- ✅ **Kitty** - Prompt display
- ✅ **Any standard terminal** - Basic prompt display

### Shells
- ✅ **Zsh** - Full support (recommended)
- ✅ **Bash** - Full support

### Display Modes

The system automatically detects your terminal and adapts:

1. **iTerm2 (macOS)** - Fixed status bar at top/bottom
2. **tmux** - Integrated into tmux status line
3. **Other terminals** - Clean display above prompt

### Components
1. **`prompt_reminder.py`** - Core daemon with context detection
2. **`zsh_integration.zsh`** - Shell hooks and iTerm2 integration
3. **`install_prompt.sh`** - Automated setup script
4. **Conda Environment** - Isolated Python dependencies

### Technology Stack
- **Python 3.9** - Core logic and daemon
- **psutil** - System information (optional)
- **Zsh hooks** - Shell integration
- **iTerm2 escape codes** - Status bar communication

## 🚀 Installation

```bash
# 1. Install the system
./install_prompt.sh

# 2. Configure iTerm2 status bar
# iTerm2 → Preferences → Profiles → Session → Configure Status Bar
# Add "Interpolated String" component with value: \(user.reminder)

# 3. Reload shell
source ~/.zshrc
```

## 💡 Usage Examples

### In a Git Repository
When you `cd` into a git repo, you'll see more Git tips:
```
🌿 Git: 'git stash' - Save changes temporarily
🌿 Git: 'git rebase -i HEAD~3' - Interactive rebase last 3 commits
🌿 Git: 'git cherry-pick commit_hash' - Apply specific commit
```

### After Using Git Commands
If you just ran `git status`, the next tip is likely Git-related:
```
🌿 Git: 'git add -p' - Stage changes interactively
🌿 Git: 'git diff --staged' - Show staged changes
```

### General Usage
When not in a specific context, shows balanced tips:
```
⌨️  Shortcut: Ctrl+R - Reverse search command history
🎯 Trick: Use && to chain commands (run if previous succeeds)
🐧 Linux: 'find . -type f -size +100M' - Find files larger than 100MB
```

## 🎨 Customization

### Add Your Own Tips
Edit `prompt_reminder.py` and add to any category:
```python
LINUX_TIPS = [
    "🐧 Linux: Your custom tip here",
    # ... existing tips
]
```

### Adjust Context Weights
Modify weighting in `get_weighted_reminder()`:
```python
if context['is_git_repo']:
    weights['git'] *= 5.0  # Show even more Git tips!
```

### Change Update Frequency
Edit daemon loop interval (default: 5 seconds):
```python
def daemon_loop():
    while True:
        update_reminder()
        time.sleep(3)  # Update every 3 seconds
```

## 📈 Future Enhancements

### Possible Additions
1. **GitHub Copilot API Integration** - AI-powered command suggestions
2. **Error Detection** - Detect failed commands and suggest fixes
3. **Learning Mode** - Track which tips you've acted on
4. **Category Filtering** - Show only Git tips, only shortcuts, etc.
5. **Multi-language Support** - Python, JavaScript, Go command suggestions
6. **Statistics Dashboard** - Track your command usage patterns
7. **Export/Import** - Share custom tip collections

## 🏆 Competition Advantages

1. **Practical & Educational** - Solves real problem (learning terminal)
2. **Smart Context Awareness** - Not just random tips
3. **Professional Implementation** - Clean code, proper architecture
4. **Extensible Design** - Easy to add features
5. **Real-world Usage** - Actually useful daily tool
6. **Technical Depth** - Demonstrates shell scripting, Python, daemon processes

## 📝 Project Statistics

- **200+ curated tips** across 6 categories
- **Context-aware weighting** for 4+ project types
- **Command history analysis** (last 20 commands)
- **5-second update cycle** for fresh suggestions
- **Zero-configuration** after initial setup
- **Cross-shell compatible** (Zsh primary, Bash supported)

## 🎓 Learning Value

Users learn:
- Terminal shortcuts they didn't know existed
- Git commands beyond the basics
- Linux system administration
- Shell scripting tricks and patterns
- Best practices for command-line productivity

---

**Built for the CLI Challenge 2026**
*Making terminal learning automatic, intelligent, and effortless*
