#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Verify n8n connection with detailed diagnostics
"""
import sys
import io
import requests
from dotenv import load_dotenv
from pathlib import Path
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://192.168.0.244:32768/webhook/voice-assistant")

print("="*60)
print("🔍 n8n Connection Diagnostics")
print("="*60)
print(f"\nWebhook URL from .env: {N8N_WEBHOOK_URL}")

# Extract base URL and path
from urllib.parse import urlparse
parsed = urlparse(N8N_WEBHOOK_URL)
base_url = f"{parsed.scheme}://{parsed.netloc}"
webhook_path = parsed.path

print(f"Base URL: {base_url}")
print(f"Webhook Path: {webhook_path}")
print("\n" + "-"*60)

# Test 1: Check if server is reachable
print("\n[Test 1] Checking if n8n server is reachable...")
try:
    response = requests.get(base_url, timeout=5)
    print(f"✓ Server is reachable! Status: {response.status_code}")
except requests.exceptions.Timeout:
    print("✗ TIMEOUT - Server took too long to respond")
    print("  Possible causes:")
    print("  - Server is down")
    print("  - Wrong IP address")
    print("  - Firewall blocking connection")
except requests.exceptions.ConnectionError:
    print("✗ CONNECTION REFUSED - Cannot connect to server")
    print("  Possible causes:")
    print("  - Server is not running")
    print("  - Wrong IP address or port")
    print("  - Network issue")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "-"*60)

# Test 2: Check webhook endpoint
print("\n[Test 2] Testing webhook endpoint...")
try:
    response = requests.post(
        N8N_WEBHOOK_URL,
        json={"text": "connection test", "test": True},
        timeout=10
    )
    print(f"✓ Webhook responded! Status: {response.status_code}")
    if response.status_code == 200:
        print(f"✓ Response: {response.text[:200]}")
    elif response.status_code == 404:
        print("✗ 404 NOT FOUND - Webhook doesn't exist in n8n")
        print("  Action needed: Create a webhook in n8n workflow")
    else:
        print(f"⚠️  Unexpected status: {response.status_code}")
except requests.exceptions.Timeout:
    print("✗ TIMEOUT - Webhook took too long to respond")
except requests.exceptions.ConnectionError:
    print("✗ CONNECTION REFUSED - Cannot connect to webhook")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("📋 Next Steps")
print("="*60)

print("\n1. Verify n8n is running:")
print(f"   Open in browser: {base_url}")

print("\n2. Check if webhook exists:")
print("   - Open n8n editor")
print("   - Look for workflow with Webhook node")
print("   - Webhook path should be: 'voice-assistant'")

print("\n3. Create webhook if missing:")
print("   - Create new workflow in n8n")
print("   - Add 'Webhook' node")
print("   - Set path to: voice-assistant")
print("   - Method: POST")
print("   - Respond with: using 'Respond to Webhook' node")

print("\n4. Test in browser:")
print(f"   {N8N_WEBHOOK_URL}")

print("\n" + "="*60)
