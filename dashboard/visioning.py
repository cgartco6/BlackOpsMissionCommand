# dashboard/visioning.py
import math
import numpy as np
import pygame
from config import MAP_WIDTH, MAP_HEIGHT, SIGHT_RANGE, FOW_UNEXPLORED, FOW_EXPLORED

class VisionSystem:
    def __init__(self, game_map):
        self.game_map = game_map
        self.visible = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=bool)
        self.explored = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=bool)
        self.sight_range = SIGHT_RANGE
        self.fow_surface = None
        
    def update_vision(self, observer_pos):
        """Update visible and explored tiles using raycasting"""
        self.visible.fill(False)
        x0, y0 = observer_pos
        
        if not (0 <= x0 < MAP_WIDTH and 0 <= y0 < MAP_HEIGHT):
            return
            
        # Mark observer position
        self.visible[x0, y0] = True
        self.explored[x0, y0] = True
        
        # Scan through 360 degrees
        for angle in range(0, 360, 2):  # Step by 2 degrees
            rad = math.radians(angle)
            dx = math.cos(rad)
            dy = math.sin(rad)
            
            # Cast ray
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
                    
        # Invalidate cached fog surface
        self.fow_surface = None

    def is_visible(self, pos):
        """Check if position is currently visible"""
        x, y = pos
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            return self.visible[x, y]
        return False

    def get_fow_surface(self):
        """Generate fog-of-war overlay surface"""
        if self.fow_surface:
            return self.fow_surface
            
        # Create surface with per-pixel alpha
        from config import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
        self.fow_surface = pygame.Surface(
            (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE), 
            pygame.SRCALPHA
        )
        
        # Draw fog based on visibility
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if not self.explored[x, y]:
                    pygame.draw.rect(
                        self.fow_surface, FOW_UNEXPLORED,
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
                elif not self.visible[x, y]:
                    pygame.draw.rect(
                        self.fow_surface, FOW_EXPLORED,
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
                    
        return self.fow_surface

    def reset_exploration(self):
        """Reset map exploration"""
        self.explored.fill(False)
        self.visible.fill(False)
        self.fow_surface = None
