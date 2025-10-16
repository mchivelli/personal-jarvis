# Streaming Voice Assistant Setup

## 🚀 Features

- ✅ **Real-time streaming responses** - See AI response word-by-word
- ✅ **Interrupt capability** - Stop AI mid-sentence by pressing STOP or ESC
- ✅ **Conversation context** - AI remembers previous messages
- ✅ **Intent detection** - Automatically routes to n8n tools when needed
- ✅ **Low latency** - Optimized for speed
- ✅ **Push-to-talk** - Hold button or spacebar to record

## 📦 Installation

### 1. Install Dependencies

```bash
cd voice-assistant
source venv/bin/activate  # On Windows: .\venv\Scripts\Activate.ps1
pip install websockets flask-socketio python-socketio
```

### 2. Verify Configuration

Make sure your `.env` file has:

```bash
# n8n webhook (update with your actual address)
N8N_WEBHOOK_URL=http://172.22.32.1:32768/webhook/voice-assistant

# Ollama (for streaming responses)
OLLAMA_HOST=http://172.22.32.1:11434

# Whisper
WHISPER_MODEL=base.en
```

### 3. Ensure Ollama is Running

The streaming server uses Ollama's streaming API for real-time responses.

**Test Ollama:**
```bash
curl http://172.22.32.1:11434/api/generate -d '{
  "model": "qwen2.5:3b",
  "prompt": "Hello!",
  "stream": false
}'
```

## 🎯 Usage

### Start the Server

```bash
cd voice-assistant/web_test
python streaming_server.py
```

**Expected output:**
```
============================================================
🎙️ Real-Time Streaming Voice Assistant
============================================================
Whisper Available: True
Whisper Model: base.en
Ollama Host: http://172.22.32.1:11434
n8n Webhook: http://172.22.32.1:32768/webhook/voice-assistant
============================================================

Features:
  ✓ Real-time streaming responses
  ✓ Interrupt capability
  ✓ Conversation history
  ✓ Intent detection
  ✓ n8n tool integration
============================================================

Starting server on http://localhost:5002
Open http://localhost:5002 in your browser!
```

### Open in Browser

Navigate to: **http://localhost:5002**

### Controls

**Recording:**
- **Press and hold** microphone button to record
- **Or hold SPACEBAR** to record
- Release to send

**Interrupting:**
- **Click STOP button** while AI is speaking
- **Or press ESC** to interrupt
- AI will stop immediately

**Keyboard Shortcuts:**
- `SPACE` - Push to talk
- `ESC` - Interrupt AI response

## 🎭 How It Works

### Conversation Flow

```
1. You speak → Whisper transcribes
   ↓
2. Intent detected (CONVERSATION or TOOLS)
   ↓
3a. If CONVERSATION:
    → Ollama streams response in real-time
    → Words appear as they're generated
    → Can interrupt anytime
   
3b. If TOOLS:
    → Request sent to n8n
    → Waits for result
    → Returns complete response
```

### Interrupt Flow

```
User presses STOP/ESC
    ↓
Signal sent to server
    ↓
Server stops Ollama streaming
    ↓
UI shows partial response
    ↓
Ready for next input
```

## 🧪 Testing

### Test 1: Simple Conversation

1. Hold microphone button
2. Say: *"Hello, how are you today?"*
3. Release button
4. Watch response stream in real-time

### Test 2: Interrupting

1. Hold microphone button
2. Say: *"Tell me a long story about space"*
3. Release button
4. While AI is responding, click **STOP** or press **ESC**
5. AI should stop immediately

### Test 3: Tool Usage

1. Hold microphone button
2. Say: *"What is 25 times 47?"*
3. Release button
4. Should detect "TOOLS" intent and use Calculator

### Test 4: Conversation Context

1. Say: *"My name is John"*
2. Wait for response
3. Say: *"What is my name?"*
4. AI should remember "John"

## 📊 Metrics

The UI displays:

- **Latency** - Time from button release to first response
- **Messages** - Number of exchanges in conversation
- **Mode** - Current intent (CONVERSATION or TOOLS)

## 🐛 Troubleshooting

### "Disconnected from server"
- Check if streaming server is running
- Verify port 5002 is not in use
- Look for errors in server console

### "Could not access microphone"
- Allow microphone permissions in browser
- Use Chrome or Firefox (best support)
- Try HTTPS or localhost (not IP address)

### Slow streaming responses
- Check Ollama is running: `ollama list`
- Verify model is loaded: `ollama run qwen2.5:3b`
- Check CPU usage (Ollama needs resources)

### Interrupt not working
- Make sure response is still streaming
- Click STOP button directly
- Check browser console for errors

### n8n tools not working
- Verify n8n workflow is active
- Test webhook with curl:
  ```bash
  curl -X POST http://YOUR_N8N_URL/webhook/voice-assistant \
    -H "Content-Type: application/json" \
    -d '{"text":"test","intent":"TOOLS","source":"test"}'
  ```

## 🔄 Switching Between Modes

You now have **3 voice interfaces**:

### 1. Basic (index.html) - Port 5000
```bash
python server_windows.py
# http://localhost:5000
```
- Simple record → response
- Good for testing
- No streaming

### 2. Optimized (voice_optimized.html) - Port 5000
```bash
python server_windows.py
# http://localhost:5000/voice_optimized.html
```
- Push-to-talk
- Latency metrics
- Conversation history
- No streaming

### 3. Streaming (streaming_ui.html) - Port 5002
```bash
python streaming_server.py
# http://localhost:5002
```
- **Real-time streaming** ⚡
- **Interrupt capability** ⚡
- Best for natural conversation
- Most advanced

## 🎯 Best Practices

1. **Speak clearly** - Good audio = better transcription
2. **Hold 2-3 seconds** - Give Whisper enough audio
3. **Use interrupts** - Don't wait for long responses
4. **Check metrics** - Monitor latency to optimize
5. **Clear history** - Start fresh when changing topics

## 🚀 Next Steps

Once comfortable with streaming:

1. **Add wake word detection** - "Hey Jarvis"
2. **Voice Activity Detection** - Auto-detect when you're speaking
3. **Raspberry Pi integration** - Use as satellite
4. **Multi-room audio** - Connect multiple devices
5. **Custom voices** - Train your own TTS

## 📝 Performance Tips

### Reduce Latency

1. **Use faster Whisper model:**
   ```bash
   WHISPER_MODEL=tiny.en  # Faster but less accurate
   ```

2. **Use smaller Ollama model:**
   ```bash
   ollama pull qwen2.5:1.5b  # Even faster
   ```

3. **Run on better hardware:**
   - GPU acceleration for Whisper
   - More RAM for Ollama

### Improve Quality

1. **Use better Whisper model:**
   ```bash
   WHISPER_MODEL=small.en  # More accurate
   ```

2. **Better microphone:**
   - External USB mic
   - Headset with noise cancellation

3. **Reduce background noise:**
   - Quiet environment
   - Close windows
   - Turn off fans

---

**Enjoy your real-time streaming voice assistant!** 🎉
