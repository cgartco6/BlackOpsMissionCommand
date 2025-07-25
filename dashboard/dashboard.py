# dashboard/dashboard.py
import pygame
import numpy as np
from config import *
from visioning import VisionSystem
from game_map import GameMap

class TacticalDashboard:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(GAME_TITLE)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font("assets/fonts/default.ttf", 24)
        
        # Game state
        self.game_map = GameMap()
        self.vision = VisionSystem(self.game_map)
        self.player_pos = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.enemies = self.generate_enemies(5)
        self.vision.update_vision(self.player_pos)
        
    def generate_enemies(self, count):
        """Generate enemy positions"""
        enemies = []
        for _ in range(count):
            while True:
                x = np.random.randint(5, MAP_WIDTH - 5)
                y = np.random.randint(5, MAP_HEIGHT - 5)
                # Ensure enemies aren't too close to player
                if (abs(x - self.player_pos[0]) > 10 or 
                    abs(y - self.player_pos[1]) > 10) and not self.game_map.is_obstacle(x, y):
                    enemies.append((x, y))
                    break
        return enemies
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                x, y = self.player_pos
                if event.key == pygame.K_UP and y > 0 and not self.game_map.is_obstacle(x, y-1):
                    self.player_pos = (x, y-1)
                elif event.key == pygame.K_DOWN and y < MAP_HEIGHT-1 and not self.game_map.is_obstacle(x, y+1):
                    self.player_pos = (x, y+1)
                elif event.key == pygame.K_LEFT and x > 0 and not self.game_map.is_obstacle(x-1, y):
                    self.player_pos = (x-1, y)
                elif event.key == pygame.K_RIGHT and x < MAP_WIDTH-1 and not self.game_map.is_obstacle(x+1, y):
                    self.player_pos = (x+1, y)
                elif event.key == pygame.K_r:
                    self.vision.reset_exploration()
                elif event.key == pygame.K_ESCAPE:
                    return False
                    
                self.vision.update_vision(self.player_pos)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // TILE_SIZE
                    grid_y = mouse_y // TILE_SIZE
                    if 0 <= grid_x < MAP_WIDTH and 0 <= grid_y < MAP_HEIGHT:
                        self.player_pos = (grid_x, grid_y)
                        self.vision.update_vision(self.player_pos)
        return True
        
    def render_map(self):
        """Render the game map"""
        map_data = self.game_map.get_render_data()
        for x in range(MAP_WIDTH):
            for y in range(MAP_HEIGHT):
                rect = (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                if map_data[x][y] == 1:
                    pygame.draw.rect(self.screen, OBSTACLE, rect)
                else:
                    pygame.draw.rect(self.screen, GROUND, rect)
                    
                # Draw grid
                pygame.draw.rect(self.screen, GRID_COLOR, rect, 1)
    
    def render_entities(self):
        """Render player and enemies"""
        # Draw enemies
        for ex, ey in self.enemies:
            if self.vision.is_visible((ex, ey)):
                pygame.draw.circle(
                    self.screen, ENEMY_COLOR,
                    (ex * TILE_SIZE + TILE_SIZE//2, ey * TILE_SIZE + TILE_SIZE//2),
                    TILE_SIZE//3
                )
        
        # Draw player
        px, py = self.player_pos
        pygame.draw.circle(
            self.screen, PLAYER_COLOR,
            (px * TILE_SIZE + TILE_SIZE//2, py * TILE_SIZE + TILE_SIZE//2),
            TILE_SIZE//2
        )
    
    def render_ui(self):
        """Render the dashboard UI"""
        # UI background
        ui_rect = (0, SCREEN_HEIGHT - UI_HEIGHT, SCREEN_WIDTH, UI_HEIGHT)
        pygame.draw.rect(self.screen, UI_BG, ui_rect)
        pygame.draw.line(
            self.screen, (80, 80, 100), 
            (0, SCREEN_HEIGHT - UI_HEIGHT), 
            (SCREEN_WIDTH, SCREEN_HEIGHT - UI_HEIGHT), 
            3
        )
        
        # UI text
        controls = [
            "CONTROLS:",
            "Arrow Keys - Move",
            "Mouse Click - Teleport",
            "R - Reset Fog of War",
            "ESC - Quit"
        ]
        
        for i, text in enumerate(controls):
            rendered = self.font.render(text, True, TEXT_COLOR)
            self.screen.blit(rendered, (20, SCREEN_HEIGHT - UI_HEIGHT + 10 + i * 25))
            
        # Stats
        visible = np.sum(self.vision.visible)
        explored = np.sum(self.vision.explored)
        total = MAP_WIDTH * MAP_HEIGHT
        stats = f"VISIBLE: {visible}/{total} | EXPLORED: {explored}/{total}"
        rendered = self.font.render(stats, True, (150, 200, 255))
        self.screen.blit(rendered, (SCREEN_WIDTH - 400, SCREEN_HEIGHT - 30))
    
    def render(self):
        """Main rendering function"""
        self.screen.fill(BACKGROUND)
        self.render_map()
        self.render_entities()
        self.screen.blit(self.vision.get_fow_surface(), (0, 0))
        self.render_ui()
        pygame.display.flip()
        
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = TacticalDashboard()
    game.run()
