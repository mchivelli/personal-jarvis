# Voice Assistant Web Test Interface

A simple web interface to test your voice assistant without a Raspberry Pi.

## Features

- 🎤 **Record audio** directly from your browser
- 🗣️ **Transcription** using Faster-Whisper
- 🤖 **AI Response** from your n8n workflow
- 🔊 **Text-to-Speech** playback with Piper

## Quick Start

### 1. Install Dependencies

```bash
cd /mnt/c/Users/paulm/OneDrive/Desktop/Projects/Bots/n8n/voice-assistant
source venv/bin/activate
pip install flask flask-cors
```

### 2. Start the Server

```bash
cd web_test
python server.py
```

### 3. Open in Browser

Open **http://localhost:5000** in your browser (Chrome or Firefox recommended)

### 4. Test It!

1. Click the microphone button
2. Speak your question
3. Click again to stop recording
4. Watch the transcription and response appear
5. Click "Play Response" to hear the TTS audio

## How It Works

```
Browser (Mic) 
    ↓ (Audio Recording)
Flask Server
    ↓ (Faster-Whisper)
Transcription
    ↓ (HTTP POST)
n8n Webhook
    ↓ (Ultimate Assistant)
AI Response
    ↓ (Piper TTS)
Audio Output
    ↓ (Base64)
Browser (Speaker)
```

## Troubleshooting

### "Could not access microphone"
- Allow microphone permissions in your browser
- Check browser security settings
- Try using HTTPS or localhost

### "TTS not working"
- Ensure Piper is installed: `pip install piper-tts`
- Check `PIPER_MODEL_PATH` in `.env`
- Audio playback still works without TTS

### "n8n not responding"
- Make sure your n8n workflow is **active**
- Check `N8N_WEBHOOK_URL` in `.env`
- Verify port 32768 (or your n8n port)

## Configuration

The server uses your existing `.env` file:
- `WHISPER_MODEL` - Whisper model size
- `PIPER_MODEL_PATH` - Path to Piper TTS model
- `N8N_WEBHOOK_URL` - Your n8n webhook endpoint

## Next Steps

Once this works, you can:
1. Set up the Raspberry Pi satellite (see `../docs/RASPBERRY_PI.md`)
2. Run the full voice service (`../voice_service.py`)
3. Deploy to production

Enjoy testing! 🎉
