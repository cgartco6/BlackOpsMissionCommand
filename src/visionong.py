import math
import numpy as np
from config import MAP_WIDTH, MAP_HEIGHT, TILE_SIZE

class VisionSystem:
    def __init__(self, game_map):
        self.game_map = game_map
        self.visible = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=bool)
        self.explored = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=bool)
        self.sight_range = 8  # Default vision radius

    def update_vision(self, observer_pos):
        """Update visible and explored tiles using raycasting"""
        self.visible.fill(False)
        x0, y0 = observer_pos
        
        # Scan through 360 degrees
        for angle in range(0, 360, 2):  # Step by 2 degrees for optimization
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            
            # Cast ray with small increments
            for distance in range(1, self.sight_range + 1):
                x = int(x0 + dx * distance)
                y = int(y0 + dy * distance)
                
                # Stop if out of bounds
                if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
                    break
                
                # Mark as visible and explored
                self.visible[x, y] = True
                self.explored[x, y] = True
                
                # Stop ray at obstacles
                if self.game_map.is_obstacle(x, y):
                    break

    def is_visible(self, pos):
        """Check if position is currently visible"""
        x, y = pos
        return self.visible[x, y]

    def get_fow_render(self):
        """Generate fog-of-war overlay for rendering"""
        fow = np.zeros((MAP_WIDTH, MAP_HEIGHT, 3), dtype=np.uint8)
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if self.visible[x, y]:
                    fow[x, y] = [0, 0, 0]  # Visible = transparent
                elif self.explored[x, y]:
                    fow[x, y] = [50, 50, 70]  # Explored = dark blue
                else:
                    fow[x, y] = [20, 20, 30]  # Unexplored = darker
        return fow

    def reset_exploration(self):
        """Reset map exploration (for new missions)"""
        self.explored.fill(False)
        self.visible.fill(False)
