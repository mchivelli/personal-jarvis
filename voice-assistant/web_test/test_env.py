#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv

print("="*60)
print("Testing .env loading")
print("="*60)

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
print(f"\n.env path: {env_path}")
print(f".env exists: {env_path.exists()}")

load_dotenv(env_path)

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "DEFAULT_NOT_SET")
print(f"\nLoaded N8N_WEBHOOK_URL: {N8N_WEBHOOK_URL}")

if "192.168.0.244" in N8N_WEBHOOK_URL:
    print("❌ PROBLEM: Still using old IP!")
elif "ngrok" in N8N_WEBHOOK_URL:
    print("✅ Correct: Using ngrok URL")
else:
    print("⚠️  Unknown URL")

print("="*60)
