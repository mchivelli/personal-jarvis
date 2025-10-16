# n8n Voice Integration - Visual Setup Guide

## Workflow Structure After Integration

```
┌─────────────────────────┐
│ Voice Assistant Webhook │ (NEW)
│ Path: voice-assistant   │
│ Method: POST            │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Extract Voice Data      │ (NEW)
│ text, intent, source    │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Ultimate Assistant      │ (EXISTING)
│ AI Agent with Tools     │
└─────────────────────────┘
```

## Step-by-Step in n8n UI

### 1. Add Webhook Node
- Click **+** button in n8n canvas
- Search for "webhook"
- Select **Webhook** node
- Configure:
  - **Webhook URLs**: Production
  - **Path**: `voice-assistant`
  - **Method**: POST
  - **Response**: 
    - Mode: "Respond Immediately"
    - Response Code: 200
    - Response Body: Leave empty or `{"status":"received"}`

### 2. Add Set Node
- Click **+** after webhook
- Search for "set"
- Select **Set** node
- Click "Add Field" 3 times:
  
  **Field 1:**
  - Name: `text`
  - Value: `{{ $json.text }}`
  
  **Field 2:**
  - Name: `intent`
  - Value: `{{ $json.intent }}`
  
  **Field 3:**
  - Name: `source`
  - Value: `{{ $json.source }}`

### 3. Connect to Ultimate Assistant
- Drag connection from "Extract Voice Data" output
- Connect to "Ultimate Assistant" input
- **Save** workflow
- **Activate** workflow (toggle at top right)

## Test Webhook

### From Command Line
```bash
curl -X POST http://localhost:5678/webhook/voice-assistant \
  -H "Content-Type: application/json" \
  -d '{"text":"send an email to john","intent":"TOOLS","source":"voice_satellite"}'
```

### From Voice Service
```bash
cd /mnt/c/Users/paulm/OneDrive/Desktop/Projects/Bots/n8n/voice-assistant
source venv/bin/activate
python voice_service.py test
```

Look for log: `🔧 Executing n8n tools for: 'Send an email to John'`

## Verify in n8n

1. Go to **Executions** tab in n8n
2. Look for execution triggered by "Voice Assistant Webhook"
3. Check if Ultimate Assistant received the request
4. Verify tool agents (Email Agent, etc.) were called

## Troubleshooting

### Webhook not found (404)
- Verify path is exactly `voice-assistant`
- Check workflow is activated
- Try saving and reactivating

### No data in Ultimate Assistant
- Check "Extract Voice Data" node output
- Verify field mappings are correct
- Test with manual webhook execution in n8n

### Voice service can't reach n8n
- Verify n8n is running: `docker ps | grep n8n`
- Check .env has correct URL: `cat .env | grep N8N_WEBHOOK`
- Test with curl first before using voice service
