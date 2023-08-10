#!/bin/bash

# Check if Git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Installing..."
    sudo apt update
    sudo apt install -y git
fi

# Clone repository
#git clone https://github.com/GuinnessShep/GuinnessLikeBot
#cd GuinnessLikeBot

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    sudo apt update
    sudo apt install -y python3
fi

# Install required Python packages
python3 -m pip install console httpx pyyaml pystyle
python3 -m pip install -r bot/requirements.txt

# Run Python scripts
python3 bot/GenerateDevices.py 50000

# Ask if proxies should be used
read -p "Would you like to use proxies? (yes/no) " USE_PROXIES

if [[ "${USE_PROXIES}" = 'yes' ]]; then
    python3 proxy/scraper.py
    python3 proxy/pl.py
fi

python3 bot/Modern.py
