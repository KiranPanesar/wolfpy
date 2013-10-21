#!/usr/bin/env python
# encoding: utf-8

import sys
import pygame
import character

class GameEngine(object):
	"""docstring for GameEngine"""
	def __init__(self):
		super(GameEngine, self).__init__()
		self.screen = pygame.display.set_mode((900, 480))

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
		self.player 		  = character.Character("./img/goat.bmp")
		self.player.rect.top  = 320

		self.cabbage 		  = character.Character("./img/cabbage.bmp")
		self.cabbage.rect.top = 320


		self.refresh_characters()
		pass
	def refresh_characters(self):
		if self.player.equipped_item:
			self.player.equipped_item.rect.top  = self.player.rect.top-self.player.equipped_item.rect.height
			self.player.equipped_item.rect.left = self.player.rect.left

		self.screen.blit(self.player.game_image, self.player.rect)
		self.screen.blit(self.cabbage.game_image, self.cabbage.rect)
		pass
	def deposit_item(self):
		if self.player.equipped_item:

			self.player.equipped_item.rect.top  = self.player.rect.top
			self.player.equipped_item.rect.left = self.player.rect.right
			
			self.screen.blit(self.player.equipped_item.game_image, self.player.equipped_item.rect)
			self.player.deposit_item()

			self.refresh_characters()
			pass
		pass

	def start_title_sequence(self):
		self.screen.fill((255,255,255))
		play_button = pygame.Rect(300,50,250,180)
		# play_button.fill((0,210,255))
		self.screen.blit(play_button)

		pygame.display.flip()

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if play_button.collidepoint(pos):
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
								elif event.key == pygame.K_LEFT:
									self.player.rect = self.player.rect.move([-50,0])
						elif event.type == pygame.MOUSEBUTTONUP:
								print pygame.mouse.get_pos()
								if self.player.equipped_item:
									self.deposit_item()
								else:
									self.player.equip_item(self.cabbage)
				self.refresh_characters()
				pygame.display.flip()