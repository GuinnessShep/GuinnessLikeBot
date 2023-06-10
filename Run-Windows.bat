@echo off

REM Check if Python 3 is installed
python --version 2>NUL
if %errorlevel% neq 0 (
    echo Python 3 is not installed. Installing Python 3...
    
    REM Download Python 3 installer
    powershell -command "(New-Object System.Net.WebClient).DownloadFile('https://www.python.org/ftp/python/3.9.7/python-3.9.7-amd64.exe', 'python-3.9.7-amd64.exe')"
    
    REM Install Python 3
    python-3.9.7-amd64.exe /quiet PrependPath=1

    REM Delete the installer
    del python-3.9.7-amd64.exe

    echo Python 3 installed successfully.
)

REM Install required Python packages
python -m pip install console httpx pyyaml pystyle

REM Install packages from requirements.txt
python -m pip install -r requirements.txt

REM Run the Python scripts
python GenerateDevices.py 50000
python scraper.py
python pl.py
python GuinnessBot.py

REM Pause the script to keep the console window open
pause
