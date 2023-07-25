#!/bin/bash
# Check if Homebrew is installed
if ! command -v brew &>/dev/null; then
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi
# Check if Git is installed
if ! command -v git &>/dev/null; then
    echo "Installing Git..."
    brew install git
fi
# Clone repository
echo "Cloning repository..."
git clone https://github.com/GuinnessShep/GuinnessLikeBot
cd GuinnessLikeBot
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
# Ask for proxy usage
read -p "Do you want to use proxies? [y/n] " use_proxies
# Run Python scripts
echo "Running Python scripts..."
python3 bot/GenerateDevices.py 50000
if [[ $use_proxies == "y" || $use_proxies == "Y" ]]; then
    python3 proxy/scraper.py
    python3 proxy/pl.py
fi
python3 bot/GuinnessBot.py
