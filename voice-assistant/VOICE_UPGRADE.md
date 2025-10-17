# Voice Quality Upgrade Guide

## 🎤 Upgrading to Better, More Natural Voice

You're currently using: `en-us-lessac-medium`  
**Recommended upgrade**: `en-us-amy-low` (Fastest + Most Natural)

---

## Quick Setup on n8n Server

### Option 1: en-us-amy-low (RECOMMENDED - Fastest & Natural)

```bash
# SSH into your n8n server
ssh user@your-n8n-server

# Navigate to Piper models directory
cd /opt/piper/models/piper_voices

# Download the voice
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/voice-en-us-amy-low.tar.gz

# Extract
tar -xzf voice-en-us-amy-low.tar.gz

# Verify files exist
ls -la en-us-amy-low.onnx en-us-amy-low.onnx.json
```

### Option 2: en-us-libritts-high (Highest Quality)

If you want the most natural voice (slightly slower but still fast):

```bash
cd /opt/piper/models/piper_voices
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/voice-en-us-libritts-high.tar.gz
tar -xzf voice-en-us-libritts-high.tar.gz
```

---

## Update n8n Workflow

In your n8n voice-assistant workflow, update the **Piper TTS node**:

**Current Model Path:**
```
/opt/piper/models/piper_voices/en-us-lessac-medium.onnx
```

**New Model Path (choose one):**
```bash
# For Amy (recommended):
/opt/piper/models/piper_voices/en-us-amy-low.onnx

# For LibriTTS (highest quality):
/opt/piper/models/piper_voices/en-us-libritts-high.onnx
```

---

## Voice Comparison

| Voice | Quality | Speed | Latency | Character | Best For |
|-------|---------|-------|---------|-----------|----------|
| **en-us-amy-low** | ⭐⭐⭐⭐ | **Fastest** | ~100ms | Young female, clear | **Pi Nano 2 (RECOMMENDED)** |
| en-us-libritts-high | ⭐⭐⭐⭐⭐ | Medium | ~200ms | Very natural | High-quality responses |
| en-us-lessac-medium | ⭐⭐⭐ | Medium | ~150ms | Neutral male | Current default |
| en-us-ryan-high | ⭐⭐⭐⭐⭐ | Medium | ~200ms | Professional male | Formal assistant |

---

## Testing the New Voice

After updating n8n:

1. Restart your n8n workflow (or just the TTS node)
2. Test with: http://localhost:5002
3. Say something and listen to the new voice!

---

## Prompt for n8n Assistant

Copy and send this to your n8n Assistant:

```
Download and install the Piper voice "en-us-amy-low" for better voice quality.

Commands to run on the n8n server:
cd /opt/piper/models/piper_voices
wget https://github.com/rhasspy/piper/releases/download/v1.2.0/voice-en-us-amy-low.tar.gz
tar -xzf voice-en-us-amy-low.tar.gz

Then update my voice-assistant workflow's Piper TTS node to use:
Model Path: /opt/piper/models/piper_voices/en-us-amy-low.onnx

This voice is optimized for low latency (~100ms) and sounds much more natural than lessac-medium. Perfect for the Pi Nano 2.
```

---

## Performance on Pi Nano 2

**en-us-amy-low** specifications:
- **Latency**: ~100-150ms (very fast)
- **Quality**: High (22kHz output)
- **CPU Usage**: Low (optimized for Pi)
- **Model Size**: ~8MB (very lightweight)
- **RAM**: ~50MB during inference

Perfect for real-time conversation! 🚀
