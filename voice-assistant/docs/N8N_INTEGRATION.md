# n8n Integration Guide

## Setup Webhook in n8n

1. Open "Assistant Agent" workflow at http://localhost:5678
2. Add **Webhook** node:
   - Path: `voice-assistant`
   - Method: POST
   - Response: Immediately
3. Add **Set** node to extract:
   - `text` = `{{ $json.text }}`
   - `intent` = `{{ $json.intent }}`
   - `source` = `{{ $json.source }}`
4. Connect to Ultimate Assistant

## Test

```bash
curl -X POST http://localhost:5678/webhook/voice-assistant \
  -H "Content-Type: application/json" \
  -d '{"text":"test","intent":"TOOLS","source":"voice_satellite"}'
```

## Payload Format

```json
{
  "text": "user command",
  "intent": "TOOLS|HOME_CONTROL|CONVERSATION",
  "source": "voice_satellite",
  "timestamp": 1234567890
}
```
