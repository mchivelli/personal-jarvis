# Troubleshooting

## Cannot Connect to Ollama

```bash
# Test connection
curl http://172.22.32.1:11434/api/tags
```

Fix: Run `scripts/setup_ollama.ps1` in Windows PowerShell as Admin

## Missing config.yaml

```bash
# Verify file exists
ls config/config.yaml
```

Fix: Re-run `./scripts/install.sh`

## n8n Webhook Not Working

```bash
# Test webhook
curl -X POST http://localhost:5678/webhook/voice-assistant \
  -d '{"text":"test","intent":"TOOLS"}'
```

Fix: Check webhook path in n8n workflow

## Service Won't Start

```bash
# Check logs
tail -f logs/voice-assistant.log
```

Fix: Verify .env file and config.yaml exist
