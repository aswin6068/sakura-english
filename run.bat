@echo off
echo 🌸 Starting Sakura English Learning App...
echo.

REM Check if .env exists
if not exist .env (
    echo ❌ .env file not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if API key is configured
findstr /C:"your_groq_api_key_here" .env >nul
if %errorlevel% equ 0 (
    echo ❌ API key not configured!
    echo Please edit .env file and add your Groq API key
    pause
    exit /b 1
)

echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
echo 🌐 Open your browser to: http://localhost:8000/app
echo.

python main.py
