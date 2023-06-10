#!/bin/bash

# Check if Homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Installing Python 3..."
    brew install python
fi

# Install Python packages
echo "Installing Python packages..."
python3 -m pip install console httpx pyyaml pystyle

# Install requirements from requirements.txt
echo "Installing requirements..."
python3 -m pip install -r requirements.txt

# Run Python scripts
echo "Running Python scripts..."
python3 GenerateDevices.py 50000
python3 scraper.py
python3 pl.py
python3 GuinnessBot.py
