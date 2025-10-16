#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Voice Server - HARD-CODED ngrok URL
"""
import sys
import io

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# HARD-CODED ngrok URL - NO .env file dependency
N8N_WEBHOOK_URL = "https://skeptically-intermetallic-jerome.ngrok-free.dev/webhook/voice-assistant"

print("="*60)
print(f"🌐 USING URL: {N8N_WEBHOOK_URL}")
print("="*60)

@app.route('/')
def index():
    """Serve the voice chat page"""
    with open('voice_chat.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    response = Response(html_content, mimetype='text/html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    """Forward text to n8n"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        print(f"\n📤 Sending: {text}")
        print(f"🌐 To URL: {N8N_WEBHOOK_URL}\n")
        
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={
                "text": text,
                "intent": "CONVERSATION",
                "source": "web_voice_chat"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('output', result.get('message', 'Message received'))
            print(f"✅ Response: {response_text}\n")
            
            return jsonify({
                'success': True,
                'response': response_text
            })
        else:
            error_msg = f"n8n returned status {response.status_code}"
            print(f"❌ {error_msg}\n")
            return jsonify({'success': False, 'error': error_msg}), 500
            
    except requests.exceptions.Timeout:
        print("❌ Timeout\n")
        return jsonify({'success': False, 'error': 'n8n request timeout'}), 504
        
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_connection():
    """Test n8n connection"""
    print(f"\n🔍 Testing connection to: {N8N_WEBHOOK_URL}\n")
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"text": "test", "test": True},
            timeout=5
        )
        return jsonify({
            'success': True,
            'status': response.status_code,
            'n8n_url': N8N_WEBHOOK_URL
        })
    except Exception as e:
        print(f"❌ Test failed: {e}\n")
        return jsonify({
            'success': False,
            'error': str(e),
            'n8n_url': N8N_WEBHOOK_URL
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current config"""
    return jsonify({
        'n8n_url': N8N_WEBHOOK_URL,
        'version': '2.0-hardcoded'
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎤 Voice Server - HARD-CODED ngrok")
    print("="*60)
    print(f"\n✅ n8n URL: {N8N_WEBHOOK_URL}")
    print("\n🚀 Starting on http://localhost:5001\n")
    
    app.run(host='127.0.0.1', port=5001, debug=False)
