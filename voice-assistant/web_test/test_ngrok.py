#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test ngrok connection
"""
import sys
import io
import requests

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NGROK_URL = "https://skeptically-intermetallic-jerome.ngrok-free.dev/webhook/voice-assistant"

print("="*60)
print("🧪 Testing ngrok connection")
print("="*60)
print(f"\nWebhook URL: {NGROK_URL}")
print("\nSending test request...")

try:
    response = requests.post(
        NGROK_URL,
        json={
            "text": "Hello from voice assistant test",
            "intent": "CONVERSATION",
            "source": "test_script"
        },
        timeout=10
    )
    
    print(f"\n✅ Status: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ SUCCESS! n8n is responding!")
        try:
            data = response.json()
            print(f"\nResponse data:")
            print(data)
        except:
            print(f"\nResponse text:")
            print(response.text[:500])
    elif response.status_code == 404:
        print("❌ 404 - Webhook not found in n8n")
        print("   Create a webhook workflow in n8n with path: voice-assistant")
    else:
        print(f"⚠️  Unexpected status code")
        print(f"Response: {response.text[:200]}")
        
except requests.exceptions.Timeout:
    print("❌ TIMEOUT - Request took too long")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60)
