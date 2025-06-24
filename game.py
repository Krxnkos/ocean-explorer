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
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ocean Explorer')

# Colors
BLUE = (0, 119, 190)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

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
    player_img = load_image('player.png', 0.2)
    dolphin_img = load_image('dolphin.png', 0.3)
    turtle_img = load_image('turtle.png', 0.2)
    starfish_img = load_image('starfish.png', 0.15)
    octopus_img = load_image('octopus.png', 0.25)
    fish_img = load_image('fish.png', 0.15)
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
    def __init__(self, x, y, image, name, question, answers, correct_answer):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)  # Make sure center is set properly
        self.visited = False
    
    def draw(self):
        # Make sure the rect is at the right position before drawing
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

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

class Bubble:
    def __init__(self):
        self.x = random.randint(50, SCREEN_WIDTH - 50)
        self.y = random.randint(50, SCREEN_HEIGHT - 150)  # Keep bubbles away from the bottom
        self.speed = random.uniform(0.5, 1.5)
        self.image = bubble_img
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.popped = False
    
    def update(self):
        if not self.popped:
            # Bubbles slowly rise and drift
            self.y -= self.speed
            self.x += random.uniform(-0.5, 0.5)
            
            # Wrap around if they go off screen
            if self.y < -20:
                self.y = SCREEN_HEIGHT + 20
                self.x = random.randint(50, SCREEN_WIDTH - 50)
            
            self.rect.center = (self.x, self.y)
    
    def draw(self):
        if not self.popped:
            screen.blit(self.image, self.rect)
    
    def check_pop(self, pos):
        if not self.popped and self.rect.collidepoint(pos):
            self.popped = True
            if bubble_pop_sound:
                try:
                    bubble_pop_sound.play()
                except:
                    pass
            return True
        return False

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

class Game:
    def __init__(self):
        self.player = Player()
        self.state = EXPLORE
        self.current_creature = None
        self.answer_buttons = []
        self.result_message = ""
        self.result_time = 0
        self.clock = pygame.time.Clock()
        self.creatures = self.create_creatures()
        self.last_position_update = 0
        self.show_collision_circles = False  # Toggle for visual debugging
        
        self.bubbles = [Bubble() for _ in range(15)]  # Create 15 bubbles
        self.treasures = [Treasure() for _ in range(3)]  # Create 3 treasures
        self.seashells = [Seashell() for _ in range(5)]  # Create 5 seashells
        self.corals = [Coral(random.randint(50, SCREEN_WIDTH - 50), 
                           random.randint(50, SCREEN_HEIGHT - 50)) for _ in range(8)]  # Create 8 coral formations
        
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

    def create_creatures(self):
        creatures = [
            Creature(600, 150, dolphin_img, "Dolphin", 
                    "Which animal is smart and can jump out of water?",
                    ["Dolphin", "Shark", "Crab"], 0),
            Creature(200, 450, turtle_img, "Turtle", 
                    "Which sea creature has a shell?",
                    ["Jellyfish", "Turtle", "Eel"], 1),
            Creature(400, 100, starfish_img, "Starfish", 
                    "How many arms does a starfish usually have?",
                    ["Three", "Four", "Five"], 2),
            Creature(700, 400, octopus_img, "Octopus", 
                    "How many legs does the octopus have?",
                    ["Six", "Eight", "Ten"], 1),
            Creature(300, 300, fish_img, "Fish", 
                    "Can you find the blue and yellow fish?",
                    ["Yes! Here it is!", "No, I can't see it", "What fish?"], 0)
        ]
        return creatures

    def handle_events(self):
        # Store current mouse position outside the event loop
        mouse_pos = pygame.mouse.get_pos()
        
        # Track if any mouse clicks happened this frame
        click_occurred = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            # Track mouse clicks for all states
            if event.type == MOUSEBUTTONDOWN:
                click_occurred = True
                debug_print(f"Mouse click detected at position: {mouse_pos}, current state: {self.state}")
            
            # Handle debug key presses
            if event.type == KEYDOWN:
                global DEBUG_MODE
                
                # R key - Reset game
                if event.key == K_r:
                    debug_print("Reset key pressed - restarting game", True)
                    self.__init__()
                
                # D key - Toggle debug mode
                elif event.key == K_d:
                    DEBUG_MODE = not DEBUG_MODE
                    debug_print(f"Debug mode {'enabled' if DEBUG_MODE else 'disabled'}", True)
                    
                    if DEBUG_MODE:
                        self.print_debug_info()
                
                # F key - Force next state
                elif event.key == K_f:
                    old_state = self.state
                    self.state = (self.state + 1) % 4  # Cycle through states
                    debug_print(f"Forced state change: {old_state} -> {self.state}", True)
                
                # Number keys - Teleport to creatures
                elif event.key in [K_1, K_2, K_3, K_4, K_5]:
                    idx = event.key - K_1  # Convert key to index (0-4)
                    if idx < len(self.creatures):
                        creature = self.creatures[idx]
                        old_pos = (self.player.x, self.player.y)
                        # Position player near the creature
                        self.player.x = creature.x - 50
                        self.player.y = creature.y
                        debug_print(f"Teleported player from {old_pos} to {(self.player.x, self.player.y)} near {creature.name}", True)
                
                # S key - Add a star
                elif event.key == K_s:
                    self.player.stars += 1
                    debug_print(f"Added star: {self.player.stars}/{len(self.creatures)}", True)
                
                # G key - Go to game over
                elif event.key == K_g:
                    debug_print("Going to game over screen", True)
                    self.state = GAME_OVER
                    
                # C key - Toggle collision circles
                elif event.key == K_c:
                    self.show_collision_circles = not self.show_collision_circles
                    debug_print(f"Collision circles {'shown' if self.show_collision_circles else 'hidden'}", True)
            
            if self.state == QUIZ:
                for button in self.answer_buttons:
                    button.check_hover(mouse_pos)
                    if click_occurred and button.rect.collidepoint(mouse_pos):
                        self.check_answer(self.answer_buttons.index(button))
                        # Consume the click to prevent it from affecting other states
                        click_occurred = False
        
        # Handle reward state clicks outside the event loop to make sure they're detected
        if self.state == REWARD and click_occurred:
            debug_print("Click processed in REWARD state, returning to EXPLORE")
            self.state = EXPLORE
            # Important: actually reset the current_creature to None
            self.current_creature = None
        
        # Handle game over state clicks
        elif self.state == GAME_OVER and click_occurred:
            debug_print("Click processed in GAME_OVER state, restarting game")
            self.__init__()  # Re-initialize the game
        
        # Handle movement keys only in EXPLORE state
        if self.state == EXPLORE:
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[K_LEFT]:
                dx = -self.player.speed
            if keys[K_RIGHT]:
                dx = self.player.speed
            if keys[K_UP]:
                dy = -self.player.speed
            if keys[K_DOWN]:
                dy = self.player.speed
            
            if dx != 0 or dy != 0:
                # Only move if actually pressing direction keys
                self.player.move(dx, dy)
                
                # Only log position occasionally to avoid terminal flood
                current_time = pygame.time.get_ticks()
                if DEBUG_MODE and current_time - self.last_position_update > 1000:  # Once per second at most
                    debug_print(f"Player moved to: ({self.player.x}, {self.player.y})")
                    self.last_position_update = current_time
            
            # Check for creature collisions - only if we're not currently handling one
            self.check_creature_collisions()
        
        # Handle bubble popping with mouse clicks
        if click_occurred:
            for bubble in self.bubbles:
                if bubble.check_pop(mouse_pos):
                    self.bubble_count += 1

    def check_creature_collisions(self):
        """Separate method to check for collisions with creatures"""
        if self.state != EXPLORE or self.current_creature is not None:
            return
            
        # Only print creature positions in debug mode and not too frequently
        current_time = pygame.time.get_ticks()
        if DEBUG_MODE and current_time - last_debug_time > DEBUG_INTERVAL:
            debug_print("\nCreature positions:")
            for i, creature in enumerate(self.creatures):
                debug_print(f"{i}: {creature.name} at ({creature.x}, {creature.y}) - Visited: {creature.visited}")
            debug_print(f"Player at ({self.player.x}, {self.player.y})")
        
        # Check for collisions with any unvisited creature
        for creature in self.creatures:
            if not creature.visited:
                # Calculate distance-based collision instead of rect-based
                distance = math.sqrt((self.player.x - creature.x)**2 + (self.player.y - creature.y)**2)
                # Use a more generous collision radius
                collision_radius = max(creature.image.get_width(), creature.image.get_height()) / 2
                
                # Only log distances in debug mode and not too frequently
                if DEBUG_MODE and current_time - last_debug_time > DEBUG_INTERVAL:
                    debug_print(f"Distance to {creature.name}: {distance}, collision radius: {collision_radius}")
                
                if distance < collision_radius + 30:  # Add 30px buffer for easier collision
                    debug_print(f"Collision with creature: {creature.name} (distance-based)", True)
                    self.current_creature = creature
                    self.state = QUIZ
                    self.setup_quiz()
                    return

    def setup_quiz(self):
        # Create answer buttons
        self.answer_buttons = []
        for i, answer in enumerate(self.current_creature.answers):
            button = Button(SCREEN_WIDTH // 2 - 125, 350 + i * 60, 250, 50, answer, (200, 200, 255))
            self.answer_buttons.append(button)

    def check_answer(self, answer_index):
        if answer_index == self.current_creature.correct_answer:
            self.result_message = "Correct! Well done!"
            if correct_sound:
                try:
                    correct_sound.play()
                except:
                    pass
            self.player.stars += 1
            self.current_creature.visited = True
            debug_print(f"Correct answer! Stars: {self.player.stars}/{len(self.creatures)}", True)
        else:
            self.result_message = "Try again! That's not right."
            if wrong_sound:
                try:
                    wrong_sound.play()
                except:
                    pass
            debug_print("Incorrect answer", True)
        
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

        # Update all bubbles
        for bubble in self.bubbles:
            bubble.update()

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
            
            # Draw question
            question_text = font.render(self.current_creature.question, True, BLACK)
            screen.blit(question_text, (SCREEN_WIDTH // 2 - question_text.get_width() // 2, 220))
            
            # Draw answer buttons
            for button in self.answer_buttons:
                button.draw()
        
        # Draw reward message if in reward state
        if self.state == REWARD:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            screen.blit(overlay, (0, 0))
            
            # Make the reward box larger and more visible
            result_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 100, 500, 200)
            pygame.draw.rect(screen, WHITE, result_box, border_radius=15)
            pygame.draw.rect(screen, (0, 0, 0), result_box, 3, border_radius=15)  # Add thicker border
            
            # Split result message for better display
            result_lines = self.result_message.split('\n')
            y_offset = SCREEN_HEIGHT // 2 - 50
            
            for line in result_lines:
                result_text = font.render(line, True, BLACK)
                screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, y_offset))
                y_offset += 30
            
            # Add a more visible and explicit continue prompt with animation
            continue_text = font.render("Click anywhere or press SPACE to continue", True, (200, 0, 0))
            # Make the text pulse for visibility
            pulse = (math.sin(pygame.time.get_ticks() * 0.01) + 1) * 0.5  # 0 to 1 pulsing value
            pulse_scale = 1.0 + (0.1 * pulse)
            pulse_font = pygame.font.SysFont('Arial', int(24 * pulse_scale))
            continue_text = pulse_font.render("Click anywhere or press SPACE to continue", True, (200, 0, 0))
            screen.blit(continue_text, (SCREEN_WIDTH // 2 - continue_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))
            
            if "Correct" in self.result_message:
                # Draw stars for visual reward
                for i in range(5):
                    star_x = SCREEN_WIDTH // 2 - 100 + i * 50
                    star_y = SCREEN_HEIGHT // 2 + 50  # Move stars down to accommodate text
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
        
        # Draw debug status with D key info
        debug_status = "Debug Mode: OFF (press D to enable)" if not DEBUG_MODE else "Debug Mode: ON (press D to disable)"
        debug_status_text = font.render(debug_status, True, (200, 200, 200))
        screen.blit(debug_status_text, (SCREEN_WIDTH - debug_status_text.get_width() - 10, 10))
        
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

