import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullets
from alien import Alien
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

class AlienInvasion :

	 def __init__(self) :
	 	# initialise the game and create game resourses
	 	pygame.init()
	 	self.settings = Settings()

	 	self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
	 	self.settings.screen_width = self.screen.get_rect().width
	 	self.settings.screen_height = self.screen.get_rect().height

	 	# self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

	 	pygame.display.set_caption("Alien Invasion")

	 	# Set the background color
	 	self.bg_color = self.settings.bg_color

	 	# Create an instance of game statics
	 	self.stats = GameStats(self)
	 	self.sb = ScoreBoard(self)

	 	self.ship = Ship(self)
	 	self.bullets = pygame.sprite.Group()
	 	self.aliens = pygame.sprite.Group()
	 	self.stars = pygame.sprite.Group()	

	 	self._create_fleet()

	 	# Make the play button
	 	self.play_button = Button(self, "Play")


	 def run_game(self) :
	 	# start the main loop for the game

	 	while True :
	 		# start the main loop for the game
	 		self._check_events()

	 		if self.stats.game_active :
		 		self.ship.update()
		 		self._update_bullets()
		 		self._update_aliens()

	 		self._update_screen()

	 def _check_events(self) :
	 	# Respond to keypress and mouse clicks
	 	for events in pygame.event.get() :
	 		if events.type == pygame.QUIT :
	 			sys.exit()
	 		elif events.type == pygame.KEYDOWN :
	 			self._check_keydown_events(events)
	 		elif events.type == pygame.KEYUP :
	 			self._check_keyup_events(events)
	 		elif events.type == pygame.MOUSEBUTTONDOWN :
	 			mouse_pos = pygame.mouse.get_pos()
	 			self._check_play_button(mouse_pos)

	 def _check_play_button(self, mouse_pos) :
	 	# Start the new game when player clicks Play
	 	button_clicked = self.play_button.rect.collidepoint(mouse_pos)
	 	if button_clicked and not self.stats.game_active :

	 		# Reset the game settings
	 		self.settings.intialize_dynamic_settings()

	 		# Resets the game statistics
	 		self.stats.reset_stats()
	 		self.stats.game_active = True
	 		self.sb.prep_score()
	 		self.sb.prep_level()
	 		self.sb.prep_ships()

	 		# Get rid of remaining aliens and bullets
	 		self.bullets.empty()
	 		self.aliens.empty()

	 		# Create new fleet and center the sheep
	 		self._create_fleet()
	 		self.ship.center_ship()

	 		# Hide the mouse cursor
	 		pygame.mouse.set_visible(False)

	 def _check_keydown_events(self, events) :
	 	# Respond to keypress
	 	if events.key == pygame.K_RIGHT :
	 		self.ship.move_right = True
	 	elif events.key == pygame.K_LEFT :
	 		self.ship.move_left = True
	 	elif events.key == pygame.K_SPACE :
	 		self._fire_bullets()
	 	elif events.key == pygame.K_q :
	 		sys.exit()

	 def _check_keyup_events(self, events) :
	 	# Repsond to keypress
	 	if events.key == pygame.K_RIGHT :
	 		self.ship.move_right = False
	 	elif events.key == pygame.K_LEFT :
	 		self.ship.move_left = False

	 def _fire_bullets(self) :
	 	# Create new bullet and add it to the bullet group
	 	if len(self.bullets) < self.settings.bullet_allowed :
	 		new_bullet = Bullets(self)
	 		self.bullets.add(new_bullet)

	 def _update_bullets(self) :
	 	# Update the bullets and get rid of the old bullets
	 	# Update bullet positions
	 	self.bullets.update()

	 	# Get rid of the bullets that are gone
 		for bullet in self.bullets.copy() :
 			if bullet.rect.bottom <= 0 :
 				self.bullets.remove(bullet)
 			
 		self._check_for_collisions()

	 def _check_for_collisions(self) :
 	 	# Check for alien bullet collision
 	 	# Destroy bullet and alien after collision
 	 	collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

 	 	if collisions :
 	 		for aliens in collisions.values() :
 	 			self.stats.score += self.settings.alien_points*len(aliens)
 	 		self.sb.prep_score()
 	 		self.sb.check_highscore()

 	 	if not self.aliens :
 	 		# Destroy existing bullets create new fleet
 	 		self.bullets.empty()
 	 		self._create_fleet()
 	 		self.settings.increase_speed()

 	 		# Increase levels
 	 		self.stats.level += 1
 	 		self.prep_level()

	 def _update_aliens(self) :
 		# Update the position of aliens on the screen
 		self._check_fleet_edges()
 		self.aliens.update()

 		# Check for alien-ship collision
 		if pygame.sprite.spritecollideany(self.ship, self.aliens) :
 			self._ship_hit()

 		# Check for ship-alien collision at bottom
 		self._check_alien_bottom()

	 def _ship_hit(self) :
 	 	# ALien ship collision
 	 	if self.settings.ship_limits > 0 :
 	 		# Decrement the ship limit
 	 		self.settings.ship_limits -= 1
 	 		self.sb.prep_ships()

 	 		# Get rid of remaining bullets and aliens
 	 		self.aliens.empty()
 	 		self.bullets.empty()

 	 		# Create new fleet of aliens and center the ship
 	 		self._create_fleet()
 	 		self.ship.center_ship()

 	 		# Pause
 	 		sleep(1.0)
 	 	else :
 	 		self.stats.game_active = False
 	 		pygame.mouse.set_visible(True)

	 def _check_alien_bottom(self) :
 	 	# Check if the aliens have reached the bottom
 	 	screen_rect = self.screen.get_rect()
 	 	for alien in self.aliens.sprites() :
 	 		if alien.rect.bottom >= screen_rect.bottom :
 	 			# Consider this as collision
 	 			self._ship_hit()
 	 			break

	 def _create_fleet(self) :
	 	# Create the fleet of aliens
	 	# Create aliens
	 	alien = Alien(self)
	 	alien_width, alien_height = alien.rect.size
	 	available_space_x = self.settings.screen_width - (2*alien_width)
	 	number_aliens_x = available_space_x // (2*alien_width)

	 	# Determine the number of rows of aliens on screen
	 	ship_height = self.ship.rect.height
	 	available_space_y = self.settings.screen_height - ship_height - 3*alien_height
	 	number_rows = available_space_y // (2*alien_height)

	 	# Create the full fleet of aliens
	 	for row_number in range(number_rows) :
	 		for alien_number in range(number_aliens_x) :
	 			self._create_alien(alien_number, row_number)

	 def _create_alien(self, alien_number, row_number) :
	 	# Create aliens and place it on the row
	 	alien = Alien(self)
	 	alien_width, alien_height = alien.rect.size
	 	alien.x = alien_width + 2*alien_width*alien_number
	 	alien.rect.x = alien.x
	 	alien.rect.y = alien_height + 2*alien.rect.height*row_number
	 	self.aliens.add(alien)

	 def _check_fleet_edges(self) :
	 	# Change the fleet direction
	 	for alien in self.aliens.sprites() :
	 		if alien.check_edges() :
	 			self._change_fleet_directions()
	 			break

	 def _change_fleet_directions(self) :
	 	# Drop the fleet down and change the direction
	 	for alien in self.aliens.sprites() :
	 		alien.rect.y += self.settings.fleet_dropspeed
	 		self.settings.fleet_direction *= -1

	 def _update_screen(self) :
	 	# Update the image on the screen and flip to the new screen
	 	self.screen.fill(self.settings.bg_color)
	 	self.ship.blitme()

	 	for bullet in self.bullets.sprites() :
	 		bullet.draw_bullet()

	 	self.aliens.draw(self.screen)

	 	# Draw the score information
	 	self.sb.show_score()

	 	# Draw the play button if the game is inactive
	 	if not self.stats.game_active :
	 		self.play_button.draw_button()

	 	# Make the most recently drawn screen visible
	 	pygame.display.flip()

if __name__ == "__main__" :
	# Make the game instance and run the game

	ai = AlienInvasion()
	ai.run_game()