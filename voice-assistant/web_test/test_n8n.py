#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test n8n connectivity
"""
import sys
import io
import requests
import time

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("="*60)
print("Testing n8n Connectivity")
print("="*60)

# Test different possible URLs
test_urls = [
    "http://192.168.0.244:32768",
    "http://192.168.0.244:32768/webhook/voice-assistant",
    "http://192.168.0.244:5678",
    "http://192.168.0.244:5678/webhook/voice-assistant",
    "http://localhost:32768",
    "http://localhost:5678",
]

for url in test_urls:
    print(f"\n🔍 Testing: {url}")
    try:
        response = requests.get(url, timeout=3)
        print(f"   ✓ Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✓ Server is reachable!")
    except requests.exceptions.Timeout:
        print(f"   ✗ Timeout - server not responding")
    except requests.exceptions.ConnectionError as e:
        print(f"   ✗ Connection refused - server not running or unreachable")
    except Exception as e:
        print(f"   ✗ Error: {e}")

print("\n" + "="*60)
print("Diagnostic Information")
print("="*60)
print("\n📋 Possible Issues:")
print("1. n8n server is not running at 192.168.0.244:32768")
print("2. Webhook 'voice-assistant' doesn't exist in n8n")
print("3. Firewall blocking connection")
print("4. Wrong IP address or port")
print("\n💡 Solutions:")
print("1. Check n8n is running: Open http://192.168.0.244:32768 in browser")
print("2. Create webhook in n8n: Workflow → Webhook node → Path: 'voice-assistant'")
print("3. Verify IP with: ipconfig (look for your server's IP)")
print("4. Check n8n port in docker: docker ps")
print("\n" + "="*60)
