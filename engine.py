#!/usr/bin/env python
# encoding: utf-8
# Created by Kiran Panesar and Dan Koehler - 22/10/2013

import sys, pygame
import time
import lib.character as character
import lib.gifsprite as gifsprite
import lib.button
import fblib.fbrequest as fbrequest
import lib.message_popup as message_popup
import game_over
import settings
import main_menu
import game_complete

class GameEngine(object):
		"""docstring for GameEngine"""
		def __init__(self, screen): 
				super(GameEngine, self).__init__()
				#Check is we're being passed a screen, from other game 'views'
				if screen == None:
					screen = pygame.display.set_mode((900,480))
					#Initiate PyGame's mixer class, and pass it our 'ambiance sound' file.
					pygame.mixer.init()
					pygame.mixer.music.load("./sounds/background.wav")
					#Loop file infinitely
					pygame.mixer.music.play(-1)
				self.screen = screen
				# Create arrays required for engine logic
				self.left_shore_characters = []
				self.right_shore_characters = []
				# Create a UNIX time stamp for game completion timing 
				self.game_start_time = time.time()
				# Create Var to hold previous left/right key-press event to loop until keyup
				self.key_held = 0 # 0 if no key, 1 if right, -1 is left

		def draw_background(self):
			#Initially load into memory all the resources required to render background
			self.cloud = pygame.image.load('./img/Cloud.png').convert_alpha()
			self.sun = pygame.image.load('./img/Sun.png').convert_alpha()
			self.river = gifsprite.Create(['River 1.png', 'River 1a.png'], 300, 400)
			self.background = pygame.image.load('./img/Background.png').convert_alpha()
			self.left_bank = pygame.image.load('./img/Bank Left.png').convert_alpha()
			self.right_bank = pygame.image.load('./img/Bank Right.png').convert_alpha()

		def refresh_background(self):
			#Paint background from resources loaded to memory
			self.screen.blit(self.background, (0, 0))
			self.draw_clock()
			self.screen.blit(self.cloud, (145, 24))
			self.screen.blit(self.cloud, (425, 54))
			self.screen.blit(self.sun, (720, 24))
			self.screen.blit(self.left_bank, (0, 380))
			self.screen.blit(self.right_bank, (600, 380))
			self.river.group.draw(self.screen)

		def clock_ticked(self):
			# This method fires - at least - once a second, if fired by in game timing function update the 'gif' image for th river and re-paint.
			self.river.update()
			self.refresh_characters()
			
		def draw_clock(self):
			#function to draw in game timing meter 
			#Fetch new UNIX time stamp to work out game play time
			game_time = int(time.time() - self.game_start_time)
			#Instantiate and and render from PyGame font class
			label = pygame.font.Font(None, 25).render(str(game_time)+" seconds", 1, (236, 240, 241))
			# Create Rect and set values for label positioning
			labelPos = label.get_rect()
			labelPos.top = 10
			labelPos.left = 10
			#Paint over area of background consumed by the label with itself
			self.screen.blit(self.background,labelPos,labelPos)
			#Paint label to background
			self.screen.blit(label, labelPos)

		def draw_characters(self):
			#Instantiate Characters, loading their respective images into the GifSprite class we wrote to return and object of that class for use in animations.
			#For player set attributes of direction and the distance they move on key-down.
			self.player = character.Character(gifsprite.Create(['Farmer01.png', 'Farmer02.png','Farmer03.png','Farmer04.png'], 60, 265))
			self.player.direction = 0
			self.player.step_interval = 50
			#Create a Cabbage attribute of the engine and set initial positioning
			self.cabbage = character.Character(gifsprite.Create(['Cabbage01.png', 'Cabbage02.png','Cabbage03.png','Cabbage04.png'], 100, 304))
			#Create a Wolf attribute of the engine and set initial positioning
			self.wolf = character.Character(gifsprite.Create(['Wolf01.png', 'Wolf02.png','Wolf03.png'], 200, 333))
			#Create a Sheep attribute of the engine and set initial positioning
			self.sheep = character.Character(gifsprite.Create(['Sheep01.png', 'Sheep02.png'], 15, 333))
			#Create a Boat attribute of the engine and set initial positioning as well as creating an attribute to dictate whether or not to 'bind' the boat's position to that of the player
			self.boat = gifsprite.Create(['Boat-02a.png', 'Boat-03a.png'], 266, 325)
			self.boat.binding = 0
			#Append the Sheep, Wolf and Cabbage to the array left shore array, so that we can keep track of where a given character is at a given time
			self.left_shore_characters.append(self.cabbage)
			self.left_shore_characters.append(self.wolf)
			self.left_shore_characters.append(self.sheep)
			#Paint characters to screen
			self.refresh_characters()

		def refresh_characters(self):
				#Ensure we paint background before we paint characters
				self.refresh_background()
				#check id the character has an equipped item
				if self.player.equipped_item:
					# Check which side we want to draw the equipped character on
					if self.player.direction:
						#Move the character to the left side of the player
						self.player.equipped_item.game_image.rect.right = self.player.game_image.rect.left
					else:
						#Move the character to the right side of the player
						self.player.equipped_item.game_image.rect.left = self.player.game_image.rect.right
				#Draw each character
				self.player.game_image.group.draw(self.screen)
				self.cabbage.game_image.group.draw(self.screen)
				self.wolf.game_image.group.draw(self.screen)
				self.sheep.game_image.group.draw(self.screen)
				self.boat.group.draw(self.screen)

		def deposit_item(self):
				#Check if the player is out of the sea and has an equipped item
				if self.player.equipped_item and (self.player.equipped_item.game_image.rect.right < 290 or self.player.equipped_item.game_image.rect.left > 610):
						#Check which direction the player is looking and drop the equipped character 10 pixels behind or in front of it.
						if self.player.direction == 0:
							self.player.equipped_item.game_image.rect.right += 10
						else:
							self.player.equipped_item.game_image.rect.right -= 10
						self.player.equipped_item.game_image.group.draw(self.screen)
						
						# Remove the equipped item from both shore arrays
						if self.player.equipped_item in self.left_shore_characters:
							self.left_shore_characters.remove(self.player.equipped_item)
						elif self.player.equipped_item in self.right_shore_characters:
							self.right_shore_characters.remove(self.player.equipped_item)

						# Check which shore the item is on and add it
						current_side = []
						if self.player.equipped_item.game_image.rect.left >= 600:
							current_side = self.right_shore_characters
						elif self.player.equipped_item.game_image.rect.right <= 300:
							current_side = self.left_shore_characters
						#Add the equipped item to the array shore side on which it currently resides
						current_side.append(self.player.equipped_item)
						# Call the character deposit item method
						self.player.deposit_item()
						#Refresh characters
						self.refresh_characters()
				#Call check characters either way
				self.check_characters()

		def check_characters(self):
				current_side = []
				# Check if all the characters are on the right side and load the finished game screen - passing the completion time
				if len(self.right_shore_characters) == 3:
					complete_screen = game_complete.GameCompletedScreen(self.screen, int(time.time()-self.game_start_time))
					complete_screen.show_screen()

				if self.player.game_image.rect.right > 300 and self.player.game_image.rect.left < 600:
					#Make sure we have enough characters on a side for the conditions the below look for can be true
					if len(self.right_shore_characters) > 1:
						# Check if the sheep has been left with the cabbage, or the wolf with the sheep - and load appropriate exit screen if needed
						if self.cabbage in self.right_shore_characters and self.sheep in self.right_shore_characters:
							print "cabbage eaten by sheep"
							self.refresh_characters()
							end_game = game_over.GameOverScreen(self.screen, 0)
							end_game.show_screen()
						elif self.sheep in self.right_shore_characters and self.wolf in self.right_shore_characters:
							print "sheep eaten by wolf"
							self.refresh_characters()
							end_game = game_over.GameOverScreen(self.screen, 1)
							end_game.show_screen()

					else:
						# Check if the sheep has been left with the cabbage, or the wolf with the sheep - and load appropriate exit screen if needed
						if self.sheep in self.left_shore_characters and self.wolf in self.left_shore_characters:
							print "sheep eaten by wolf"
							self.refresh_characters()
							end_game = game_over.GameOverScreen(self.screen, 1)
							end_game.show_screen()

						elif self.cabbage in self.left_shore_characters and self.sheep in self.left_shore_characters:
							print "cabbage eaten by sheep"
							self.refresh_characters()
							end_game = game_over.GameOverScreen(self.screen, 0)
							end_game.show_screen()


		def get_item_clicked(self, position):
			#Function to return whether a mouse click has intercepted a character and return the character object
			current_side = []
			if self.player.game_image.rect.left >= 601:
				current_side = self.right_shore_characters
			elif self.player.game_image.rect.right <= 299:
				current_side = self.left_shore_characters
			if self.sheep.rect.collidepoint(position) and self.sheep in current_side:
				return self.sheep
			elif self.wolf.rect.collidepoint(position) and self.wolf in current_side:
				return self.wolf
			elif self.cabbage.rect.collidepoint(position) and self.cabbage in current_side:
				return self.cabbage
				
		def title_screen(self):
			#Function to load the main menu screen class and then ask it to render the screen overlay
			main_screen = main_menu.MainMenuScreen(self.screen)
			main_screen.show_screen()

		def settings(self):
			#Function to load the setting screen class and then ask it to render the screen overlay
			settings_page = settings.SettingsScreen(self.screen)
			settings_page.show_screen()

		def start_game(self):
			#Function that handles the main game functionality - it handles user event and timing functions for the engine
			#Initially draw the background and characters
			self.draw_background()
			self.draw_characters()
			#Start and instance of the PyGame clock to handle frame rate for us
			clock = pygame.time.Clock()
			#Create var to store the number of milliseconds since we last called the clock and river refresh functions  
			time_elapsed_since_last_action = 0
			# Loop code segment while infinitely
			while 1:
					#Use PyGame clock to manage the frame rate
					dt = clock.tick(10)
					#Loop through events provided by PyGame to for user input 						
					for event in pygame.event.get():
						#Provide action for user pressing the windows exit cross
						if event.type == pygame.QUIT:
							sys.exit()
						# Look for user moving player left or right or exiting to title 
						elif event.type == pygame.KEYDOWN: # Check for key-down events   
							if event.key == pygame.K_RIGHT: # Moving right
								#User may be holding right navigation key - store this to 'key_held' engine attribute
								self.key_held = 1
							elif event.key == pygame.K_LEFT: # Moving left
								#User may be holding left navigation key - store this to 'key_held' engine attribute
								self.key_held = -1
							#look for quite to title and call engine function to deal with this if this is the case
							elif event.key == pygame.K_ESCAPE: # Quit to title
								self.title_screen();
						#Look for user lifting key
						elif event.type == pygame.KEYUP:
							#Set 'key_held' engine attribute to 0 - no key held.
							self.key_held = 0	
						#Look for user mouse up events						
						elif event.type == pygame.MOUSEBUTTONUP: # Mouse event
							#Check if the user has an equipped item 
							if self.player.equipped_item:
								#Call engine function to deposit this item     
								self.deposit_item()
							else:
								#Check whether a characters was clicked
								if self.get_item_clicked(pygame.mouse.get_pos()): # Check which item was clicked	
									#Equip item is one was clicked							
									self.player.equip_item(self.get_item_clicked(pygame.mouse.get_pos()))
									if self.player.equipped_item in self.left_shore_characters:
										self.left_shore_characters.remove(self.player.equipped_item)
									if self.player.equipped_item in self.right_shore_characters:
										self.right_shore_characters.remove(self.player.equipped_item)
							#Refresh characters 
							self.refresh_characters()

					#Check whether a key is being held (1 is the right-arrow, -1 is the left-arrow)
					if self.key_held == 1 or self.key_held == -1:
						# If the right arrow is being pressed
						if self.key_held == 1:
							# Set the player's direction to be right
							self.player.direction = 1

							# Flip the player to be facing right
							self.player.game_image.setFlip(1)
							
							# If the player has an equipped item, update that item too
							if self.player.equipped_item:
								self.player.equipped_item.game_image.update()
								self.player.equipped_item.game_image.setFlip(1)

							# If the player is less than 50px away from the right
							# then move it one interval closer to the right
							if self.player.game_image.rect.right <= 850:
								self.player.game_image.rect = self.player.game_image.rect.move([self.player.step_interval, 0])
						#Else it's the left key being pressed
						else:
							# Set the player's direction to be left
							self.player.direction = 0

							#Transform flip the player image left
							self.player.game_image.setFlip(0)

							# If the player has an equipped item, update the transform for the item also
							if self.player.equipped_item:
								self.player.equipped_item.game_image.update()
								self.player.equipped_item.game_image.setFlip(0)
							# If the player is less than 50px away from the left of the screen
							# then move it one interval closer to the right
							if self.player.game_image.rect.left >= 50:
								self.player.game_image.rect = self.player.game_image.rect.move([-self.player.step_interval, 0])
						#Update the player's 'Gif' animation image
						self.player.game_image.update()

						# Check that the player is in the sea area						
						if self.player.game_image.rect.right > 300 and self.player.game_image.rect.left < 600: # Keep, change values later for boat docking						
							# Check the direction the player is facing
							if self.player.direction: #going right
								#Flip the boat to match
								self.boat.setFlip(0)
								# Check that the player is far enough into the boat
								if self.player.game_image.rect.centerx > self.boat.rect.centerx + 50:
									#Move the boat to keep up with to the player
									self.boat.rect.centerx = self.player.game_image.rect.centerx - 50
									#Stop the player 'Gif' from animation
									self.player.game_image.setImage(0)
									#Do the same for an equipped character if it exists
									if self.player.equipped_item:
										self.player.equipped_item.game_image.setImage(0)
							else: #Going left
								#Flip the boat to match
								self.boat.setFlip(1)
								# Check that the player is far enough into the boat
								if self.player.game_image.rect.centerx < self.boat.rect.centerx:
									#Move the boat to keep up with to the player
									self.boat.rect.centerx = self.player.game_image.rect.centerx + 50
									#Stop the player 'Gif' from animation
									self.player.game_image.setImage(0)
									#Do the same for an equipped character if it exists
									if self.player.equipped_item:
										self.player.equipped_item.game_image.setImage(0)
						# Check character positions and perform engine logic operations 
						self.check_characters()
						# Refresh characters
						self.refresh_characters()

					#Update time var to difference
					time_elapsed_since_last_action += dt
					#If one second has passed
					#then perform time specific functions and reset time since variable
					if time_elapsed_since_last_action > 1000:
						time_elapsed_since_last_action = 0
						self.clock_ticked()
					#Finally, update the PyGame display
					pygame.display.flip()

