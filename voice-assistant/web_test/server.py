#!/usr/bin/env python3
"""
Simple Flask server for voice assistant web testing
"""
import os
import sys
import base64
import tempfile
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
import asyncio
import aiohttp

# Add parent directory to path to import voice_service
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import from voice_service
from faster_whisper import WhisperModel
import subprocess
import yaml

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

# Load configuration
CONFIG_PATH = Path(__file__).parent.parent / "config" / "config.yaml"
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

# Initialize Whisper
print("Loading Whisper model...")
whisper_model = WhisperModel(
    os.getenv("WHISPER_MODEL", "base.en"),
    device=os.getenv("WHISPER_DEVICE", "cpu"),
    compute_type=os.getenv("WHISPER_COMPUTE_TYPE", "int8")
)
print("✓ Whisper model loaded")

# Piper TTS path
PIPER_MODEL = os.getenv("PIPER_MODEL_PATH")
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL")


def transcribe_audio(audio_path: str) -> str:
    """Transcribe audio using Faster-Whisper"""
    segments, info = whisper_model.transcribe(audio_path, beam_size=5)
    text = " ".join([segment.text for segment in segments]).strip()
    return text


def synthesize_speech(text: str) -> bytes:
    """Synthesize speech using Piper TTS"""
    try:
        if not PIPER_MODEL or not os.path.exists(PIPER_MODEL):
            print(f"Warning: Piper model not found at {PIPER_MODEL}")
            return None
            
        # Run piper TTS
        result = subprocess.run(
            ["piper", "--model", PIPER_MODEL, "--output-raw"],
            input=text,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.encode() if result.stdout else None
    except Exception as e:
        print(f"TTS error: {e}")
        return None


async def call_n8n_webhook(text: str, intent: str = "CONVERSATION") -> dict:
    """Call n8n webhook"""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                N8N_WEBHOOK,
                json={"text": text, "intent": intent, "source": "web_test"},
                timeout=aiohttp.ClientTimeout(total=30)
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                else:
                    return {"error": f"n8n returned status {resp.status}"}
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
        'whisper_available': True
    })


@app.route('/api/chat', methods=['POST'])
async def handle_chat():
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
            n8n_response = await call_n8n_webhook(text, "CONVERSATION")
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
        
        # Save to temp file with original extension first
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_audio:
            audio_file.save(temp_audio.name)
            temp_audio_path = temp_audio.name
        
        # Convert to WAV using ffmpeg if needed
        wav_path = temp_audio_path.replace('.webm', '.wav')
        
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
            
            # Convert to WAV using ffmpeg
            try:
                subprocess.run([
                    'ffmpeg', '-i', temp_audio_path,
                    '-ar', '16000',  # 16kHz sample rate
                    '-ac', '1',       # Mono
                    '-y',             # Overwrite
                    wav_path
                ], check=True, capture_output=True)
                print(f"Converted to WAV: {wav_path}")
            except subprocess.CalledProcessError:
                # If ffmpeg fails, try using the file as-is
                print("FFmpeg conversion failed, trying original file...")
                wav_path = temp_audio_path
            except FileNotFoundError:
                print("FFmpeg not found, trying original file...")
                wav_path = temp_audio_path
            
            # Transcribe
            print(f"Transcribing audio from {wav_path}...")
            transcript = transcribe_audio(wav_path)
            print(f"Transcript: {transcript}")
            
            if not transcript or len(transcript.strip()) < 2:
                return jsonify({
                    'success': False,
                    'error': 'Could not transcribe audio - please speak clearly and record for longer',
                    'transcript': transcript or ''
                })
            
            # Send to n8n
            print(f"Sending to n8n: {transcript}")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            n8n_response = loop.run_until_complete(
                call_n8n_webhook(transcript, "CONVERSATION")
            )
            loop.close()
            
            print(f"n8n response: {n8n_response}")
            
            # Extract response text (adjust based on your n8n output)
            response_text = n8n_response.get('output', n8n_response.get('message', 'I received your message.'))
            
            # Synthesize speech
            audio_bytes = synthesize_speech(response_text)
            audio_base64 = base64.b64encode(audio_bytes).decode() if audio_bytes else None
            
            return jsonify({
                'success': True,
                'transcript': transcript,
                'response': response_text,
                'audio_base64': audio_base64
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
    print("🎤 Voice Assistant Web Test Server")
    print("="*60)
    print(f"Whisper Model: {os.getenv('WHISPER_MODEL', 'base.en')}")
    print(f"Piper Model: {PIPER_MODEL or 'Not configured'}")
    print(f"n8n Webhook: {N8N_WEBHOOK}")
    print("="*60)
    print("\nStarting server on http://localhost:5000")
    print("Open http://localhost:5000 in your browser to test!\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
