#!/usr/bin/env python
# encoding: utf-8
# Created by Kiran Panesar and Dan Khoeler - 22/10/2013

from Tkinter import *
import sys, pygame
import character
import lib.gifsprite
import lib.button
import fblib.fbrequest as fbrequest

class GameEngine(object):
		"""docstring for GameEngine"""
		def __init__(self):
				super(GameEngine, self).__init__()
				self.screen = pygame.display.set_mode((900,480))
				self.left_shore_characters = []
				self.right_shore_characters = []


		def draw_background(self):
				blue = 52, 152, 219
				self.screen.fill(blue)
				green = 0, 0, 0
				orange = 241, 196, 15
				
				pygame.draw.rect(self.screen, (44, 62, 80), (0, 400, 900, 100), 0)
				pygame.draw.rect(self.screen, green, (0, 379, 300, 100), 0)
				pygame.draw.circle(self.screen, orange, (800, 100), 80, 0)
				pygame.draw.rect(self.screen, green, (621, 379, 300, 100), 0) # right shore

		def draw_characters(self):
				self.player = character.Character("./img/farmer.bmp")
				self.player.rect.top = 320

				self.cabbage = character.Character("./img/cabbage.bmp")
				self.cabbage.rect.top = 320
				self.cabbage.rect.left = 50
				self.cabbage.positionLeft = 50
				self.cabbage.positionRight = 850

				self.wolf = character.Character("./img/wolf.bmp")
				self.wolf.rect.top = 320
				self.wolf.rect.left = 110
				self.wolf.positionLeft = 110
				self.wolf.positionRight = 790

				self.sheep = character.Character("./img/goat.bmp")
				self.sheep.rect.top = 320
				self.sheep.rect.left = 170
				self.sheep.positionLeft = 170
				self.sheep.positionRight = 730

				self.left_shore_characters.append(self.cabbage)
				self.left_shore_characters.append(self.wolf)
				self.left_shore_characters.append(self.sheep)

				self.refresh_characters()

		def refresh_characters(self):
				if self.player.equipped_item:
					self.player.equipped_item.rect.top  = self.player.rect.top-self.player.equipped_item.rect.height
					self.player.equipped_item.rect.left = self.player.rect.left

				self.screen.blit(self.player.game_image, self.player.rect)
				self.screen.blit(self.cabbage.game_image, self.cabbage.rect)
				self.screen.blit(self.wolf.game_image, self.wolf.rect)
				self.screen.blit(self.sheep.game_image, self.sheep.rect)

		def deposit_item(self):
				if self.player.equipped_item:
						self.player.equipped_item.rect.bottom  = self.player.rect.bottom
						if self.player.equipped_item.rect.centerx > 450:
							self.player.equipped_item.rect.right = self.player.equipped_item.positionRight
						else:
							self.player.equipped_item.rect.left = self.player.equipped_item.positionLeft
						self.screen.blit(self.player.equipped_item.game_image, self.player.equipped_item.rect)
						
						# Remove the equipped item from both the sides
						if self.player.equipped_item in self.left_shore_characters:
							self.left_shore_characters.remove(self.player.equipped_item)
						elif self.player.equipped_item in self.right_shore_characters:
							self.right_shore_characters.remove(self.player.equipped_item)

						# Check which shore the item is on and add it
						current_side = []
						if self.player.equipped_item.rect.left >= 621:
							current_side = self.right_shore_characters
						elif self.player.equipped_item.rect.right <= 379:
							current_side = self.left_shore_characters

						current_side.append(self.player.equipped_item)

						self.player.deposit_item()

						self.refresh_characters()
						pass
				pass

		def check_characters(self):
				current_side = []

				if self.player.rect.right > 380 and self.player.rect.left < 620:
					# if self.player.rect.right > 380:
					# 	current_side = self.left_shore_characters
					# 	print "leaving left"
					# elif self.player.rect.left < 620:
					# 	current_side = self.right_shore_characters
					# 	print "leaving right"

				# Check if the sheep has been left with the cabbage, or the wolf with the sheep
					if len(self.right_shore_characters) > 1:
						if self.cabbage in self.right_shore_characters and self.sheep in self.right_shore_characters:
							print "cabbage eaten by sheep"
						elif self.sheep in self.right_shore_characters and self.wolf in self.right_shore_characters:
							print "sheep eaten by wolf"
					else:
						if self.sheep in self.left_shore_characters and self.wolf in self.left_shore_characters:
							print "sheep eaten by wolf"
						elif self.cabbage in self.left_shore_characters and self.sheep in self.left_shore_characters:
							print "cabbage eaten by sheep"

		def get_item_clicked(self, position):
				current_side = []
				if self.player.rect.left >= 621:
					current_side = self.right_shore_characters
				elif self.player.rect.right <= 379:
					current_side = self.left_shore_characters
				if self.cabbage.rect.collidepoint(position) and self.cabbage in current_side:
					return self.cabbage
				elif self.wolf.rect.collidepoint(position) and self.wolf in current_side:
					return self.wolf
				elif self.sheep.rect.collidepoint(position) and self.sheep in current_side:
					return self.sheep

		def start_title_sequence(self):

				self.screen.fill((255, 255, 255))
				startBtn = lib.button.Create(self.screen,(0,210,255), None, 200, "Start Game", 300, 50, (255,255,255), 32, 2,(10,10,10));
			
				pygame.display.flip()

				while 1:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()
						if event.type == pygame.MOUSEBUTTONUP:
							if startBtn.rect.collidepoint(pygame.mouse.get_pos()):
								self.start_game()

		def start_game(self):
			
			self.draw_background()
			self.draw_characters()
			
			clock = pygame.time.Clock()

			while 1:
					clock.tick(30)
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()
						elif event.type == pygame.KEYDOWN:
							self.draw_background()                  
							if event.key == pygame.K_RIGHT:
								if self.player.rect.right <= 850:
									self.player.rect = self.player.rect.move([50, 0])
									self.check_characters()
								elif self.player.rect.right != 900:
									self.player.rect = self.player.rect.move([900 - self.player.rect.right, 0])
									self.check_characters()
							elif event.key == pygame.K_LEFT:
								if self.player.rect.left >= 50:
									self.player.rect = self.player.rect.move([-50,0])
									self.check_characters()
							elif event.key == pygame.K_ESCAPE:
								self.start_title_sequence();
						elif event.type == pygame.MOUSEBUTTONUP:
							self.draw_background()
							if self.player.equipped_item:     
								self.deposit_item()
							else:
								if self.get_item_clicked(pygame.mouse.get_pos()):								
									self.player.equip_item(self.get_item_clicked(pygame.mouse.get_pos()))
									if self.player.equipped_item in self.left_shore_characters:
										self.left_shore_characters.remove(self.player.equipped_item)
									if self.player.equipped_item in self.right_shore_characters:
										self.right_shore_characters.remove(self.player.equipped_item)
					self.refresh_characters()
					pygame.display.flip()

		def share_score(self):
			master = Tk()
			master.title("Share Score")

			e = Entry(master, width=50)
			e.pack()

			e.focus_set()
			e.insert(0,"I just completed River Crossing Game in 23 seconds!")

			def callback_block():
			    print e.get()
			    if len(e.get()) > 0:
			    	fb_request_manager = fbrequest.FBRequestManager("CAAJH14AVcDEBAIRjloeHaGqtJrzCr5jsSIiUNfuML6FASAZAFyAmdF2xumvszd3Vku9xnrn0pWKhxxuAZBVYecvxXLBZCJrVkPJaioWvP3gHETjlzpK6uuNyD5DrDYU3KFGBNBU6UqbMBwdo3zJSY3qvLHhhSEZD")
			    	fb_request_manager.fb_post_message(e.get())
			    	pass
			    master.destroy()

			b = Button(master, text="Share!", width=10, command=callback_block)
			b.pack()

			mainloop()
