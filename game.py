import pygame
import sys
import random
import os
import math
from pygame.locals import *

# Initialize pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ocean Explorer')

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

# Add a global debug flag to control console output
DEBUG_MODE = False
DEBUG_INTERVAL = 5000  # milliseconds between debug outputs
last_debug_time = 0

def debug_print(message, force=False):
    """Print debug messages only when DEBUG_MODE is on or force is True"""
    global last_debug_time
    current_time = pygame.time.get_ticks()
    
    # Always print forced messages or errors
    if force or "Error" in message:
        print(message)
        return
        
    # Only print regular debug messages when debug mode is on
    if DEBUG_MODE:
        # Further limit spammy position updates to the debug interval
        if "position" in message.lower() or "distance" in message.lower():
            if current_time - last_debug_time > DEBUG_INTERVAL:
                print(message)
                last_debug_time = current_time
        else:
            # Non-spammy messages can print more often
            print(message)

# Load images
def load_image(name, scale=1.0):
    try:
        fullname = os.path.join('assets', 'images', name)
        # First check if the file exists
        if not os.path.isfile(fullname):
            debug_print(f"Warning: Cannot find image file: {fullname}", True)
            # Create a colored surface as placeholder
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
        # Create a colored surface as placeholder
        surf = pygame.Surface((100, 100))
        surf.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        return surf

# Load sounds
def load_sound(name):
    try:
        fullname = os.path.join('assets', 'sounds', name)
        # Check if the file exists first
        if not os.path.isfile(fullname):
            debug_print(f"Warning: Cannot find sound file: {fullname}", True)
            return None
        sound = pygame.mixer.Sound(fullname)
        return sound
    except pygame.error as e:
        debug_print(f"Cannot load sound: {name}", True)
        debug_print(str(e), True)
        return None

# Create default background if image is not available
def create_default_background():
    bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Create gradient blue background
    for y in range(SCREEN_HEIGHT):
        blue_value = max(50, 150 - y // 3)
        color = (0, blue_value, 255 - blue_value // 2)
        pygame.draw.line(bg, color, (0, y), (SCREEN_WIDTH, y))
    
    # Add some simple underwater elements
    # Sand at the bottom
    pygame.draw.rect(bg, (240, 220, 130), (0, SCREEN_HEIGHT - 80, SCREEN_WIDTH, 80))
    
    # Some random seaweed
    for i in range(10):
        x = random.randint(0, SCREEN_WIDTH)
        height = random.randint(40, 100)
        width = random.randint(5, 15)
        pygame.draw.rect(bg, (0, 150, 0), (x, SCREEN_HEIGHT - 80 - height, width, height))
    
    # Some bubbles
    for i in range(20):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT - 100)
        r = random.randint(2, 8)
        pygame.draw.circle(bg, (200, 200, 255), (x, y), r)
    
    return bg

# Game assets
try:
    player_img = load_image('player.png', 0.15)  # Reduced from 0.2
    dolphin_img = load_image('dolphin.png', 0.2)  # Reduced from 0.3
    turtle_img = load_image('turtle.png', 0.15)   # Reduced from 0.2
    starfish_img = load_image('starfish.png', 0.1) # Reduced from 0.15
    octopus_img = load_image('octopus.png', 0.2)  # Reduced from 0.25
    fish_img = load_image('fish.png', 0.1)        # Reduced from 0.15
    bubble_img = load_image('bubble.png', 0.1)
    treasure_img = load_image('treasure.png', 0.2)
    seashell_img = load_image('seashell.png', 0.15)
    coral_img = load_image('coral.png', 0.3)
    
    # Try to load background, use default if it fails
    background_img = load_image('ocean_bg.png')
    # Make sure the background is the right size
    if background_img.get_width() != SCREEN_WIDTH or background_img.get_height() != SCREEN_HEIGHT:
        background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
except:
    debug_print("Error loading game assets. Creating default images.", True)
    background_img = create_default_background()
    bubble_img = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(bubble_img, (200, 200, 255, 180), (10, 10), 10)
    treasure_img = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.rect(treasure_img, (139, 69, 19), (0, 0, 40, 30))
    pygame.draw.rect(treasure_img, (255, 215, 0), (5, 5, 30, 20))
    seashell_img = pygame.Surface((30, 20), pygame.SRCALPHA)
    pygame.draw.arc(seashell_img, (255, 222, 173), (0, 0, 30, 20), 0, 3.14, 3)
    coral_img = pygame.Surface((50, 60), pygame.SRCALPHA)
    pygame.draw.rect(coral_img, (255, 127, 127), (10, 0, 10, 60))
    pygame.draw.rect(coral_img, (255, 127, 127), (25, 10, 10, 50))
    pygame.draw.rect(coral_img, (255, 127, 127), (40, 20, 10, 40))

# Sound effects - don't throw an error if they can't load
try:
    correct_sound = load_sound('correct.wav')
    wrong_sound = load_sound('wrong.wav')
    background_music = load_sound('ocean_music.wav')
    bubble_pop_sound = load_sound('bubble_pop.wav')
    treasure_sound = load_sound('treasure.wav')
    seashell_sound = load_sound('seashell.wav')
except:
    debug_print("Error loading sound assets.", True)
    correct_sound = None
    wrong_sound = None
    background_music = None
    bubble_pop_sound = None
    treasure_sound = None
    seashell_sound = None

# Font
font = pygame.font.SysFont('Arial', 24)
large_font = pygame.font.SysFont('Arial', 32)
small_font = pygame.font.SysFont('Arial', 18)

# Game states
EXPLORE = 0
QUIZ = 1
REWARD = 2
GAME_OVER = 3
BUBBLE_GAME = 4
TREASURE_GAME = 5
SEASHELL_GAME = 6

class Player:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.image = player_img
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)  # Make sure center is set properly
        self.stars = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Keep player within bounds
        self.x = max(50, min(self.x, SCREEN_WIDTH - 50))
        self.y = max(50, min(self.y, SCREEN_HEIGHT - 50))
        # Make sure the rect follows the player position
        self.rect.center = (self.x, self.y)

    def draw(self):
        # Make sure the rect is at the right position before drawing
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        
        # Draw a small collision circle for debugging
        pygame.draw.circle(screen, (0, 255, 0), (self.x, self.y), 5)

class Creature:
    def __init__(self, x, y, image, name, questions_data):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.questions = questions_data
        self.current_question_index = 0
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.visited = False
        self.discovered = False
        self.is_hovered = False
        self.proximity_indicator = 0  # For pulsing effect
        self.in_range = False
        self.interaction_radius = 150
        self.can_interact = False
        
        # Swimming behavior attributes
        self.original_x = x
        self.original_y = y
        self.swim_pattern = random.choice(['circle', 'figure8', 'zigzag', 'random'])
        self.movement_speed = random.uniform(0.3, 1.5)
        self.movement_radius = random.randint(30, 100)
        self.movement_time = random.uniform(0, math.pi * 2)  # Random start phase
        self.next_direction_change = 0
        self.current_direction = random.uniform(0, math.pi * 2)
        self.target_x = self.x
        self.target_y = self.y

    def get_next_question(self):
        """Get the next question from the questions list"""
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            return question
        return None

    def update(self, player_pos, mouse_pos):
        if not self.visited:
            current_time = pygame.time.get_ticks() * 0.001  # Convert to seconds
            self.movement_time += self.movement_speed * 0.02

            # Apply different swimming patterns
            if self.swim_pattern == 'circle':
                # Circular motion
                self.x = self.original_x + math.cos(self.movement_time) * self.movement_radius
                self.y = self.original_y + math.sin(self.movement_time) * self.movement_radius
                self.flip_image = math.cos(self.movement_time) < 0
                
            elif self.swim_pattern == 'figure8':
                # Figure-8 pattern
                scale_x = self.movement_radius * 1.5
                scale_y = self.movement_radius
                self.x = self.original_x + math.sin(self.movement_time) * scale_x
                self.y = self.original_y + math.sin(self.movement_time * 2) * scale_y
                self.flip_image = math.cos(self.movement_time) < 0
                
            elif self.swim_pattern == 'zigzag':
                # Zigzag pattern
                self.x = self.original_x + math.sin(self.movement_time * 2) * self.movement_radius
                self.y = self.original_y + self.movement_time % (self.movement_radius * 2) - self.movement_radius
                self.flip_image = math.sin(self.movement_time * 2) < 0
                
            elif self.swim_pattern == 'random':
                # Random wandering
                if current_time > self.next_direction_change:
                    self.current_direction = random.uniform(0, math.pi * 2)
                    self.next_direction_change = current_time + random.uniform(1, 3)
                    self.target_x = self.original_x + random.randint(-self.movement_radius, self.movement_radius)
                    self.target_y = self.original_y + random.randint(-self.movement_radius, self.movement_radius)
                
                # Move towards target
                dx = self.target_x - self.x
                dy = self.target_y - self.y
                dist = math.sqrt(dx*dx + dy*dy)
                if dist > 0:
                    self.x += (dx/dist) * self.movement_speed
                    self.y += (dy/dist) * self.movement_speed
                self.flip_image = dx < 0

            # Keep within bounds of original position
            max_distance = self.movement_radius * 1.5
            dx = self.x - self.original_x
            dy = self.y - self.original_y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > max_distance:
                angle = math.atan2(dy, dx)
                self.x = self.original_x + math.cos(angle) * max_distance
                self.y = self.original_y + math.sin(angle) * max_distance

            # Update interaction checks
            player_distance = math.sqrt(
                (player_pos[0] - self.x)**2 + 
                (player_pos[1] - self.y)**2
            )
            self.can_interact = player_distance < self.interaction_radius
            
            if self.can_interact:
                mouse_distance = math.sqrt(
                    (mouse_pos[0] - self.x)**2 + 
                    (mouse_pos[1] - self.y)**2
                )
                self.is_hovered = mouse_distance < 50
            else:
                self.is_hovered = False

    def draw(self):
        self.rect.center = (self.x, self.y)
        # Flip image if needed
        if self.flip_image:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        
        # Show interaction prompt only when in range
        if self.in_range and self.is_hovered and not self.visited:
            text = "Click to interact!"  # Changed from "Press SPACE"
            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, self.y - 70))
            screen.blit(text_surface, text_rect)
        
        # Only show name if discovered
        elif self.discovered:
            name_text = font.render(self.name, True, WHITE)
            screen.blit(name_text, (self.x - name_text.get_width() // 2, self.y - 50))

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (min(color[0] + 30, 255), min(color[1] + 30, 255), min(color[2] + 30, 255))
        self.is_hovered = False

    def draw(self):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)
        
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
    
    def is_clicked(self, pos, event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(pos):
            return True
        return False

class AnimatedButton(Button):
    def __init__(self, x, y, width, height, text, color):
        super().__init__(x, y, width, height, text, color)
        self.original_y = y
        self.bounce_offset = 0
        self.bounce_speed = 0.002  # Reduced from previous value
        self.selected = False
        self.correct = False
        self.wrong = False
        
    def update(self):
        # Make the bounce much gentler
        if not self.selected:
            self.bounce_offset = math.sin(pygame.time.get_ticks() * self.bounce_speed) * 2  # Reduced amplitude
            self.rect.y = self.original_y + self.bounce_offset
            
        # Update hover state
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def draw(self):
        # Draw fun shadow
        shadow_rect = self.rect.copy()
        shadow_rect.y += 5
        pygame.draw.rect(screen, (0, 0, 0, 128), shadow_rect, border_radius=15)
        
        # Draw main button with gradient
        color = self.color
        if self.correct:
            color = (100, 255, 100)  # Green for correct
        elif self.wrong:
            color = (255, 100, 100)  # Red for wrong
        elif self.is_hovered:
            # Lighten the color when hovered
            color = tuple(min(c + 30, 255) for c in self.color)
            
        pygame.draw.rect(screen, color, self.rect, border_radius=15)
        
        # Draw text with better contrast
        text_surface = font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        
        # Add subtle text shadow for better readability
        shadow_surface = font.render(self.text, True, (100, 100, 100))
        shadow_rect = text_rect.copy()
        shadow_rect.x += 1
        shadow_rect.y += 1
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
        
        # Add sparkles if correct
        if self.correct:
            current_time = pygame.time.get_ticks()
            for i in range(5):
                angle = (current_time * 0.01 + i * 72) % 360
                radius = 20 + math.sin(current_time * 0.01) * 5
                sparkle_x = self.rect.centerx + math.cos(math.radians(angle)) * radius
                sparkle_y = self.rect.centery + math.sin(math.radians(angle)) * radius
                pygame.draw.circle(screen, YELLOW, (int(sparkle_x), int(sparkle_y)), 3)

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
            # Calculate distance between mouse click and bubble center
            dx = mouse_pos[0] - self.x
            dy = mouse_pos[1] - self.y
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Check if click was inside bubble
            if distance <= self.size:
                self.popped = True
                # Play pop sound if available
                if bubble_pop_sound:
                    try:
                        bubble_pop_sound.play()
                    except:
                        pass
                return True
        return False
        
    def update(self):
        if not self.popped:
            self.y -= self.speed
            self.x += math.sin(pygame.time.get_ticks() * 0.001 + self.y * 0.1) * 0.5
            self.sparkle = (self.sparkle + 1) % 360
            
    def draw(self):
        if not self.popped:
            # Draw main bubble
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
            # Add shine effect
            shine_pos = (int(self.x + math.cos(self.sparkle * 0.1) * self.size * 0.3),
                        int(self.y + math.sin(self.sparkle * 0.1) * self.size * 0.3))
            pygame.draw.circle(screen, (255, 255, 255), shine_pos, self.size // 4)

class Treasure:
    def __init__(self):
        self.x = random.randint(100, SCREEN_WIDTH - 100)
        self.y = SCREEN_HEIGHT - 100  # Place treasures near the bottom
        self.image = treasure_img
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collected = False
    
    def draw(self):
        if not self.collected:
            screen.blit(self.image, self.rect)
    
    def check_collect(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            if treasure_sound:
                try:
                    treasure_sound.play()
                except:
                    pass
            return True
        return False

class Seashell:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(SCREEN_HEIGHT - 150, SCREEN_HEIGHT - 50)  # Place shells near the bottom
        self.image = seashell_img
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.collected = False
    
    def draw(self):
        if not self.collected:
            screen.blit(self.image, self.rect)
    
    def check_collect(self, player_rect):
        if not self.collected and self.rect.colliderect(player_rect):
            self.collected = True
            if seashell_sound:
                try:
                    seashell_sound.play()
                except:
                    pass
            return True
        return False

class Coral:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = coral_img
        self.rect = self.image.get_rect(center=(self.x, self.y))
    
    def draw(self):
        screen.blit(self.image, self.rect)
    
    def check_collision(self, player_rect):
        return self.rect.colliderect(player_rect)

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
    
    def draw(self):
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
    
    def draw(self):
        if not self.collected:
            # Draw glowing effect when hovered
            if self.is_hovered:
                glow_radius = 20 + math.sin(pygame.time.get_ticks() * 0.005) * 3
                pygame.draw.circle(screen, (255, 255, 150), (self.x, self.y), int(glow_radius))
            
            pygame.draw.circle(screen, (255, 215, 0), (self.x, self.y), 15)
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), 15, 2)
            text = font.render("?", True, BLACK)
            screen.blit(text, (self.x - text.get_width()//2, self.y - text.get_height()//2))
            
            # Show hint text when hovered
            if self.is_hovered:
                hint_text = font.render(self.text, True, WHITE)
                hint_rect = hint_text.get_rect(center=(self.x, self.y - 30))
                pygame.draw.rect(screen, (0, 0, 0, 128), hint_rect.inflate(20, 10))
                screen.blit(hint_text, hint_rect)

class Game:
    def __init__(self):
        self.player = Player()
        self.state = EXPLORE
        self.current_creature = None
        self.answer_buttons = []
        self.result_message = ""
        self.result_time = 0
        self.clock = pygame.time.Clock()
        self.safe_margin = 100
        self.min_creature_distance = 200
        self.creatures = self.create_creatures()
        self.clues = self.create_clues()
        
        # Add collision circles debug flag
        self.show_collision_circles = False  # Add this line
        
        self.celebration_effects = []
        
        # Add ocean currents
        self.ocean_currents = [
            {
                'x': random.randint(0, SCREEN_WIDTH),
                'y': random.randint(0, SCREEN_HEIGHT),
                'strength': random.uniform(0.5, 2.0),
                'radius': random.randint(200, 400)
            } for _ in range(5)
        ]
        
        # Add collectibles
        self.bubbles = [Bubble() for _ in range(30)]  # More bubbles
        self.seashells = [Seashell() for _ in range(10)]
        self.treasures = [Treasure() for _ in range(5)]
        
        # Add score system
        self.score = 0
        self.combo_multiplier = 1.0
        self.last_collect_time = 0

        self.clues = [
            Clue(300, 200, "Look for splashing near the surface!", "Dolphin"),
            Clue(500, 400, "Some creatures carry their homes with them.", "Sea Turtle"),
            # Add more clues
        ]
        self.collected_clues = []
        
        self.bubble_count = 0
        self.treasure_count = 0
        self.seashell_count = 0
        
        self.game_start_time = pygame.time.get_ticks()
        self.elapsed_time = 0
        
        self.mini_game_timer = 0
        self.mini_game_duration = 10000  # 10 seconds for mini-games
        
        # Tutorial message shown at start
        self.show_tutorial = True
        self.tutorial_time = pygame.time.get_ticks()
        
        # Play background music on loop if available
        if background_music:
            try:
                background_music.play(-1)
            except:
                debug_print("Could not play background music", True)

    def get_random_position(self, existing_positions=None):
        """Generate a random position that's not too close to existing ones"""
        if existing_positions is None:
            existing_positions = []
            
        for attempt in range(100):  # Limit attempts to prevent infinite loop
            x = random.randint(self.safe_margin, SCREEN_WIDTH - self.safe_margin)
            y = random.randint(self.safe_margin, SCREEN_HEIGHT - self.safe_margin)
            
            # Check distance from existing positions
            valid_position = True
            for pos in existing_positions:
                distance = math.sqrt((x - pos[0])**2 + (y - pos[1])**2)
                if distance < self.min_creature_distance:
                    valid_position = False
                    break
                    
            if valid_position:
                return x, y
                
        # If we couldn't find a good position, return a fallback
        return (random.randint(0, SCREEN_WIDTH), 
                random.randint(0, SCREEN_HEIGHT))

    def create_creatures(self):
        creature_data = [
            (dolphin_img, "Dolphin", [
                {
                    "question": "I'm a friendly creature that loves to jump and play! What am I?",
                    "answers": ["A happy dolphin", "A grumpy shark", "A dancing crab"],
                    "correct": 0
                },
                {
                    "question": "What special sound do I use to find my way?",
                    "answers": ["Barking", "Echolocation", "Humming"],
                    "correct": 1
                },
                {
                    "question": "What's my favorite thing to do?",
                    "answers": ["Sleep in the sand", "Jump and flip in the air", "Hide in rocks"],
                    "correct": 1
                }
            ]),
            (turtle_img, "Sea Turtle", [
                {
                    "question": "I carry my home with me wherever I go. Who am I?",
                    "answers": ["A hermit crab", "A sea turtle", "A snail"],
                    "correct": 1
                },
                {
                    "question": "What's my favorite food?",
                    "answers": ["Seaweed", "Jellyfish", "Fish"],
                    "correct": 1
                },
                {
                    "question": "How do I breathe?",
                    "answers": ["Through my shell", "I swim to the surface", "Through my flippers"],
                    "correct": 1
                }
            ]),
            (starfish_img, "Starfish", [
                {
                    "question": "I'm a colorful star of the sea! How many arms do I have?",
                    "answers": ["Three", "Four", "Five"],
                    "correct": 2
                },
                {
                    "question": "What do I like to eat?",
                    "answers": ["Tiny sea creatures", "Seaweed", "Sand"],
                    "correct": 0
                },
                {
                    "question": "What color can I be?",
                    "answers": ["Only yellow", "Only red", "Many different colors"],
                    "correct": 2
                }
            ]),
            (octopus_img, "Octopus", [
                {
                    "question": "I'm very smart and have lots of arms! Who am I?",
                    "answers": ["A jellyfish", "An octopus", "A seahorse"],
                    "correct": 1
                },
                {
                    "question": "How many arms do I have?",
                    "answers": ["Four", "Six", "Eight"],
                    "correct": 2
                },
                {
                    "question": "What's my special trick?",
                    "answers": ["I can change color", "I can fly", "I can walk on land"],
                    "correct": 0
                }
            ]),
            (fish_img, "Tropical Fish", [
                {
                    "question": "I'm small, colorful, and swim in groups! What am I?",
                    "answers": ["A tropical fish", "A shark", "A whale"],
                    "correct": 0
                },
                {
                    "question": "What helps me swim?",
                    "answers": ["My fins", "My legs", "My arms"],
                    "correct": 0
                },
                {
                    "question": "Where do I like to live?",
                    "answers": ["Deep dark ocean", "Warm coral reefs", "Cold arctic waters"],
                    "correct": 1
                }
            ])
        ]
        
        creatures = []
        positions = []
        
        for img, name, questions in creature_data:
            x, y = self.get_random_position(positions)
            positions.append((x, y))
            creatures.append(Creature(x, y, img, name, questions))
            
        return creatures
        
    def create_clues(self):
        clues = []
        positions = [(c.x, c.y) for c in self.creatures]  # Avoid creature positions
        
        clue_data = [
            ("Look for splashing near the surface!", "Dolphin"),
            ("Some creatures carry their homes with them.", "Sea Turtle"),
            ("Look for colorful stars in the coral!", "Starfish"),
            ("Search for clever creatures with many arms!", "Octopus"),
            ("Watch for bright colors in the reef!", "Tropical Fish")
        ]
        
        for text, creature_hint in clue_data:
            x, y = self.get_random_position(positions)
            positions.append((x, y))
            clues.append(Clue(x, y, text, creature_hint))
            
        return clues

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        click_occurred = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                click_occurred = True
                
                # Handle creature clicks in EXPLORE state
                if self.state == EXPLORE:
                    for creature in self.creatures:
                        if not creature.visited and creature.can_interact and creature.is_hovered:
                            self.current_creature = creature
                            self.state = QUIZ
                            self.setup_quiz()
                            break
                
                # Handle quiz state clicks
                elif self.state == QUIZ:
                    for i, button in enumerate(self.answer_buttons):
                        if button.rect.collidepoint(mouse_pos):
                            # Visual feedback
                            button.selected = True
                            self.check_answer(i)
                            break
                
                # Handle reward state clicks
                elif self.state == REWARD:
                    debug_print("Click processed in REWARD state, returning to EXPLORE")
                    if self.current_creature and not self.current_creature.visited:
                        self.state = QUIZ
                        self.setup_quiz()
                    else:
                        self.state = EXPLORE
                        self.current_creature = None
                
                # Handle game over state clicks
                elif self.state == GAME_OVER:
                    debug_print("Click processed in GAME_OVER state, restarting game")
                    self.__init__()  # Re-initialize the game
        
        # Handle movement keys only in EXPLORE state
        if self.state == EXPLORE:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            # Add WASD support alongside arrow keys
            if keys[K_LEFT] or keys[K_a]:
                dx = -self.player.speed
            if keys[K_RIGHT] or keys[K_d]:
                dx = self.player.speed
            if keys[K_UP] or keys[K_w]:
                dy = -self.player.speed
            if keys[K_DOWN] or keys[K_s]:
                dy = self.player.speed
            
            if dx != 0 or dy != 0:
                # Only move if actually pressing direction keys
                self.player.move(dx, dy)
                
                # Only log position occasionally
                current_time = pygame.time.get_ticks()
                if DEBUG_MODE and current_time - self.last_position_update > 1000:
                    debug_print(f"Player moved to: ({self.player.x}, {self.player.y})")
                    self.last_position_update = current_time
        
        # Handle bubble popping with mouse clicks
        if click_occurred:
            for bubble in self.bubbles:
                if bubble.check_pop(mouse_pos):
                    self.bubble_count += 1

    def check_creature_collisions(self):
        if self.state != EXPLORE:
            return
        
        for creature in self.creatures:
            if not creature.visited and creature.can_interact:
                if creature.is_hovered:
                    # Show interaction hint
                    hint_text = "Swim closer to interact!"
                    if creature.can_interact:
                        hint_text = "Click to interact!"  # Changed from "Press SPACE"
                
                    text_surface = font.render(hint_text, True, WHITE)
                    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
                    screen.blit(text_surface, text_rect)

    def setup_quiz(self):
        current_question = self.current_creature.get_next_question()
        if current_question:
            self.answer_buttons = []
            for i, answer in enumerate(current_question["answers"]):
                button = AnimatedButton(
                    SCREEN_WIDTH // 2 - 125,
                    350 + i * 60,
                    250, 50,
                    answer,
                    (200, 200, 255)
                )
                self.answer_buttons.append(button)
            return True
        return False

    def check_answer(self, answer_index):
        current_question = self.current_creature.questions[
            self.current_creature.current_question_index - 1
        ]
        
        if answer_index == current_question["correct"]:
            self.celebration_effects.append(
                CelebrationEffect(self.player.x, self.player.y)
            )
            
            # Check if all questions are answered
            if self.current_creature.current_question_index >= len(self.current_creature.questions):
                self.current_creature.discovered = True
                self.current_creature.visited = True
                self.player.stars += 1
                self.result_message = f"Congratulations! You've discovered the {self.current_creature.name}!"
            else:
                self.result_message = "Correct! Here's another question..."
                self.state = QUIZ
                self.setup_quiz()
                return
                
            if correct_sound:
                correct_sound.play()
        else:
            self.result_message = "Not quite! Try again..."
            if wrong_sound:
                wrong_sound.play()
        
        self.state = REWARD
        self.result_time = pygame.time.get_ticks()
        debug_print(f"Changing to REWARD state at time: {self.result_time}", True)
        
        # Added a more visible prompt
        self.result_message += "\n\nClick anywhere to continue"

    def print_debug_info(self):
        """Print detailed debugging information about the game state"""
        debug_print("\n----- GAME DEBUG INFORMATION -----", True)
        debug_print(f"Current State: {['EXPLORE', 'QUIZ', 'REWARD', 'GAME_OVER'][self.state]}", True)
        debug_print(f"Stars Collected: {self.player.stars}/{len(self.creatures)}", True)
        debug_print(f"Player Position: ({self.player.x}, {self.player.y})", True)
        
        debug_print("\nCreature Status:", True)
        for i, creature in enumerate(self.creatures):
            debug_print(f"{i}: {creature.name} at ({creature.x}, {creature.y}) - Visited: {creature.visited}", True)
            if not creature.visited:
                distance = math.sqrt((self.player.x - creature.x)**2 + (self.player.y - creature.y)**2)
                debug_print(f"   Distance: {distance:.1f} pixels", True)
        
        debug_print("\nMemory Usage:", True)
        debug_print(f"Sounds loaded: {correct_sound is not None}, {wrong_sound is not None}, {background_music is not None}", True)
        debug_print("----- END DEBUG INFORMATION -----\n", True)

    def update(self):
        # Add a key press fallback for reward state
        if self.state == REWARD:
            keys = pygame.key.get_pressed()
            if keys[K_SPACE] or keys[K_RETURN] or keys[K_ESCAPE]:
                debug_print("Key press detected in REWARD state, returning to EXPLORE")
                self.state = EXPLORE
                self.current_creature = None  # Reset current creature
        
        # Only use timer-based transition as a backup
        current_time = pygame.time.get_ticks()
        if self.state == REWARD and current_time - self.result_time > 5000:  # Increased to 5 seconds
            debug_print(f"Reward timeout after {current_time - self.result_time}ms - changing state to EXPLORE")
            self.state = EXPLORE
            self.current_creature = None  # Reset current creature
        
        # Check for game completion
        if self.player.stars >= len(self.creatures):
            debug_print("All stars collected, changing to GAME_OVER state", True)
            self.state = GAME_OVER
        
        # Debug info at very rare intervals to prevent console flood
        if DEBUG_MODE and current_time % 30000 < 100:  # Print debug info roughly every 30 seconds
            visited_count = sum(1 for creature in self.creatures if creature.visited)
            debug_print(f"Current state: {self.state}, Stars: {self.player.stars}, Visited creatures: {visited_count}/{len(self.creatures)}")

        # Update celebration effects
        for effect in self.celebration_effects[:]:  # Create a copy of the list for iteration
            effect.update()
            if not effect.alive:
                self.celebration_effects.remove(effect)

        # Update all bubbles
        for bubble in self.bubbles:
            bubble.update()
        
        # Update clues
        mouse_pos = pygame.mouse.get_pos()
        for clue in self.clues:
            clue.update(mouse_pos)
    
        # Update creatures with player position
        for creature in self.creatures:
            creature.update((self.player.x, self.player.y), mouse_pos)
        
        # Apply ocean currents to player movement
        if self.state == EXPLORE:
            for current in self.ocean_currents:
                dist = math.sqrt(
                    (self.player.x - current['x'])**2 + 
                    (self.player.y - current['y'])**2
                )
                if dist < current['radius']:
                    # Calculate current effect
                    force = (1 - dist/current['radius']) * current['strength']
                    angle = math.atan2(self.player.y - current['y'], 
                                     self.player.x - current['x'])
                    self.player.x += math.cos(angle) * force
                    self.player.y += math.sin(angle) * force
        
        # Update combo system
        current_time = pygame.time.get_ticks()
        if current_time - self.last_collect_time > 5000:  # Reset combo after 5 seconds
            self.combo_multiplier = 1.0

    def draw(self):
        # Draw background
        screen.blit(background_img, (0, 0))
        
        # Draw debug info
        debug_info = f"State: {['EXPLORE', 'QUIZ', 'REWARD', 'GAME_OVER'][self.state]} | Stars: {self.player.stars}/{len(self.creatures)}"
        debug_text = font.render(debug_info, True, (255, 255, 255))
        screen.blit(debug_text, (10, SCREEN_HEIGHT - 30))
        
        # Draw invisible collision circles for debugging - only when enabled
        if self.state == EXPLORE and self.show_collision_circles:
            for creature in self.creatures:
                if not creature.visited:
                    # Draw collision radius
                    collision_radius = max(creature.image.get_width(), creature.image.get_height()) / 2 + 30
                    pygame.draw.circle(screen, (255, 0, 0), (creature.x, creature.y), int(collision_radius), 1)
        
        # Draw creatures
        for creature in self.creatures:
            if not creature.visited:
                creature.draw()
                # Draw name label above each creature for better visibility
                name_text = font.render(creature.name, True, WHITE)
                screen.blit(name_text, (creature.x - name_text.get_width() // 2, creature.y - 50))
        
        # Draw player
        self.player.draw()
        
        # Draw stars counter
        star_text = font.render(f"Stars: {self.player.stars}/{len(self.creatures)}", True, WHITE)
        screen.blit(star_text, (20, 20))
        
        # Draw clues
        for clue in self.clues:
            clue.draw()
        
        # Draw collected clues panel
        if self.collected_clues:
            clue_panel = pygame.Rect(10, 50, 200, 30 * len(self.collected_clues))
            pygame.draw.rect(screen, (255, 255, 255, 180), clue_panel)
            for i, clue in enumerate(self.collected_clues):
                clue_text = small_font.render(clue, True, BLACK)
                screen.blit(clue_text, (15, 55 + i * 30))
        
        # Draw quiz if in quiz state
        if self.state == QUIZ:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            # Draw question box
            question_box = pygame.Rect(SCREEN_WIDTH // 2 - 300, 150, 600, 150)
            pygame.draw.rect(screen, WHITE, question_box, border_radius=15)
            pygame.draw.rect(screen, BLACK, question_box, 2, border_radius=15)
            
            # Draw creature name
            name_text = large_font.render(self.current_creature.name, True, BLACK)
            screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 170))
            
            # Get current question text from questions list
            current_question = self.current_creature.questions[
                self.current_creature.current_question_index - 1
            ]
            question_text = font.render(current_question["question"], True, BLACK)
            screen.blit(question_text, (SCREEN_WIDTH // 2 - question_text.get_width() // 2, 220))
            
            # Update and draw answer buttons
            for button in self.answer_buttons:
                button.update()
                button.draw()
        
        # Draw reward message if in reward state
        if self.state == REWARD:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            # Make the box even larger and add text wrapping
            result_box = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 200, 600, 400)
            
            # Draw box and shadow
            shadow_box = result_box.copy()
            shadow_box.x += 5
            shadow_box.y += 5
            pygame.draw.rect(screen, (100, 100, 100), shadow_box, border_radius=15)
            pygame.draw.rect(screen, WHITE, result_box, border_radius=15)
            
            # Word wrap the message
            words = self.result_message.split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = large_font.render(test_line, True, BLACK)
                if test_surface.get_width() <= result_box.width - 40:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
            
            # Draw wrapped text
            y_offset = result_box.top + 30
            for line in lines:
                text_surface = large_font.render(line, True, BLACK)
                x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
                screen.blit(text_surface, (x, y_offset))
                y_offset += 40
            
            # Draw stars if correct
            if "Correct" in self.result_message:
                star_y = y_offset + 60
                for i in range(5):
                    star_x = SCREEN_WIDTH // 2 - 100 + i * 50
                    pygame.draw.polygon(screen, YELLOW, [
                        (star_x, star_y - 15),
                        (star_x + 5, star_y - 5),
                        (star_x + 15, star_y - 5),
                        (star_x + 7, star_y + 5),
                        (star_x + 10, star_y + 15),
                        (star_x, star_y + 10),
                        (star_x - 10, star_y + 15),
                        (star_x - 7, star_y + 5),
                        (star_x - 15, star_y - 5),
                        (star_x - 5, star_y - 5)
                    ])
            
            # Draw continue prompt with gentle animation
            continue_y = result_box.bottom - 60  # Position inside the box
            pulse = (math.sin(pygame.time.get_ticks() * 0.005) + 1) * 0.5  # Slower, gentler pulse
            continue_color = (0, 100, 200)  # Friendly blue color
            pulse_font = pygame.font.SysFont('Arial', int(24 + pulse * 4))  # Smaller pulse range
            continue_text = pulse_font.render("Click anywhere or press SPACE to continue", True, continue_color)
            continue_x = SCREEN_WIDTH // 2 - continue_text.get_width() // 2
            screen.blit(continue_text, (continue_x, continue_y))
        
        # Draw celebration effects
        for effect in self.celebration_effects:
            effect.draw()

        # Draw game over screen
        if self.state == GAME_OVER:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            completion_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100, 500, 200)
            pygame.draw.rect(screen, WHITE, completion_box, border_radius=15)
            
            congrats_text = large_font.render("Congratulations!", True, BLACK)
            screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, SCREEN_HEIGHT // 2 - 75))
            
            complete_text = font.render("You've explored the entire ocean!", True, BLACK)
            screen.blit(complete_text, (SCREEN_WIDTH // 2 - complete_text.get_width() // 2, SCREEN_HEIGHT // 2 - 25))
            
            stars_text = font.render(f"You collected all {self.player.stars} stars!", True, BLACK)
            screen.blit(stars_text, (SCREEN_WIDTH // 2 - stars_text.get_width() // 2, SCREEN_HEIGHT // 2 + 25))
            
            restart_text = font.render("Click anywhere to play again!", True, BLACK)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 75))
        
        pygame.display.flip()

    def run(self):
        debug_print("Game starting...", True)
        # Add a failsafe mechanism to track game state
        last_state = None
        state_change_time = pygame.time.get_ticks()
        
        while True:
            self.clock.tick(60)
            
            # Track state changes for debugging
            if self.state != last_state:
                current_time = pygame.time.get_ticks()
                debug_print(f"State changed from {last_state} to {self.state} after {current_time - state_change_time}ms", True)
                last_state = self.state
                state_change_time = current_time
            
            # Process events and update game
            self.handle_events()
            self.update()
            self.draw()
            
            # Update window title with state
            state_names = ["EXPLORE", "QUIZ", "REWARD", "GAME_OVER"]
            pygame.display.set_caption(f'Ocean Explorer - State: {state_names[self.state]} - Stars: {self.player.stars}/{len(self.creatures)}')

# Main function with improved setup
def main():
    # Create asset directories if they don't exist
    os.makedirs(os.path.join('assets', 'images'), exist_ok=True)
    os.makedirs(os.path.join('assets', 'sounds'), exist_ok=True)
    
    debug_print("Ocean Explorer starting...", True)
    game = Game()
    game.run()

if __name__ == "__main__":
    main()

