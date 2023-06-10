#!/bin/bash

# Check if Python 3 is installed
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3
fi

# Install required Python packages
python3 -m pip install console httpx pyyaml pystyle
python3 -m pip install -r requirements.txt

# Run Python scripts
python3 GenerateDevices.py 50000
python3 scraper.py
python3 pl.py
python3 GuinnessBot.py
