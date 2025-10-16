# Voice Assistant for n8n

Ultra-low latency voice assistant integrated with n8n workflows.

## Features

- **Voice Input**: Wyoming protocol satellite support
- **Fast Transcription**: Faster-Whisper (CPU optimized)
- **Smart Intent Routing**: Cached patterns + LLM classification
- **n8n Integration**: Webhook-based tool execution
- **Local AI**: Ollama models (llama3.2, qwen2.5)
- **Low Latency**: 500-800ms response time

## Architecture

```
Windows 11 Host
├─ Ollama (Native, Port 11434)
│  └─ Models: llama3.2:1b, llama3.2:3b, qwen2.5:7b
└─ WSL2 (Ubuntu 22.04)
   ├─ Voice Assistant Service (Python)
   │  ├─ Wyoming Protocol Server (Port 10300)
   │  ├─ Faster-Whisper (CPU optimized)
   │  ├─ Intent Classification
   │  └─ Piper TTS
   ├─ Docker: n8n (Port 5678)
   └─ Raspberry Pi Satellite (Wyoming client)
      ├─ Microphone input
      └─ Speaker output
```

## Installation

See `docs/INSTALLATION.md` for complete setup instructions.

**Quick Install:**
```bash
cd /mnt/c/Users/paulm/OneDrive/Desktop/Projects/Bots/n8n/voice-assistant
chmod +x scripts/install.sh
./scripts/install.sh
```

## Quick Test

```bash
source venv/bin/activate
python voice_service.py test
```

## Documentation

- **[docs/INSTALLATION.md](docs/INSTALLATION.md)** - Complete installation guide
- **[docs/N8N_INTEGRATION.md](docs/N8N_INTEGRATION.md)** - n8n webhook setup
- **[docs/RASPBERRY_PI.md](docs/RASPBERRY_PI.md)** - RPi satellite guide
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System architecture

## Configuration

- `.env` - Environment variables (created during installation)
- `config/config.yaml` - Service configuration
- `requirements.txt` - Python dependencies

## Performance Targets

| Component | Latency |
|-----------|---------|
| Transcription | 150-200ms |
| Intent Classification | 50-100ms |
| Home Assistant Agent | 150-250ms |
| Conversation Agent | 300-500ms |
| TTS (Piper) | 100-150ms |
| **Total (Home Control)** | **500-800ms** |

## Project Structure

```
voice-assistant/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── voice_service.py         # Main service
├── config/
│   └── config.yaml          # Service configuration
├── scripts/
│   ├── install.sh          # Installation script
│   └── setup_ollama.ps1    # Windows Ollama setup
├── models/                 # AI models (auto-downloaded)
├── logs/                   # Service logs
└── docs/                   # Documentation
    ├── INSTALLATION.md
    ├── N8N_INTEGRATION.md
    ├── RASPBERRY_PI.md
    ├── TROUBLESHOOTING.md
    └── ARCHITECTURE.md
```

## License

MIT License - Use freely!
