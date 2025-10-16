#!/usr/bin/env python3
"""
Voice Assistant Service for n8n Integration
Handles voice input, intent classification, and response generation
Optimized for Windows 11 + WSL2 + AMD GPU + i9 CPU
"""

import asyncio
import time
import logging
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import json

import numpy as np
from faster_whisper import WhisperModel
import ollama
import aiohttp
import yaml
from dotenv import load_dotenv
import colorlog

# Load environment variables
load_dotenv()

# Setup colorful logging
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    log_colors={
        'DEBUG': 'cyan',
        'INFO': 'green',
        'WARNING': 'yellow',
        'ERROR': 'red',
        'CRITICAL': 'red,bg_white',
    }
))

logger = logging.getLogger('VoiceAssistant')
logger.addHandler(handler)
logger.setLevel(os.getenv('LOG_LEVEL', 'INFO'))


class VoiceAssistantService:
    """Main voice processing service optimized for i9 CPU"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        logger.info("=" * 60)
        logger.info("🎙️  Voice Assistant Service Starting")
        logger.info("=" * 60)
        
        # Load configuration
        try:
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except FileNotFoundError:
            logger.error(f"Config file not found: {config_path}")
            logger.error("Please run the installation script first!")
            sys.exit(1)
        
        # Initialize Whisper (CPU-optimized for i9)
        logger.info("Loading Whisper model (CPU-optimized for i9)...")
        start = time.time()
        self.whisper = WhisperModel(
            os.getenv('WHISPER_MODEL', 'base.en'),
            device=os.getenv('WHISPER_DEVICE', 'cpu'),
            compute_type=os.getenv('WHISPER_COMPUTE_TYPE', 'int8'),
            num_workers=4,  # Utilize i9 cores
            cpu_threads=8   # i9 can handle this
        )
        logger.info(f"✓ Whisper loaded in {time.time()-start:.2f}s")
        
        # Ollama configuration
        ollama_host = os.getenv('OLLAMA_HOST')
        logger.info(f"Connecting to Ollama at {ollama_host}")
        self.ollama = ollama.AsyncClient(host=ollama_host)
        
        # Test Ollama connection
        self._test_ollama_connection()
        
        # Model configuration
        self.models = self.config['models']
        
        # Intent cache
        self.intent_cache = self.config.get('intent_cache', {})
        
        # n8n webhook
        self.n8n_webhook = os.getenv('N8N_WEBHOOK_URL')
        
        # Performance tracking
        self.stats = {
            'total_requests': 0,
            'avg_latency': 0,
            'intents': {'HOME_CONTROL': 0, 'TOOLS': 0, 'CONVERSATION': 0}
        }
        
        logger.info("✓ Voice Assistant Service ready!")
        logger.info("=" * 60)
    
    def _test_ollama_connection(self):
        """Test connection to Ollama"""
        try:
            import requests
            ollama_host = os.getenv('OLLAMA_HOST')
            response = requests.get(f"{ollama_host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get('models', [])
                logger.info(f"✓ Ollama connected. Available models: {len(models)}")
            else:
                logger.warning(f"Ollama connection issue: {response.status_code}")
        except Exception as e:
            logger.error(f"Cannot connect to Ollama: {e}")
            logger.error("Make sure Ollama is running on Windows and accessible from WSL")
            logger.error("See docs/TROUBLESHOOTING.md for help")
            sys.exit(1)
    
    async def classify_intent(self, text: str) -> str:
        """Fast intent classification with caching"""
        start_time = time.time()
        
        # Check cache first (5-10ms)
        text_lower = text.lower()
        for phrase, intent in self.intent_cache.items():
            if phrase in text_lower:
                elapsed = time.time() - start_time
                logger.info(f"🎯 Intent (cached): {intent} ({elapsed*1000:.0f}ms)")
                return intent
        
        # Use LLM classifier (50-100ms)
        try:
            model_config = self.models['classifier']
            prompt = f"""Classify this query into exactly ONE category:
HOME_CONTROL - controlling devices, lights, temperature, locks
TOOLS - email, calendar, timers, alarms, reminders
CONVERSATION - questions, information, chat

Query: {text}
Category:"""
            
            response = await self.ollama.generate(
                model=model_config['name'],
                prompt=prompt,
                options={
                    'num_predict': model_config['max_tokens'],
                    'temperature': model_config['temperature'],
                    'top_k': 1
                }
            )
            
            intent = response['response'].strip().upper()
            
            # Validate
            if intent not in ['HOME_CONTROL', 'TOOLS', 'CONVERSATION']:
                intent = 'CONVERSATION'
            
            elapsed = time.time() - start_time
            logger.info(f"🎯 Intent (LLM): {intent} ({elapsed*1000:.0f}ms)")
            
            return intent
        
        except Exception as e:
            logger.error(f"Intent classification error: {e}")
            return 'CONVERSATION'
    
    async def home_assistant_agent(self, text: str) -> str:
        """Fast home automation control"""
        start_time = time.time()
        
        try:
            model_config = self.models['home_assistant']
            
            # Get device list from config
            devices = self.config.get('home_assistant', {}).get('devices', {})
            device_list = []
            for category, items in devices.items():
                device_list.extend(items)
            
            prompt = f"""You control smart home devices. Parse this command and respond naturally.

Available devices: {', '.join(device_list)}

Command: {text}

Respond briefly what you did (max 1 sentence)."""
            
            response = await self.ollama.generate(
                model=model_config['name'],
                prompt=prompt,
                options={
                    'num_predict': model_config['max_tokens'],
                    'temperature': model_config['temperature']
                }
            )
            
            result = response['response'].strip()
            
            elapsed = time.time() - start_time
            logger.info(f"🏠 HA Agent response ({elapsed*1000:.0f}ms)")
            
            return result
        
        except Exception as e:
            logger.error(f"HA agent error: {e}")
            return "I had trouble controlling that device."
    
    async def conversation_agent(self, text: str) -> str:
        """General conversation"""
        start_time = time.time()
        
        try:
            model_config = self.models['conversation']
            
            prompt = f"""You are a helpful voice assistant. Answer briefly and naturally.

User: {text}
Assistant:"""
            
            response = await self.ollama.generate(
                model=model_config['name'],
                prompt=prompt,
                options={
                    'num_predict': model_config['max_tokens'],
                    'temperature': model_config['temperature']
                }
            )
            
            result = response['response'].strip()
            
            elapsed = time.time() - start_time
            logger.info(f"💬 Conversation Agent response ({elapsed*1000:.0f}ms)")
            
            return result
        
        except Exception as e:
            logger.error(f"Conversation agent error: {e}")
            return "I'm having trouble responding right now."
    
    async def execute_tools_async(self, text: str):
        """Execute n8n tools asynchronously"""
        try:
            logger.info(f"🔧 Executing n8n tools for: '{text}'")
            
            async with aiohttp.ClientSession() as session:
                payload = {
                    "text": text,
                    "intent": "TOOLS",
                    "source": "voice_satellite",
                    "timestamp": time.time()
                }
                
                async with session.post(
                    self.n8n_webhook,
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as resp:
                    if resp.status == 200:
                        result = await resp.json()
                        logger.info(f"✓ n8n tool execution complete: {result}")
                    else:
                        logger.warning(f"n8n returned status {resp.status}")
        
        except asyncio.TimeoutError:
            logger.error("n8n execution timeout")
        except Exception as e:
            logger.error(f"n8n execution error: {e}")


async def test_mode():
    """Test the service with sample queries"""
    logger.info("Running in TEST mode")
    service = VoiceAssistantService()
    
    # Test text inputs
    test_queries = [
        "Turn on the living room lights",
        "What's the weather like today?",
        "Send an email to John"
    ]
    
    for query in test_queries:
        logger.info(f"\n{'='*60}")
        logger.info(f"Testing: {query}")
        logger.info(f"{'='*60}")
        
        # Classify intent
        intent = await service.classify_intent(query)
        
        # Execute based on intent
        if intent == "HOME_CONTROL":
            response = await service.home_assistant_agent(query)
        elif intent == "CONVERSATION":
            response = await service.conversation_agent(query)
        elif intent == "TOOLS":
            asyncio.create_task(service.execute_tools_async(query))
            response = "I'm working on that right now."
        else:
            response = "I'm not sure how to help with that."
        
        logger.info(f"Response: {response}")
        await asyncio.sleep(1)
    
    logger.info(f"\n{'='*60}")
    logger.info("Test complete!")
    logger.info(f"{'='*60}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        asyncio.run(test_mode())
    else:
        logger.info("Usage: python voice_service.py test")
        logger.info("(Full Wyoming server implementation coming next)")
