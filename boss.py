import pygame
from pygame.sprite import Sprite
import random

class Boss(Sprite):
    """A class to represent the boss alien."""

    def __init__(self, ai_settings, screen, level):
        super(Boss, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Scale Boss size based on screen width
        self.width = int(ai_settings.screen_width * 0.15) # 15% of screen width
        self.height = int(self.width * 0.66) # Proportional height
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.draw_boss_image()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = ai_settings.screen_width / 2
        self.rect.top = 50

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        
        # Scaling boss stats with level
        self.health = 50 + (level * 20)
        self.max_health = self.health
        
        self.speed = ai_settings.alien_speed_factor * 1.5
        self.direction = 1
        self.frame_count = 0

    def draw_boss_image(self):
        """Draws a cool UFO boss on the surface."""
        self.image.fill((0, 0, 0, 0)) # Clear surface
        
        w, h = self.width, self.height
        
        # 1. Saucer main body (Metallic grey)
        pygame.draw.ellipse(self.image, (120, 120, 130), [0, h*0.33, w, h*0.5])
        pygame.draw.ellipse(self.image, (80, 80, 90), [0, h*0.33, w, h*0.5], 3) # Outline
        
        # 2. Cockpit/Dome (Glowing blue)
        pygame.draw.ellipse(self.image, (0, 191, 255, 180), [w*0.28, h*0.12, w*0.44, h*0.41])
        pygame.draw.ellipse(self.image, (255, 255, 255, 200), [w*0.36, h*0.2, w*0.16, h*0.12]) # Shine
        
        # 3. Bottom engine/core (Red)
        pygame.draw.ellipse(self.image, (255, 0, 0), [w*0.33, h*0.7, w*0.33, h*0.16])
        
        # 4. Animated Lights
        light_color = (255, 255, 0) if (pygame.time.get_ticks() // 500) % 2 == 0 else (255, 165, 0)
        for i in range(5):
            pygame.draw.circle(self.image, light_color, (int(w*0.16 + i*w*0.16), int(h*0.58)), int(w*0.03))

    def update(self):
        """Move the boss side to side erratically and update animations."""
        self.x += self.speed * self.direction
        self.rect.x = self.x

        # Redraw image to animate lights
        self.draw_boss_image()

        # Erratic change of direction
        if random.random() < 0.02:
            self.direction *= -1

    def check_edges(self):
        """Return True if boss is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right - 10:
            return True
        elif self.rect.left <= 10:
            return True
        return False

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            return True # Destroyed
        return False

    def draw_health_bar(self):
        # Draw a health bar at the top
        bar_width = 400
        bar_height = 20
        fill = (self.health / self.max_health) * bar_width
        outline_rect = pygame.Rect((self.ai_settings.screen_width/2 - bar_width/2, 10, bar_width, bar_height))
        fill_rect = pygame.Rect((self.ai_settings.screen_width/2 - bar_width/2, 10, fill, bar_height))
        
        pygame.draw.rect(self.screen, (255, 0, 0), fill_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), outline_rect, 2)

    def blitme(self):
        self.screen.blit(self.image, self.rect)
        self.draw_health_bar()