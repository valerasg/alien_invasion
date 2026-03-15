class Settings():
	"""A class to store all settings for Alien invasion"""

	def __init__(self):
		"""Initialize the game's static settings"""
		# Screen Settings
		self.screen_width = 1440
		self.screen_height = 790
		self.bg_color = (10, 10, 30)

		# Ship settings
		self.ship_limit = 3

		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 255, 255)
		self.bullets_allowed = 4

		# Super bullet settings
		self.super_bullet_width = 15
		self.super_bullet_height = 30
		self.super_bullet_color = (255, 50, 50)
		self.shots_to_super = 5

		# Starfield settings
		self.star_count = 100
		self.star_speeds = [0.5, 1, 1.5]
		self.star_colors = [(200, 200, 255), (255, 255, 255), (255, 200, 200)]

		# Enemy bullet settings
		self.enemy_bullet_color = (255, 20, 147)
		self.enemy_bullets_allowed = 7

		# Alien settings
		self.fleet_drop_speed = 8

		# How quickly the game speeds up.
		self.speed_up_scale = 1.1
		# How quickly the alien point values increase
		self.score_scale = 1.5

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game."""
		self.ship_speed_factor = 10
		self.bullet_speed_factor = 17
		self.alien_speed_factor = 4
		self.enemy_bullet_speed_factor = 8

		# Fleet_direction of 1 represents right; -1 represents left.
		self.fleet_direction = 1

		# Scoring
		self.alien_points = 50

	def increase_speed(self):
		"""Increase speed settings."""
		self.ship_speed_factor *= self.speed_up_scale
		self.bullet_speed_factor *= self.speed_up_scale
		self.alien_speed_factor *= self.speed_up_scale
		self.enemy_bullet_speed_factor *= self.speed_up_scale

		self.alien_points = int(self.alien_points * self.score_scale)
