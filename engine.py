#!/usr/bin/env python
# encoding: utf-8

import sys, pygame
import character
import lib.gifsprite
import lib.textbox


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

				pygame.draw.rect(self.screen, green, (0, 379, 300, 100), 0)
				pygame.draw.circle(self.screen, orange, (800, 100), 80, 0)
				pygame.draw.rect(self.screen, green, (621, 379, 300, 100), 0)

				pass
		def draw_characters(self):
				self.player = character.Character("./img/farmer.bmp")
				self.player.rect.top = 320

				self.cabbage = character.Character("./img/cabbage.bmp")
				self.cabbage.rect.top = 320
				self.cabbage.rect.left = 50

				self.wolf = character.Character("./img/wolf.bmp")
				self.wolf.rect.top = 320
				self.wolf.rect.left = 100

				self.sheep = character.Character("./img/goat.bmp")
				self.sheep.rect.top = 320
				self.wolf.rect.left = 150

				self.left_shore_characters.append(self.cabbage)
				self.left_shore_characters.append(self.wolf)
				self.left_shore_characters.append(self.sheep)

				self.refresh_characters()
				pass
		def refresh_characters(self):
				if self.player.equipped_item:
					self.player.equipped_item.rect.top  = self.player.rect.top-self.player.equipped_item.rect.height
					self.player.equipped_item.rect.left = self.player.rect.left

				self.screen.blit(self.player.game_image, self.player.rect)
				self.screen.blit(self.cabbage.game_image, self.cabbage.rect)
				self.screen.blit(self.wolf.game_image, self.wolf.rect)
				self.screen.blit(self.sheep.game_image, self.sheep.rect)

				pass
		def deposit_item(self):
				if self.player.equipped_item:
						self.player.equipped_item.rect.top  = self.player.rect.top
						self.player.equipped_item.rect.left = self.player.rect.right
						
						self.screen.blit(self.player.equipped_item.game_image, self.player.equipped_item.rect)
						
						# Remove the equipped item from both the sides
						if self.player.equipped_item in self.left_shore_characters:
							self.left_shore_characters.remove(self.player.equipped_item)
							pass
						elif self.player.equipped_item in self.right_shore_characters:
							self.right_shore_characters.remove(self.player.equipped_item)
							pass

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

				if 379 < self.player.rect.left < 450:
					current_side = self.left_shore_characters
					print "leaving left"
				elif self.player.rect.right < 621 and self.player.rect.left >= 450:
					current_side = self.right_shore_characters
					print "leaving right"

				# Check if the sheep has been left with the cabbage, or the wolf with the sheep
				if self.cabbage in current_side and self.sheep in current_side:
					print "cabbage eaten by sheep"
					pass
				elif self.sheep in current_side and self.wolf in current_side:
					print "sheep eaten by wolf"
					pass
				else:
					print "all good"
					pass
				pass
				
		def get_item_clicked(self, position):
				if self.cabbage.rect.collidepoint(position):
					return self.cabbage
				elif self.wolf.rect.collidepoint(position):
					return self.wolf
				elif self.sheep.rect.collidepoint(position):
					return self.sheep
					pass
				pass
		def start_title_sequence(self):
				self.screen.fill((255, 255, 255))
				pygame.display.update()
				while 1:
					for event in pygame.event.get():
						if event.type == pygame.MOUSEBUTTONUP:
							self.start_game()
		def start_game(self):
			self.draw_background()
			self.draw_characters()

			while 1:
					for event in pygame.event.get():
						if event.type == pygame.QUIT:
							sys.exit()
						if event.type == pygame.KEYDOWN:
							self.draw_background()                  
							if event.key == pygame.K_UP:
								self.goatrect = self.player.rect.move([0,-10])
							elif event.key == pygame.K_RIGHT:
								self.player.rect = self.player.rect.move([50, 0])
								self.check_characters()
							elif event.key == pygame.K_LEFT:
								self.player.rect = self.player.rect.move([-50,0])
								self.check_characters()
							elif event.key == pygame.K_ESCAPE:
								self.start_title_sequence();
						elif event.type == pygame.MOUSEBUTTONUP:
							print pygame.mouse.get_pos()
							if self.player.equipped_item:
								self.deposit_item()
							else:
								self.player.equip_item(self.get_item_clicked(pygame.mouse.get_pos()))
								if self.player.equipped_item in self.left_shore_characters:
									self.left_shore_characters.remove(self.player.equipped_item)
								if self.player.equipped_item in self.right_shore_characters:
									self.right_shore_characters.remove(self.player.equipped_item)
					self.refresh_characters()
					pygame.display.flip()