import pygame
from pygame.sprite import Sprite
import random

class PowerUp(Sprite):
    """A class to represent a power-up."""
    def __init__(self, ai_settings, screen, centerx, centery):
        super(PowerUp, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Types of power-ups
        self.type = random.choice(['shield', 'multi_shot', 'speed'])
        
        # Set color based on type
        if self.type == 'shield':
            self.color = (0, 100, 255) # Blue
        elif self.type == 'multi_shot':
            self.color = (0, 255, 0) # Green
        elif self.type == 'speed':
            self.color = (255, 255, 0) # Yellow
            
        self.radius = 10
        self.rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        self.rect.centerx = centerx
        self.rect.centery = centery
        
        self.y = float(self.rect.y)
        self.speed_factor = 2.0

    def update(self):
        """Move the power-up down the screen."""
        self.y += self.speed_factor
        self.rect.y = self.y

    def draw_powerup(self):
        """Draw the power-up."""
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)
        # Draw a white outline
        pygame.draw.circle(self.screen, (255, 255, 255), self.rect.center, self.radius, 2)
