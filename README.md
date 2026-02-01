# Dynamic Terminal Prompt Reminder 🎯

A Python-based terminal enhancement that displays rotating tips, useful commands, system information, and GitHub Copilot tips **as ghost text** (like IDE autocomplete) after your cursor. Reminders auto-refresh every 5 seconds!

## Features ✨

- 👻 **Ghost Text Display**: Appears as grayed-out suggestion text after cursor (like IDE autocomplete)
- ⏱️ **Auto-Refresh**: Updates every 5 seconds automatically
- 🎲 **Random Reminders**: Continuously rotating tips and information
- 💻 **System Info**: Shows CPU, RAM, and disk usage
- 💡 **Command Tips**: Useful terminal shortcuts and commands
- 🐧 **Linux Tips**: Essential Linux command reminders
- 🤖 **GitHub Copilot Tips**: Maximize your Copilot usage
- 🌿 **Git Commands**: Quick git command references
- 🎨 **Subtle Design**: Light gray color that doesn't distract

## Requirements 📋

- **Zsh shell** (required for ghost text integration)
- Conda (Anaconda or Miniconda)
- The installation script will automatically create a dedicated conda environment

**Note**: This version uses Zsh's powerful line editor (ZLE) to display ghost text. Bash support may be added in future versions.

## Installation 🚀

### Quick Install (Recommended)

1. **Run the installation script**:
   ```bash
   chmod +x install_prompt.sh
   ./install_prompt.sh
   ```
   
   This will:
   - Create a dedicated conda environment named `prompt-reminder`
   - Install all required dependencies (Python 3.9 + psutil)
   - Configure your shell to use the reminder system

2. **Activate in your current session**:
   ```bash
   source ~/.bashrc   # For Bash
   # or
   source ~/.zshrc    # For Zsh
   ```

   Or simply open a new terminal window.

### Manual Install

If you prefer to set up the conda environment manually:

```bash
# Create conda environment
conda env create -f environment.yml

# Activate it
conda activate prompt-reminder

# Test the script
python prompt_reminder.py
```

Then follow the Quick Install steps above.

## Usage 📖

Once installed, you'll see reminders appear as **ghost text** (light gray) after your cursor as you type. The reminders automatically update every 5 seconds in the background!

The reminders rotate through:
- Keyboard shortcuts (Ctrl+R, Ctrl+L, etc.)
- Linux commands (df, grep, find, etc.)
- Git commands (status, log, diff, etc.)
- GitHub Copilot tips
- System resource usage (CPU, RAM, Disk)

### Example Visual

```
user@computer:~$ ls   💡 Tip: Use 'Ctrl+R' to search command history
                      ↑ Ghost text appears here in light gray
```

The daemon runs in the background and updates the suggestion every 5 seconds, so you'll continuously see new tips!

### Manual Control

```bash
reminder-start   # Start the background daemon
reminder-stop    # Stop the daemon
reminder-get     # Get current reminder
```

## Testing Without Installation 🧪

You can test the reminder system:

```bash
# Activate the conda environment
conda activate prompt-reminder

# Get a single reminder
python prompt_reminder.py get

# Run daemon in foreground (Ctrl+C to stop)
python prompt_reminder.py daemon

# Or start daemon in background
python prompt_reminder.py start

# Stop background daemon
python prompt_reminder.py stop
```

## Customization 🎨

Edit `prompt_reminder.py` to customize:

- **Add your own reminders**: Edit the lists at the top of the file
  - `USEFUL_COMMANDS`
  - `LINUX_TIPS`
  - `GITHUB_COPILOT_TIPS`
  - `GIT_COMMANDS`

- **Change colors**: Modify the `Colors` class

- **Adjust probability**: Change the 0.7 value in `get_random_reminder()` to control how often system info appears (currently 30%)

### Example: Adding Your Own Tip

```python
USEFUL_COMMANDS = [
    "💡 Tip: Use 'Ctrl+R' to search command history",
    "💡 Tip: Your custom tip here",  # Add this line
    # ... rest of the tips
]
```

## Uninstallation 🗑️

To remove the dynamic prompt reminder:

1. Restore your shell configuration backup:
   ```bash
   # Find your backup file
   ls ~/.bashrc.backup.*  # or ~/.zshrc.backup.*
   
   # Restore it
   cp ~/.bashrc.backup.YYYYMMDD_HHMMSS ~/.bashrc
   ```

2. Reload your shell:
   ```bash
   source ~/.bashrc  # or ~/.zshrc
   ```

Or manually remove the "Dynamic Prompt Reminder" section from your `.bashrc` or `.zshrc` file.

## Managing the Conda Environment 🐍

### List all conda environments
```bash
conda env list
```

### Activate the environment manually
```bash
conda activate prompt-reminder
```

### Update dependencies
```bash
conda activate prompt-reminder
conda env update -f environment.yml
```

### Remove the environment
```bash
conda env remove -n prompt-reminder
```

## Troubleshooting 🔧

### "Conda not found" error
Install Anaconda or Miniconda from:
- Anaconda: https://www.anaconda.com/download
- Miniconda: https://docs.conda.io/en/latest/miniconda.html

### "No module named 'psutil'" error
The conda environment should handle this automatically. If you still see this error:
```bash
conda activate prompt-reminder
pip install psutil
```

### Prompt appears twice
This might happen if you have multiple prompt commands. Check your shell config file for duplicate `PROMPT_COMMAND` or `precmd` definitions.

### Reminders not showing
1. Make sure the conda environment was created: `conda env list | grep prompt-reminder`
2. Check the path in your `.bashrc` or `.zshrc` is correct
3. Try running the script manually:
   ```bash
   conda activate prompt-reminder
   python /full/path/to/prompt_reminder.py
   ```

## How It Works 🔍

The system uses two components:

1. **Background Daemon**: A Python process that updates a cache file every 5 seconds with a new random reminder
2. **Zsh Integration**: Uses Zsh's line editor (ZLE) hooks to read the cache and display it as ghost text after your cursor

The ghost text is displayed with a light gray color and appears automatically as you type, giving you a continuous stream of helpful reminders without interrupting your workflow.

## Contributing 🤝

Feel free to add your own tips and reminders to make this even more useful!

## License 📄

Free to use and modify for your own purposes.

---

**Enjoy your enhanced terminal experience! 🎉**
