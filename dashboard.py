import pygame
import sys
from config import *
from player_analytics import PlayerAnalyticsDashboard

class PlayerDataDashboard:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("BlackOpsMissionCommand - Player Data Dashboard")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Initialize dashboard components
        self.analytics_dashboard = PlayerAnalyticsDashboard()
        
        # Navigation
        self.current_view = "analytics"
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True
    
    def render(self):
        """Main rendering function"""
        # Draw background
        self.screen.fill((25, 30, 40))
        
        # Draw current view
        if self.current_view == "analytics":
            self.analytics_dashboard.render(self.screen)
        
        # Draw footer
        self._render_footer()
        
        pygame.display.flip()
    
    def _render_footer(self):
        """Render dashboard footer"""
        pygame.draw.rect(self.screen, (30, 35, 45), (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), 0)
        pygame.draw.line(self.screen, (60, 70, 90), (0, SCREEN_HEIGHT - 40), (SCREEN_WIDTH, SCREEN_HEIGHT - 40), 2)
        
        font = pygame.font.Font("assets/fonts/default.ttf", 18)
        footer_text = font.render("BlackOpsMissionCommand Player Data Dashboard | Press ESC to exit", True, (150, 160, 180))
        self.screen.blit(footer_text, (20, SCREEN_HEIGHT - 30))
        
        # Draw data freshness indicator
        update_text = font.render("Data Updated: Today", True, (100, 255, 150))
        self.screen.blit(update_text, (SCREEN_WIDTH - 200, SCREEN_HEIGHT - 30))
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            running = self.handle_events()
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    dashboard = PlayerDataDashboard()
    dashboard.run()
