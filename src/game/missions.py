import pygame
from game.enemies import Enemy
from game.ui import *

class Mission:
    def __init__(self, title, description, location, difficulty, enemies):
        self.title = title
        self.description = description
        self.location = location
        self.difficulty = difficulty
        self.enemies = enemies
        self.completed = False
        self.unlocked = False
        
    def draw(self, surface, x, y, width, height, is_current=False):
        # Draw mission card
        color = ACCENT if is_current else DARK_GRAY
        pygame.draw.rect(surface, color, (x, y, width, height), 0, 15)
        pygame.draw.rect(surface, LIGHT_GRAY, (x, y, width, height), 2, 15)
        
        # Draw title
        title_text = subtitle_font.render(self.title, True, WHITE)
        surface.blit(title_text, (x+20, y+15))
        
        # Draw location
        loc_text = normal_font.render(f"Location: {self.location}", True, LIGHT_BLUE)
        surface.blit(loc_text, (x+20, y+55))
        
        # Draw difficulty
        diff_text = normal_font.render(f"Difficulty: {'★' * self.difficulty}", True, YELLOW)
        surface.blit(diff_text, (x+20, y+85))
        
        # Draw status
        status_text = normal_font.render("COMPLETED" if self.completed else "IN PROGRESS" if is_current else "AVAILABLE", 
                                       True, GREEN_ACCENT if self.completed else YELLOW if is_current else LIGHT_BLUE)
        surface.blit(status_text, (x+width-150, y+15))

def create_missions():
    """Create all game missions"""
    return [
        Mission(
            "Operation: Midnight Sun",
            "A criminal organization has taken hostages in downtown Oslo. Neutralize the threat and rescue the hostages.",
            "Oslo, Norway",
            2,
            [
                Enemy("Thug Leader", 80, 20, 5, (180, 60, 60)),
                Enemy("Thug", 50, 12, 3, (150, 70, 70)),
                Enemy("Thug", 50, 12, 3, (150, 70, 70)),
                Enemy("Thug", 50, 12, 3, (150, 70, 70))
            ]
        ),
        Mission(
            "Operation: Jungle Thunder",
            "An illegal weapons facility hidden in the Amazon. Infiltrate and destroy their operations.",
            "Amazon Rainforest",
            3,
            [
                Enemy("Mercenary Captain", 100, 25, 8, (70, 100, 150)),
                Enemy("Elite Mercenary", 70, 18, 6, (80, 110, 160)),
                Enemy("Elite Mercenary", 70, 18, 6, (80, 110, 160)),
                Enemy("Mercenary Sniper", 60, 22, 4, (90, 120, 170))
            ]
        ),
        Mission(
            "Operation: Frozen Shield",
            "A secret research facility developing dangerous technology. Prevent the weapon from being activated.",
            "Arctic Circle",
            4,
            [
                Enemy("Security Chief", 120, 28, 10, (60, 80, 120)),
                Enemy("Combat Drone", 80, 20, 8, (100, 100, 120)),
                Enemy("Combat Drone", 80, 20, 8, (100, 100, 120)),
                Enemy("Scientist", 60, 15, 3, (120, 140, 180))
            ]
        ),
        Mission(
            "Operation: Final Hour",
            "The mastermind behind global operations is making his last stand. End his reign of terror.",
            "Volcano Lair",
            5,
            [
                Enemy("Mastermind", 200, 35, 15, (180, 40, 40)),
                Enemy("Elite Guard", 90, 25, 10, (160, 60, 60)),
                Enemy("Elite Guard", 90, 25, 10, (160, 60, 60)),
                Enemy("Tech Specialist", 70, 20, 5, (140, 100, 160))
            ]
        )
    ]
