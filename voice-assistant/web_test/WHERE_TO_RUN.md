# 🎯 WHERE TO RUN EVERYTHING

## Simple Answer:

**Run `streaming_server.py` on YOUR WINDOWS PC**  
**Piper TTS runs on the n8n SERVER**

---

## 📍 Complete Setup Map

### YOUR WINDOWS PC
```
Location: C:\Users\paulm\OneDrive\Desktop\n8n-Bot\personal-jarvis\voice-assistant\web_test

What runs here:
├─ streaming_server.py     ← START THIS
└─ Browser (localhost:5002) ← OPEN THIS
```

**Command:**
```powershell
cd C:\Users\paulm\OneDrive\Desktop\n8n-Bot\personal-jarvis\voice-assistant\web_test
python streaming_server.py
```

**Then open:** http://localhost:5002

---

### REMOTE n8n SERVER
```
What runs there:
├─ n8n workflow (voice-assistant)
├─ Ollama (LLM - generates responses)
└─ Piper TTS (generates voice audio)
```

**You DON'T start these manually** - they're already running as services!

---

## 🔄 How Data Flows

```
1. YOU speak into browser mic
   ↓
2. Browser converts speech → text (instant)
   ↓
3. streaming_server.py sends text via ngrok
   ↓
4. n8n workflow receives text
   ↓
5. Ollama generates response
   ↓
6. Piper TTS converts to audio
   ↓
7. n8n returns: {output: "text", audio: "base64"}
   ↓
8. streaming_server.py forwards to browser
   ↓
9. Browser shows text + plays audio
```

---

## ✅ What's Currently Working

### On Windows PC:
- ✅ Browser speech recognition (instant)
- ✅ streaming_server.py (forwards to n8n)
- ✅ WebSocket connection
- ✅ TTS audio playback

### On n8n Server (via ngrok):
- ✅ ngrok tunnel active
- ✅ n8n webhook receiving requests
- ⚠️ TTS might need setup (see below)

---

## 🔧 What n8n Needs to Return

Your n8n workflow must return this format:

```json
{
  "output": "I'm doing great! How can I help?",
  "audio": "UklGRiQAAABXQVZFZm..."
}
```

**If n8n only returns `{"output": "text"}`:**
- Text will work ✅
- Audio won't play ❌

**To add TTS**, send this to your n8n Agent:

```
Add Piper TTS to my voice-assistant workflow.

After Ollama generates the response, convert it to audio using Piper:
/opt/piper/piper --model /opt/piper/models/piper_voices/en-us-amy-low.onnx --output_raw

Then return both:
{"output": "text response", "audio": "base64_encoded_wav"}

The audio must be WAV format, base64 encoded.
```

---

## 🚀 Quick Start (Right Now)

### Step 1: Start Server
```powershell
cd C:\Users\paulm\OneDrive\Desktop\n8n-Bot\personal-jarvis\voice-assistant\web_test
python streaming_server.py
```

You should see:
```
============================================================
🎙️ Real-Time Streaming Voice Assistant
============================================================
n8n Webhook: https://skeptically-intermetallic-jerome.ngrok-free.dev/webhook/voice-assistant
Starting server on http://localhost:5002
```

### Step 2: Open Browser
```
http://localhost:5002
```

### Step 3: Test
1. Click the 🎤 microphone
2. Say "Hello, how are you?"
3. Watch for text response
4. Listen for audio (if TTS is set up in n8n)

---

## 📊 Current Status Check

Run this to verify everything:

```powershell
# Test ngrok connection
python test_ngrok.py

# Should show:
# ✅ ngrok tunnel working
# ✅ n8n responding
```

---

## 🎤 Why This Architecture?

**Windows PC runs streaming_server.py because:**
- You're testing locally
- Easy to restart/debug
- Browser can't directly connect to remote n8n
- Acts as a bridge between browser and n8n

**n8n Server runs Piper because:**
- Server has more power than Pi
- Piper needs to be close to Ollama
- Audio generation is heavy
- Server has the models installed

**Later on Pi Nano 2:**
- Pi will run the equivalent of streaming_server.py
- Pi will use local Whisper (not browser)
- Same n8n setup (Ollama + Piper)
- Even faster because Pi is dedicated hardware

---

## 🔍 Verification Checklist

**Windows PC:**
- [ ] Python installed ✓
- [ ] Requirements installed ✓ (`pip install flask flask-socketio flask-cors python-dotenv`)
- [ ] streaming_server.py running ✓
- [ ] Browser at localhost:5002 ✓
- [ ] Can click microphone ✓

**n8n Server (via ngrok):**
- [ ] ngrok URL working ✓ (https://skeptically-intermetallic-jerome.ngrok-free.dev)
- [ ] n8n webhook responding ✓
- [ ] Ollama working ✓
- [ ] Piper TTS configured ⚠️ (might need setup)

---

## 🆘 If Something's Not Working

### "Connection failed"
- Check streaming_server.py is running
- Check firewall isn't blocking port 5002
- Try http://127.0.0.1:5002 instead

### "n8n not responding"
- Check ngrok URL is correct in .env
- Test with: `python test_ngrok.py`
- Verify n8n server is online

### "Text works but no audio"
- n8n isn't returning audio
- Tell n8n Agent to add Piper TTS
- See TTS_SETUP_COMPLETE.md for details

### "Speech recognition not working"
- Use Chrome or Edge browser
- Allow microphone permissions
- Check mic works in other apps

---

## 📁 Important Files

**On Windows PC:**
```
web_test/
├─ streaming_server.py      ← Run this
├─ streaming_ui.html         ← Served by server
├─ .env                      ← Has ngrok URL
├─ WHERE_TO_RUN.md          ← This file
└─ TTS_SETUP_COMPLETE.md    ← Full TTS guide
```

**On n8n Server:**
```
/opt/piper/
├─ piper                     ← TTS binary
└─ models/piper_voices/
   └─ en-us-amy-low.onnx    ← Voice model
```

---

## 🎯 Summary

**To start testing RIGHT NOW:**

```powershell
# On Windows PC:
cd C:\Users\paulm\OneDrive\Desktop\n8n-Bot\personal-jarvis\voice-assistant\web_test
python streaming_server.py

# Open browser:
# http://localhost:5002

# Click mic and talk!
```

Everything else is already running on the remote n8n server. You just need to make sure n8n returns audio (see TTS_SETUP_COMPLETE.md).

🎉 **That's it! You're good to go!**
