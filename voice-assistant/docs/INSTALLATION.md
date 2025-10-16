# Installation Guide

## Step 1: Configure Ollama (Windows)

Run PowerShell as Administrator:

```powershell
cd C:\Users\paulm\OneDrive\Desktop\Projects\Bots\n8n\voice-assistant\scripts
.\setup_ollama.ps1
```

Or manually:
```powershell
[System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'User')
New-NetFirewallRule -DisplayName "Ollama WSL" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 11434

ollama pull llama3.2:1b
ollama pull llama3.2:3b
ollama pull qwen2.5:7b
```

## Step 2: Install Voice Service (WSL)

```bash
cd /mnt/c/Users/paulm/OneDrive/Desktop/Projects/Bots/n8n/voice-assistant
chmod +x scripts/install.sh
./scripts/install.sh
```

## Step 3: Test Service

```bash
source venv/bin/activate
python voice_service.py test
```

## Step 4: Configure n8n

See N8N_INTEGRATION.md

## Troubleshooting

If Ollama connection fails:
```bash
curl http://172.22.32.1:11434/api/tags
```

See TROUBLESHOOTING.md for more help.
