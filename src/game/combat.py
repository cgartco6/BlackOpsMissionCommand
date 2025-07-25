import pygame
import math
import random
from .particles import Particle

def handle_combat_events(event, mouse_pos, team, enemies, selected_character, player_turn, combat_log, particles):
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        # Character selection
        selected_character = None
        for char in team:
            if not char.alive:
                continue
            dist = math.sqrt((char.x - mouse_pos[0])**2 + (char.y - mouse_pos[1])**2)
            if dist < 80:
                selected_character = char
                char.selected = True
                combat_log.append(f"{char.name} selected")
            else:
                char.selected = False
                
        # Enemy selection for attack
        if selected_character:
            for enemy in enemies:
                if enemy.health <= 0:
                    continue
                dist = math.sqrt((enemy.x - mouse_pos[0])**2 + (enemy.y - mouse_pos[1])**2)
                if dist < 60:
                    # Attack
                    damage = selected_character.attack
                    actual_damage = enemy.take_damage(damage)
                    combat_log.append(f"{selected_character.name} attacks {enemy.name} for {actual_damage} damage!")
                    
                    # Create particles
                    for _ in range(20):
                        particles.append(Particle(enemy.x, enemy.y, (255, 100, 100)))
                    
                    # Check if enemy defeated
                    if enemy.health <= 0:
                        combat_log.append(f"{enemy.name} defeated!")
                    
                    selected_character.selected = False
                    selected_character = None
                    return None, False
    
    return selected_character, player_turn

def enemy_turn(enemies, team, combat_log, particles):
    # Simple AI: enemies attack random alive character
    for enemy in enemies:
        if enemy.health > 0:
            # Find random alive character
            alive_chars = [char for char in team if char.alive]
            if not alive_chars:
                return "lose"
                
            target = random.choice(alive_chars)
            damage = enemy.attack
            actual_damage = target.take_damage(damage)
            combat_log.append(f"{enemy.name} attacks {target.name} for {actual_damage} damage!")
            
            # Create particles
            for _ in range(15):
                particles.append(Particle(target.x, target.y, (255, 100, 100)))
            
            if not target.alive:
                combat_log.append(f"{target.name} is down!")
    
    # Check if all enemies defeated
    if all(enemy.health <= 0 for enemy in enemies):
        return "win"
        
    # Check if all characters down
    if all(not char.alive for char in team):
        return "lose"
        
    return "continue"
