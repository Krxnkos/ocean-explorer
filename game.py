import pygame
import sys
import random
import os
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

# Load images
def load_image(name, scale=1.0):
    try:
        fullname = os.path.join('assets', 'images', name)
        image = pygame.image.load(fullname)
        if scale != 1.0:
            new_size = (int(image.get_width() * scale), int(image.get_height() * scale))
            image = pygame.transform.scale(image, new_size)
        return image.convert_alpha()
    except pygame.error as e:
        print(f"Cannot load image: {name}")
        print(e)
        return pygame.Surface((50, 50))

# Load sounds
def load_sound(name):
    try:
        fullname = os.path.join('assets', 'sounds', name)
        sound = pygame.mixer.Sound(fullname)
        return sound
    except pygame.error as e:
        print(f"Cannot load sound: {name}")
        print(e)
        return None

# Game assets
player_img = load_image('player.png', 0.2)
dolphin_img = load_image('dolphin.png', 0.3)
turtle_img = load_image('turtle.png', 0.2)
starfish_img = load_image('starfish.png', 0.15)
octopus_img = load_image('octopus.png', 0.25)
fish_img = load_image('fish.png', 0.15)
background_img = load_image('ocean_bg.png')

# Sound effects
correct_sound = load_sound('correct.wav')
wrong_sound = load_sound('wrong.wav')
background_music = load_sound('ocean_music.wav')

# Font
font = pygame.font.SysFont('Arial', 24)
large_font = pygame.font.SysFont('Arial', 32)

# Game states
EXPLORE = 0
QUIZ = 1
REWARD = 2

class Player:
    def __init__(self):
        self.x = 100
        self.y = 300
        self.image = player_img
        self.speed = 5
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.stars = 0

    def move(self, dx, dy):
        self.x += dx
        self.y += dy
        # Keep player within bounds
        self.x = max(50, min(self.x, SCREEN_WIDTH - 50))
        self.y = max(50, min(self.y, SCREEN_HEIGHT - 50))
        self.rect.center = (self.x, self.y)

    def draw(self):
        screen.blit(self.image, self.rect)

class Creature:
    def __init__(self, x, y, image, name, question, answers, correct_answer):
        self.x = x
        self.y = y
        self.image = image
        self.name = name
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.visited = False
    
    def draw(self):
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
        
        # Play background music on loop
        if background_music:
            background_music.play(-1)

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
            Creature(300, 300, fish_img, "Red Fish", 
                    "Can you find the red fish?",
                    ["Yes! Here it is!", "No, I can't see it", "What fish?"], 0)
        ]
        return creatures

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            mouse_pos = pygame.mouse.get_pos()
            
            if self.state == QUIZ:
                for button in self.answer_buttons:
                    button.check_hover(mouse_pos)
                    if event.type == MOUSEBUTTONDOWN and button.is_clicked(mouse_pos, event):
                        self.check_answer(self.answer_buttons.index(button))
            
            if self.state == REWARD and event.type == MOUSEBUTTONDOWN:
                self.state = EXPLORE
                
        keys = pygame.key.get_pressed()
        if self.state == EXPLORE:
            dx, dy = 0, 0
            if keys[K_LEFT]:
                dx = -self.player.speed
            if keys[K_RIGHT]:
                dx = self.player.speed
            if keys[K_UP]:
                dy = -self.player.speed
            if keys[K_DOWN]:
                dy = self.player.speed
            self.player.move(dx, dy)
            
            # Check for creature collisions
            for creature in self.creatures:
                if not creature.visited and self.player.rect.colliderect(creature.rect):
                    self.current_creature = creature
                    self.state = QUIZ
                    self.setup_quiz()
                    break

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
                correct_sound.play()
            self.player.stars += 1
            self.current_creature.visited = True
        else:
            self.result_message = "Try again! That's not right."
            if wrong_sound:
                wrong_sound.play()
        
        self.state = REWARD
        self.result_time = pygame.time.get_ticks()

    def update(self):
        if self.state == REWARD and pygame.time.get_ticks() - self.result_time > 2000:
            if "Correct" in self.result_message:
                self.state = EXPLORE
            else:
                self.state = QUIZ

    def draw(self):
        # Draw background
        screen.blit(background_img, (0, 0))
        
        # Draw creatures
        for creature in self.creatures:
            if not creature.visited:
                creature.draw()
        
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
            
            result_box = pygame.Rect(SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50, 400, 100)
            pygame.draw.rect(screen, WHITE, result_box, border_radius=15)
            
            result_text = large_font.render(self.result_message, True, BLACK)
            screen.blit(result_text, (SCREEN_WIDTH // 2 - result_text.get_width() // 2, SCREEN_HEIGHT // 2 - 25))
            
            if "Correct" in self.result_message:
                # Draw stars for visual reward
                for i in range(5):
                    star_x = SCREEN_WIDTH // 2 - 100 + i * 50
                    star_y = SCREEN_HEIGHT // 2 + 30
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
        
        # Check for game completion
        all_visited = all(creature.visited for creature in self.creatures)
        if all_visited:
            # Draw completion message
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
        
        pygame.display.flip()

    def run(self):
        while True:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

# Main function
def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
