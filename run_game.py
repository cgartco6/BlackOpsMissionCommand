#!/usr/bin/env python3
"""
Black Ops: Mission Command - Game Launcher
"""
import sys
import os
import platform
import subprocess
import argparse
import pygame
from src.versioning import get_version
from src.game.ai_agents.agent_orchestrator import AIOrchestrator

def setup_environment():
    """Configure environment for optimal performance"""
    # Add src directory to Python path
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # Set Pygame environment variables
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
    
    # Platform-specific optimizations
    system = platform.system()
    if system == "Windows":
        # Enable high DPI awareness
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    elif system == "Darwin":  # macOS
        os.environ['PYGAME_MAC_FULLSCREEN'] = "1"
    
    # Initialize self-healing
    self_heal()

def self_heal():
    """Self-healing system to recover from common issues"""
    try:
        # Check for required data files
        required_dirs = ["data/player_data", "data/transaction_logs", "data/models", "data/marketing"]
        for dir_path in required_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
        
        # Create default config if missing
        if not os.path.exists("config.ini"):
            create_default_config()
    
    except Exception as e:
        print(f"Self-healing failed: {e}")

def create_default_config():
    """Create default configuration file"""
    from configparser import ConfigParser
    config = ConfigParser()
    
    # Game settings
    config['GAME'] = {
        'TOKENS_PER_DAY': '3',
        'ADS_PER_DAY': '3',
        'BASE_DIFFICULTY': '3'
    }
    
    # Monetization settings
    config['MONETIZATION'] = {
        'PAYPAL_EMAIL': 'your.paypal@email.com',
        'AD_NETWORK': 'high_cpm',
        'SUBSCRIPTION_PRICES': '4.99,9.99',
        'UPGRADE_PRICES': '4.99,9.99,19.99'
    }
    
    # AI agents settings
    config['AI_AGENTS'] = {
        'ENABLED': 'true',
        'MARKETING_PLATFORMS': 'tiktok,instagram,facebook,twitter,youtube_shorts,snapchat',
        'FREE_AI_TOOLS': 'huggingface,stablediffusion,openai-free-tier'
    }
    
    # Player settings
    config['PLAYERS'] = {
        'COUNT': '0'
    }
    
    # Launch settings
    config['LAUNCH'] = {
        'DATE': '2023-01-01'  # Will be updated on first run
    }
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def main():
    parser = argparse.ArgumentParser(description='Black Ops: Mission Command')
    parser.add_argument('--player', type=str, default="default", help='Player ID')
    parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen mode')
    parser.add_argument('--resolution', type=str, default="1000x700", 
                        help='Set custom resolution (e.g. 1280x720)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Store arguments in environment
    os.environ['GAME_PLAYER_ID'] = args.player
    os.environ['GAME_FULLSCREEN'] = str(args.fullscreen)
    os.environ['GAME_RESOLUTION'] = args.resolution
    os.environ['GAME_DEBUG'] = str(args.debug)
    
    try:
        from src.main import main as run_game
        # Initialize AI Orchestrator
        game_version = get_version()
        ai_orchestrator = AIOrchestrator(game_version)
        ai_orchestrator.start()
        
        # Run the game
        run_game()
    except Exception as e:
        print(f"Fatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        
        # Attempt self-healing
        self_heal()
        print("Attempting to restart game...")
        subprocess.Popen([sys.executable, __file__] + sys.argv[1:])

if __name__ == "__main__":
    setup_environment()
    main()
