#!/bin/bash
# Dukan EXE Builder for Linux/Mac
# This script compiles the Python backend into a standalone executable
#
# NOTE: This EXE is for LOCAL TESTING ONLY with ngrok
# For production, deploy to a cloud server (Render, Railway, etc.)

echo "==========================================="
echo "  DUKAN - EXE Builder"
echo "==========================================="
echo ""

# Check if Python is installed
echo "[1/5] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python is not installed!"
    echo "Please install Python 3.10+ from https://python.org"
    exit 1
fi
echo "Python found: $(python3 --version)"
echo ""

# Install pyinstaller
echo "[2/5] Installing PyInstaller..."
pip3 install pyinstaller --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install pyinstaller"
    exit 1
fi
echo ""

# Install dependencies
echo "[3/5] Installing dependencies..."
pip3 install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo ""

# Initialize database
echo "[4/5] Initializing database..."
python3 main.py --init-db
if [ $? -ne 0 ]; then
    echo "WARNING: Database initialization may have failed"
fi
echo ""

# Build EXE
echo "[5/5] Building executable (this may take a few minutes)..."
echo ""

if [ "$(uname)" == "Darwin" ]; then
    # Mac
    pyinstaller --onefile --windowed --name DukanBot main.py
else
    # Linux
    pyinstaller --onefile --name DukanBot main.py
fi

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to build executable"
    exit 1
fi

echo ""
echo "==========================================="
echo "  SUCCESS! Executable created in dist/DukanBot"
echo "==========================================="
echo ""
echo "IMPORTANT NOTES:"
echo "1. This executable is for LOCAL TESTING ONLY"
echo "2. You MUST run ngrok to expose it to the internet"
echo "3. For production, deploy to a cloud server"
echo ""
echo "To run:"
echo "  1. Start ngrok: ngrok http 8000"
echo "  2. Set WEBHOOK_URL in .env to your ngrok URL"
echo "  3. Run: ./dist/DukanBot"
echo ""
echo "For production deployment, see CLOUD_DEPLOY.md"
echo ""
