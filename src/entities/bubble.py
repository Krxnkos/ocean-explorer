import pygame
import random
import math
from ..utils.constants import BUBBLE_COLORS, SCREEN_WIDTH, SCREEN_HEIGHT

class Bubble:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = SCREEN_HEIGHT + random.randint(0, 100)
        self.speed = random.uniform(1, 3)
        self.size = random.randint(20, 40)
        self.color = random.choice(BUBBLE_COLORS)
        self.sparkle = 0
        self.popped = False
        
    def check_pop(self, mouse_pos):
        if not self.popped:
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance <= self.size:
                self.popped = True
                return True
        return False
        
    def update(self):
        if not self.popped:
            self.y -= self.speed
            self.x += math.sin(pygame.time.get_ticks() * 0.001 + self.y * 0.1) * 0.5
            self.sparkle = (self.sparkle + 1) % 360
            
    def draw(self, screen):
        if not self.popped:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            shine_pos = (int(self.x + math.cos(self.sparkle * 0.1) * self.size * 0.3),
                        int(self.y + math.sin(self.sparkle * 0.1) * self.size * 0.3))
            pygame.draw.circle(screen, (255, 255, 255), shine_pos, self.size // 4)