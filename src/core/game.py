import pygame
import sys
import random
import math
from pygame.locals import *

from ..utils.constants import *
from ..utils.debug import debug_print
from ..utils.loader import load_image, load_sound, create_default_background
from ..entities.player import Player
from ..entities.creature import Creature
from ..entities.bubble import Bubble
from ..entities.treasure import Treasure
from ..entities.seashell import Seashell
from ..entities.clue import Clue  # Add this import
from ..ui.button import Button
from ..ui.animated_button import AnimatedButton
from ..ui.effects import CelebrationEffect

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Ocean Explorer')
        
        # Load assets
        self.load_game_assets()
        
        # Initialize game state
        self.init_game_state()
        
        # Start background music
        if self.background_music:
            try:
                self.background_music.play(-1)
            except:
                debug_print("Could not play background music", True)

    def load_game_assets(self):
        # Load images with proper scaling
        self.player_img = load_image('player.png', 0.15)
        self.dolphin_img = load_image('dolphin.png', 0.2)
        self.turtle_img = load_image('turtle.png', 0.15)
        self.starfish_img = load_image('starfish.png', 0.1)
        self.octopus_img = load_image('octopus.png', 0.2)
        self.fish_img = load_image('fish.png', 0.1)
        
        # Load background
        self.background_img = load_image('ocean_bg.png')
        if self.background_img.get_width() != SCREEN_WIDTH or self.background_img.get_height() != SCREEN_HEIGHT:
            self.background_img = pygame.transform.scale(self.background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Load sounds
        self.correct_sound = load_sound('correct.wav')
        self.wrong_sound = load_sound('wrong.wav')
        self.background_music = load_sound('ocean_music.wav')
        
        # Initialize fonts
        self.font = pygame.font.SysFont('Arial', 24)
        self.large_font = pygame.font.SysFont('Arial', 32)
        self.small_font = pygame.font.SysFont('Arial', 18)

    def init_game_state(self):
        self.player = Player(self.player_img)
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
        self.show_collision_circles = False
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
        
        # Initialize collectibles with fewer bubbles
        self.bubbles = [Bubble() for _ in range(15)]  # Reduced from 30
        self.bubble_count = 0
        self.last_bubble_spawn = 0
        self.bubble_spawn_delay = 2000  # 2 seconds between spawns
        
        # Initialize game timer
        self.game_start_time = pygame.time.get_ticks()
        self.elapsed_time = 0

    def get_random_position(self, existing_positions=None):
        if existing_positions is None:
            existing_positions = []
            
        for attempt in range(100):
            x = random.randint(self.safe_margin, SCREEN_WIDTH - self.safe_margin)
            y = random.randint(self.safe_margin, SCREEN_HEIGHT - self.safe_margin)
            
            valid_position = True
            for pos in existing_positions:
                distance = math.sqrt((x - pos[0])**2 + (y - pos[1])**2)
                if distance < self.min_creature_distance:
                    valid_position = False
                    break
                    
            if valid_position:
                return x, y
        return (random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT))

    def create_creatures(self):
        creature_data = [
            (self.dolphin_img, "Dolphin", [
                {
                    "question": "I love to jump and play! What am I?",
                    "answers": ["A friendly dolphin", "A grumpy shark", "A dancing crab"],
                    "correct": 0
                },
                {
                    "question": "What special sound power do I have?",
                    "answers": ["Barking", "Echolocation", "Humming"],
                    "correct": 1
                },
                {
                    "question": "What's my favorite thing to do?",
                    "answers": ["Sleep in sand", "Jump and flip", "Hide in rocks"],
                    "correct": 1
                }
            ]),
            (self.turtle_img, "Sea Turtle", [
                {
                    "question": "I carry my home with me! Who am I?",
                    "answers": ["A hermit crab", "A sea turtle", "A snail"],
                    "correct": 1
                },
                {
                    "question": "What do I love to eat?",
                    "answers": ["Seaweed", "Jellyfish", "Fish"],
                    "correct": 1
                },
                {
                    "question": "How long can I hold my breath?",
                    "answers": ["1 minute", "5 minutes", "Several hours"],
                    "correct": 2
                }
            ]),
            (self.starfish_img, "Starfish", [
                {
                    "question": "How many arms do I usually have?",
                    "answers": ["Three", "Four", "Five"],
                    "correct": 2
                },
                {
                    "question": "What amazing thing can I do if I lose an arm?",
                    "answers": ["Grow it back", "Swim faster", "Change color"],
                    "correct": 0
                },
                {
                    "question": "Where do I like to live?",
                    "answers": ["Deep ocean", "Tide pools", "Rivers"],
                    "correct": 1
                }
            ]),
            (self.octopus_img, "Octopus", [
                {
                    "question": "I'm super smart and have lots of arms!",
                    "answers": ["An octopus", "A jellyfish", "A seahorse"],
                    "correct": 0
                },
                {
                    "question": "What's my special hiding trick?",
                    "answers": ["Become invisible", "Change colors", "Dig in sand"],
                    "correct": 1
                },
                {
                    "question": "How many arms do I have?",
                    "answers": ["Four", "Six", "Eight"],
                    "correct": 2
                }
            ]),
            (self.fish_img, "Tropical Fish", [
                {
                    "question": "We swim together in a big group called a...",
                    "answers": ["School", "Party", "Team"],
                    "correct": 0
                },
                {
                    "question": "What helps us swim?",
                    "answers": ["Our fins", "Our tails only", "Magic"],
                    "correct": 0
                },
                {
                    "question": "Where do we love to live?",
                    "answers": ["Cold waters", "Warm coral reefs", "Dark caves"],
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
        """Create clues at random positions, avoiding creature positions"""
        clues = []
        positions = [(c.x, c.y) for c in self.creatures]
        
        clue_data = [
            ("I've seen splashing and jumping near the surface!", "Dolphin"),
            ("Look for someone who carries their home everywhere!", "Sea Turtle"),
            ("I spotted something with five colorful arms!", "Starfish"),
            ("Something smart with many arms lives here...", "Octopus"),
            ("Watch for bright colors dancing in the coral!", "Fish")
        ]
        
        for text, creature_hint in clue_data:
            x, y = self.get_random_position(positions)
            positions.append((x, y))
            clues.append(Clue(x, y, text, creature_hint))
            
        return clues
        
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
            
            if self.current_creature.current_question_index >= len(self.current_creature.questions):
                self.current_creature.discovered = True
                self.current_creature.visited = True
                self.player.stars += 1
                self.result_message = f"Amazing! You've discovered something new!"
            else:
                self.result_message = "Correct! Here's another question..."
                self.state = QUIZ
                self.setup_quiz()
                return
                
            if self.correct_sound:
                self.correct_sound.play()
        else:
            self.result_message = "Not quite! Try again!"
            if self.wrong_sound:
                self.wrong_sound.play()
        
        self.state = REWARD
        self.result_time = pygame.time.get_ticks()

    def update(self):
        if self.state == EXPLORE:
            # Update player position from keyboard input
            keys = pygame.key.get_pressed()
            dx, dy = 0, 0
            if keys[K_LEFT] or keys[K_a]:
                dx = -self.player.speed
            if keys[K_RIGHT] or keys[K_d]:
                dx = self.player.speed
            if keys[K_UP] or keys[K_w]:
                dy = -self.player.speed
            if keys[K_DOWN] or keys[K_s]:
                dy = self.player.speed
                
            if dx != 0 or dy != 0:
                self.player.move(dx, dy)
            
            # Apply ocean currents
            for current in self.ocean_currents:
                dist = math.sqrt(
                    (self.player.x - current['x'])**2 + 
                    (self.player.y - current['y'])**2
                )
                if dist < current['radius']:
                    force = (1 - dist/current['radius']) * current['strength']
                    angle = math.atan2(self.player.y - current['y'], 
                                     self.player.x - current['x'])
                    self.player.x += math.cos(angle) * force
                    self.player.y += math.sin(angle) * force
            
            # Update creatures
            for creature in self.creatures:
                creature.update((self.player.x, self.player.y), pygame.mouse.get_pos())
            
            # Update bubbles
            for bubble in self.bubbles:
                bubble.update()
                if bubble.y < -50:  # Reset bubbles that float off screen
                    bubble.y = SCREEN_HEIGHT + random.randint(0, 100)
                    bubble.x = random.randint(50, SCREEN_WIDTH - 50)
                    bubble.popped = False
        
        elif self.state == QUIZ:
            mouse_pos = pygame.mouse.get_pos()
            for button in self.answer_buttons:
                button.update()
                button.check_hover(mouse_pos)
                
        # Update celebration effects
        for effect in self.celebration_effects[:]:
            effect.update()
            if not effect.alive:
                self.celebration_effects.remove(effect)

    def draw(self):
        # Draw background
        self.screen.blit(self.background_img, (0, 0))
        
        # Draw ocean currents (subtle visualization)
        for current in self.ocean_currents:
            surf = pygame.Surface((current['radius']*2, current['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (0, 100, 255, 50), 
                             (current['radius'], current['radius']), 
                             current['radius'])
            self.screen.blit(surf, (current['x'] - current['radius'], 
                                  current['y'] - current['radius']))
        
        # Draw bubbles
        for bubble in self.bubbles:
            bubble.draw(self.screen)
        
        # Draw creatures
        for creature in self.creatures:
            creature.draw(self.screen, self.font)
        
        # Draw player
        self.player.draw(self.screen)
        
        # Draw quiz state
        if self.state == QUIZ:
            # Draw semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            # Draw question box
            question_box = pygame.Rect(SCREEN_WIDTH // 2 - 300, 150, 600, 150)
            pygame.draw.rect(self.screen, WHITE, question_box, border_radius=15)
            pygame.draw.rect(self.screen, BLACK, question_box, 2, border_radius=15)
            
            # Draw current question
            current_question = self.current_creature.questions[
                self.current_creature.current_question_index - 1
            ]
            question_text = self.font.render(current_question["question"], True, BLACK)
            self.screen.blit(question_text, (SCREEN_WIDTH // 2 - question_text.get_width() // 2, 220))
            
            # Draw answer buttons
            for button in self.answer_buttons:
                button.draw(self.screen, self.font)
        
        # Draw reward state
        elif self.state == REWARD:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            result_box = pygame.Rect(SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 150, 500, 300)
            shadow_box = result_box.copy()
            shadow_box.x += 5
            shadow_box.y += 5
            pygame.draw.rect(self.screen, (100, 100, 100), shadow_box, border_radius=15)
            pygame.draw.rect(self.screen, WHITE, result_box, border_radius=15)
            
            # Draw result message with word wrap
            words = self.result_message.split()
            lines = []
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = self.large_font.render(test_line, True, BLACK)
                if test_surface.get_width() <= result_box.width - 40:
                    current_line.append(word)
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
            lines.append(' '.join(current_line))
            
            y_offset = result_box.top + 30
            for line in lines:
                text_surface = self.large_font.render(line, True, BLACK)
                x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
                self.screen.blit(text_surface, (x, y_offset))
                y_offset += 40
            
            # Draw continue prompt
            continue_text = self.font.render("Click anywhere to continue", True, (0, 100, 200))
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH // 2, result_box.bottom - 50))
            self.screen.blit(continue_text, continue_rect)
        
        # Draw celebration effects
        for effect in self.celebration_effects:
            effect.draw(self.screen)
        
        pygame.display.flip()
        
    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.state == EXPLORE:
                        # Check creature interactions
                        for creature in self.creatures:
                            if not creature.visited and creature.can_interact and creature.is_hovered:
                                self.current_creature = creature
                                self.state = QUIZ
                                self.setup_quiz()
                                break
                                
                        # Check bubble pops
                        for bubble in self.bubbles:
                            if bubble.check_pop(mouse_pos):
                                self.bubble_count += 1
                                
                    elif self.state == QUIZ:
                        for i, button in enumerate(self.answer_buttons):
                            if button.is_clicked(mouse_pos, event):
                                self.check_answer(i)
                                break
                                
                    elif self.state == REWARD:
                        if self.current_creature and not self.current_creature.visited:
                            self.state = QUIZ
                            self.setup_quiz()
                        else:
                            self.state = EXPLORE
                            self.current_creature = None
            
            self.update()
            self.draw()
            
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()