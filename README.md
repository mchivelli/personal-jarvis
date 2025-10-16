# Personal Jarvis - AI Voice Assistant

A complete voice assistant system powered by Whisper, Ollama, and n8n for natural conversation and task automation.

## 🚀 Features

- **Voice Input**: Whisper AI transcription (faster-whisper)
- **Natural Conversation**: Ollama LLM (qwen2.5:3b)
- **Task Automation**: n8n workflows for emails, calendar, contacts
- **Intent Classification**: Smart routing (conversation vs. tools)
- **Web Testing**: Browser-based interface for easy testing
- **Modular Design**: Easy to extend with new tools

## 📋 Components

### 1. Voice Assistant Service (`voice-assistant/`)
Python service handling:
- Audio transcription (Whisper)
- Intent classification
- n8n webhook integration
- Wyoming protocol support (for Raspberry Pi satellites)

### 2. n8n Workflows
- **Assistant Agent** - Main workflow with AI agent
- **Email Agent** - Email management
- **Calendar Agent** - Calendar operations  
- **Contact Agent** - Contact lookup
- **Content Creator Agent** - Content generation

### 3. Web Test Interface (`voice-assistant/web_test/`)
Browser-based testing without Raspberry Pi:
- Record audio directly in browser
- Real-time transcription
- Live n8n integration
- Works on Windows (no RDP issues!)

## 🛠️ Quick Start

### Prerequisites

- **Python 3.10+**
- **n8n** (Docker or standalone)
- **Ollama** with `qwen2.5:3b` model
- **FFmpeg** (for audio conversion)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/mchivelli/personal-jarvis.git
cd personal-jarvis
```

2. **Configure environment**
```bash
cd voice-assistant
cp .env.example .env
# Edit .env with your n8n server address
nano .env
```

**Important**: Update `N8N_WEBHOOK_URL` in `.env`:
```bash
# Local n8n
N8N_WEBHOOK_URL=http://localhost:5678/webhook/voice-assistant

# Docker/WSL n8n
N8N_WEBHOOK_URL=http://172.22.32.1:32768/webhook/voice-assistant

# Remote n8n server
N8N_WEBHOOK_URL=http://YOUR_SERVER_IP:PORT/webhook/voice-assistant
```

3. **Install Python dependencies**

**On Linux/WSL:**
```bash
cd voice-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**On Windows:**
```powershell
cd voice-assistant
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

4. **Import n8n workflows**
- Open n8n UI
- Import `Assistant Agent.json` from the repository root
- Import other agent workflows (Email, Calendar, Contact, Content Creator)
- **Activate** the "Assistant Agent" workflow

5. **Pull Ollama model**
```bash
ollama pull qwen2.5:3b
```

## 🎤 Testing with Web Interface

**Easy way to test without Raspberry Pi!**

### On Windows (Recommended for best audio quality)

```powershell
cd voice-assistant\web_test
python server_windows.py
```

Then open **http://localhost:5000** in your browser.

### On Linux/WSL

```bash
cd voice-assistant/web_test
python server.py
```

**Note**: Remote Desktop audio may not work well. Use Windows native version or access from another device.

## 🔧 Configuration

### n8n Webhook Connection

The voice assistant connects to n8n via webhook. Make sure:

1. **n8n is running** and accessible
2. **Workflow is active** (toggle in n8n UI)
3. **Webhook URL is correct** in `.env`

Test the webhook:
```bash
curl -X POST http://YOUR_N8N_URL/webhook/voice-assistant \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello","intent":"CONVERSATION","source":"test"}'
```

Expected response: `{"message":"Workflow was started"}`

### Remote n8n Server

To connect to a remote n8n server:

1. **Find your n8n server's IP/domain**
2. **Update `.env`**:
```bash
N8N_WEBHOOK_URL=http://YOUR_SERVER_IP:5678/webhook/voice-assistant
```
3. **Ensure firewall allows** connections to n8n port
4. **Test connection** with curl command above

## 📁 Project Structure

```
personal-jarvis/
├── voice-assistant/           # Voice assistant service
│   ├── config/               # Configuration files
│   ├── web_test/             # Browser-based testing
│   │   ├── index.html        # Web UI
│   │   ├── server.py         # Linux/WSL server
│   │   ├── server_windows.py # Windows server
│   │   └── start_windows.bat # Quick start for Windows
│   ├── docs/                 # Documentation
│   ├── requirements.txt      # Python dependencies
│   ├── .env.example          # Environment template
│   └── README.md             # Detailed docs
├── Assistant Agent.json      # Main n8n workflow
└── README.md                 # This file
```

## 🎯 Usage

### Test Conversation

1. Start web server (see Testing section above)
2. Open http://localhost:5000
3. Click microphone button
4. Say: *"Hello, how are you today?"*
5. See transcription and AI response

### Test Tools

Try these commands:
- **Math**: "What is 25 times 47?"
- **Web Search**: "What's happening in the world?" (requires Tavily API)
- **Email**: "Send an email to John" (requires Email Agent setup)

## 🐛 Troubleshooting

### Audio not being captured
- **Use Windows native version** (not via RDP)
- **Check microphone permissions** in browser
- **Speak for 2+ seconds** clearly
- **Try different browser** (Chrome/Firefox work best)

### n8n webhook not responding
- **Check workflow is active** (toggle in n8n UI)
- **Verify URL** in `.env` matches your n8n instance
- **Test with curl** command above
- **Check firewall** if using remote server

### Whisper transcription fails
- **Model will download** on first run (be patient)
- **Check disk space** (models are ~150MB)
- **Try smaller model** in `.env`: `WHISPER_MODEL=tiny.en`

### "You" as transcript
- **Audio quality is poor** (common with RDP)
- **Record for longer** (3+ seconds minimum)
- **Speak louder** and closer to mic
- **Use local machine** not remote desktop

## 🔮 Future Enhancements

- [ ] Raspberry Pi satellite setup guide
- [ ] Home Assistant integration
- [ ] Multi-language support
- [ ] Wake word detection
- [ ] Voice profiles/recognition
- [ ] Mobile app interface

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions welcome! Please open an issue or PR.

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Built with ❤️ using Whisper, Ollama, and n8n**
