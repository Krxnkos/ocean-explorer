import os
import pygame
import random
from .debug import debug_print
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT

def load_image(name, scale=1.0):
    try:
        fullname = os.path.join('assets', 'images', name)
        if not os.path.isfile(fullname):
            debug_print(f"Warning: Cannot find image file: {fullname}", True)
            surf = pygame.Surface((100, 100))
            surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            return surf
        image = pygame.image.load(fullname)
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image.convert_alpha()
    except pygame.error as e:
        debug_print(f"Cannot load image: {name}", True)
        debug_print(str(e), True)
        surf = pygame.Surface((100, 100))
        surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return surf

def load_sound(name):
    try:
        fullname = os.path.join('assets', 'sounds', name)
        if not os.path.isfile(fullname):
            debug_print(f"Warning: Cannot find sound file: {fullname}", True)
            return None
        sound = pygame.mixer.Sound(fullname)
        return sound
    except pygame.error as e:
        debug_print(f"Cannot load sound: {name}", True)
        debug_print(str(e), True)
        return None

def create_default_background():
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Create gradient blue background
    for y in range(SCREEN_HEIGHT):
        blue_value = max(50, 150 - y // 3)
        color = (0, blue_value, 255 - blue_value // 2)
        pygame.draw.line(bg, color, (0, y), (SCREEN_WIDTH, y))
    
    # Add sand at the bottom
    pygame.draw.rect(bg, (240, 220, 130), (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
    
    # Add seaweed
    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH)
        height = random.randint(40, 100)
        width = random.randint(5, 15)
        pygame.draw.rect(bg, (0, 150, 0), (x, SCREEN_HEIGHT - 80 - height, width, height))
    
    # Add bubbles
    for i in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT - 100)
        r = random.randint(2, 8)
        pygame.draw.circle(bg, (200, 200, 255), (x, y), r)
    
    return bg