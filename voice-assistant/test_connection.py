#!/usr/bin/env python3
"""
Test connectivity to Ollama and n8n
"""
import requests
import sys
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

print("=" * 60)
print("🔍 Testing Connections")
print("=" * 60)

# Test Ollama
ollama_host = os.getenv('OLLAMA_HOST', 'http://172.22.32.1:11434')
print(f"\n1. Testing Ollama at: {ollama_host}")
try:
    response = requests.get(f"{ollama_host}/api/tags", timeout=5)
    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f"   ✓ Ollama Connected!")
        print(f"   Available models: {len(models)}")
        for model in models:
            print(f"      - {model.get('name')}")
    else:
        print(f"   ✗ Ollama returned status {response.status_code}")
        sys.exit(1)
except Exception as e:
    print(f"   ✗ Cannot connect to Ollama: {e}")
    print(f"   Make sure Ollama is running on Windows")
    sys.exit(1)

# Test n8n Webhook
n8n_webhook = os.getenv('N8N_WEBHOOK_URL', 'http://192.168.0.244:32768/webhook/voice-assistant')
print(f"\n2. Testing n8n webhook at: {n8n_webhook}")
try:
    # Send a test payload
    payload = {
        "text": "connection test",
        "intent": "TOOLS",
        "source": "connection_test",
        "test": True
    }
    response = requests.post(n8n_webhook, json=payload, timeout=10)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        print(f"   ✓ n8n Webhook Connected!")
        try:
            result = response.json()
            print(f"   Response: {result}")
        except:
            print(f"   Response (text): {response.text[:200]}")
    elif response.status_code == 404:
        print(f"   ✗ Webhook endpoint not found (404)")
        print(f"   Make sure you have created the webhook in n8n")
        print(f"   Expected path: /webhook/voice-assistant")
    else:
        print(f"   ⚠️  n8n returned status {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        
except requests.exceptions.ConnectTimeout:
    print(f"   ✗ Connection timeout")
    print(f"   n8n server might not be reachable at {n8n_webhook}")
except requests.exceptions.ConnectionError as e:
    print(f"   ✗ Connection error: {e}")
    print(f"   Make sure n8n is running at http://192.168.0.244:32768")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 60)
print("Test Complete!")
print("=" * 60)
