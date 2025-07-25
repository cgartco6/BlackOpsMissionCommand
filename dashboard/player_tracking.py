import pygame
import random
from config import *

class PlayerTracking:
    def __init__(self):
        self.font = pygame.font.Font("assets/fonts/default.ttf", 20)
        self.title_font = pygame.font.Font("assets/fonts/default.ttf", 28)
        self.data = {
            "total_players": 0,
            "new_players": 0,
            "sessions": 0,
            "avg_session": 0,
            "completion": 0
        }
        self.player_locations = []
        
    def update_data(self, new_data):
        """Update player tracking data"""
        self.data.update(new_data)
        
        # Generate fake player locations
        if random.random() < 0.4 or not self.player_locations:
            self.player_locations = []
            for _ in range(min(100, self.data["total_players"])):
                self.player_locations.append((
                    random.randint(50, SCREEN_WIDTH - 50),
                    random.randint(200, SCREEN_HEIGHT - 200)
                ))
        
    def render(self, screen):
        """Render player tracking dashboard"""
        # Draw title
        title = self.title_font.render("Player Tracking", True, TEXT_COLOR)
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
        
        # Draw metrics
        self._draw_metric(screen, "Total Players", self.data["total_players"], 100, 80)
        self._draw_metric(screen, "New Players (24h)", self.data["new_players"], 100, 140)
        self._draw_metric(screen, "Sessions (24h)", self.data["sessions"], 100, 200)
        self._draw_metric(screen, "Avg Session (min)", self.data["avg_session"], 100, 260)
        self._draw_metric(screen, "Mission Completion", f"{self.data['completion']}%", 100, 320)
        
        # Draw world map
        self._draw_world_map(screen, SCREEN_WIDTH//2 - 250, 380, 500, 300)
        
        # Draw heatmap
        self._draw_heatmap(screen, 100, 700, SCREEN_WIDTH - 200, 150)
    
    def _draw_metric(self, screen, label, value, x, y):
        """Render a single metric"""
        label_text = self.font.render(label, True, TEXT_COLOR)
        value_text = self.font.render(str(value), True, (150, 200, 255))
        
        screen.blit(label_text, (x, y))
        screen.blit(value_text, (x + 300, y))
        
        # Draw icon
        icon_size = 30
        pygame.draw.circle(screen, (50, 100, 150), (x + 250, y + icon_size//2), icon_size//2)
    
    def _draw_world_map(self, screen, x, y, width, height):
        """Render player distribution map"""
        # Draw map background
        pygame.draw.rect(screen, (20, 30, 40), (x, y, width, height), 0)
        pygame.draw.rect(screen, (60, 80, 100), (x, y, width, height), 2)
        
        # Draw title
        title = self.font.render("Player Geographic Distribution", True, TEXT_COLOR)
        screen.blit(title, (x + width//2 - title.get_width()//2, y + 10))
        
        # Draw continent outlines
        continents = [
            {"name": "NA", "rect": (x + width//8, y + height//3, width//6, height//3)},
            {"name": "EU", "rect": (x + width//2.5, y + height//4, width//5, height//3)},
            {"name": "AS", "rect": (x + width//1.7, y + height//3, width//4, height//3)},
            {"name": "SA", "rect": (x + width//3, y + height//1.7, width//5, height//3)},
            {"name": "OC", "rect": (x + width//1.3, y + height//1.5, width//6, height//4)}
        ]
        
        for continent in continents:
            pygame.draw.rect(screen, (40, 60, 80), continent["rect"], 1)
            name_text = self.font.render(continent["name"], True, (100, 150, 200))
            screen.blit(name_text, (
                continent["rect"][0] + continent["rect"][2]//2 - name_text.get_width()//2,
                continent["rect"][1] + continent["rect"][3]//2 - name_text.get_height()//2
            ))
        
        # Draw player dots
        for px, py in self.player_locations:
            if x <= px <= x + width and y <= py <= y + height:
                pygame.draw.circle(screen, (0, 200, 255), (px, py), 3)
    
    def _draw_heatmap(self, screen, x, y, width, height):
        """Render player activity heatmap"""
        # Draw section background
        pygame.draw.rect(screen, (30, 35, 45), (x, y, width, height), 0)
        pygame.draw.rect(screen, (60, 70, 90), (x, y, width, height), 2)
        
        # Draw title
        title = self.font.render("Daily Activity Heatmap (UTC)", True, TEXT_COLOR)
        screen.blit(title, (x + width//2 - title.get_width()//2, y + 10))
        
        # Draw heatmap grid
        cell_size = 30
        cols = 8
        rows = 6
        start_x = x + (width - cols * cell_size) // 2
        start_y = y + 40
        
        # Draw hour labels
        hours = ["00", "04", "08", "12", "16", "20"]
        for i, hour in enumerate(hours):
            hour_text = self.font.render(hour, True, TEXT_COLOR)
            screen.blit(hour_text, (start_x - 30, start_y + i * cell_size + cell_size//3))
        
        # Draw day labels
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            day_text = self.font.render(day, True, TEXT_COLOR)
            screen.blit(day_text, (start_x + i * cell_size + cell_size//4, start_y - 30))
        
        # Draw heat cells
        for col in range(cols):
            for row in range(rows):
                cell_x = start_x + col * cell_size
                cell_y = start_y + row * cell_size
                
                # Generate fake activity data
                activity = random.randint(0, 100)
                if col == 5 and row == 2:  # Peak time
                    activity = random.randint(70, 100)
                
                # Determine color based on activity level
                if activity < 20:
                    color = (30, 50, 70)
                elif activity < 40:
                    color = (50, 80, 120)
                elif activity < 60:
                    color = (70, 120, 180)
                elif activity < 80:
                    color = (90, 160, 220)
                else:
                    color = (100, 200, 255)
                
                pygame.draw.rect(screen, color, (cell_x, cell_y, cell_size, cell_size), 0)
                pygame.draw.rect(screen, (40, 50, 60), (cell_x, cell_y, cell_size, cell_size), 1)
                
                # Draw activity percentage
                if activity > 20:
                    activity_text = self.font.render(f"{activity}%", True, (20, 20, 30))
                    screen.blit(activity_text, 
                              (cell_x + cell_size//2 - activity_text.get_width()//2,
                               cell_y + cell_size//2 - activity_text.get_height()//2))
