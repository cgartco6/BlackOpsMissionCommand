#!/usr/bin/env python3
"""
Black Ops: Mission Command - Platform Launcher
"""
import sys
import os
import platform
import subprocess
import argparse

def setup_environment():
    """Configure environment variables and paths"""
    # Add src directory to Python path
    src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'src'))
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)
    
    # Set Pygame environment variables
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
    
    # Platform-specific configurations
    system = platform.system()
    if system == "Windows":
        # Enable high DPI awareness on Windows
        try:
            import ctypes
            ctypes.windll.user32.SetProcessDPIAware()
        except:
            pass
    
    # Check for required dependencies
    try:
        import pygame
    except ImportError:
        install_dependencies()

def install_dependencies():
    """Install required Python packages"""
    print("Installing required dependencies...")
    requirements_file = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", requirements_file])
        print("Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("Failed to install dependencies. Please install manually:")
        print(f"  pip install -r {requirements_file}")
        sys.exit(1)

def check_python_version():
    """Verify Python version meets requirements"""
    if sys.version_info < (3, 8):
        print("Python 3.8 or newer is required to run this game.")
        print(f"Your current Python version: {sys.version}")
        print("Please upgrade your Python installation.")
        sys.exit(1)

def main():
    """Main entry point for the game"""
    parser = argparse.ArgumentParser(description='Black Ops: Mission Command')
    parser.add_argument('--fullscreen', action='store_true', help='Run in fullscreen mode')
    parser.add_argument('--resolution', type=str, default="1000x700", 
                        help='Set custom resolution (e.g. 1280x720)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    args = parser.parse_args()
    
    # Store arguments in environment for game to access
    os.environ['GAME_FULLSCREEN'] = str(args.fullscreen)
    os.environ['GAME_RESOLUTION'] = args.resolution
    os.environ['GAME_DEBUG'] = str(args.debug)
    
    try:
        from main import main as run_game
        run_game()
    except ImportError as e:
        print(f"Error: {e}")
        print("The game files might be missing or corrupted.")
        print("Please ensure the 'src' directory exists with all game files.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Check Python version first
    check_python_version()
    
    # Configure environment
    setup_environment()
    
    # Launch the game
    main()
