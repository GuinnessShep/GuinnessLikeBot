@echo off

REM Check if Chocolatey is installed
choco -v 2>NUL
if %errorlevel% neq 0 (
    echo Chocolatey is not installed. Installing Chocolatey...

    REM Download and install Chocolatey
    @powershell -NoProfile -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin

    echo Chocolatey installed successfully.
)

REM Check if Git is installed
git --version 2>NUL
if %errorlevel% neq 0 (
    echo Git is not installed. Installing Git...
    
    REM Install Git
    choco install git -y

    echo Git installed successfully.
)

REM Clone Git repository
git clone https://github.com/GuinnessShep/GuinnessLikeBot
cd GuinnessLikeBot

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
python bot/GenerateDevices.py 50000

SET /P USEPROXIES="Would you like to use proxies? (Y/N) "
IF /I "%USEPROXIES%" NEQ "N" (
    python proxy/scraper.py
    python proxy/pl.py
)

python bot/GuinnessBot.py

REM Pause the script to keep the console window open
pause
