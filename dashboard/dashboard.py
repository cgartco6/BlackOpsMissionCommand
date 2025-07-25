import pygame
import random
import sys
from config import *
from analytics_ui import AnalyticsUI
from revenue_report import RevenueReport
from player_tracking import PlayerTracking

class AnalyticsDashboard:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("BlackOpsMissionCommand - Analytics Dashboard")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Initialize dashboard components
        self.analytics_ui = AnalyticsUI()
        self.revenue_report = RevenueReport()
        self.player_tracking = PlayerTracking()
        
        # Set initial state
        self.current_tab = "analytics"
        self.tabs = {
            "analytics": "Game Analytics",
            "revenue": "Revenue Report",
            "players": "Player Tracking"
        }
        
        # Initialize with fake data
        self._generate_initial_data()
        
    def _generate_initial_data(self):
        """Generate initial data for all dashboards"""
        self.analytics_ui.update_data({
            "active_players": random.randint(5000, 10000),
            "avg_session": random.randint(25, 45),
            "retention": random.randint(30, 60),
            "dau": random.randint(10000, 50000),
            "mau": random.randint(200000, 500000)
        })
        
        self.revenue_report.update_data({
            "daily_revenue": random.uniform(5000, 20000),
            "total_revenue": random.uniform(500000, 2000000),
            "arpu": random.uniform(1.50, 5.00),
            "conversion": random.uniform(1.5, 4.5),
            "top_product": "Elite Pack"
        })
        
        self.player_tracking.update_data({
            "total_players": random.randint(500000, 1000000),
            "new_players": random.randint(5000, 15000),
            "sessions": random.randint(50000, 200000),
            "avg_session": random.randint(20, 40),
            "completion": random.randint(15, 35)
        })
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_1:
                    self.current_tab = "analytics"
                elif event.key == pygame.K_2:
                    self.current_tab = "revenue"
                elif event.key == pygame.K_3:
                    self.current_tab = "players"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self._check_tab_click(mouse_x, mouse_y)
                    
        return True
    
    def _check_tab_click(self, x, y):
        """Check if a tab was clicked"""
        tab_width = SCREEN_WIDTH // len(self.tabs)
        for i, (tab_id, tab_name) in enumerate(self.tabs.items()):
            tab_rect = (i * tab_width, 0, tab_width, 60)
            if tab_rect[0] <= x <= tab_rect[0] + tab_rect[2] and tab_rect[1] <= y <= tab_rect[1] + tab_rect[3]:
                self.current_tab = tab_id
    
    def _update_data(self):
        """Update data with small random variations"""
        if self.current_tab == "analytics":
            self.analytics_ui.update_data({
                "active_players": max(0, self.analytics_ui.data["active_players"] + random.randint(-50, 100)),
                "avg_session": max(1, self.analytics_ui.data["avg_session"] + random.randint(-1, 1)),
                "retention": max(0, min(100, self.analytics_ui.data["retention"] + random.randint(-1, 1)))
            })
        elif self.current_tab == "revenue":
            self.revenue_report.update_data({
                "daily_revenue": max(0, self.revenue_report.data["daily_revenue"] + random.uniform(-100, 300))
            })
        elif self.current_tab == "players":
            self.player_tracking.update_data({
                "total_players": max(0, self.player_tracking.data["total_players"] + random.randint(-50, 200)),
                "new_players": max(0, self.player_tracking.data["new_players"] + random.randint(-10, 50))
            })
    
    def _render_tabs(self):
        """Render navigation tabs"""
        tab_width = SCREEN_WIDTH // len(self.tabs)
        
        for i, (tab_id, tab_name) in enumerate(self.tabs.items()):
            # Draw tab background
            color = (60, 70, 100) if tab_id == self.current_tab else (40, 45, 60)
            pygame.draw.rect(self.screen, color, (i * tab_width, 0, tab_width, 60), 0)
            
            # Draw tab border
            pygame.draw.rect(self.screen, (80, 90, 120), (i * tab_width, 0, tab_width, 60), 2)
            
            # Draw tab text
            font = pygame.font.Font("assets/fonts/default.ttf", 24)
            text = font.render(tab_name, True, TEXT_COLOR)
            self.screen.blit(text, (i * tab_width + tab_width//2 - text.get_width()//2, 20))
            
            # Draw tab shortcut
            shortcut = font.render(f"[{i+1}]", True, (150, 200, 255))
            self.screen.blit(shortcut, (i * tab_width + tab_width - 40, 20))
    
    def _render_footer(self):
        """Render dashboard footer"""
        pygame.draw.rect(self.screen, (30, 35, 45), (0, SCREEN_HEIGHT - 40, SCREEN_WIDTH, 40), 0)
        pygame.draw.line(self.screen, (60, 70, 90), (0, SCREEN_HEIGHT - 40), (SCREEN_WIDTH, SCREEN_HEIGHT - 40), 2)
        
        font = pygame.font.Font("assets/fonts/default.ttf", 18)
        footer_text = font.render("BlackOpsMissionCommand Analytics Dashboard | Press ESC to exit", True, (150, 160, 180))
        self.screen.blit(footer_text, (20, SCREEN_HEIGHT - 30))
        
        # Draw auto-update indicator
        update_text = font.render("Live Data", True, (0, 200, 100))
        pygame.draw.circle(self.screen, (0, 200, 100), (SCREEN_WIDTH - 90, SCREEN_HEIGHT - 20), 5)
        self.screen.blit(update_text, (SCREEN_WIDTH - 80, SCREEN_HEIGHT - 30))
    
    def render(self):
        """Main rendering function"""
        # Draw background
        self.screen.fill((25, 30, 40))
        
        # Draw tabs
        self._render_tabs()
        
        # Draw current dashboard
        if self.current_tab == "analytics":
            self.analytics_ui.render(self.screen)
        elif self.current_tab == "revenue":
            self.revenue_report.render(self.screen)
        elif self.current_tab == "players":
            self.player_tracking.render(self.screen)
        
        # Draw footer
        self._render_footer()
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        running = True
        last_update = pygame.time.get_ticks()
        
        while running:
            running = self.handle_events()
            
            # Update data every 3 seconds
            current_time = pygame.time.get_ticks()
            if current_time - last_update > 3000:
                self._update_data()
                last_update = current_time
            
            self.render()
            self.clock.tick(FPS)
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    dashboard = AnalyticsDashboard()
    dashboard.run()
