import pygame

class TutorialSystem:
    def __init__(self, screen):
        self.screen = screen
        self.current_phase = 0
        self.phases = [
            self.phase1_introduction,
            self.phase2_combat,
            self.phase3_economy
        ]
        self.completed = False
        self.tokens_earned = False
    
    def start(self):
        self.current_phase = 0
    
    def update(self):
        if self.current_phase < len(self.phases):
            return self.phases[self.current_phase]()
        else:
            self.completed = True
            return True
    
    def phase1_introduction(self):
        # Draw tutorial overlay
        overlay = pygame.Surface((1000, 700), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        
        # Draw tutorial content
        font = pygame.font.SysFont("Arial", 36)
        text = font.render("Welcome to Black Ops: Mission Command!", True, (255, 255, 255))
        self.screen.blit(text, (250, 200))
        
        text = pygame.font.SysFont("Arial", 24).render(
            "In this game, you command an elite team on dangerous missions around the world", 
            True, (200, 200, 200))
        self.screen.blit(text, (150, 280))
        
        # Draw continue button
        continue_btn = Button(400, 500, 200, 50, "Continue")
        continue_btn.draw(self.screen)
        
        # Check for button click
        return False
    
    def phase2_combat(self):
        # Similar structure with combat tutorial
        return False
    
    def phase3_economy(self):
        # Economy and token system tutorial
        if not self.tokens_earned:
            # Award tokens for completing tutorial
            self.tokens_earned = True
            return "tokens_awarded"
        return False
    
    def is_completed(self):
        return self.completed
