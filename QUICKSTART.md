# 🚀 Quick Start Guide

Get your English Learning App running in 5 minutes!

## Step 1: Install Python Dependencies

```bash
cd english_tutor_app
pip install -r requirements.txt
```

**What this installs:**
- FastAPI - Web framework
- Uvicorn - Web server
- Groq - AI API client
- Pydantic - Data validation

## Step 2: Get Your Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Go to API Keys section
4. Create a new API key
5. Copy the key (starts with `gsk_...`)

## Step 3: Create .env File

```bash
# Copy the example
cp .env.example .env

# Edit with your API key
nano .env
# or
notepad .env
# or
code .env
```

Paste your API key:
```
GROQ_API_KEY=gsk_your_actual_key_here
```

Save and close!

## Step 4: Run the App

```bash
python main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Starting English Tutor API with Groq
INFO:     Chat Model: llama-3.3-70b-versatile
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 5: Open in Browser

Go to: **http://localhost:8000/app**

You should see Sakura! 🌸

## First Conversation

1. Select "Cafe" scenario
2. Choose "Beginner" level
3. Type: "I want to ordering coffee"
4. Click "Send"
5. Watch Sakura correct you! ✨

## Testing Voice Features

### Speech-to-Text (Record)
1. Click "🎤 Record" button
2. Allow microphone access
3. Say: "Hello, how are you?"
4. Click "⏹️ Stop"
5. Your text appears in the input box!

### Text-to-Speech (Listen)
1. After Sakura responds
2. Click "🔊 Listen" button
3. Hear the pronunciation!

## Common First-Time Issues

### ❌ "GROQ_API_KEY not found"
→ You forgot to create `.env` file or add the API key

### ❌ "Port 8000 already in use"
→ Run on different port: `uvicorn main:app --port 8001`

### ❌ "Cannot access microphone"
→ Allow microphone permissions in your browser

### ❌ "Module not found"
→ Install dependencies: `pip install -r requirements.txt`

## What's in the App?

```
english_tutor_app/
├── main.py              ← Backend API (FastAPI)
├── static/
│   └── index.html       ← Frontend UI (Anime interface)
├── requirements.txt     ← Python packages
├── .env.example         ← Template for config
└── README.md            ← Full documentation
```

## Key Files Explained

### main.py
The backend server that:
- Connects to Groq AI
- Handles chat, speech-to-text, text-to-speech
- Validates inputs
- Manages conversations

### static/index.html
The beautiful anime interface that:
- Shows Sakura character
- Displays chat messages
- Records audio
- Plays audio
- Tracks progress

### .env
Your secret configuration:
- API key
- Model settings
- Voice preferences

## Try These Commands

```bash
# Start server
python main.py

# Start with auto-reload (for development)
uvicorn main:app --reload

# Start on different port
uvicorn main:app --port 8001

# Check if server is running
curl http://localhost:8000/

# View API docs
# Go to: http://localhost:8000/docs
```

## Next Steps

1. ✅ Run the app
2. ✅ Have your first conversation
3. ✅ Try voice features
4. 📖 Read full README.md for advanced features
5. 🎨 Customize colors and characters
6. 🚀 Deploy to production

## Need Help?

Check these files:
- `README.md` - Complete documentation
- `ANIME_APP_GUIDE.md` - Design and concept details
- Groq Docs: [console.groq.com/docs](https://console.groq.com/docs)

## Example API Test

Test the backend directly:

```bash
# Test health check
curl http://localhost:8000/

# Test chat (with jq for pretty output)
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_message": "I want coffee",
    "scenario": "cafe",
    "level": "beginner"
  }' | jq
```

## System Requirements

- **Python**: 3.9 or higher
- **RAM**: 2GB minimum
- **Internet**: Required for Groq API
- **Browser**: Chrome, Firefox, Safari, Edge (modern versions)

## Supported Platforms

- ✅ Windows
- ✅ macOS
- ✅ Linux
- ✅ Cloud servers (AWS, Azure, GCP, etc.)

---

**That's it! You're ready to learn English with Sakura! 🌸**

Happy learning! 🎉
