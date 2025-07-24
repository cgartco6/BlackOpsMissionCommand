import pygame
import sys
import random
from game.characters import create_team
from game.missions import create_missions
from game.ui import Button
from game.combat import handle_combat_events, enemy_turn
from game.particles import update_particles
from game.ui import draw_mission_select_screen, draw_combat_screen, draw_mission_complete_screen, draw_game_over_screen, draw_victory_screen

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 700
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Black Ops: Mission Command")

# Colors
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

def start_combat(missions, current_mission, team):
    """Reset characters for new combat"""
    for char in team:
        char.health = char.max_health
        char.alive = True
        char.special_cooldown = 0
    return [f"Mission: {missions[current_mission].title}", "Combat initiated!"]

def main():
    # Create characters
    team = create_team()
    
    # Create missions
    missions = create_missions()
    
    # Initialize game state
    current_mission = 0
    game_state = "mission_select"  # mission_select, combat, mission_complete, game_over
    selected_character = None
    combat_log = []
    player_turn = True
    particles = []
    
    # Unlock first mission
    missions[0].unlocked = True
    
    # Create buttons
    start_mission_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50, "START MISSION")
    next_mission_button = Button(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50, "NEXT MISSION")
    retry_button = Button(SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT - 100, 140, 50, "RETRY")
    main_menu_button = Button(SCREEN_WIDTH//2 + 10, SCREEN_HEIGHT - 100, 140, 50, "MAIN MENU")
    attack_button = Button(SCREEN_WIDTH//2 - 220, SCREEN_HEIGHT - 90, 200, 50, "ATTACK")
    special_button = Button(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT - 90, 200, 50, "SPECIAL")
    back_button = Button(50, SCREEN_HEIGHT - 70, 120, 40, "BACK")
    
    # Main game loop
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            # Handle button clicks
            if game_state == "mission_select":
                if start_mission_button.handle_event(event):
                    combat_log = start_combat(missions, current_mission, team)
                    game_state = "combat"
                    player_turn = True
                    selected_character = None
                    
            elif game_state == "mission_complete":
                if next_mission_button.handle_event(event):
                    if current_mission < len(missions) - 1:
                        current_mission += 1
                        missions[current_mission].unlocked = True
                        game_state = "mission_select"
                    else:
                        game_state = "victory"
                        
            elif game_state == "combat":
                result = handle_combat_events(
                    event, mouse_pos, team, missions[current_mission].enemies, 
                    selected_character, player_turn, combat_log, particles
                )
                if result:
                    selected_character, player_turn = result
                
            # Back button handling
            if back_button.handle_event(event):
                if game_state == "combat":
                    game_state = "mission_select"
            
            # Handle retry and main menu buttons
            if game_state == "game_over":
                if retry_button.handle_event(event):
                    combat_log = start_combat(missions, current_mission, team)
                    game_state = "combat"
                    player_turn = True
                    selected_character = None
                if main_menu_button.handle_event(event):
                    game_state = "mission_select"
                    
            if game_state == "victory":
                if main_menu_button.handle_event(event):
                    game_state = "mission_select"
        
        # Enemy turn in combat
        if game_state == "combat" and not player_turn:
            result = enemy_turn(missions[current_mission].enemies, team, combat_log, particles)
            if result == "win":
                combat_log.append("Mission successful!")
                missions[current_mission].completed = True
                game_state = "mission_complete"
            elif result == "lose":
                combat_log.append("Mission failed! All team members down.")
                game_state = "game_over"
            else:
                player_turn = True
                # Reduce cooldowns
                for char in team:
                    if char.special_cooldown > 0:
                        char.special_cooldown -= 1
        
        # Update particles
        particles = update_particles(particles)
        
        # Draw everything
        screen.fill(BACKGROUND)
        
        # Draw decorative elements
        for i in range(20):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            pygame.draw.circle(screen, (100, 150, 200, 100), (x, y), size)
        
        # Draw particles
        for particle in particles:
            particle.draw(screen)
        
        # Draw UI based on game state
        if game_state == "mission_select":
            draw_mission_select_screen(
                screen, team, missions, current_mission, 
                start_mission_button, mouse_pos
            )
            
        elif game_state == "combat":
            draw_combat_screen(
                screen, missions[current_mission], team, selected_character, 
                combat_log, player_turn, attack_button, special_button, 
                back_button, mouse_pos
            )
            
        elif game_state == "mission_complete":
            draw_mission_complete_screen(
                screen, missions[current_mission], 
                next_mission_button, mouse_pos
            )
            
        elif game_state == "game_over":
            draw_game_over_screen(
                screen, retry_button, 
                main_menu_button, mouse_pos
            )
            
        elif game_state == "victory":
            draw_victory_screen(
                screen, main_menu_button, 
                mouse_pos
            )
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
