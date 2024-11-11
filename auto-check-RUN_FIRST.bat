@echo off
echo Checking for pip installation...

REM Try to get pip version, suppress output
pip --version >nul 2>&1

REM If pip is not found, error level will be 1
if %errorlevel% neq 0 (
    echo Pip is not installed on this system.
    echo Opening Python 3.11 download page...
    start "" "https://www.python.org/downloads/release/python-3110/"
    pause
    exit /b
)

echo Pip is installed. Proceeding with package installation...

pip install kivy
pip install arabic-reshaper
pip install python-bidi
pip install sympy
pip install numpy
pip install matplotlib

echo All packages have been installed!
pause
