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
	def __init__(self, primary_image_name, secondary_image_name):
		super(Character, self).__init__()
		self.primary_image   = primary_image_name
		self.secondary_image = secondary_image_name

	def move_left(distance):
		pass

	def move_right(distance):
		pass

	def jump():
		pass
	def move_using_keyboard_input(key_pressed, distance):
		if key_pressed == K_RIGHT:
			move_right(distance)
		elif key_pressed == K_LEFT:
			move_left(distance)
		elif key_pressed == K_SPACE:
			jump()