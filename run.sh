#!/bin/bash
# Quick launcher for Backlight
cd "$(dirname "$(readlink -f "$0")")" || exit

# Check if venv exists, create if not
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install requirements if needed
pip install -q -r requirements.txt

# Run the application
exec python3 backlight.py
