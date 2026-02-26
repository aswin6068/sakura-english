#!/bin/bash

echo "🌸 Starting Sakura English Learning App..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if API key is set
if grep -q "your_groq_api_key_here" .env; then
    echo "❌ API key not configured!"
    echo "Please edit .env file and add your Groq API key"
    exit 1
fi

# Start the server
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""
echo "🌐 Open your browser to: http://localhost:8000/app"
echo ""

python3 main.py
