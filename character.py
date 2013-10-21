import pygame

class Character(object):
	"""This is the class for all the characters in the game
		Characters can perform actions such as:
			- Move with arrow keys
			- Jump with spacebar
			- 'Equip' items
	"""
	# Method used to intialise the character object
	# Will pass the primary and secondary image names of the character (used for walking)
	def __init__(self, image_name):
		super(Character, self).__init__()
		

		self.image_name 	 = image_name

		self.game_image      = pygame.image.load(self.image_name)
		self.rect 			 = self.game_image.get_rect()
		self.equipped_item   = None

	def equip_item(self, item):
		self.deposit_item()
		self.equipped_item = item

		pass
	def deposit_item(self):
		self.equipped_item = None