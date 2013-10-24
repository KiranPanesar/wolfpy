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
				
				if screen == None:
					screen = pygame.display.set_mode((900,480))
					pygame.mixer.init()
					sounda= pygame.mixer.Sound("./sounds/background.wav")
					sounda.play()
				self.screen = screen
				self.left_shore_characters = []
				self.right_shore_characters = []
				self.sound = True
				self.game_start_time = time.time()

		def draw_background(self):
				self.cloud = pygame.image.load('./img/Cloud.png').convert_alpha()
				self.sun = pygame.image.load('./img/Sun.png').convert_alpha()
				self.river = gifsprite.Create(['River 1.png', 'River 1a.png'], 300, 400)
				self.background = pygame.image.load('./img/Background.png').convert_alpha()
				self.left_bank = pygame.image.load('./img/Bank Left.png').convert_alpha()
				self.right_bank = pygame.image.load('./img/Bank Right.png').convert_alpha()

		def refresh_background(self):
				self.screen.blit(self.background, (0, 0)) # Draw First!
				self.screen.blit(self.cloud, (145, 24))
				self.screen.blit(self.cloud, (425, 54))
				self.screen.blit(self.sun, (720, 24))
				self.screen.blit(self.left_bank, (0, 380))
				self.screen.blit(self.right_bank, (600, 380))
				self.river.group.draw(self.screen)

		def clock_ticked(self, update_river = 1):
			if update_river:
				self.river.update()
				self.refresh_characters(0)
			
		def draw_clock(self):
			game_time = int(time.time() - self.game_start_time)
			label = pygame.font.Font(None, 25).render(str(game_time)+" seconds", 1, (236, 240, 241))
			labelPos = label.get_rect()
			labelPos.top = 10
			labelPos.left = 10
			self.screen.blit(self.background,labelPos,labelPos)
			self.screen.blit(label, labelPos)

			# pygame.display.flip()

		def draw_characters(self):
				self.player = character.Character(gifsprite.Create(['Farmer01.png', 'Farmer02.png','Farmer03.png','Farmer04.png'], 60, 265)) # Must start step multiple+10
				self.player.direction = 0
				self.player.step_interval = 50

				self.cabbage = character.Character(gifsprite.Create(['Cabbage01.png', 'Cabbage02.png','Cabbage03.png','Cabbage04.png'], 100, 304))
				self.cabbage.positionLeft = 50
				self.cabbage.positionRight = 850

				self.wolf = character.Character(gifsprite.Create(['Wolf01.png', 'Wolf02.png','Wolf03.png'], 200, 333))
				self.wolf.positionLeft = 200
				self.wolf.positionRight = 790

				self.sheep = character.Character(gifsprite.Create(['Sheep01.png', 'Sheep02.png'], 15, 333))
				self.sheep.positionLeft = 170
				self.sheep.positionRight = 730

				self.boat = gifsprite.Create(['Boat-02a.png', 'Boat-03a.png'], 266, 325)
				self.boat.binding = 0

				self.left_shore_characters.append(self.cabbage)
				self.left_shore_characters.append(self.wolf)
				self.left_shore_characters.append(self.sheep)

				self.refresh_characters()

		def boat_binding(self):
			# only called when player on water
			if self.player.direction: #going right
				self.boat.setFlip(0)
				if self.player.game_image.rect.centerx > self.boat.rect.centerx + 50:
					self.boat.binding = self.player.game_image.rect.centerx - self.boat.rect.centerx - 50
			else: #Going left
				self.boat.setFlip(1)
				if self.player.game_image.rect.centerx < self.boat.rect.centerx - 50:
					self.boat.binding = self.player.game_image.rect.centerx - self.boat.rect.centerx + 50

		def refresh_characters(self,call_clock = 1):
				self.refresh_background()
				self.draw_clock()
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
				if self.player.equipped_item and (self.player.equipped_item.game_image.rect.right < 290 or self.player.equipped_item.game_image.rect.left > 610):
						if self.player.direction == 0:
							self.player.equipped_item.game_image.rect.right += 10
						else:
							self.player.equipped_item.game_image.rect.right -= 10
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
						elif self.player.equipped_item.game_image.rect.right <= 279:
							current_side = self.left_shore_characters

						current_side.append(self.player.equipped_item)

						self.player.deposit_item()
						self.refresh_characters()
				self.check_characters()

		def check_characters(self):
				current_side = []
				# Check if all the characters are on the right side
				if len(self.right_shore_characters) == 3:
					complete_screen = game_complete.GameCompletedScreen(self.screen, int(time.time()-self.game_start_time))
					complete_screen.show_screen()

				if self.player.game_image.rect.right > 300 and self.player.game_image.rect.left < 600: # Keep, change values later for boat docking
					self.player.game_image.setImage(0)
					self.boat_binding();

				if self.player.game_image.rect.right > 300 and self.player.game_image.rect.left < 600:
					# Check if the sheep has been left with the cabbage, or the wolf with the sheep
					if len(self.right_shore_characters) > 1:
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
			main_screen = main_menu.MainMenuScreen(self.screen)
			main_screen.show_screen()

		def settings(self):
			settings_page = settings.SettingsScreen(self.screen)
			settings_page.show_screen()

		def start_game(self):
			self.draw_background()
			self.draw_characters()
			
			# scheduler = sched.scheduler(time.time, time.sleep)
			# scheduler.enter(1, 1, self.clock_ticked(), (scheduler,))
			# scheduler.run()
			
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
								if self.player.equipped_item:
									self.player.equipped_item.game_image.update()
									self.player.equipped_item.game_image.setFlip(1)
								if self.player.game_image.rect.right <= 850:
									self.player.game_image.rect = self.player.game_image.rect.move([self.player.step_interval, 0])
									self.check_characters()
							elif event.key == pygame.K_LEFT: # Moving left
								self.player.direction = 0
								self.player.game_image.update()
								self.player.game_image.setFlip(0)
								if self.player.equipped_item:
									self.player.equipped_item.game_image.update()
									self.player.equipped_item.game_image.setFlip(0)
								if self.player.game_image.rect.left >= self.player.step_interval:
									self.player.game_image.rect = self.player.game_image.rect.move([-(self.player.step_interval),0])
									self.check_characters()
							elif event.key == pygame.K_ESCAPE: # Quit to title
								self.title_screen();
							
							# Move boat 
							if self.boat.binding > 0:
								position = self.boat.rect.centerx + self.boat.binding
								self.boat.rect.centerx = position
								self.player.game_image.setImage(0)
							elif self.boat.binding < 0:
								position = self.boat.rect.centerx + self.boat.binding
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
					
					#Timer Function
					time_elapsed_since_last_action += dt
									
					if time_elapsed_since_last_action > 1000:
						self.boat.update()
						time_elapsed_since_last_action = 0
						self.clock_ticked()
					pygame.display.flip()

