import pygame
from pygame.sprite import Sprite
import random

class Bullet(Sprite):
	""" A class to manage bullets fired from the ship"""

	def __init__(self, ai_settings, screen, ship, is_super=False, dx=0):
		"""Create a bullet object at the ship's current position"""
		super().__init__()
		self.screen = screen
		self.is_super = is_super

		# Create a bullet rect at (0, 0) and then set correct position.
		if self.is_super:
			self.rect = pygame.Rect(0, 0, ai_settings.super_bullet_width, ai_settings.super_bullet_height)
			self.color = ai_settings.super_bullet_color
		else:
			self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
			self.color = ai_settings.bullet_color

		self.rect.centerx = ship.rect.centerx
		self.rect.top = ship.rect.top

		#Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)
		self.x = float(self.rect.x)

		# Bullet properties
		self.speed_factor = ai_settings.bullet_speed_factor
		self.dx = dx


	def update(self):
		"""Move the bullet up the screen."""
		# Update the decimal position of the bullet.
		self.y -= self.speed_factor
		self.x += self.dx
		# Update the rect position
		self.rect.y = self.y
		self.rect.x = self.x
		

	def draw_bullet(self):
		"""Draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)

class Enemy_Bullet(Sprite):
	""" A class to manage bullets fired from the alien"""

	def __init__(self, ai_settings, screen, aliens):
		"""Create a bullet object at the alien's current position"""
		super().__init__()
		self.screen = screen

		# Create a bullet rect at (0, 0) and then set correct position.
		self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
		
		# Choose a random alien from the group.
		enemy_list = list(aliens)
		if enemy_list:
			alien = random.choice(enemy_list)
			self.rect.centerx = alien.rect.centerx
			self.rect.bottom = alien.rect.bottom
		else:
			# Fallback if no aliens exist (should not happen with current logic)
			self.rect.x = -100
			self.rect.y = -100

		# Store the bullet's position as a decimal value.
		self.y = float(self.rect.y)

		self.color = ai_settings.enemy_bullet_color
		self.speed_factor = ai_settings.enemy_bullet_speed_factor


	def update(self):
		"""Move the bullet up the screen."""
		# Update the decimal position of the bullet.
		self.y += self.speed_factor
		# Update the rect position
		self.rect.y = self.y

	def draw_enemy_bullet(self):
		"""Draw the bullet to the screen"""
		pygame.draw.rect(self.screen, self.color, self.rect)
