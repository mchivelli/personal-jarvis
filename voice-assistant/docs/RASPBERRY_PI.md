# Raspberry Pi Satellite Setup

## Installation

```bash
# On RPi
ssh pi@voice-satellite.local
mkdir ~/voice-satellite && cd ~/voice-satellite
python3 -m venv venv
source venv/bin/activate
pip install wyoming-satellite
```

## Start Satellite

```bash
# Get server IP from WSL: hostname -I
python3 -m wyoming_satellite \
    --name "echo" \
    --uri tcp://YOUR_SERVER_IP:10300 \
    --mic-device default \
    --snd-device default
```

## Auto-Start

Create systemd service for automatic startup on boot.
