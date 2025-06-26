import pygame
import math
from .button import Button
from ..utils.constants import BLACK, YELLOW

class AnimatedButton(Button):
    def __init__(self, x, y, width, height, text, color):
        super().__init__(x, y, width, height, text, color)
        self.original_y = y
        self.bounce_offset = 0
        self.bounce_speed = 0.002
        self.selected = False
        self.correct = False
        self.wrong = False
        
    def update(self):
        if not self.selected:
            self.bounce_offset = math.sin(pygame.time.get_ticks() * self.bounce_speed) * 2
            self.rect.y = self.original_y + self.bounce_offset
            
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, screen, font):
        # Draw shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=15)
        
        # Draw button with state-based color
        color = self.color
        if self.correct:
            color = (100, 255, 100)
        elif self.wrong:
            color = (255, 100, 100)
        elif self.is_hovered:
            color = tuple(min(c + 30, 255) for c in self.color)
            
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        
        # Draw text with shadow
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        shadow_surface = font.render(self.text, True, (100, 100, 100))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
        
        # Add sparkles for correct answers
        if self.correct:
            current_time = pygame.time.get_ticks()
            for i in range(5):
                angle = (current_time * 0.01 + i * 72) % 360
                radius = 20 + math.sin(current_time * 0.01) * 5
                sparkle_x = self.rect.centerx + math.cos(math.radians(angle)) * radius
                sparkle_y = self.rect.centery + math.sin(math.radians(angle)) * radius
                pygame.draw.circle(screen, YELLOW, (int(sparkle_x), int(sparkle_y)), 3)