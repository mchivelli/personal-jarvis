#!/bin/bash
set -e

echo "================================"
echo "Voice Assistant Installation"
echo "================================"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

cd "$PROJECT_DIR"
echo "Installing in: $PROJECT_DIR"
echo ""

# Detect Windows host
echo "Detecting Windows host..."
WINDOWS_HOST=$(ip route | grep default | awk '{print $3}')
echo "Windows Host IP: $WINDOWS_HOST"
echo ""

# Test Ollama connection
echo "Testing Ollama connection..."
if curl -s -m 5 http://$WINDOWS_HOST:11434/api/tags > /dev/null 2>&1; then
    echo "✓ Ollama is accessible!"
else
    echo "✗ Cannot reach Ollama at $WINDOWS_HOST:11434"
    echo ""
    echo "Please configure Ollama first:"
    echo "1. Open PowerShell as Administrator"
    echo "2. Run: [System.Environment]::SetEnvironmentVariable('OLLAMA_HOST', '0.0.0.0:11434', 'User')"
    echo "3. Run: New-NetFirewallRule -DisplayName \"Ollama WSL\" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 11434"
    echo "4. Restart Ollama"
    echo ""
    echo "See docs/INSTALLATION.md for details"
    exit 1
fi
echo ""

# Check Python 3.11
if ! command -v python3.11 &> /dev/null; then
    echo "Installing Python 3.11..."
    sudo apt update -qq
    sudo apt install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update -qq
    sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
    echo "✓ Python 3.11 installed"
else
    echo "✓ Python 3.11 found"
fi
echo ""

# Install system dependencies
echo "Installing system dependencies..."
sudo apt install -y \
    build-essential \
    git \
    curl \
    wget \
    ffmpeg \
    portaudio19-dev \
    libsndfile1 \
    sox \
    pkg-config \
    > /dev/null 2>&1
echo "✓ System dependencies installed"
echo ""

# Create virtual environment
echo "Creating Python virtual environment..."
python3.11 -m venv venv
source venv/bin/activate
echo "✓ Virtual environment created"
echo ""

# Install Python packages
echo "Installing Python packages (this may take a few minutes)..."
pip install -q --upgrade pip setuptools wheel
pip install -q -r requirements.txt
echo "✓ Python packages installed"
echo ""

# Create .env from template
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    sed -i "s|WINDOWS_HOST=.*|WINDOWS_HOST=$WINDOWS_HOST|g" .env
    sed -i "s|OLLAMA_HOST=.*|OLLAMA_HOST=http://$WINDOWS_HOST:11434|g" .env
    sed -i "s|PIPER_MODEL_PATH=.*|PIPER_MODEL_PATH=$PROJECT_DIR/models/piper_voices/en-us-lessac-medium.onnx|g" .env
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi
echo ""

# Download Whisper model
echo "Downloading Whisper model (~150MB, may take a few minutes)..."
mkdir -p models
cd models
python3 << 'EOFPY'
from faster_whisper import WhisperModel
import sys
try:
    model = WhisperModel("base.en", device="cpu", compute_type="int8", download_root="./whisper")
    print("✓ Whisper model downloaded")
except Exception as e:
    print(f"✗ Error downloading Whisper: {e}")
    sys.exit(1)
EOFPY
cd ..
echo ""

# Download Piper TTS
echo "Downloading Piper TTS..."
cd models
if [ ! -f ../bin/piper ]; then
    mkdir -p ../bin
    wget -q https://github.com/rhasspy/piper/releases/download/2023.11.14-2/piper_linux_x86_64.tar.gz
    tar -xzf piper_linux_x86_64.tar.gz
    mv piper/piper ../bin/
    chmod +x ../bin/piper
    rm -rf piper piper_linux_x86_64.tar.gz
    echo "✓ Piper binary installed"
else
    echo "✓ Piper binary already installed"
fi

if [ ! -d piper_voices ]; then
    mkdir -p piper_voices
    cd piper_voices
    wget -q https://github.com/rhasspy/piper/releases/download/v1.2.0/voice-en-us-lessac-medium.tar.gz
    tar -xzf voice-en-us-lessac-medium.tar.gz
    rm voice-en-us-lessac-medium.tar.gz
    echo "✓ Piper voice model downloaded"
    cd ..
else
    echo "✓ Piper voice model already installed"
fi
cd ..
echo ""

# Create logs directory
mkdir -p logs

echo ""
echo "================================"
echo "✓ Installation Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo ""
echo "1. Test the service:"
echo "   source venv/bin/activate"
echo "   python voice_service.py test"
echo ""
echo "2. Configure n8n webhook:"
echo "   See docs/N8N_INTEGRATION.md"
echo ""
echo "3. Set up RPi satellite (optional):"
echo "   See docs/RASPBERRY_PI.md"
echo ""
