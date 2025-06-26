import pygame
import random
import math
from ..utils.constants import WHITE

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
        self.interaction_radius = 150
        self.can_interact = False
        
        # Swimming behavior attributes - reduced movement speed and radius
        self.original_x = x
        self.original_y = y
        self.swim_pattern = 'random' if name == "Octopus" else random.choice(['circle', 'figure8', 'zigzag', 'random'])
        self.movement_speed = random.uniform(0.1, 0.4) if name == "Octopus" else random.uniform(0.3, 1.5)
        self.movement_radius = random.randint(20, 40) if name == "Octopus" else random.randint(30, 100)
        self.movement_time = random.uniform(0, math.pi * 2)
        self.next_direction_change = 0
        self.current_direction = random.uniform(0, math.pi * 2)
        self.target_x = self.x
        self.target_y = self.y
        self.flip_image = False
        
        # Add smoothing for movement
        self.dx = 0
        self.dy = 0
        self.smoothing = 0.95 if name == "Octopus" else 0.8  # Higher smoothing for octopus

    def get_next_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.current_question_index += 1
            return question
        return None

    def update(self, player_pos, mouse_pos):
        if not self.visited:
            current_time = pygame.time.get_ticks() * 0.001
            self.movement_time += self.movement_speed * 0.02

            old_x, old_y = self.x, self.y

            # Apply different swimming patterns
            if self.swim_pattern == 'circle':
                target_x = self.original_x + math.cos(self.movement_time) * self.movement_radius
                target_y = self.original_y + math.sin(self.movement_time) * self.movement_radius
                
            elif self.swim_pattern == 'figure8':
                scale_x = self.movement_radius * 1.5
                scale_y = self.movement_radius
                target_x = self.original_x + math.sin(self.movement_time) * scale_x
                target_y = self.original_y + math.sin(self.movement_time * 2) * scale_y
                
            elif self.swim_pattern == 'zigzag':
                target_x = self.original_x + math.sin(self.movement_time * 2) * self.movement_radius
                target_y = self.original_y + self.movement_time % (self.movement_radius * 2) - self.movement_radius
                
            elif self.swim_pattern == 'random':
                if current_time > self.next_direction_change:
                    self.current_direction = random.uniform(0, math.pi * 2)
                    self.next_direction_change = current_time + random.uniform(2, 4)
                    self.target_x = self.original_x + random.randint(-self.movement_radius, self.movement_radius)
                    self.target_y = self.original_y + random.randint(-self.movement_radius, self.movement_radius)
                
                target_x = self.target_x
                target_y = self.target_y

            # Apply smoothing to movement
            self.dx = self.dx * self.smoothing + (target_x - self.x) * (1 - self.smoothing)
            self.dy = self.dy * self.smoothing + (target_y - self.y) * (1 - self.smoothing)
            
            self.x += self.dx
            self.y += self.dy
            
            # Keep within bounds of original position
            max_distance = self.movement_radius * 1.5
            dx = self.x - self.original_x
            dy = self.y - self.original_y
            distance = math.sqrt(dx*dx + dy*dy)
            if distance > max_distance:
                angle = math.atan2(dy, dx)
                self.x = self.original_x + math.cos(angle) * max_distance
                self.y = self.original_y + math.sin(angle) * max_distance

            # Update flip direction based on actual movement rather than target
            self.flip_image = (self.x - old_x) < 0

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

    def draw(self, screen, font):
        # Don't draw if visited
        if self.visited:
            return

        self.rect.center = (self.x, self.y)
        if self.flip_image:
            flipped_image = pygame.transform.flip(self.image, True, False)
            screen.blit(flipped_image, self.rect)
        else:
            screen.blit(self.image, self.rect)
        
        if self.can_interact and self.is_hovered and not self.visited:
            text = "Click to interact!"
            text_surface = font.render(text, True, WHITE)
            text_rect = text_surface.get_rect(center=(self.x, self.y - 70))
            screen.blit(text_surface, text_rect)
        
        elif self.discovered:
            name_text = font.render(self.name, True, WHITE)
            screen.blit(name_text, (self.x - name_text.get_width() // 2, self.y - 50))