# D3 (Dynamic Discovery Daemon) -- Dynamic Terminal Prompt Reminder 

A context-aware terminal learning assistant that intelligently suggests commands and tips based on your project type and command history. Now enhanced with **GitHub Copilot AI integration** for dynamic, context-aware suggestions!

## Features 

- 🎲 **Context Awareness**: Smart tips based on current directory, project type, and recent commands
- 🤖 **AI-Powered**: GitHub Copilot CLI integration for dynamic command suggestions (optional)
- 💡 **Command Tips**: Useful terminal shortcuts and commands
- 🐧 **Linux Tips**: Essential Linux command reminders
- 🌿 **Git Commands**: Quick git command references
- ⌨️  **Terminal Tricks**: Productivity shortcuts and advanced techniques

## Requirements 

- **Zsh shell** (required for status line/ above prompt integration)
- Conda (Anaconda or Miniconda)
- The installation script will automatically create a dedicated conda environment

- **iTerm2** (recommended for status bar integration. See Iterm2 Setup)

## GitHub Copilot Integration (Optional)

For AI-powered, context-aware command suggestions:

1. **Install GitHub CLI** (if not already installed):
   ```bash
   brew install gh
   ```

2. **Authenticate with GitHub**:
   ```bash
   gh auth login
   ```

3. **Install Copilot CLI extension**:
   ```bash
   gh extension install github/gh-copilot
   ```

**No Copilot?** The system works with 200+ curated tips without it!

## iTerm2 Status Bar Setup (Recommended) 

For the best experience on macOS with iTerm2, follow these steps to display tips in a fixed status bar:

### Step-by-Step Guide:

1. **Open iTerm2 Preferences**
   - Press `⌘,` (Command + Comma) 
   - Or go to `iTerm2 → Preferences` from menu

2. **Navigate to Profiles**
   - Click on the **Profiles** tab at the top
   - Select your current profile (usually "Default")

3. **Go to Session Settings**
   - Click on the **Session** tab in the profile settings

4. **Enable Status Bar**
   - Scroll down to find **Status bar enabled**
   - Check the box ☑️ to enable it

5. **Configure Status Bar**
   - Click the **Configure Status Bar** button
   - A configuration window will open showing:
     - Available components (left side)
     - Active components (bottom)

6. **Add Interpolated String Component**
   - Find **"Interpolated String"** in the available components list
   - Drag it to the active components area at the bottom
   - Position it where you want (left, center, or right)

7. **Configure the Component**
   - Double-click the **Interpolated String** component you just added
   - In the "String Value" field, enter exactly:
     ```
     \(user.reminder)
     ```
   - **Important**: Include the backslash before the opening parenthesis
   - Optionally adjust:
     - **Max Width**: 80-100 characters (to prevent truncation)
     - **Font**: Match your terminal font

8. **Adjust Status Bar Position (Optional)**
   - At the bottom of Configure Status Bar window:
     - Choose **Top** or **Bottom** for status bar position
     - Adjust background color/transparency if desired

9. **Save and Close**
   - Click **OK** to close the Configure Status Bar window
   - Click **OK** again to close Preferences

10. **Verify It's Working**
    - You should now see tips appearing in your status bar
    - Tips will update every 5 seconds automatically
    - Try entering a Git repository to see context-aware Git tips!

### Troubleshooting iTerm2 Setup:

**Not seeing tips?**
- Make sure you entered `\(user.reminder)` exactly (backslash before parenthesis)
- Check daemon is running: `ps aux | grep prompt_reminder`
- Restart daemon: `reminder-start`
- Reload shell: `source ~/.zshrc`

**Tips cut off?**
- Increase Max Width in the Interpolated String settings
- Use a smaller font size for status bar
- Position the component where there's more space

**Status bar not showing?**
- Make sure "Status bar enabled" checkbox is checked
- Try restarting iTerm2
- Check you're editing the correct profile


## Installation 

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

## Usage 

Once installed, you'll see reminders above prompt. The reminders automatically update every 5 seconds in the background.

The reminders rotate through:
- Keyboard shortcuts (Ctrl+R, Ctrl+L, etc.)
- Linux commands (df, grep, find, etc.)
- Git commands (status, log, diff, etc.)
- GitHub Copilot tips

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

## Uninstallation 

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


## License 

Free to use and modify for your own purposes.

