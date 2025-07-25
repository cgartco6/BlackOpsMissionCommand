import math
import numpy as np
import pygame

# Configuration Constants (adjust based on your game needs)
MAP_WIDTH = 50   # Grid cells wide
MAP_HEIGHT = 50  # Grid cells high
TILE_SIZE = 32   # Pixels per grid cell

class VisionSystem:
    def __init__(self, game_map):
        """
        Initialize the vision system
        :param game_map: 2D array representing the game map (0 = walkable, 1 = obstacle)
        """
        self.game_map = game_map
        self.visible = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=bool)
        self.explored = np.zeros((MAP_WIDTH, MAP_HEIGHT), dtype=bool)
        self.sight_range = 8  # Default vision radius
        self.fow_surface = None
        
    def update_vision(self, observer_pos):
        """
        Update visible and explored tiles using raycasting
        :param observer_pos: (x, y) tuple of observer's grid position
        """
        self.visible.fill(False)
        x0, y0 = observer_pos
        
        # If out of bounds, return early
        if not (0 <= x0 < MAP_WIDTH and 0 <= y0 < MAP_HEIGHT):
            return
            
        # Mark observer's position as visible
        self.visible[x0, y0] = True
        self.explored[x0, y0] = True
        
        # Scan through 360 degrees
        for angle in range(0, 360, 2):  # Step by 2 degrees
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
                if self.game_map[x][y] == 1:  # 1 represents obstacle
                    break
                    
        # Invalidate cached fog surface
        self.fow_surface = None

    def is_visible(self, pos):
        """
        Check if position is currently visible
        :param pos: (x, y) grid position
        :return: Boolean visibility status
        """
        x, y = pos
        if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
            return self.visible[x, y]
        return False

    def get_fow_surface(self):
        """
        Generate fog-of-war overlay surface
        :return: Pygame surface with fog of war
        """
        if self.fow_surface:
            return self.fow_surface
            
        # Create new surface with per-pixel alpha
        self.fow_surface = pygame.Surface(
            (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE), 
            pygame.SRCALPHA
        )
        
        # Draw fog based on visibility states
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                if not self.explored[x, y]:
                    # Unexplored - dark gray
                    pygame.draw.rect(
                        self.fow_surface, (30, 30, 40, 240),
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
                elif not self.visible[x, y]:
                    # Explored but not visible - medium gray
                    pygame.draw.rect(
                        self.fow_surface, (60, 60, 80, 200),
                        (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    )
                # Visible areas remain transparent
                    
        return self.fow_surface

    def reset_exploration(self):
        """Reset map exploration (for new missions)"""
        self.explored.fill(False)
        self.visible.fill(False)
        self.fow_surface = None

# Example usage with PyGame dashboard
class GameDashboard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(
            (MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE)
        )
        pygame.display.set_caption("BlackOpsMissionCommand - Tactical Dashboard")
        self.clock = pygame.time.Clock()
        
        # Generate a sample map (0 = empty, 1 = obstacle)
        self.game_map = np.random.choice(
            [0, 1], size=(MAP_WIDTH, MAP_HEIGHT), p=[0.7, 0.3]
        ).tolist()
        
        # Create vision system
        self.vision = VisionSystem(self.game_map)
        self.player_pos = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.vision.update_vision(self.player_pos)
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                x, y = self.player_pos
                if event.key == pygame.K_UP and y > 0:
                    self.player_pos = (x, y-1)
                elif event.key == pygame.K_DOWN and y < MAP_HEIGHT-1:
                    self.player_pos = (x, y+1)
                elif event.key == pygame.K_LEFT and x > 0:
                    self.player_pos = (x-1, y)
                elif event.key == pygame.K_RIGHT and x < MAP_WIDTH-1:
                    self.player_pos = (x+1, y)
                elif event.key == pygame.K_r:
                    self.vision.reset_exploration()
                    
                self.vision.update_vision(self.player_pos)
        return True
        
    def render(self):
        # Draw terrain
        self.screen.fill((40, 40, 50))  # Dark background
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if self.game_map[x][y] == 1:
                    pygame.draw.rect(self.screen, (80, 70, 60), rect)  # Obstacles
                else:
                    pygame.draw.rect(self.screen, (50, 60, 40), rect)  # Ground
                    
        # Draw player
        px, py = self.player_pos
        pygame.draw.circle(
            self.screen, (0, 255, 0),
            (px * TILE_SIZE + TILE_SIZE//2, py * TILE_SIZE + TILE_SIZE//2),
            TILE_SIZE//3
        )
        
        # Draw fog of war
        self.screen.blit(self.vision.get_fow_surface(), (0, 0))
        
        # Draw UI elements
        font = pygame.font.SysFont(None, 24)
        text = font.render("Arrow keys: Move | R: Reset Fog of War", True, (255, 255, 255))
        self.screen.blit(text, (10, 10))
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(60)
            
if __name__ == "__main__":
    dashboard = GameDashboard()
    dashboard.run()
    pygame.quit()
