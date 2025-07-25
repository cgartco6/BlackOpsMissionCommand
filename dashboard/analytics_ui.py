import pygame
import numpy as np
from config import *

class AnalyticsUI:
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/default.ttf", 20)
        self.title_font = pygame.font.Font("assets/fonts/default.ttf", 32)
        self.data = {
            "active_players": 0,
            "avg_session": 0,
            "retention": 0,
            "dau": 0,
            "mau": 0
        }
        self.chart_data = []
        self.max_chart_value = 100
        
    def update_data(self, new_data):
        """Update analytics data"""
        self.data.update(new_data)
        
        # Update chart data
        self.chart_data.append(self.data["active_players"])
        if len(self.chart_data) > 10:
            self.chart_data.pop(0)
            
        # Update max chart value
        if self.data["active_players"] > self.max_chart_value:
            self.max_chart_value = self.data["active_players"]
        
    def render(self, screen):
        """Render analytics dashboard"""
        # Draw title
        title = self.title_font.render("Game Analytics Dashboard", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        # Draw metrics
        self._draw_metric(screen, "Active Players", self.data["active_players"], 100, 80)
        self._draw_metric(screen, "Avg Session (min)", self.data["avg_session"], 100, 140)
        self._draw_metric(screen, "Retention (%)", self.data["retention"], 100, 200)
        self._draw_metric(screen, "DAU", self.data["dau"], 100, 260)
        self._draw_metric(screen, "MAU", self.data["mau"], 100, 320)
        
        # Draw chart
        self._draw_chart(screen, SCREEN_WIDTH//2, 100, 500, 300)
        
    def _draw_metric(self, screen, label, value, x, y):
        """Render a single metric"""
        label_text = self.font.render(label, True, TEXT_COLOR)
        value_text = self.font.render(str(value), True, (100, 255, 200))
        
        screen.blit(label_text, (x, y))
        screen.blit(value_text, (x + 200, y))
        
        # Draw progress bar
        pygame.draw.rect(screen, (50, 50, 70), (x + 300, y, 200, 20), 0)
        if value > 0:
            pygame.draw.rect(screen, (0, 200, 150), (x + 300, y, 200 * min(1, value/100), 20), 0)
    
    def _draw_chart(self, screen, x, y, width, height):
        """Render player activity chart"""
        # Draw chart background
        pygame.draw.rect(screen, (30, 35, 45), (x, y, width, height), 0)
        pygame.draw.rect(screen, (60, 70, 90), (x, y, width, height), 2)
        
        # Draw title
        chart_title = self.font.render("Player Activity (Last 10 Updates)", True, TEXT_COLOR)
        screen.blit(chart_title, (x + width//2 - chart_title.get_width()//2, y + 10))
        
        # Draw grid lines
        for i in range(1, 5):
            pygame.draw.line(screen, (50, 55, 65), 
                            (x, y + i * height//5), 
                            (x + width, y + i * height//5), 1)
        
        # Draw data points
        if not self.chart_data:
            return
            
        point_width = width / (len(self.chart_data) - 1)
        points = []
        
        for i, value in enumerate(self.chart_data):
            x_pos = x + i * point_width
            y_pos = y + height - (value / self.max_chart_value) * (height - 40)
            points.append((x_pos, y_pos))
            
            # Draw data point
            pygame.draw.circle(screen, (0, 200, 150), (x_pos, y_pos), 5)
            
            # Draw value label
            if i == len(self.chart_data) - 1:
                value_text = self.font.render(str(value), True, (100, 255, 200))
                screen.blit(value_text, (x_pos - value_text.get_width()//2, y_pos - 25))
        
        # Draw line connecting points
        if len(points) > 1:
            pygame.draw.lines(screen, (0, 180, 140), False, points, 2)
