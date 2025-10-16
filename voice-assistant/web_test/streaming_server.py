#!/usr/bin/env python3
"""
Real-time Streaming Voice Assistant Server
Supports interrupts, streaming transcription, and fluid conversation
"""
import os
import sys
import asyncio
import base64
import tempfile
import time
from pathlib import Path
from flask import Flask, render_template, send_from_directory, request
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import requests
import subprocess

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from faster_whisper import WhisperModel
    WHISPER_AVAILABLE = True
except ImportError:
    WHISPER_AVAILABLE = False
    print("WARNING: faster-whisper not installed")

app = Flask(__name__, static_folder='.', template_folder='.')
app.config['SECRET_KEY'] = 'voice-assistant-secret'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Configuration
N8N_WEBHOOK = os.getenv("N8N_WEBHOOK_URL", "http://172.22.32.1:32768/webhook/voice-assistant")
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "base.en")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://172.22.32.1:11434")

# Initialize Whisper
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

# Session state for each client
sessions = {}


class VoiceSession:
    """Manages state for a single voice conversation session"""
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.conversation_history = []
        self.is_processing = False
        self.should_interrupt = False
        self.current_response = ""
        
    def add_message(self, role, content):
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        
    def interrupt(self):
        """Signal to stop current processing"""
        self.should_interrupt = True
        self.is_processing = False


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


async def stream_ollama_response(prompt: str, session: VoiceSession, sid: str):
    """Stream response from Ollama with interrupt capability"""
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "qwen2.5:3b",
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200
                }
            },
            stream=True,
            timeout=30
        )
        
        full_response = ""
        for line in response.iter_lines():
            # Check for interrupt
            if session.should_interrupt:
                print(f"Response interrupted for session {sid}")
                socketio.emit('response_interrupted', {}, room=sid)
                break
                
            if line:
                import json
                data = json.loads(line)
                
                if 'response' in data:
                    chunk = data['response']
                    full_response += chunk
                    
                    # Send chunk to client
                    socketio.emit('response_chunk', {
                        'chunk': chunk,
                        'done': data.get('done', False)
                    }, room=sid)
                    
                    # Small delay to prevent overwhelming client
                    await asyncio.sleep(0.01)
                
                if data.get('done'):
                    break
        
        session.current_response = full_response
        session.add_message("assistant", full_response)
        return full_response
        
    except Exception as e:
        print(f"Ollama error: {e}")
        error_msg = f"Error: {str(e)}"
        socketio.emit('error', {'message': error_msg}, room=sid)
        return error_msg


def call_n8n_webhook(text: str, intent: str = "CONVERSATION") -> dict:
    """Call n8n webhook for tool execution"""
    try:
        resp = requests.post(
            N8N_WEBHOOK,
            json={"text": text, "intent": intent, "source": "streaming"},
            timeout=30
        )
        if resp.status_code == 200:
            return resp.json()
        else:
            return {"error": f"n8n returned status {resp.status_code}"}
    except Exception as e:
        return {"error": str(e)}


def detect_intent(text: str) -> str:
    """Quick intent detection based on keywords"""
    text_lower = text.lower()
    
    # Tool keywords
    if any(kw in text_lower for kw in ['send email', 'email', 'write email']):
        return "TOOLS"
    if any(kw in text_lower for kw in ['calendar', 'schedule', 'appointment', 'meeting']):
        return "TOOLS"
    if any(kw in text_lower for kw in ['contact', 'phone number', 'address']):
        return "TOOLS"
    if any(kw in text_lower for kw in ['search', 'look up', 'find on internet']):
        return "TOOLS"
    
    # Default to conversation
    return "CONVERSATION"


@app.route('/')
def index():
    """Serve the streaming UI"""
    return send_from_directory('.', 'streaming_ui.html')


@app.route('/api/test')
def test_connection():
    """Test endpoint"""
    return {
        'success': True,
        'message': 'Streaming server is running',
        'whisper_available': WHISPER_AVAILABLE,
        'n8n_configured': bool(N8N_WEBHOOK)
    }


@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connection"""
    sid = request.sid if hasattr(request, 'sid') else 'unknown'
    sessions[sid] = VoiceSession(sid)
    print(f"Client connected: {sid}")
    emit('connected', {'session_id': sid})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    sid = request.sid if hasattr(request, 'sid') else 'unknown'
    if sid in sessions:
        del sessions[sid]
    print(f"Client disconnected: {sid}")


@socketio.on('audio_data')
def handle_audio(data):
    """Handle incoming audio data"""
    sid = request.sid if hasattr(request, 'sid') else 'unknown'
    session = sessions.get(sid)
    
    if not session:
        emit('error', {'message': 'Session not found'})
        return
    
    try:
        # Get audio data
        audio_b64 = data.get('audio')
        if not audio_b64:
            emit('error', {'message': 'No audio data'})
            return
        
        # Decode audio
        audio_bytes = base64.b64decode(audio_b64)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(suffix='.webm', delete=False) as temp_audio:
            temp_audio.write(audio_bytes)
            temp_audio_path = temp_audio.name
        
        try:
            # Convert to WAV if ffmpeg available
            wav_path = temp_audio_path.replace('.webm', '.wav')
            try:
                subprocess.run([
                    'ffmpeg', '-i', temp_audio_path,
                    '-ar', '16000', '-ac', '1', '-y', wav_path
                ], check=True, capture_output=True, 
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0)
            except:
                wav_path = temp_audio_path
            
            # Transcribe
            emit('status', {'message': 'Transcribing...'})
            transcript = transcribe_audio(wav_path)
            
            if transcript and len(transcript) > 2:
                # Send transcript to client
                emit('transcript', {'text': transcript})
                session.add_message("user", transcript)
                
                # Detect intent
                intent = detect_intent(transcript)
                emit('intent', {'intent': intent})
                
                if intent == "TOOLS":
                    # Use n8n for tools
                    emit('status', {'message': 'Executing tools...'})
                    n8n_response = call_n8n_webhook(transcript, "TOOLS")
                    
                    response_text = n8n_response.get('output') or n8n_response.get('message', 'Tool executed')
                    
                    emit('response_complete', {'text': response_text})
                    session.add_message("assistant", response_text)
                    
                else:
                    # Stream conversation response
                    emit('status', {'message': 'Thinking...'})
                    session.is_processing = True
                    session.should_interrupt = False
                    
                    # Build context from history
                    context = "You are a helpful AI assistant. Be conversational and natural.\n\n"
                    if len(session.conversation_history) > 1:
                        context += "Previous conversation:\n"
                        for msg in session.conversation_history[-4:]:  # Last 4 messages
                            context += f"{msg['role']}: {msg['content']}\n"
                    
                    prompt = f"{context}\nuser: {transcript}\nassistant:"
                    
                    # Stream response (run in thread to not block)
                    import threading
                    def stream_response():
                        loop = asyncio.new_event_loop()
                        asyncio.set_event_loop(loop)
                        loop.run_until_complete(stream_ollama_response(prompt, session, sid))
                        loop.close()
                        session.is_processing = False
                    
                    thread = threading.Thread(target=stream_response)
                    thread.start()
            else:
                emit('error', {'message': 'Could not transcribe audio'})
            
        finally:
            # Cleanup temp files
            try:
                os.unlink(temp_audio_path)
                if wav_path != temp_audio_path and os.path.exists(wav_path):
                    os.unlink(wav_path)
            except:
                pass
    
    except Exception as e:
        print(f"Error processing audio: {e}")
        import traceback
        traceback.print_exc()
        emit('error', {'message': str(e)})


@socketio.on('interrupt')
def handle_interrupt():
    """Handle interrupt signal from client"""
    sid = request.sid if hasattr(request, 'sid') else 'unknown'
    session = sessions.get(sid)
    
    if session and session.is_processing:
        print(f"Interrupting session {sid}")
        session.interrupt()
        emit('interrupted', {'message': 'Response interrupted'})


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎙️ Real-Time Streaming Voice Assistant")
    print("="*60)
    print(f"Whisper Available: {WHISPER_AVAILABLE}")
    print(f"Whisper Model: {WHISPER_MODEL if WHISPER_AVAILABLE else 'Not installed'}")
    print(f"Ollama Host: {OLLAMA_HOST}")
    print(f"n8n Webhook: {N8N_WEBHOOK}")
    print("="*60)
    print("\nFeatures:")
    print("  ✓ Real-time streaming responses")
    print("  ✓ Interrupt capability")
    print("  ✓ Conversation history")
    print("  ✓ Intent detection")
    print("  ✓ n8n tool integration")
    print("="*60)
    print("\nStarting server on http://localhost:5002")
    print("Open http://localhost:5002 in your browser!\n")
    
    socketio.run(app, host='0.0.0.0', port=5002, debug=True, allow_unsafe_werkzeug=True)
