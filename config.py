# Root directory configuration
import os

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Data directories
DATA_DIR = os.path.join(BASE_DIR, "data")
PLAYER_DATA_FILE = os.path.join(DATA_DIR, "player_data.json")

# Analytics settings
PLAYER_SAMPLE_SIZE = 10000
