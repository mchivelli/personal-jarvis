# Setup on Your Local Machine

Follow these steps to set up Personal Jarvis on your local machine after cloning from GitHub.

## Prerequisites

Make sure you have:
- ✅ Python 3.10 or higher
- ✅ Git installed
- ✅ Access to your remote n8n server (note the IP/domain and port)

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/mchivelli/personal-jarvis.git
cd personal-jarvis
```

### 2. Find Your n8n Server Address

You need to know how to reach your n8n server from your local machine.

**If n8n is on the same machine:**
```
http://localhost:5678
```

**If n8n is on another machine/server:**
```
http://YOUR_SERVER_IP:PORT
```

Test connectivity:
```bash
curl http://YOUR_N8N_ADDRESS/healthz
```

### 3. Configure Environment

```bash
cd voice-assistant
cp .env.example .env
```

Edit `.env` and update:
```bash
# IMPORTANT: Update this line with your n8n server address
N8N_WEBHOOK_URL=http://YOUR_N8N_ADDRESS/webhook/voice-assistant

# Example for remote server:
# N8N_WEBHOOK_URL=http://192.168.1.100:32768/webhook/voice-assistant
```

### 4. Install Python Dependencies

**On Windows:**
```powershell
cd voice-assistant
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**On Mac/Linux:**
```bash
cd voice-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Install Ollama (if not on server)

If you want to run Ollama locally instead of on the server:

**Download and install:**
- Windows: https://ollama.ai/download/windows
- Mac: `brew install ollama`
- Linux: `curl -fsSL https://ollama.ai/install.sh | sh`

**Pull the model:**
```bash
ollama pull qwen2.5:3b
```

**Update `.env`:**
```bash
OLLAMA_HOST=http://localhost:11434
```

### 6. Verify n8n Workflows

1. Open your n8n UI (http://YOUR_N8N_ADDRESS)
2. Ensure "Assistant Agent" workflow is imported
3. **Make sure it's ACTIVE** (toggle in top-right)
4. Check that it uses the correct Ollama connection

### 7. Test the Setup

**Test webhook connectivity:**
```bash
curl -X POST http://YOUR_N8N_ADDRESS/webhook/voice-assistant \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello test","intent":"CONVERSATION","source":"test"}'
```

Expected response: `{"message":"Workflow was started"}`

**Start web test interface:**

Windows:
```powershell
cd voice-assistant\web_test
python server_windows.py
```

Mac/Linux:
```bash
cd voice-assistant/web_test
python server.py
```

**Open browser:**
```
http://localhost:5000
```

Test with your microphone!

## Network Configuration

### Firewall Rules

If n8n is on a remote server, ensure:

1. **Server firewall allows** connections to n8n port
2. **Your network can reach** the server
3. **n8n is bound to** 0.0.0.0 (not just localhost)

### Docker/WSL n8n

If n8n runs in Docker on Windows, you might need:

```bash
# Find the WSL IP
ip addr show eth0 | grep inet

# Use that IP in .env
N8N_WEBHOOK_URL=http://WSL_IP:PORT/webhook/voice-assistant
```

### Remote n8n Behind Nginx/Reverse Proxy

If your n8n is behind a reverse proxy:

```bash
# Use the public domain
N8N_WEBHOOK_URL=https://n8n.yourdomain.com/webhook/voice-assistant

# Make sure SSL certificate is valid
# Or use http:// for testing (not recommended for production)
```

## Troubleshooting

### Can't connect to n8n

1. **Check n8n is running:**
   ```bash
   curl http://YOUR_N8N_ADDRESS/healthz
   ```

2. **Check network connectivity:**
   ```bash
   ping YOUR_N8N_SERVER
   ```

3. **Check firewall:**
   - Windows: `Windows Defender Firewall`
   - Linux: `sudo ufw status`

4. **Check n8n logs** for errors

### Webhook returns 404

- **Workflow is not active** → Activate it in n8n UI
- **Wrong webhook path** → Check it's `/webhook/voice-assistant`
- **Workflow not imported** → Import `Assistant Agent.json`

### Whisper model won't download

1. **Check internet connection**
2. **Check disk space** (need ~500MB)
3. **Try manual download:**
   ```bash
   python -c "from faster_whisper import WhisperModel; WhisperModel('base.en')"
   ```

### Audio not working

1. **Check microphone permissions** in browser
2. **Use Chrome or Firefox** (best support)
3. **Test microphone** in system settings first
4. **Record for 3+ seconds** minimum

## Next Steps

Once everything works:

1. ✅ Test simple conversation
2. ✅ Test calculator tool ("what is 5 times 7")
3. ✅ Configure other agents (email, calendar) if needed
4. ✅ Set up Raspberry Pi satellite (optional)
5. ✅ Deploy for production use

## Getting Help

If you encounter issues:

1. Check the main README.md
2. Review n8n execution logs
3. Check Python service logs
4. Open a GitHub issue with details

---

**Welcome to your personal Jarvis! 🚀**
