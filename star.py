import pygame
from pygame.sprite import Sprite
import random

class Star(Sprite):
    """A class to represent a single star in the starfield."""
    def __init__(self, ai_settings, screen):
        super(Star, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        
        # Pick a random color and speed from settings
        self.color = random.choice(ai_settings.star_colors)
        self.speed = random.choice(ai_settings.star_speeds)
        self.radius = random.randint(1, 3)
        
        self.rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        
        # Start at a random position
        self.rect.x = random.randint(0, ai_settings.screen_width)
        self.rect.y = random.randint(0, ai_settings.screen_height)
        
        self.y = float(self.rect.y)

    def update(self):
        """Move the star down."""
        self.y += self.speed
        if self.y > self.ai_settings.screen_height:
            self.y = 0
            self.rect.x = random.randint(0, self.ai_settings.screen_width)
        self.rect.y = self.y

    def draw_star(self):
        """Draw the star on the screen."""
        pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)
