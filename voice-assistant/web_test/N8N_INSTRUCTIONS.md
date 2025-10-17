# 🎯 Instructions for n8n Agent

## Quick Summary

**Tell your n8n Agent to REMOVE Piper TTS from the workflow.**

TTS should run locally (on Windows PC for testing, on Pi for production), NOT on the n8n server. This reduces latency by 3x and network traffic by 250x.

---

## 📋 Exact Prompt for n8n Agent

Copy and paste this:

```
REMOVE Piper TTS from my voice-assistant workflow.

Current problem: The workflow is generating audio on the server and sending it over the network, which adds 200-1000ms latency per response.

New requirement: Return ONLY text, no audio.

Please modify the workflow to:

Input (from webhook):
{
  "text": "user message",
  "intent": "CONVERSATION",
  "source": "streaming"
}

Processing:
1. Webhook receives text
2. Ollama generates response text
3. That's it - no TTS needed

Output (to webhook response):
{
  "output": "AI response text here"
}

Remove these nodes if present:
- Piper TTS node
- Execute Command (piper)
- Base64 encoding node
- Any audio processing nodes

Keep only:
- Webhook
- Ollama
- Respond to Webhook

Reason: TTS will run locally on the client device for instant, zero-latency audio playback. This is much faster than sending audio files over the network.
```

---

## ✅ What the Workflow Should Look Like

### Simplified n8n Workflow:

```
┌──────────────┐
│   Webhook    │  Path: /webhook/voice-assistant
│   (Trigger)  │  Method: POST
└──────┬───────┘
       │
       ↓
┌──────────────┐
│   Ollama     │  Model: qwen2.5:3b
│    Node      │  Temperature: 0.7
└──────┬───────┘  Prompt: {{ $json.text }}
       │
       ↓
┌──────────────┐
│  Respond to  │  Response: {{ $json }}
│   Webhook    │  Format: {"output": "..."}
└──────────────┘
```

**That's it! 3 nodes total.**

---

## 🧪 Testing the n8n Response

After your n8n Agent makes the change, test it:

### Test Command:
```powershell
curl -X POST `
  -H "Content-Type: application/json" `
  -d '{\"text\":\"Hello, how are you?\",\"intent\":\"CONVERSATION\"}' `
  https://skeptically-intermetallic-jerome.ngrok-free.dev/webhook/voice-assistant
```

### Expected Response:
```json
{
  "output": "I'm doing great! How can I help you today?"
}
```

### ❌ Wrong Response (if TTS still there):
```json
{
  "output": "I'm doing great!",
  "audio": "UklGRiQAAABXQVZFZm..."
}
```

**If you see "audio" field, TTS is still in the workflow. Tell n8n Agent to remove it.**

---

## 🎤 What Handles TTS Now

### Windows PC (Testing):
- **Browser Web Speech API**
- Built into Chrome/Edge
- Zero latency
- No setup needed
- ✅ Already working in your code

### Pi Nano 2 (Production):
- **Local Piper TTS**
- Installed on Pi
- ~100ms latency
- Better voice quality
- ✅ Will be configured when deploying to Pi

---

## 📊 Benefits Explained

### Why Local TTS is Better:

**Latency:**
- Remote TTS: ~3-8 seconds
- Local TTS: ~1-3 seconds
- **Improvement: 3x faster**

**Network Usage:**
- Remote TTS: ~100KB per message
- Local TTS: ~400 bytes per message
- **Improvement: 250x less data**

**Reliability:**
- Remote TTS: Fails if network slow/down
- Local TTS: Always works
- **Improvement: More robust**

---

## 🔍 Verification Checklist

After n8n Agent makes changes:

- [ ] Test webhook with curl (see above)
- [ ] Response should have "output" field only
- [ ] Response should NOT have "audio" field
- [ ] Text response should be natural
- [ ] No TTS-related errors in n8n logs

---

## 🆘 Common Issues

### "n8n Agent says TTS is needed"

**Response:**
```
No, TTS should NOT be in n8n. The client handles TTS locally.

Benefits:
1. 3x faster responses
2. 250x less network traffic
3. Works offline
4. Better voice quality
5. Lower server load

Please remove all TTS and audio processing from the workflow.
```

### "n8n Agent asks what handles TTS then"

**Response:**
```
The client handles TTS:

Windows (testing): Browser Web Speech API (already implemented)
Pi Nano 2 (production): Local Piper TTS (will be configured on Pi)

n8n only needs to return text. The client converts text to speech instantly.
```

### "Response still includes audio"

**Actions:**
1. Check n8n workflow for Piper/TTS nodes
2. Check for base64 encoding nodes
3. Verify "Respond to Webhook" node only returns text
4. Ask n8n Agent: "Show me the workflow nodes. Are there any TTS or audio nodes?"

---

## 📁 Where This Fits

```
Your Setup:
├─ Windows PC
│  ├─ streaming_server.py  (forwards text only)
│  └─ Browser (handles TTS locally)
│
└─ n8n Server (via ngrok)
   └─ Workflow (text only, no TTS)
```

---

## 🚀 Final Check

After changes, your workflow should:

✅ Receive text from webhook  
✅ Process with Ollama  
✅ Return text response  
❌ NOT generate audio  
❌ NOT encode audio to base64  
❌ NOT include "audio" field in response  

**Simple = Fast = Correct! 🎉**
