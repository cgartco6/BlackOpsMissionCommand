import pygame
from game.ui import *

class Enemy:
    def __init__(self, name, health, attack, defense, image_color):
        self.name = name
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.image_color = image_color
        self.x = 0
        self.y = 0
        
    def draw(self, surface, x, y, size=60):
        self.x, self.y = x, y
        pygame.draw.rect(surface, self.image_color, (x-size, y-size, size*2, size*2), 0, 10)
        pygame.draw.rect(surface, WHITE, (x-size, y-size, size*2, size*2), 2, 10)
        
        # Draw enemy icon
        icon_text = heading_font.render("E", True, WHITE)
        icon_rect = icon_text.get_rect(center=(x, y))
        surface.blit(icon_text, icon_rect)
        
        # Draw health bar
        bar_width = 80
        bar_height = 8
        bar_x = x - bar_width//2
        bar_y = y + size + 5
        pygame.draw.rect(surface, HEALTH_RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = max(0, int(bar_width * (self.health / self.max_health)))
        pygame.draw.rect(surface, HEALTH_GREEN, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 1)
        
        # Draw name
        name_text = small_font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(x, y - size - 15))
        surface.blit(name_text, name_rect)
        
    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
        return actual_damage
