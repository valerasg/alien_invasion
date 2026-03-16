import pygame
from pygame.sprite import Sprite
import random

class Particle(Sprite):
    """A class to represent an explosion particle."""
    def __init__(self, screen, x, y, color=(255, 100, 0)):
        super(Particle, self).__init__()
        self.screen = screen
        self.radius = random.randint(2, 6)
        self.color = color
        
        self.rect = pygame.Rect(0, 0, self.radius*2, self.radius*2)
        self.rect.centerx = x
        self.rect.centery = y
        
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)
        
        # Random velocity
        self.vx = random.uniform(-4, 4)
        self.vy = random.uniform(-4, 4)
        
        self.lifetime = random.randint(20, 40)

    def update(self):
        """Update particle position and lifetime."""
        self.x += self.vx
        self.y += self.vy
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.lifetime -= 1

    def draw_particle(self):
        """Draw the particle."""
        if self.lifetime > 0:
            pygame.draw.circle(self.screen, self.color, self.rect.center, self.radius)
