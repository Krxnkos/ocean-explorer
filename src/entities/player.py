import pygame
from ..utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

class Player:
    def __init__(self, image):
        self.x = 100
        self.y = 300
        self.image = image
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.stars = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Keep player within bounds
        self.x = max(50, min(self.x, SCREEN_WIDTH - 50))
        self.y = max(50, min(self.y, SCREEN_HEIGHT - 50))
        # Update rect position
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        # Draw collision circle for debugging
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 5)