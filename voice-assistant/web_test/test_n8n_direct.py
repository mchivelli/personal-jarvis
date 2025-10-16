#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test n8n webhook directly
"""
import requests

NGROK_URL = "https://skeptically-intermetallic-jerome.ngrok-free.dev/webhook/voice-assistant"

print("Testing n8n webhook directly...")
print(f"URL: {NGROK_URL}\n")

try:
    response = requests.post(
        NGROK_URL,
        json={
            "text": "Hello, this is a test from Python",
            "intent": "CONVERSATION",
            "source": "test_script"
        },
        timeout=10
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response:\n{response.text}\n")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Success!")
        print(f"Output: {data.get('output', data.get('message', 'No output field'))}")
    else:
        print(f"❌ Error: Unexpected status code")
        
except Exception as e:
    print(f"❌ Error: {e}")
