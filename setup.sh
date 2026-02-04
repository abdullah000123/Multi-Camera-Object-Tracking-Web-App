#!/bin/bash

set -e

echo "🚀 Starting setup..."

# -----------------------------
# 1. Check Homebrew
# -----------------------------
if ! command -v brew &> /dev/null; then
    echo "🍺 Homebrew not found. Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# -----------------------------
# 2. Check Python 3.11 or 3.12
# -----------------------------
PYTHON_BIN=""

if command -v python3.12 &> /dev/null; then
    PYTHON_BIN=python3.12
elif command -v python3.11 &> /dev/null; then
    PYTHON_BIN=python3.11
else
    echo "🐍 Python 3.11/3.12 not found. Installing Python 3.11..."
    brew install python@3.11
    PYTHON_BIN=python3.11
fi

echo "✅ Using $($PYTHON_BIN --version)"

# -----------------------------
# 3. Create virtual environment
# -----------------------------
if [ -d "venv" ]; then
    echo "⚠️ venv already exists. Using existing environment."
else
    echo "📦 Creating virtual environment..."
    $PYTHON_BIN -m venv venv
fi

# Activate venv
source venv/bin/activate

# -----------------------------
# 4. Upgrade pip
# -----------------------------
pip install --upgrade pip setuptools wheel

# -----------------------------
# 5. Install PyTorch (macOS CPU/MPS)
# -----------------------------
echo "🔥 Installing PyTorch..."
pip install torch torchvision torchaudio

# -----------------------------
# 6. Install dependencies (Flask pinned)
# -----------------------------
echo "📚 Installing Ultralytics and Flask 3.0.0..."
pip install ultralytics
pip install flask==3.0.0

# -----------------------------
# 7. Run the app
# -----------------------------
echo "✅ Setup complete!"
echo "▶️ Starting app.py..."
echo "🌐 Open the IP address shown below in your browser"

python app.py
