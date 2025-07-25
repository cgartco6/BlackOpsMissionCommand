# dashboard/game_map.py
import numpy as np
from config import MAP_WIDTH, MAP_HEIGHT, OBSTACLE_DENSITY

class GameMap:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.grid = self.generate_map()
        
    def generate_map(self):
        """Generate a random map with obstacles"""
        # 0 = walkable, 1 = obstacle
        grid = np.zeros((self.width, self.height), dtype=int)
        
        # Add random obstacles
        for x in range(self.width):
            for y in range(self.height):
                if np.random.random() < OBSTACLE_DENSITY:
                    grid[x][y] = 1
        
        # Ensure center is walkable
        center_x, center_y = self.width // 2, self.height // 2
        grid[center_x-2:center_x+3, center_y-2:center_y+3] = 0
        
        return grid.tolist()
    
    def is_obstacle(self, x, y):
        """Check if a position is an obstacle"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[x][y] == 1
        return True  # Out of bounds counts as obstacle
    
    def get_render_data(self):
        """Get map data for rendering"""
        return self.grid
