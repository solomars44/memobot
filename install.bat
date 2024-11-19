@echo off
echo Installing MemoryBot dependencies...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or later.
    pause
    exit /b 1
)

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install Python dependencies
pip install -r requirements.txt

echo Installation complete!
pause