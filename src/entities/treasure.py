import pygame
import random
from ..utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Treasure:
    def __init__(self, image):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = SCREEN_HEIGHT - 100
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