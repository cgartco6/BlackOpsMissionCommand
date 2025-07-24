import pygame
import math
from game.characters import *
from game.missions import *

# Colors (defined here for UI elements)
BACKGROUND = (15, 25, 45)
ACCENT = (0, 150, 200)
RED_ACCENT = (200, 50, 50)
GREEN_ACCENT = (50, 200, 100)
YELLOW = (255, 215, 0)
LIGHT_BLUE = (100, 180, 255)
WHITE = (240, 240, 240)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)
HEALTH_GREEN = (50, 200, 80)
HEALTH_RED = (200, 50, 50)

# Fonts
title_font = pygame.font.SysFont("Arial", 48, bold=True)
heading_font = pygame.font.SysFont("Arial", 36, bold=True)
subtitle_font = pygame.font.SysFont("Arial", 28, bold=True)
normal_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 20)

class Button:
    def __init__(self, x, y, width, height, text, color=ACCENT, hover_color=LIGHT_BLUE):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, 0, 10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, 10)
        
        text_surf = normal_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.hovered = self.rect.collidepoint(pos)
        return self.hovered
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered:
                return True
        return False

def draw_mission_select_screen(surface, team, missions, current_mission, start_mission_button, mouse_pos):
    # Title
    title_text = title_font.render("BLACK OPS: MISSION COMMAND", True, ACCENT)
    surface.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 30))
    
    subtitle = subtitle_font.render("Select a Mission", True, LIGHT_BLUE)
    surface.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 90))
    
    # Draw team
    team_text = subtitle_font.render("Your Team", True, WHITE)
    surface.blit(team_text, (100, 150))
    
    for i, char in enumerate(team):
        char.draw(surface, 120 + i*160, 280, 70)
    
    # Draw character stats
    if team:
        team[0].draw_stats(surface, SCREEN_WIDTH - 350, 180)
    
    # Draw missions
    missions_text = subtitle_font.render("Available Missions", True, WHITE)
    surface.blit(missions_text, (100, 380))
    
    for i, mission in enumerate(missions):
        if mission.unlocked:
            mission.draw(surface, 100, 430 + i*140, 800, 120, i == current_mission)
    
    # Draw start mission button
    start_mission_button.check_hover(mouse_pos)
    start_mission_button.draw(surface)

def draw_combat_screen(surface, mission, team, selected_character, combat_log, player_turn, 
                      attack_button, special_button, back_button, mouse_pos):
    # Draw mission title
    mission_title = subtitle_font.render(f"MISSION: {mission.title}", True, ACCENT)
    surface.blit(mission_title, (SCREEN_WIDTH//2 - mission_title.get_width()//2, 20))
    
    # Draw team
    team_title = subtitle_font.render("YOUR TEAM", True, GREEN_ACCENT)
    surface.blit(team_title, (SCREEN_WIDTH//2 - 350, 70))
    
    for i, char in enumerate(team):
        char.draw(surface, 200 + i*200, 200, 90)
        if char.special_cooldown > 0:
            cooldown_text = small_font.render(f"{char.special_name} on cooldown: {char.special_cooldown}", True, YELLOW)
            surface.blit(cooldown_text, (200 + i*200 - cooldown_text.get_width()//2, 330))
    
    # Draw enemies
    enemies_title = subtitle_font.render("ENEMIES", True, RED_ACCENT)
    surface.blit(enemies_title, (SCREEN_WIDTH//2 + 150, 70))
    
    for i, enemy in enumerate(mission.enemies):
        enemy.draw(surface, SCREEN_WIDTH//2 + 150 + i*150, 200)
    
    # Draw combat log
    pygame.draw.rect(surface, (10, 20, 35), (50, 350, SCREEN_WIDTH-100, 200), 0, 10)
    pygame.draw.rect(surface, ACCENT, (50, 350, SCREEN_WIDTH-100, 200), 2, 10)
    
    log_title = small_font.render("COMBAT LOG", True, LIGHT_BLUE)
    surface.blit(log_title, (70, 360))
    
    # Display last 8 log entries
    for i, entry in enumerate(combat_log[-8:]):
        log_text = small_font.render(entry, True, WHITE)
        surface.blit(log_text, (70, 400 + i*25))
    
    # Draw action buttons
    if player_turn:
        action_text = subtitle_font.render("YOUR TURN - Select a character and action", True, GREEN_ACCENT)
        surface.blit(action_text, (SCREEN_WIDTH//2 - action_text.get_width()//2, SCREEN_HEIGHT - 150))
        
        attack_button.check_hover(mouse_pos)
        special_button.check_hover(mouse_pos)
        attack_button.draw(surface)
        special_button.draw(surface)
    else:
        enemy_text = subtitle_font.render("ENEMY TURN", True, RED_ACCENT)
        surface.blit(enemy_text, (SCREEN_WIDTH//2 - enemy_text.get_width()//2, SCREEN_HEIGHT - 150))
    
    # Draw back button
    back_button.check_hover(mouse_pos)
    back_button.draw(surface)

def draw_mission_complete_screen(surface, mission, next_mission_button, mouse_pos):
    # Mission complete screen
    pygame.draw.rect(surface, (20, 40, 80), (100, 100, SCREEN_WIDTH-200, SCREEN_HEIGHT-250), 0, 20)
    pygame.draw.rect(surface, ACCENT, (100, 100, SCREEN_WIDTH-200, SCREEN_HEIGHT-250), 4, 20)
    
    complete_text = title_font.render("MISSION COMPLETE!", True, GREEN_ACCENT)
    surface.blit(complete_text, (SCREEN_WIDTH//2 - complete_text.get_width()//2, 150))
    
    mission_title = subtitle_font.render(f"{mission.title}", True, YELLOW)
    surface.blit(mission_title, (SCREEN_WIDTH//2 - mission_title.get_width()//2, 220))
    
    desc_text = normal_font.render(mission.description, True, WHITE)
    surface.blit(desc_text, (SCREEN_WIDTH//2 - desc_text.get_width()//2, 280))
    
    reward_text = heading_font.render("Rewards Unlocked:", True, LIGHT_BLUE)
    surface.blit(reward_text, (SCREEN_WIDTH//2 - reward_text.get_width()//2, 350))
    
    pygame.draw.rect(surface, (30, 60, 100), (SCREEN_WIDTH//2 - 200, 400, 400, 120), 0, 15)
    pygame.draw.rect(surface, LIGHT_BLUE, (SCREEN_WIDTH//2 - 200, 400, 400, 120), 2, 15)
    
    reward1 = normal_font.render("+ Team Experience", True, WHITE)
    surface.blit(reward1, (SCREEN_WIDTH//2 - 180, 420))
    
    reward2 = normal_font.render("+ New Equipment", True, WHITE)
    surface.blit(reward2, (SCREEN_WIDTH//2 - 180, 450))
    
    reward3 = normal_font.render("+ Funding for Upgrades", True, WHITE)
    surface.blit(reward3, (SCREEN_WIDTH//2 - 180, 480))
    
    # Draw next mission button
    next_mission_button.check_hover(mouse_pos)
    next_mission_button.draw(surface)

def draw_game_over_screen(surface, retry_button, main_menu_button, mouse_pos):
    # Game over screen
    surface.fill((20, 10, 10))
    
    game_over_text = title_font.render("MISSION FAILED", True, RED_ACCENT)
    surface.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, 200))
    
    over_text = subtitle_font.render("Your team was overwhelmed", True, LIGHT_GRAY)
    surface.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, 280))
    
    # Draw buttons
    retry_button.check_hover(mouse_pos)
    main_menu_button.check_hover(mouse_pos)
    retry_button.draw(surface)
    main_menu_button.draw(surface)

def draw_victory_screen(surface, main_menu_button, mouse_pos):
    # Victory screen
    surface.fill((10, 20, 10))
    
    victory_text = title_font.render("VICTORY!", True, GREEN_ACCENT)
    surface.blit(victory_text, (SCREEN_WIDTH//2 - victory_text.get_width()//2, 200))
    
    congrats = subtitle_font.render("You've completed all missions and saved the world!", True, YELLOW)
    surface.blit(congrats, (SCREEN_WIDTH//2 - congrats.get_width()//2, 280))
    
    # Draw button
    main_menu_button.rect.center = (SCREEN_WIDTH//2, 400)
    main_menu_button.check_hover(mouse_pos)
    main_menu_button.draw(surface)

# Screen dimensions (define here for UI)
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
