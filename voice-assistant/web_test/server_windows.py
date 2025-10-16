#!/usr/bin/env python3
"""
Windows-native Flask server for voice assistant web testing
Runs on Windows directly (not WSL) to avoid RDP audio issues
"""
import os
import base64
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

# Add parent directory to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("WARNING: faster-whisper not installed. Install with: pip install faster-whisper")

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Configuration
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL", "http://172.22.32.1:32768/webhook/voice-assistant")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base.en")

# Initialize Whisper if available
whisper_model = None
if WHISPER_AVAILABLE:
    print("Loading Whisper model...")
    try:
        whisper_model = WhisperModel(
            WHISPER_MODEL,
            device="cpu",
            compute_type="int8"
        )
        print("✓ Whisper model loaded")
    except Exception as e:
        print(f"Failed to load Whisper: {e}")


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio using Faster-Whisper"""
    if not whisper_model:
        return "[Whisper not available]"
    
    try:
        segments, info = whisper_model.transcribe(audio_path, beam_size=5)
        text = " ".join([segment.text for segment in segments]).strip()
        return text
    except Exception as e:
        print(f"Transcription error: {e}")
        return f"[Error: {e}]"


def call_n8n_webhook(text: str, intent: str = "CONVERSATION") -> dict:
    """Call n8n webhook"""
    try:
        resp = requests.post(
            N8N_WEBHOOK,
            json={"text": text, "intent": intent, "source": "web_test"},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"n8n returned status {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}


@app.route('/')
def index():
    """Serve the main page"""
    return send_from_directory('.', 'index.html')


@app.route('/api/test')
def test_connection():
    """Test endpoint for connection checking"""
    return jsonify({
        'success': True,
        'message': 'Server is running',
        'n8n_configured': bool(N8N_WEBHOOK),
        'whisper_available': WHISPER_AVAILABLE
    })


@app.route('/api/chat', methods=['POST'])
def handle_chat():
    """Handle text-only chat (no audio transcription)"""
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                'success': False,
                'error': 'No text provided'
            }), 400
        
        text = data['text']
        print(f"Chat input: {text}")
        
        # Send to n8n
        try:
            n8n_response = call_n8n_webhook(text, "CONVERSATION")
            print(f"n8n response: {n8n_response}")
            
            # Extract response text
            if isinstance(n8n_response, dict):
                response_text = n8n_response.get('output') or n8n_response.get('message') or str(n8n_response)
            else:
                response_text = str(n8n_response)
                
        except Exception as e:
            print(f"n8n webhook error: {e}")
            return jsonify({
                'success': False,
                'error': f"n8n error: {str(e)}"
            }), 500
        
        return jsonify({
            'success': True,
            'response': response_text
        })
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/voice', methods=['POST'])
def handle_voice():
    """Handle voice input from browser"""
    try:
        # Get audio file from request
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_audio:
            audio_file.save(temp_audio.name)
            temp_audio_path = temp_audio.name
        
        try:
            # Check file size
            file_size = os.path.getsize(temp_audio_path)
            print(f"Received audio file: {file_size} bytes")
            
            if file_size < 1000:
                return jsonify({
                    'success': False,
                    'error': 'Audio file too small - please record for at least 1 second',
                    'transcript': ''
                })
            
            # Try converting with ffmpeg if available
            wav_path = temp_audio_path.replace('.webm', '.wav')
            
            try:
                import subprocess
                subprocess.run([
                    'ffmpeg', '-i', temp_audio_path,
                    '-ar', '16000',  # 16kHz sample rate
                    '-ac', '1',       # Mono
                    '-y',             # Overwrite
                    wav_path
                ], check=True, capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
                print(f"Converted to WAV: {wav_path}")
            except (subprocess.CalledProcessError, FileNotFoundError):
                # Use original file if conversion fails
                print("Using original audio format (no ffmpeg conversion)")
                wav_path = temp_audio_path
            
            # Transcribe
            print(f"Transcribing audio from {wav_path}...")
            transcript = transcribe_audio(wav_path)
            print(f"Transcript: {transcript}")
            
            if not transcript or len(transcript.strip()) < 2 or transcript == "[Whisper not available]":
                return jsonify({
                    'success': False,
                    'error': 'Could not transcribe audio - please speak clearly and record for longer',
                    'transcript': transcript or ''
                })
            
            # Send to n8n
            print(f"Sending to n8n: {transcript}")
            try:
                n8n_response = call_n8n_webhook(transcript, "CONVERSATION")
                print(f"n8n response: {n8n_response}")
                
                # Extract response text
                if isinstance(n8n_response, dict):
                    response_text = n8n_response.get('output') or n8n_response.get('message') or str(n8n_response)
                else:
                    response_text = str(n8n_response)
                    
            except Exception as e:
                print(f"n8n webhook error: {e}")
                response_text = f"Error communicating with n8n: {str(e)}"
            
            return jsonify({
                'success': True,
                'transcript': transcript,
                'response': response_text,
                'audio_base64': None  # TTS not implemented on Windows version
            })
            
        finally:
            # Clean up temp files
            try:
                os.unlink(temp_audio_path)
                if wav_path != temp_audio_path and os.path.exists(wav_path):
                    os.unlink(wav_path)
            except:
                pass
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e),
            'transcript': ''
        }), 500


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎤 Voice Assistant Web Test Server (Windows)")
    print("="*60)
    print(f"Whisper Available: {WHISPER_AVAILABLE}")
    print(f"Whisper Model: {WHISPER_MODEL if WHISPER_AVAILABLE else 'Not installed'}")
    print(f"n8n Webhook: {N8N_WEBHOOK}")
    print("="*60)
    print("\nStarting server on http://localhost:5000")
    print("Open http://localhost:5000 in your browser to test!\n")
    
    app.run(host='127.0.0.1', port=5000, debug=True)
