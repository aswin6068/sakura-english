# 🌸 Sakura - English Learning App with Anime Character

An immersive English learning experience featuring **Sakura**, an anime-style AI teacher who speaks to users in English while providing corrections and explanations in **Malayalam**.

![Version](https://img.shields.io/badge/version-1.0.0-pink)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- 🌸 **Anime Character Interface** - Beautiful, animated Sakura character
- 💬 **Natural Conversations** - Chat naturally in English
- 🇮🇳 **Malayalam Explanations** - Understand corrections in your native language
- 🎯 **6 Real Scenarios** - Cafe, Restaurant, Shopping, Travel, Office, General
- 📊 **Progress Tracking** - Track lessons, corrections, and improvements
- 🎤 **Voice Features** - Record your speech, hear correct pronunciation
- 🎨 **Beautiful UI** - Vibrant anime aesthetic with smooth animations
- 📱 **Responsive Design** - Works on desktop, tablet, and mobile

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Groq API key (get it from [console.groq.com](https://console.groq.com))

### Installation

1. **Clone/Download this folder**
   ```bash
   cd english_tutor_app
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example file
   cp .env.example .env
   
   # Edit .env and add your Groq API key
   nano .env  # or use any text editor
   ```
   
   Your `.env` file should look like:
   ```
   GROQ_API_KEY=gsk_your_actual_api_key_here
   GROQ_CHAT_MODEL=llama-3.3-70b-versatile
   GROQ_STT_MODEL=whisper-large-v3-turbo
   GROQ_TTS_MODEL=canopylabs/orpheus-v1-english
   GROQ_TTS_VOICE=troy
   ```

4. **Run the application**
   ```bash
   python main.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Open in your browser**
   ```
   http://localhost:8000/app
   ```

## 📁 Project Structure

```
english_tutor_app/
├── main.py                 # FastAPI backend server
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── .env                   # Your actual config (create this)
├── static/
│   └── index.html         # Anime UI frontend
└── README.md              # This file
```

## 🎯 How to Use

### 1. Choose Your Settings
- **Scenario**: Select from Cafe, Restaurant, Shopping, Travel, Office, or General
- **Level**: Pick Beginner, Intermediate, or Advanced
- **Voice**: Choose Troy, Hannah, or Austin for text-to-speech

### 2. Start Chatting
- **Type**: Write your English sentence in the text box
- **Speak**: Click "Record" to speak (uses Speech-to-Text)
- Press **Enter** to send (Shift+Enter for new line)

### 3. Learn from Feedback
Sakura will respond with:
- ✅ **Natural Reply** - Continues the conversation
- ✏️ **Correction** - Shows your mistake vs. correct version
- 📝 **Malayalam Explanation** - Explains what's wrong and how to fix
- 🔄 **Alternatives** - Two other ways to say the same thing
- 🎯 **Practice** - Exercise to reinforce learning

### 4. Listen & Practice
- Click **"Listen"** button to hear proper pronunciation
- Try the practice exercise
- Track your progress in Sakura's stats panel

## 🎨 Features in Detail

### Anime Character: Sakura 🌸
- **Personality**: Friendly, patient, encouraging
- **Mood States**: Ready, Listening, Thinking, Excited, Correcting
- **Stats Tracking**: 
  - 📚 Lessons Today
  - ✅ Corrections Made
  - 🎯 Current Scenario
  - ⭐ Your Level

### 6 Learning Scenarios
1. **☕ Cafe** - Order coffee, chat with baristas
2. **🍽️ Restaurant** - Order food, make reservations
3. **🛍️ Shopping** - Buy items, ask for prices
4. **✈️ Travel** - Ask directions, book tickets
5. **💼 Office** - Professional conversations
6. **💬 General** - Everyday conversations

### 3 Learning Levels
- 🌱 **Beginner** - Basic vocabulary, simple sentences
- 🌿 **Intermediate** - Complex sentences, more vocabulary
- 🌳 **Advanced** - Fluent conversation, nuanced expressions

## 🔧 API Endpoints

The backend provides these endpoints:

### Chat
```http
POST /chat
Content-Type: application/json

{
  "user_message": "I want to ordering coffee",
  "scenario": "cafe",
  "level": "beginner"
}
```

### Speech-to-Text
```http
POST /stt
Content-Type: multipart/form-data

audio: <audio file>
language: en
```

### Text-to-Speech
```http
POST /tts
Content-Type: application/json

{
  "text": "Hello, how are you?",
  "voice": "troy"
}
```

### Utility Endpoints
- `GET /` - Health check
- `GET /voices` - List available voices
- `GET /scenarios` - List scenarios
- `GET /levels` - List learning levels
- `GET /docs` - Interactive API documentation

## 💡 Example Interaction

```
User: "I want to ordering coffee"

Sakura: "Of course! I can help you with that. 
Let me show you the correct way to say it."

┌─────────────────────────────────────┐
│ ✏️ Correction                        │
│ ❌ I want to ordering coffee        │
│ ✅ I want to order coffee           │
│                                     │
│ Type: grammar                       │
│ പ്രശ്നം: 'want to' കഴിഞ്ഞ് base   │
│ form of verb വരണം (order)           │
│                                     │
│ 🔄 Alternatives:                    │
│ • I'd like to order a coffee        │
│ • Can I get a coffee, please?       │
│                                     │
│ 📝 Practice:                        │
│ How do you say: "I want to buy a    │
│ book"?                              │
│ Answer: I want to buy a book        │
└─────────────────────────────────────┘
```

## 🛠️ Troubleshooting

### Issue: "GROQ_API_KEY not found"
**Solution**: Make sure you created `.env` file with your API key
```bash
cp .env.example .env
# Edit .env and add your key
```

### Issue: Port 8000 already in use
**Solution**: Use a different port
```bash
uvicorn main:app --port 8001
```
Then open `http://localhost:8001/app`

### Issue: Microphone not working
**Solution**: 
- Allow microphone permissions in browser
- Use HTTPS in production (mic requires secure context)
- Try a different browser (Chrome recommended)

### Issue: TTS not working
**Solution**: 
- Check Groq TTS model availability
- Try different voice (troy, hannah, austin)
- Check audio is not muted

### Issue: CORS errors
**Solution**: Already configured to allow all origins in development. For production, edit `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Your domain
    ...
)
```

## 🎨 Customization

### Change Character Name
Edit `static/index.html`:
```javascript
// Line ~200
<h2 class="character-name">YourName</h2>
```

### Change Colors
Edit CSS variables in `static/index.html`:
```css
:root {
    --primary: #FF6B9D;     /* Pink */
    --secondary: #C651FF;   /* Purple */
    --accent: #FFD93D;      /* Yellow */
    /* Change to your preferred colors */
}
```

### Add New Scenarios
Edit `main.py`:
```python
@validator('scenario')
def validate_scenario(cls, v):
    allowed_scenarios = ["cafe", "restaurant", "shopping", 
                         "travel", "office", "general", 
                         "your_new_scenario"]  # Add here
```

### Change AI Personality
Edit `SYSTEM_PROMPT` in `main.py` to adjust Sakura's teaching style.

## 📱 Mobile Usage

The app is fully responsive and works on mobile devices:
- Touch-friendly buttons
- Responsive layout
- Mobile microphone support
- Swipe-friendly scrolling

## 🚀 Deployment

### Option 1: Local Network
```bash
python main.py
# Access from other devices: http://your-ip:8000/app
```

### Option 2: Cloud Deployment (Heroku, Railway, etc.)
1. Add `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```
2. Set environment variables in dashboard
3. Deploy!

### Option 3: Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security Notes

**For Production:**
- [ ] Change CORS settings to specific domains
- [ ] Add rate limiting
- [ ] Use HTTPS
- [ ] Add authentication if needed
- [ ] Set up proper logging
- [ ] Monitor API usage and costs

## 📊 Performance Tips

- Speech files are automatically cleaned up
- Audio recordings limited to 25MB
- Text-to-speech limited to 200 characters for best quality
- Responses cached where possible

## 🤝 Contributing

Found a bug or want to add a feature? Feel free to:
1. Report issues
2. Suggest improvements
3. Submit pull requests

## 📄 License

MIT License - Feel free to use and modify!

## 🙏 Credits

- **AI Models**: Groq (LLaMA, Whisper, Orpheus)
- **Fonts**: Google Fonts (Lexend, Fredoka)
- **Design**: Custom anime-inspired aesthetic

## 📞 Support

If you need help:
1. Check the troubleshooting section
2. Read the full guide in `ANIME_APP_GUIDE.md`
3. Check Groq documentation at [console.groq.com](https://console.groq.com)

## 🎉 What's Next?

Future enhancements:
- [ ] Multiple anime characters
- [ ] Conversation history
- [ ] Progress reports
- [ ] Gamification (points, badges)
- [ ] Custom scenarios
- [ ] Mobile app version

---

**Made with 💖 for Malayalam speakers learning English**

*Start chatting with Sakura and improve your English today! 🌸*

## Quick Test

After starting the app, try these:

1. Type: "I goes to market yesterday"
2. Click Record and say something in English
3. Click the "Listen" button on Sakura's response
4. Watch the stats panel update!

**Happy Learning! 🎓✨**
