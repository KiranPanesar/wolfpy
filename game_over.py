#!/usr/bin/env python
# encoding: utf-8
# Created by Kiran Panesar and Dan Koehler - 22/10/2013

import sys, pygame
import lib.button as button
import engine
import main_menu

class GameOverScreen(object):
	"""
		Screen presented when one animal is eaten by another (game over)
	"""
	# if cabbage kills sheep, scenario = 0
	# if wolf kills sheep, scenario = 1
	def __init__(self, screen, scenario):
		super(GameOverScreen, self).__init__()
		self.screen = screen # Draw the screen

		# Create a transluscent background surface to overlay on the game
		background_surface = pygame.Surface((900,480))  
		background_surface.set_alpha(128)               
		background_surface.fill((255,255,255))           
		self.screen.blit(background_surface, (0,0)) 

		# Check how the game ended and set up the appropriate end game image
		image_file_string = None
		if scenario == 0:
			image_file_string = "./img/Game Over Cabbage.png"
		else:
			image_file_string = "./img/Game Over Wolf.png"

		# Import and setup the image
		image = pygame.image.load(image_file_string).convert_alpha()
		image_rect = image.get_rect()

		# Show the image on the screen
		self.screen.blit(image, image_rect)		

	# Instance method to show the screen
	def show_screen(self):
		# Create buttons to retry and go to the main menu
		retry_button	  	=  button.Create(self.screen,(0,210,255), None, 300, "Try again", 300, 50, (255,255,255), 32, 2,(10,10,10),1)
		main_menu_button 	=  button.Create(self.screen,(0,210,255), None, 370, "Main Menu", 300, 50, (255,255,255), 32, 2,(10,10,10),1)

		# Loop to catch user input
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						sys.exit()
				# If the user clicks, grab the mouse position
				# and run the clicked button's event
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if main_menu_button.rect.collidepoint(pos):
						# Show the main menu
						main_screen = main_menu.MainMenuScreen(self.screen)
						main_screen.show_screen()
					elif retry_button.rect.collidepoint(pos):
						# Show the gameplay screen
						game_engine = engine.GameEngine(self.screen)
						game_engine.start_game()
			# Render changes
			pygame.display.flip()