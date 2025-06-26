import pygame
import random
from ..utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Seashell:
    def __init__(self, image):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(SCREEN_HEIGHT - 150, SCREEN_HEIGHT - 50)
        self.image = image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collected = False
    
    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect)
    
    def check_collect(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            return True
        return False