# Simple Voice Satellite (Pi Simulator)

This is a lightweight voice chat interface that simulates a Raspberry Pi voice satellite.

## 🎯 What It Does

- **Audio Input**: Uses browser speech recognition (microphone)
- **Audio Output**: Uses browser text-to-speech (speaker)
- **All Processing**: Done remotely on your n8n server at `192.168.0.244:32768`
- **No Local AI**: No Ollama, Whisper, or other models needed locally

## 🚀 Quick Start

1. **Start the server**:
   ```bash
   python simple_server.py
   ```
   
   Or double-click: `start_simple.bat`

2. **Open in browser**:
   - Go to: http://localhost:5000
   - **Use Chrome, Edge, or Safari** (for speech recognition support)

3. **Use it**:
   - Click the microphone button 🎤
   - Speak your question
   - Wait for n8n to process
   - Listen to the spoken response 🔊

## 📋 Requirements

Only minimal Python packages needed:
```bash
pip install flask flask-cors requests python-dotenv
```

## ⚙️ Configuration

The n8n webhook URL is set in your `.env` file:
```
N8N_WEBHOOK_URL=http://192.168.0.244:32768/webhook/voice-assistant
```

## 🎙️ How It Works

```
Browser (You) → Speech Recognition → Flask Server → n8n (Remote)
                                                         ↓
Browser (You) ← Text-to-Speech ← Flask Server ← Response
```

**Simulates Raspberry Pi Satellite**:
- Input: Microphone → Speech-to-Text (browser)
- Processing: All done on remote n8n
- Output: Text-to-Speech (browser) → Speaker

## ✅ Features

- ✓ Voice input (browser speech recognition)
- ✓ Voice output (browser text-to-speech)
- ✓ Full conversation history
- ✓ Real-time status updates
- ✓ Connection testing
- ✓ No local AI models needed
- ✓ Lightweight and fast

## 🔧 Troubleshooting

**No speech recognition?**
- Use Chrome, Edge, or Safari (Firefox doesn't support it yet)
- Allow microphone permissions when prompted

**Cannot connect to n8n?**
- Check n8n is running at `http://192.168.0.244:32768`
- Verify webhook endpoint: `/webhook/voice-assistant`
- Click "Test Connection" button in the interface

**No voice output?**
- Check browser supports Web Speech API
- Check system volume is up
- Try clicking "Stop Speaking" and retry
