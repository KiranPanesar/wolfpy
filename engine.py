#!/usr/bin/env python
# encoding: utf-8
# Created by Kiran Panesar and Dan Koehler - 22/10/2013

import sys, pygame
import lib.character as character
import lib.gifsprite as gifsprite
import lib.button
import fblib.fbrequest as fbrequest
import lib.message_popup as message_popup
import game_over
import settings
import main_menu

class GameEngine(object):
		"""docstring for GameEngine"""
		def __init__(self, screen):
				super(GameEngine, self).__init__()
				
				if screen == None:
					screen = pygame.display.set_mode((900,480))
				
				self.screen = screen
				self.left_shore_characters = []
				self.right_shore_characters = []
				self.sound = True

		def draw_background(self):
				blue = 52, 152, 219
				self.screen.fill(blue)
				green = 0, 0, 0
				orange = 241, 196, 15
				
				pygame.draw.rect(self.screen, (44, 62, 80), (0, 400, 900, 100), 0)
				pygame.draw.rect(self.screen, green, (0, 379, 300, 100), 0)
				pygame.draw.circle(self.screen, orange, (800, 100), 80, 0)
				pygame.draw.rect(self.screen, green, (621, 379, 300, 100), 0) # right shore

				# self.background = pygame.image.load("./img/background.png");
				# self.screen.blit(self.background, (0,0,900,480))




		def draw_characters(self):
				self.player = character.Character(gifsprite.Create(['Farmer01.png', 'Farmer02.png','Farmer03.png','Farmer04.png'], 75, 128))
				self.player.game_image.rect.top = 265
				self.player.game_image.rect.left = 10
				self.player.direction = 0
				self.player.step_interval = 50

				self.cabbage = character.Character(gifsprite.Create(['Cabbage01.png', 'Cabbage02.png','Cabbage03.png','Cabbage04.png'], 123, 100))
				self.cabbage.game_image.rect.top = 290
				self.cabbage.game_image.rect.left = 60
				self.cabbage.positionLeft = 50
				self.cabbage.positionRight = 850

				self.wolf = character.Character(gifsprite.Create(['Wolf01.png', 'Wolf02.png','Wolf03.png'], 64, 40))
				self.wolf.game_image.rect.top = 350
				self.wolf.game_image.rect.left = 200

				self.wolf.positionLeft = 200
				self.wolf.positionRight = 790

				self.sheep = character.Character(gifsprite.Create(['Sheep01.png', 'Sheep02.png'], 40, 40))
				self.sheep.game_image.rect.top = 350
				self.sheep.game_image.rect.left = 170

				self.sheep.positionLeft = 170
				self.sheep.positionRight = 730

				self.boat = gifsprite.Create(['Boat-02a.png', 'Boat-03a.png'], 163, 90)
				self.boat.rect.top = 325
				self.boat.rect.centerx = 325
				self.boat.binding = 0

				self.left_shore_characters.append(self.cabbage)
				self.left_shore_characters.append(self.wolf)
				self.left_shore_characters.append(self.sheep)

				self.refresh_characters()

		def boat_binding(self):
			# only called when player on water
			if self.player.direction: #going right
				self.boat.setFlip(0)
				if self.player.game_image.rect.centerx > self.boat.rect.centerx:
					self.boat.binding = self.player.game_image.rect.centerx - self.boat.rect.centerx
			else: #Going left
				self.boat.setFlip(1)
				if self.player.game_image.rect.centerx < self.boat.rect.centerx:
					self.boat.binding = self.player.game_image.rect.centerx - self.boat.rect.centerx

		def refresh_characters(self):
				self.draw_background()
				
				if self.player.equipped_item:
					if self.player.direction:
						# self.player.equipped_item.game_image.rect.left  = self.player.game_image.rect.top-self.player.equipped_item.game_image.rect.height
						self.player.equipped_item.game_image.rect.right = self.player.game_image.rect.left
					else:
						self.player.equipped_item.game_image.rect.left = self.player.game_image.rect.right

				self.player.game_image.group.draw(self.screen)
				
				self.cabbage.game_image.group.draw(self.screen)
				self.wolf.game_image.group.draw(self.screen)

				self.sheep.game_image.group.draw(self.screen)
				self.boat.group.draw(self.screen)# Draw Last!

		def deposit_item(self):
				if self.player.equipped_item:
						self.player.equipped_item.game_image.rect.bottom  = self.player.game_image.rect.bottom
						if self.player.equipped_item.game_image.rect.centerx > 450:
							self.player.equipped_item.game_image.rect.right = self.player.equipped_item.positionRight
						else:
							self.player.equipped_item.game_image.rect.left = self.player.equipped_item.positionLeft
						self.player.equipped_item.game_image.group.draw(self.screen)
						# self.screen.blit(, self.player.equipped_item.game_image.rect)
						
						# Remove the equipped item from both the sides
						if self.player.equipped_item in self.left_shore_characters:
							self.left_shore_characters.remove(self.player.equipped_item)
						elif self.player.equipped_item in self.right_shore_characters:
							self.right_shore_characters.remove(self.player.equipped_item)

						# Check which shore the item is on and add it
						current_side = []
						if self.player.equipped_item.game_image.rect.left >= 621:
							current_side = self.right_shore_characters
						elif self.player.equipped_item.game_image.rect.right <= 379:
							current_side = self.left_shore_characters

						current_side.append(self.player.equipped_item)

						self.player.deposit_item()

						self.refresh_characters()
						pass
				pass

		def check_characters(self):
				current_side = []

				if self.player.game_image.rect.right > 380 and self.player.game_image.rect.left < 620: # Keep, change values later for boat docking
					self.boat_binding();

				if self.player.game_image.rect.right > 380 and self.player.game_image.rect.left < 620:
					# Check if the sheep has been left with the cabbage, or the wolf with the sheep
					if len(self.right_shore_characters) > 1:
						if self.cabbage in self.right_shore_characters and self.sheep in self.right_shore_characters:
							print "cabbage eaten by sheep"
							end_game = game_over.GameOverScreen(self.screen, 0)
							end_game.show_screen()
						elif self.sheep in self.right_shore_characters and self.wolf in self.right_shore_characters:
							print "sheep eaten by wolf"
							end_game = game_over.GameOverScreen(self.screen, 1)
							end_game.show_screen()

					else:
						if self.sheep in self.left_shore_characters and self.wolf in self.left_shore_characters:
							print "sheep eaten by wolf"
							end_game = game_over.GameOverScreen(self.screen, 1)
							end_game.show_screen()

						elif self.cabbage in self.left_shore_characters and self.sheep in self.left_shore_characters:
							print "cabbage eaten by sheep"
							end_game = game_over.GameOverScreen(self.screen, 0)
							end_game.show_screen()


		def get_item_clicked(self, position):
				current_side = []
				if self.player.game_image.rect.left >= 621:
					current_side = self.right_shore_characters
				elif self.player.game_image.rect.right <= 379:
					current_side = self.left_shore_characters
				if self.cabbage.rect.collidepoint(position) and self.cabbage in current_side:
					return self.cabbage
				elif self.wolf.rect.collidepoint(position) and self.wolf in current_side:
					return self.wolf
				elif self.sheep.rect.collidepoint(position) and self.sheep in current_side:
					return self.sheep

		def title_screen(self):
			main_screen = main_menu.MainMenuScreen(self.screen)
			main_screen.show_screen()

		def settings(self):
			settings_page = settings.SettingsScreen(self.screen)
			settings_page.show_screen()

		def start_game(self):

			self.draw_characters()
			
			clock = pygame.time.Clock()
			time_elapsed_since_last_action = 0
			while 1:
					dt = clock.tick(30)
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()
						elif event.type == pygame.KEYDOWN: # Check for keydown events   
							self.boat.binding = 0    
							if event.key == pygame.K_RIGHT: # Moving right
								self.player.direction = 1
								self.player.game_image.update()
								self.player.game_image.setFlip(1)
								if self.player.game_image.rect.right <= 850:
									self.player.game_image.rect = self.player.game_image.rect.move([self.player.step_interval, 0])
									self.check_characters()
								elif self.player.game_image.rect.right != 900:
									self.player.game_image.rect = self.player.game_image.rect.move([900 - self.player.game_image.rect.right, 0])
									self.check_characters()
							elif event.key == pygame.K_LEFT: # Moving left
								self.player.direction = 0
								self.player.game_image.update()
								self.player.game_image.setFlip(0)
								if self.player.game_image.rect.left >= self.player.step_interval:
									self.player.game_image.rect = self.player.game_image.rect.move([-(self.player.step_interval),0])
									self.check_characters()
								elif self.player.game_image.rect.left != 0:
									self.player.game_image.rect = self.player.game_image.rect.move([0 - self.player.game_image.rect.left, 0])
									self.check_characters()
							elif event.key == pygame.K_ESCAPE: # Quit to title
								self.title_screen();
							
							# Move boat 
							if self.boat.binding > 0:
								position = self.boat.rect.centerx + self.boat.binding
								if position	> 597:
									self.boat.rect.centerx = 597
								else: 
									self.boat.rect.centerx = position
								self.player.game_image.setImage(0)
							elif self.boat.binding < 0:

								position = self.boat.rect.centerx + self.boat.binding
								if position	< 375:
									self.boat.rect.centerx = 325
								else: 
									self.boat.rect.centerx = position
								self.player.game_image.setImage(0)
							self.refresh_characters()
								
						elif event.type == pygame.MOUSEBUTTONUP: # Mouse event
							if self.player.equipped_item:     
								self.deposit_item()
							else:
								if self.get_item_clicked(pygame.mouse.get_pos()): # Check which item was clicked								
									self.player.equip_item(self.get_item_clicked(pygame.mouse.get_pos()))
									if self.player.equipped_item in self.left_shore_characters:
										self.left_shore_characters.remove(self.player.equipped_item)
									if self.player.equipped_item in self.right_shore_characters:
										self.right_shore_characters.remove(self.player.equipped_item)
							self.refresh_characters()
					
					#boat update check
					# time_elapsed_since_last_action += dt
					# if time_elapsed_since_last_action > 500:
					# 	self.boat.update()
					# 	time_elapsed_since_last_action = 0
					# 	self.refresh_characters()
					pygame.display.flip()