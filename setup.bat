@echo off
echo ========================================
echo 🌸 Sakura English Learning App - Setup
echo ========================================
echo.

REM Check Python installation
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from python.org
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Found Python %PYTHON_VERSION%
echo.

REM Check pip
echo Checking pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip is not installed
    pause
    exit /b 1
)
echo ✅ pip is available
echo.

REM Install dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)
echo ✅ Dependencies installed successfully
echo.

REM Setup .env file
if not exist .env (
    echo 📝 Setting up environment file...
    copy .env.example .env
    echo ✅ Created .env file from template
    echo.
    echo ⚠️  IMPORTANT: You need to add your Groq API key to .env file
    echo.
    echo Steps:
    echo 1. Get your API key from: https://console.groq.com
    echo 2. Open .env file in Notepad
    echo 3. Replace 'your_groq_api_key_here' with your actual API key
    echo.
    pause
) else (
    echo ✅ .env file already exists
)
echo.

REM Create static directory
if not exist static (
    mkdir static
    echo ✅ Created static directory
)

echo ✨ Setup complete!
echo.
echo To start the app, run:
echo   python main.py
echo.
echo Then open your browser to:
echo   http://localhost:8000/app
echo.
echo Happy learning with Sakura! 🌸
echo.
pause
