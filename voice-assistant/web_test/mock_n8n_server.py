#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mock n8n server for testing voice functionality
This simulates n8n responses so you can test the voice interface
"""
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Mock responses
responses = {
    "hello": "Hello! I'm your voice assistant. How can I help you today?",
    "how are you": "I'm doing great! Thanks for asking. How can I assist you?",
    "weather": "I'm a mock server, so I can't check real weather. But let's pretend it's sunny and 72 degrees!",
    "time": "I don't have access to real time, but I can tell you it's a great time to test this voice interface!",
    "test": "Test successful! Your voice input and output are working perfectly. Now you just need to connect to your real n8n server.",
    "default": [
        "I received your message! This is a mock response to test the voice interface.",
        "Your voice system is working great! Now connect to your real n8n server.",
        "Mock response: I heard you loud and clear! The voice functionality works perfectly.",
        "Test successful! Your microphone and speaker are both working. Set up n8n next.",
    ]
}

@app.route('/webhook/voice-assistant', methods=['POST', 'GET'])
def webhook():
    """Mock webhook endpoint"""
    try:
        if request.method == 'POST':
            data = request.json
            text = data.get('text', '').lower()
            
            print(f"📥 Received: {text}")
            
            # Generate response based on keywords
            response_text = None
            for keyword, response in responses.items():
                if keyword != 'default' and keyword in text:
                    response_text = response
                    break
            
            if not response_text:
                response_text = random.choice(responses['default'])
            
            print(f"📤 Responding: {response_text}")
            
            return jsonify({
                'success': True,
                'output': response_text,
                'message': response_text,
                'source': 'mock_n8n_server'
            })
        else:
            return jsonify({
                'status': 'ok',
                'message': 'Mock n8n webhook endpoint is running'
            })
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    return jsonify({
        'status': 'running',
        'message': 'Mock n8n server for voice testing',
        'webhook': '/webhook/voice-assistant'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎭 Mock n8n Server")
    print("="*60)
    print("This simulates n8n so you can test voice functionality")
    print("Webhook: http://localhost:8888/webhook/voice-assistant")
    print("="*60)
    print("\n✓ Voice responses will work")
    print("✓ Test your microphone and speaker")
    print("✓ Then connect to real n8n\n")
    
    app.run(host='127.0.0.1', port=8888, debug=False)
