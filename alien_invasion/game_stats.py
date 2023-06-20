class GameStats :
	# Track the game for alien invasion
	def __init__(self, ai_game) :
		# Intialise statistics
		self.settings = ai_game.settings
		self.reset_stats()

		# Start the game in active state
		self.game_active = False	

		# High score never to be reset
		self.high_score = 0

	def reset_stats(self) :
		# Parameters that change during the game
		self.ships_left = self.settings.ship_limits
		self.score = 0
		self.level = 1