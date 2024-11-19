@echo off
echo Starting Ollama MemoryBot...

:: Activate virtual environment
call venv\Scripts\activate

:: Enhanced Ollama check with retry mechanism
echo Checking Ollama connection...
:RETRY
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo Ollama is not running! Please start Ollama first.
    echo Retrying in 5 seconds...
    timeout /t 5 >nul
    goto RETRY
)
echo Ollama connection confirmed!

:: Kill any existing processes on port 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr ":8000"') do taskkill /F /PID %%a 2>nul

:: Start the FastAPI server
python -m uvicorn main:app --host 127.0.0.1 --port 8000

pause