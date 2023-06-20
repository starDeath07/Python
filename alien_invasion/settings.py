class Settings :
	# A class to store all the settings of the game

	def __init__(self) :
		# Initialise the game static settings
		# Screen settings
		self.screen_width = 800
		self.screen_height = 600
		self.bg_color = (230, 230, 230)

		# Ship speed
		self.ship_limits = 3

		# Bullet settings
		self.bullet_width = 3
		self.bullet_height = 15
		self.bullet_color = (60, 60, 60)
		self.bullet_allowed = 3

		# Alien settings
		self.fleet_dropspeed = 7

		# How quickly the game speeds up
		self.speedup_scale = 1.1
		self.intialize_dynamic_settings()

	def intialize_dynamic_settings(self) :
		# Settigns that change throughout the game
		self.ship_speed = 1
		self.bullet_speed = 1
		self.alien_speed = 1
		self.ship_limits = 3

		# Fleet direction 1 represents right and -1 left
		self.fleet_direction = 1

		# Points
		self.alien_points = 50

	def increase_speeed(self) :
		# Increase speed settings
		self.ship_speed *= self.speedup_scale
		self.bullet_speed *= self.speedup_scale
		self.alien_speed *= self.speedup_scale