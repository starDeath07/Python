import pygame.font
from pygame.sprite import Group
from ship import Ship

class ScoreBoard :
	# A class to report score information

	def __init__(self, ai_game) :
		# Intialize the ScoreBoard
		self.ai_game = ai_game
		self.screen = ai_game.screen
		self.screen_rect = self.screen.get_rect()
		self.settings = ai_game.settings
		self.stats = ai_game.stats

		# Font settings for score information
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		# Prepare the initial score image
		self.prep_score()
		self.prep_highscore()
		self.prep_level()
		self.prep_ships()

	def prep_ships(self) :
		# Show how many ships are left
		self.ships = Group()
		for ship_number in range(self.settings.ship_limits) :
			ship = Ship(self.ai_game)
			ship.rect.x = 10 + ship_number*ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)

	def prep_level(self) :
		# Turn the level into the renderd image
		level_str = str(self.stats.level)
		self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

		# Display level below the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10


	def prep_highscore(self) :
		# Turn the highscore into the rendered image
		rounded_highscore = round(self.stats.high_score, -1)
		highscore_str = "{:,}".format(rounded_highscore)
		self.high_score_image = self.font.render(highscore_str, True, self.text_color, self.settings.bg_color)

		# Display the score at top mid of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_score(self) :
		# Turn the score into the rendered image
		rounded_score = round(self.stats.score, -1)
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

		# Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.screen_rect.top = 20

	def show_score(self) :
		# Drawn score onto the screen
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)

	def check_highscore(self) :
		# Update the high score if there is any
		if self.stats.score > self.stats.high_score :
			self.stats.high_score = self.stats.score
			self.prep_highscore()

	# def prep_level(self) :
	# 	# Turn the highscore into the rendered image
	# 	level_str = str(self.stats.level)
	# 	self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

	# 	# Display the score at top mid of the screen
	# 	self.level_rect = self.level_image.get_rect()
	# 	self.level_rect.right = self.score_rect.right
	# 	self.level_rect.top = self.score_rect.bottom + 10
