# #!/usr/bin/env python
# # encoding: utf-8
#
# Created by Kiran Panesar - 22/10/2013

import pygame

class Character(object):
	"""This is the class for all the characters in the game
		Characters can perform actions such as:
			- Move with arrow keys
			- 'Equip' items
	"""
	# Method used to intialise the character object
	# Will pass the primary and secondary image names of the character (used for walking)
	def __init__(self, image_name):
		super(Character, self).__init__()
		
		# Check if image_name is a string or a GifSprite object
		if type(image_name) is str:
			# If it's a string, load it using Pygame's methods and draw it
			self.image_name 	 = image_name
			self.game_image      = pygame.image.load(self.image_name)
			self.rect 			 = self.game_image.get_rect()
		else:
			# GifSprite is a subclass of the pygame.sprite.Sprite class, so just assign it
			self.game_image = image_name
			self.rect = image_name.rect
		
		# Initialise a blank equipped item
		self.equipped_item   = None

	# Instance method called by controller to equip an item (i.e., sheep, wolf, cabbage)
	def equip_item(self, item):
		self.deposit_item()
		self.equipped_item = item

	# Instance method to deposit an item
	def deposit_item(self):
		self.equipped_item = None