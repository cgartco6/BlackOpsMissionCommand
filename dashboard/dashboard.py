import pygame
import json
import os
from analytics_ui import AnalyticsUI
from revenue_report import RevenueReport
from player_tracking import PlayerTracker

class Dashboard:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 800))
        pygame.display.set_caption("Black Ops Mission Command - Admin Dashboard")
        self.clock = pygame.time.Clock()
        
        # Dashboard modules
        self.analytics_ui = AnalyticsUI()
        self.revenue_report = RevenueReport()
        self.player_tracker = PlayerTracker()
        self.growth_dashboard = GrowthDashboard()
        
        # Navigation
        self.current_tab = "analytics"
        self.tabs = {
            "analytics": "Game Analytics",
            "revenue": "Revenue Report",
            "players": "Player Tracking",
            "growth": "Growth Dashboard"
        }
    
    def run(self):
        running = True
        while running:
            self.screen.fill((30, 30, 50))
            
            # Draw tabs
            self.draw_tabs()
            
            # Draw current tab content
            if self.current_tab == "analytics":
                self.analytics_ui.draw(self.screen)
            elif self.current_tab == "revenue":
                self.revenue_report.draw(self.screen)
            elif self.current_tab == "players":
                self.player_tracker.draw(self.screen)
            elif self.current_tab == "growth":
                self.growth_dashboard.draw(self.screen)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(pygame.mouse.get_pos())
            
            pygame.display.flip()
            self.clock.tick(30)
        
        pygame.quit()
    
    def draw_tabs(self):
        tab_width = 1200 // len(self.tabs)
        for i, (tab_id, tab_name) in enumerate(self.tabs.items()):
            color = (70, 100, 150) if tab_id == self.current_tab else (50, 70, 100)
            pygame.draw.rect(self.screen, color, (i * tab_width, 0, tab_width, 40))
            
            font = pygame.font.SysFont("Arial", 20)
            text = font.render(tab_name, True, (255, 255, 255))
            self.screen.blit(text, (i * tab_width + 20, 10))
    
    def handle_click(self, pos):
        x, y = pos
        if y < 40:  # Clicked on tab bar
            tab_width = 1200 // len(self.tabs)
            tab_index = x // tab_width
            self.current_tab = list(self.tabs.keys())[tab_index]

if __name__ == "__main__":
    dashboard = Dashboard()
    dashboard.run()
