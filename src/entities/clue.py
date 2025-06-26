import pygame
import math
from ..utils.constants import BLACK, WHITE

class Clue:
    def __init__(self, x, y, text, creature_hint):
        self.x = x
        self.y = y
        self.text = text
        self.creature_hint = creature_hint
        self.collected = False
        self.rect = pygame.Rect(x-15, y-15, 30, 30)
        self.is_hovered = False
        
    def update(self, mouse_pos):
        if not self.collected:
            self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen, font):
        if not self.collected:
            # Draw glowing effect when hovered
            if self.is_hovered:
                glow_radius = 20 + math.sin(pygame.time.get_ticks() * 0.005) * 3
                pygame.draw.circle(screen, (255, 255, 150), (self.x, self.y), int(glow_radius))
            
            pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y), 15)
            pygame.draw.circle(screen, BLACK, (self.x, self.y), 15, 2)
            text = font.render("?", True, BLACK)
            screen.blit(text, (self.x - text.get_width()//2, self.y - text.get_height()//2))
            
            # Show hint text when hovered
            if self.is_hovered:
                hint_text = font.render(self.text, True, WHITE)
                hint_rect = hint_text.get_rect(center=(self.x, self.y - 30))
                pygame.draw.rect(screen, (0, 0, 0, 128), hint_rect.inflate(20, 10))
                screen.blit(hint_text, hint_rect)