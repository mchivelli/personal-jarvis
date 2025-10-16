# System Architecture

## Components

### 1. Voice Service (WSL2 Python)
- Wyoming protocol server (Port 10300)
- Faster-Whisper transcription (CPU optimized)
- Intent classification (cached + LLM)
- Response generation
- Piper TTS

### 2. Ollama (Windows Native)
- llama3.2:1b - Intent classifier (50-100ms)
- llama3.2:3b - Home Assistant (150-250ms)
- qwen2.5:7b - Conversation (300-500ms)

### 3. n8n (Docker)
- Tool execution workflows
- Ultimate Assistant agent
- Email/Calendar/Contact agents

### 4. RPi Satellite (Optional)
- Wyoming client
- Microphone input
- Speaker output

## Data Flow

```
Voice Input (RPi)
    ↓ audio stream
Voice Service (WSL)
    ↓ transcription
Intent Classifier
    ├─ HOME_CONTROL → Direct response (fast)
    ├─ CONVERSATION → Direct response (medium)
    └─ TOOLS → n8n webhook → async execution
```

## Performance

- Transcription: 150-200ms
- Intent: 50-100ms (cached) / 50-100ms (LLM)
- Home Control: 150-250ms
- Conversation: 300-500ms
- TTS: 100-150ms
- **Total: 500-800ms for home control**
