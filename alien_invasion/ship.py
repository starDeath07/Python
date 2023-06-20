import pygame
from pygame.sprite import Sprite

class Ship(Sprite) :
	# A class to manage the ship

	def __init__(self, ai_game) :
		# Initialise the ship and its starting position
		super().__init__()
		self.screen = ai_game.screen
		self.settings = ai_game.settings
		self.screen_rect =  ai_game.screen.get_rect()

		# Load the ship image and get its rect

		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()

		# Start each ship at the center bottom of the screen
		self.rect.midbottom = self.screen_rect.midbottom

		# Store the decimal value for x-axis position of the ship
		self.x = float(self.rect.x)

		# Movement flag
		self.move_right = False
		self.move_left = False

	def update(self) :
		# Update the ship position on x-axis
		if self.move_right and self.rect.right < self.screen_rect.right :
			self.x += self.settings.ship_speed
		if self.move_left and self.rect.left > 0 :
			self.x -= self.settings.ship_speed

		self.rect.x = self.x


	def blitme(self) :
		# Draw the ship at its current location
		self.screen.blit(self.image, self.rect)

	def center_ship(self) :
		# Center the ship on the screen
		self.rect.midbottom = self.screen_rect.midbottom
		self.x = float(self.rect.x)
