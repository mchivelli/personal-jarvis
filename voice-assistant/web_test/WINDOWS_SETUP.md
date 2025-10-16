# Voice Assistant Web Test - Windows Setup

Run the web interface directly on Windows to avoid Remote Desktop audio issues.

## Quick Start

### 1. Install Python Dependencies

Open **PowerShell** in this directory and run:

```powershell
# Install required packages
pip install flask flask-cors faster-whisper requests

# Optional: Install ffmpeg for better audio conversion
# Download from: https://www.gyan.dev/ffmpeg/builds/
# Add to PATH or place ffmpeg.exe in this folder
```

### 2. Start the Server

**Option A: Double-click the batch file**
```
start_windows.bat
```

**Option B: Run from PowerShell**
```powershell
python server_windows.py
```

### 3. Open in Browser

Open **http://localhost:5000** in Chrome or Firefox (NOT in Remote Desktop browser!)

### 4. Test Your Voice

1. Click the microphone button 🎤
2. Allow microphone access
3. Speak clearly for 2-3 seconds
4. Click to stop recording
5. See transcription and AI response

---

## Troubleshooting

### "Module not found: faster_whisper"
```powershell
pip install faster-whisper
```

### "Could not transcribe audio"
- **Speak louder** and closer to microphone
- **Record for longer** (3+ seconds)
- **Check Windows microphone settings**:
  - Settings → Privacy → Microphone → Allow apps
  - Settings → Sound → Input → Test your microphone

### "n8n webhook error"
- Make sure n8n Docker container is running
- Check n8n is accessible at http://172.22.32.1:32768
- Make sure the workflow is **active** (toggle in n8n)

### Audio still poor quality?
- Make sure you're running the server **locally on Windows**, not via RDP
- Close Remote Desktop and run directly on the machine
- Or connect via browser from another device on the network (use http://YOUR_IP:5000)

### FFmpeg not found
- Download from: https://www.gyan.dev/ffmpeg/builds/
- Extract ffmpeg.exe to this folder, OR
- Add ffmpeg to Windows PATH

---

## How It Works

```
┌──────────────────┐
│ Windows Browser  │ ← Local microphone (no RDP!)
│   (localhost)    │
└────────┬─────────┘
         │ HTTP
         ▼
┌──────────────────┐
│  Flask Server    │ ← Running on Windows
│  (Python)        │
└────────┬─────────┘
         │ Faster-Whisper
         ▼
┌──────────────────┐
│  Transcription   │
└────────┬─────────┘
         │ HTTP POST
         ▼
┌──────────────────┐
│  n8n (Docker)    │ ← 172.22.32.1:32768
│  Ultimate Agent  │
└────────┬─────────┘
         │ Ollama
         ▼
┌──────────────────┐
│  AI Response     │
└──────────────────┘
```

---

## Network Access

To test from another device on your network:

1. Find your Windows IP address:
   ```powershell
   ipconfig
   # Look for "IPv4 Address"
   ```

2. Edit `start_windows.bat`:
   ```batch
   python server_windows.py --host 0.0.0.0
   ```

3. Open from other device:
   ```
   http://YOUR_WINDOWS_IP:5000
   ```

---

## What's Different from WSL Version?

**Windows Version:**
- ✅ Runs natively on Windows
- ✅ Direct microphone access (no RDP issues)
- ✅ Simpler setup (no WSL needed)
- ❌ No Piper TTS (not needed for testing)

**WSL Version:**
- ✅ Full Piper TTS support
- ✅ Better for production
- ❌ Audio issues with Remote Desktop
- ❌ More complex setup

---

## Next Steps

Once voice testing works:
1. Set up the full voice service in WSL
2. Configure Raspberry Pi satellite
3. Deploy for production use

See main README.md for full setup instructions.
