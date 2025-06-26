import pygame
import random
import math
from ..utils.constants import RAINBOW_COLORS

class CelebrationEffect:
    def __init__(self, x, y):
        self.particles = []
        for _ in range(30):
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(2, 8)
            color = random.choice(RAINBOW_COLORS)
            self.particles.append({
                'x': x,
                'y': y,
                'dx': math.cos(angle) * speed,
                'dy': math.sin(angle) * speed,
                'color': color,
                'life': 60
            })
    
    def update(self):
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['dy'] += 0.2  # Gravity
            p['life'] -= 1
    
    def draw(self, screen):
        for p in self.particles:
            if p['life'] > 0:
                alpha = min(255, p['life'] * 4)
                color = (*p['color'], alpha)
                pygame.draw.circle(screen, color, 
                                 (int(p['x']), int(p['y'])), 
                                 3)

    @property
    def alive(self):
        return any(p['life'] > 0 for p in self.particles)