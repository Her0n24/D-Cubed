#!/bin/bash
# Installation script for Dynamic Prompt Reminder

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PYTHON_SCRIPT="$SCRIPT_DIR/prompt_reminder.py"
CONDA_ENV_NAME="prompt-reminder"

echo "🚀 Installing Dynamic Prompt Reminder..."

# Check if conda is available
if ! command -v conda &> /dev/null; then
    echo "❌ Conda not found. Please install Anaconda or Miniconda first."
    exit 1
fi

# Create conda environment if it doesn't exist
if ! conda env list | grep -q "^${CONDA_ENV_NAME} "; then
    echo "📦 Creating conda environment: $CONDA_ENV_NAME"
    conda env create -f "$SCRIPT_DIR/environment.yml"
    echo "✅ Conda environment created"
else
    echo "✅ Conda environment '$CONDA_ENV_NAME' already exists"
fi

# Get the path to the conda environment's Python
CONDA_PREFIX=$(conda info --base)
source "$CONDA_PREFIX/etc/profile.d/conda.sh" 2>/dev/null
conda activate "$CONDA_ENV_NAME"
CONDA_PYTHON=$(which python)
conda deactivate

echo "🐍 Using Python from conda env: $CONDA_PYTHON"

# Make Python script executable
chmod +x "$PYTHON_SCRIPT"

# Detect shell
SHELL_NAME=$(basename "$SHELL")
if [[ "$SHELL_NAME" == "bash" ]] || [[ -n "$BASH_VERSION" ]]; then
    SHELL_CONFIG="$HOME/.bash_profile"
    INTEGRATION_FILE="$SCRIPT_DIR/bash_integration.sh"
    SHELL_TYPE="Bash"
    
    # macOS uses .bash_profile, create if doesn't exist
    touch "$SHELL_CONFIG"
elif [[ "$SHELL_NAME" == "zsh" ]] || [[ -n "$ZSH_VERSION" ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    INTEGRATION_FILE="$SCRIPT_DIR/zsh_integration.zsh"
    SHELL_TYPE="Zsh"
else
    echo "⚠️  Unknown shell: $SHELL_NAME"
    echo "Please manually source the integration file."
    exit 1
fi

echo "📝 Detected $SHELL_TYPE shell"
echo "📁 Config file: $SHELL_CONFIG"

# Create backup if config exists and has content
if [[ -f "$SHELL_CONFIG" ]] && [[ -s "$SHELL_CONFIG" ]]; then
    cp "$SHELL_CONFIG" "${SHELL_CONFIG}.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Created backup of $SHELL_CONFIG"
fi

# Check if already installed
if grep -q "Dynamic Prompt Reminder" "$SHELL_CONFIG" 2>/dev/null; then
    echo "⚠️  Already installed. Updating configuration..."
    # Remove old configuration
    sed -i.bak '/# Dynamic Prompt Reminder/,/^$/d' "$SHELL_CONFIG"
fi

# Add configuration
cat >> "$SHELL_CONFIG" << EOF

# ========================================
# Dynamic Prompt Reminder
# Added on $(date)
# ========================================

# Source the integration
if [[ -f "$INTEGRATION_FILE" ]]; then
    source "$INTEGRATION_FILE"
fi

EOF

echo "✅ Added configuration to $SHELL_CONFIG"
echo ""
echo "🎉 Installation complete!"
echo ""
echo "To activate, run:"
echo "  source $SHELL_CONFIG"
echo ""
echo "Or simply open a new terminal window."
echo ""
echo "To uninstall, restore your backup:"
echo "  cp ${SHELL_CONFIG}.backup.* $SHELL_CONFIG"
