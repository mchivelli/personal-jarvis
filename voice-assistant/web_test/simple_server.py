#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Flask server that ONLY forwards messages to remote n8n
No local Ollama, Whisper, or processing needed
"""
import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env from parent directory
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Remote n8n webhook URL (loaded from .env file)
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL", "http://192.168.0.244:32768/webhook/voice-assistant")
print(f"[CONFIG] Using n8n webhook: {N8N_WEBHOOK_URL}")

@app.route('/')
def index():
    """Serve the voice chat page - with cache busting"""
    import time
    # Read the HTML file
    with open('voice_chat.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Add version timestamp to force reload
    html_content = html_content.replace('</title>', f'</title><meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate"><meta http-equiv="Pragma" content="no-cache"><meta http-equiv="Expires" content="0">')
    
    from flask import Response
    response = Response(html_content, mimetype='text/html')
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/api/chat', methods=['POST'])
def handle_chat():
    """Forward text to n8n and return response"""
    try:
        data = request.json
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'success': False, 'error': 'No text provided'}), 400
        
        print(f"📤 Sending to n8n: {text}")
        print(f"🌐 Using URL: {N8N_WEBHOOK_URL}")
        
        # Send to remote n8n
        try:
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
                print(f"📥 n8n response: {response_text}")
                
                return jsonify({
                    'success': True,
                    'response': response_text
                })
            else:
                error_msg = f"n8n returned status {response.status_code}"
                print(f"❌ {error_msg}")
                return jsonify({'success': False, 'error': error_msg}), 500
                
        except requests.exceptions.Timeout:
            error_msg = "n8n request timeout"
            print(f"❌ {error_msg}")
            return jsonify({'success': False, 'error': error_msg}), 504
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"Cannot connect to n8n: {str(e)}"
            print(f"❌ {error_msg}")
            return jsonify({'success': False, 'error': 'Cannot connect to n8n server'}), 503
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_connection():
    """Test connection to n8n"""
    print(f"[DEBUG] Test endpoint called, using URL: {N8N_WEBHOOK_URL}")
    try:
        response = requests.post(
            N8N_WEBHOOK_URL,
            json={"text": "connection test", "test": True},
            timeout=5
        )
        return jsonify({
            'success': True,
            'status': response.status_code,
            'n8n_url': N8N_WEBHOOK_URL
        })
    except Exception as e:
        print(f"[ERROR] Test connection failed: {e}")
        return jsonify({
            'success': False,
            'error': str(e),
            'n8n_url': N8N_WEBHOOK_URL
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    return jsonify({
        'n8n_url': N8N_WEBHOOK_URL,
        'env_loaded': env_path.exists(),
        'env_path': str(env_path)
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎤 Simple Voice Chat Server")
    print("="*60)
    print(f"Remote n8n: {N8N_WEBHOOK_URL}")
    print("="*60)
    print("\n✓ No local Ollama needed")
    print("✓ No local Whisper needed")
    print("✓ Browser handles speech recognition")
    print("✓ Only forwards to remote n8n\n")
    print("Starting server on http://localhost:5000")
    print("Open http://localhost:5000 in your browser to test!\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
