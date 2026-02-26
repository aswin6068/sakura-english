#!/bin/bash

echo "🌸 Sakura English Learning App - Setup Script"
echo "=============================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi
echo "✅ pip3 is available"
echo ""

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi
echo ""

# Setup .env file
if [ ! -f .env ]; then
    echo "📝 Setting up environment file..."
    cp .env.example .env
    echo "✅ Created .env file from template"
    echo ""
    echo "⚠️  IMPORTANT: You need to add your Groq API key to .env file"
    echo ""
    echo "Steps:"
    echo "1. Get your API key from: https://console.groq.com"
    echo "2. Open .env file in a text editor"
    echo "3. Replace 'your_groq_api_key_here' with your actual API key"
    echo ""
    read -p "Press Enter after you've added your API key..."
else
    echo "✅ .env file already exists"
fi
echo ""

# Check if API key is set
if grep -q "your_groq_api_key_here" .env; then
    echo "⚠️  Warning: API key still contains default value"
    echo "Please edit .env file and add your actual Groq API key"
    echo ""
fi

# Create static directory if it doesn't exist
if [ ! -d "static" ]; then
    mkdir -p static
    echo "✅ Created static directory"
fi

echo "✨ Setup complete!"
echo ""
echo "To start the app, run:"
echo "  python3 main.py"
echo ""
echo "Then open your browser to:"
echo "  http://localhost:8000/app"
echo ""
echo "Happy learning with Sakura! 🌸"
