import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

	def __init__(self, ai_settings, screen):
		"""Initialize the ship and set its starting position."""
		super(Ship, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		# Load the ship image and get its rect.
		self.image = pygame.image.load('images/spaceship.png')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		# Start new ship at the bottom center of the screen.
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom - 5

		# Store a decimal value for the ship's center
		self.center_x = float(self.rect.centerx)
		self.center_y = float(self.rect.centery)

		# Movement flag
		self.moving_right = False
		self.moving_left = False
		self.moving_up = False
		self.moving_down = False

		# Shot counter
		self.shots_fired = 0

	def update(self):
		"""Update the ship's position based on movement flags."""
		# Update the ship's center values not the rect.
		if self.moving_right and self.rect.right < self.screen_rect.right - 10:
			self.center_x += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 10:
			self.center_x -= self.ai_settings.ship_speed_factor
		if self.moving_up and self.rect.top > 0:
			self.center_y -= self.ai_settings.ship_speed_factor
		if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
			self.center_y += self.ai_settings.ship_speed_factor

		# Update rect object from self.center values.
		self.rect.centerx = self.center_x
		self.rect.centery = self.center_y

	def center_ship(self):
		"""Center the ship on the screen."""
		self.center_x = self.screen_rect.centerx
		self.center_y = self.screen_rect.bottom - 30
		self.rect.centerx = self.center_x
		self.rect.bottom = self.screen_rect.bottom - 5

	def blitme(self):
		"""Draw the ship at its current location."""
		self.screen.blit(self.image, self.rect)

