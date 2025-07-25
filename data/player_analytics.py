import pygame
from config import *
from data_loader import get_player_analytics

class PlayerAnalyticsDashboard:
    def __init__(self):
        self.analytics = get_player_analytics()
        self.font = pygame.font.Font("assets/fonts/default.ttf", 22)
        self.title_font = pygame.font.Font("assets/fonts/default.ttf", 36)
        self.header_font = pygame.font.Font("assets/fonts/default.ttf", 28)
        
    def render(self, screen):
        """Render the player analytics dashboard"""
        # Draw title
        title = self.title_font.render("Player Analytics Dashboard", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        # Draw metrics overview
        self._draw_metrics_overview(screen, 50, 100)
        
        # Draw distributions
        self._draw_distribution_charts(screen, 50, 300)
        
        # Draw player segments
        self._draw_player_segments(screen, SCREEN_WIDTH//2 + 50, 300)
    
    def _draw_metrics_overview(self, screen, x, y):
        """Render key metrics overview"""
        # Draw section header
        header = self.header_font.render("Key Player Metrics", True, (100, 200, 255))
        screen.blit(header, (x, y))
        y += 50
        
        # Draw metrics grid
        metrics = [
            ("Total Players", self.analytics["activity"]["total_players"]),
            ("Active Players (7d)", self.analytics["activity"]["active_players"]),
            ("Avg Session", f"{self.analytics['activity']['avg_session']} min"),
            ("Avg Playtime", f"{self.analytics['activity']['avg_playtime']} hours"),
            ("Premium Players", f"{self.analytics['activity']['premium_percent']}%"),
            ("Total Revenue", f"${self.analytics['financial']['total_revenue']:,.2f}"),
            ("ARPU", f"${self.analytics['financial']['arpu']}"),
            ("ARPPU", f"${self.analytics['financial']['arppu']}")
        ]
        
        # Draw metrics in a grid
        for i, (label, value) in enumerate(metrics):
            row = i // 2
            col = i % 2
            pos_x = x + col * 300
            pos_y = y + row * 60
            
            # Draw metric card
            pygame.draw.rect(screen, (40, 45, 60), (pos_x, pos_y, 280, 50), 0, 5)
            pygame.draw.rect(screen, (70, 80, 110), (pos_x, pos_y, 280, 50), 2, 5)
            
            # Draw label and value
            label_text = self.font.render(label, True, (180, 180, 220))
            value_text = self.font.render(str(value), True, (100, 255, 200))
            
            screen.blit(label_text, (pos_x + 15, pos_y + 8))
            screen.blit(value_text, (pos_x + 15, pos_y + 28))
    
    def _draw_distribution_charts(self, screen, x, y):
        """Render distribution charts"""
        # Draw section header
        header = self.header_font.render("Player Distributions", True, (100, 200, 255))
        screen.blit(header, (x, y))
        y += 50
        
        # Draw country distribution
        self._draw_pie_chart(
            screen, x, y, 200, 
            self.analytics["geo_distribution"], 
            "Country Distribution"
        )
        
        # Draw platform distribution
        self._draw_pie_chart(
            screen, x + 300, y, 200, 
            self.analytics["platform_distribution"], 
            "Platform Distribution"
        )
        
        # Draw level distribution
        self._draw_bar_chart(
            screen, x + 600, y, 400, 200,
            self.analytics["level_distribution"],
            "Level Distribution"
        )
    
    def _draw_pie_chart(self, screen, x, y, size, data, title):
        """Draw a pie chart"""
        # Draw chart background
        pygame.draw.circle(screen, (30, 35, 45), (x + size//2, y + size//2), size//2)
        pygame.draw.circle(screen, (60, 70, 90), (x + size//2, y + size//2), size//2, 2)
        
        # Draw title
        title_text = self.font.render(title, True, TEXT_COLOR)
        screen.blit(title_text, (x + size//2 - title_text.get_width()//2, y + size + 10))
        
        # Calculate total
        total = sum(data.values())
        if total == 0:
            return
            
        # Draw pie slices
        colors = [
            (0, 150, 200), (0, 200, 150), (200, 150, 0), 
            (200, 0, 100), (150, 0, 200), (0, 200, 200),
            (200, 100, 0), (100, 0, 200), (200, 0, 150)
        ]
        
        start_angle = 0
        items = list(data.items())
        
        for i, (label, value) in enumerate(items):
            # Calculate angle for this slice
            angle = 360 * (value / total)
            color = colors[i % len(colors)]
            
            # Draw pie slice
            pygame.draw.arc(
                screen, color, 
                (x, y, size, size),
                start_angle * (3.14/180), 
                (start_angle + angle) * (3.14/180),
                size//2
            )
            
            # Draw legend
            percent = value / total * 100
            pygame.draw.rect(screen, color, (x + size + 10, y + 20 + i * 25, 15, 15))
            label_text = self.font.render(f"{label} ({percent:.1f}%)", True, TEXT_COLOR)
            screen.blit(label_text, (x + size + 30, y + 20 + i * 25))
            
            start_angle += angle
    
    def _draw_bar_chart(self, screen, x, y, width, height, data, title):
        """Draw a bar chart"""
        # Draw chart background
        pygame.draw.rect(screen, (30, 35, 45), (x, y, width, height), 0)
        pygame.draw.rect(screen, (60, 70, 90), (x, y, width, height), 2)
        
        # Draw title
        title_text = self.font.render(title, True, TEXT_COLOR)
        screen.blit(title_text, (x + width//2 - title_text.get_width()//2, y + 10))
        
        # Draw bars
        max_value = max(data.values())
        bar_width = width // (len(data) + 2)
        colors = [(0, 180, 240), (0, 220, 180), (220, 180, 0), (220, 0, 120), (180, 0, 220), (0, 220, 220)]
        
        for i, (label, value) in enumerate(data.items()):
            bar_height = (value / max_value) * (height - 60)
            bar_x = x + (i + 1) * bar_width
            bar_y = y + height - 20 - bar_height
            
            # Draw bar
            pygame.draw.rect(
                screen, colors[i % len(colors)],
                (bar_x, bar_y, bar_width * 0.8, bar_height)
            )
            
            # Draw value
            value_text = self.font.render(str(value), True, TEXT_COLOR)
            screen.blit(value_text, (bar_x + bar_width * 0.4 - value_text.get_width()//2, bar_y - 25))
            
            # Draw label
            label_text = self.font.render(label, True, TEXT_COLOR)
            screen.blit(label_text, (bar_x + bar_width * 0.4 - label_text.get_width()//2, y + height - 15))
    
    def _draw_player_segments(self, screen, x, y):
        """Render player segments"""
        # Draw section header
        header = self.header_font.render("Player Segments", True, (100, 200, 255))
        screen.blit(header, (x, y))
        y += 50
        
        # Define player segments
        segments = [
            {
                "name": "New Players",
                "description": "Level 1-10, <5 hours playtime",
                "size": self.analytics["level_distribution"]["1-10"] * 0.7,
                "color": (0, 150, 200)
            },
            {
                "name": "Casual Players",
                "description": "Level 11-30, 5-20 hours playtime",
                "size": self.analytics["level_distribution"]["11-20"] + self.analytics["level_distribution"]["21-30"],
                "color": (0, 200, 150)
            },
            {
                "name": "Core Players",
                "description": "Level 31-50, 20-100 hours playtime",
                "size": self.analytics["level_distribution"]["31-40"] + self.analytics["level_distribution"]["41-50"],
                "color": (200, 150, 0)
            },
            {
                "name": "Hardcore Players",
                "description": "Level 51+, >100 hours playtime",
                "size": self.analytics["level_distribution"]["51+"],
                "color": (200, 0, 100)
            },
            {
                "name": "Premium Players",
                "description": "Spent >$50 in the game",
                "size": self.analytics["financial"]["premium_count"],
                "color": (150, 0, 200)
            }
        ]
        
        # Draw segment cards
        for i, segment in enumerate(segments):
            segment_y = y + i * 90
            
            # Draw card background
            pygame.draw.rect(screen, (40, 45, 60), (x, segment_y, 500, 80), 0, 5)
            pygame.draw.rect(screen, (70, 80, 110), (x, segment_y, 500, 80), 2, 5)
            
            # Draw color indicator
            pygame.draw.rect(screen, segment["color"], (x + 10, segment_y + 10, 10, 60))
            
            # Draw segment info
            name_text = self.font.render(segment["name"], True, TEXT_COLOR)
            screen.blit(name_text, (x + 30, segment_y + 15))
            
            desc_text = self.font.render(segment["description"], True, (180, 180, 220))
            screen.blit(desc_text, (x + 30, segment_y + 40))
            
            size_text = self.font.render(f"{segment['size']} players", True, (100, 255, 200))
            screen.blit(size_text, (x + 400, segment_y + 30))
