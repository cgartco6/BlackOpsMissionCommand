import random

class Character:
    def __init__(self, name, role, health, attack, defense, special_name, special_desc, image_color):
        self.name = name
        self.role = role
        self.max_health = health
        self.health = health
        self.attack = attack
        self.defense = defense
        self.special_name = special_name
        self.special_desc = special_desc
        self.image_color = image_color
        self.x = 0
        self.y = 0
        self.selected = False
        self.special_cooldown = 0
        self.alive = True
        
    def draw(self, surface, x, y, size=80):
        self.x, self.y = x, y
        pygame.draw.circle(surface, self.image_color, (x, y), size)
        pygame.draw.circle(surface, WHITE, (x, y), size, 3)
        
        # Draw character initials
        initials = self.name.split()[0][0] + self.name.split()[1][0]
        text = heading_font.render(initials, True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        surface.blit(text, text_rect)
        
        # Draw selection indicator
        if self.selected:
            pygame.draw.circle(surface, YELLOW, (x, y), size+5, 3)
            
        # Draw health bar
        bar_width = 100
        bar_height = 12
        bar_x = x - bar_width//2
        bar_y = y + size + 10
        pygame.draw.rect(surface, HEALTH_RED, (bar_x, bar_y, bar_width, bar_height))
        health_width = max(0, int(bar_width * (self.health / self.max_health)))
        pygame.draw.rect(surface, HEALTH_GREEN, (bar_x, bar_y, health_width, bar_height))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Draw name
        name_text = small_font.render(self.name, True, WHITE)
        name_rect = name_text.get_rect(center=(x, y - size - 20))
        surface.blit(name_text, name_rect)
        
        # Draw role
        role_text = small_font.render(self.role, True, LIGHT_BLUE)
        role_rect = role_text.get_rect(center=(x, y - size - 5))
        surface.blit(role_text, role_rect)
        
    def draw_stats(self, surface, x, y):
        # Draw character card
        card_width = 300
        card_height = 200
        pygame.draw.rect(surface, DARK_GRAY, (x, y, card_width, card_height), 0, 10)
        pygame.draw.rect(surface, LIGHT_GRAY, (x, y, card_width, card_height), 2, 10)
        
        # Draw character info
        name_text = subtitle_font.render(self.name, True, WHITE)
        surface.blit(name_text, (x+20, y+15))
        
        role_text = normal_font.render(self.role, True, LIGHT_BLUE)
        surface.blit(role_text, (x+20, y+50))
        
        # Draw stats
        health_text = small_font.render(f"Health: {self.health}/{self.max_health}", True, WHITE)
        surface.blit(health_text, (x+20, y+90))
        
        attack_text = small_font.render(f"Attack: {self.attack}", True, WHITE)
        surface.blit(attack_text, (x+20, y+115))
        
        defense_text = small_font.render(f"Defense: {self.defense}", True, WHITE)
        surface.blit(defense_text, (x+20, y+140))
        
        # Draw special ability
        pygame.draw.rect(surface, ACCENT, (x+150, y+90, 140, 60), 0, 8)
        special_title = small_font.render(self.special_name, True, WHITE)
        surface.blit(special_title, (x+160, y+95))
        
        # Draw cooldown indicator
        if self.special_cooldown > 0:
            cooldown_text = small_font.render(f"Cooldown: {self.special_cooldown}", True, YELLOW)
            surface.blit(cooldown_text, (x+160, y+135))
        
    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.health -= actual_damage
        if self.health <= 0:
            self.health = 0
            self.alive = False
        return actual_damage

def create_team():
    """Create the player's team"""
    chris = Character(
        "Chris Stone", 
        "Team Leader", 
        120, 
        25, 
        8, 
        "Mjolnir Strike", 
        "Deals massive damage to a single target",
        (200, 50, 50)  # Red
    )

    luke = Character(
        "Luke Steel", 
        "Tactical Specialist", 
        100, 
        18, 
        12, 
        "Shield Wall", 
        "Protects the team and reduces incoming damage",
        (50, 100, 200)  # Blue
    )

    liam = Character(
        "Liam Frost", 
        "Sniper", 
        90, 
        30, 
        5, 
        "Precision Shot", 
        "High chance for critical hit",
        (50, 150, 50)  # Green
    )
    
    return [chris, luke, liam]
