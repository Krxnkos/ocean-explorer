import pygame

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

# Colors
BLUE = (0, 119, 190)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

RAINBOW_COLORS = [
    (255, 0, 0),    # Red
    (255, 127, 0),  # Orange
    (255, 255, 0),  # Yellow
    (0, 255, 0),    # Green
    (0, 0, 255),    # Blue
    (75, 0, 130),   # Indigo
    (148, 0, 211)   # Violet
]

BUBBLE_COLORS = [(173, 216, 230), (135, 206, 235), (0, 191, 255)]  # Light blue variations

# Game states
EXPLORE = 0
QUIZ = 1
REWARD = 2
GAME_OVER = 3
BUBBLE_GAME = 4
TREASURE_GAME = 5
SEASHELL_GAME = 6