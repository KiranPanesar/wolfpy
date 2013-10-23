import pygame

class Create(pygame.Surface):
	def __init__(self, surface, background, x,y, text, width, height, colour, fontSize, border, borderColour, render):

		pygame.font.init()
		# Create container border surface
		self.colour = colour
		self.width =  width
		self.height	= height
		self.renderSurface = surface
		self.border = pygame.Surface((width,height))
		self.border.fill((borderColour))
		self.borderRect = self.border.get_rect()
		if x != None:
			self.borderRect.left = x
		else:
			self.borderRect.centerx = self.renderSurface.get_rect().centerx
		self.borderRect.top = y
		# Create container border surface
		self.render = pygame.Surface((width -(border * 2),height -(border * 2)))
		self.render.fill((background))

		self.rect =  self.render.get_rect()
		self.rect.top = border
		self.rect.left = border
		# Let's blit these two!
		self.border.blit(self.render, self.rect)
		self.rect = self.borderRect
		self.font = pygame.font.Font(None, fontSize)
		
		text = self.font.render(text, 1, (colour))
		textpos = text.get_rect()
		textpos.centerx = width / 2
		textpos.centery = height / 2
		self.background_store = self.border.copy()
		
		self.border.blit(text, textpos)
		self.render = self.border
		if render:
			self.renderSurface.blit(self.border, self.borderRect)

	def change_text(self, text, colour = 0, render=1):
		if colour == 0:
			colour = self.colour
		text = self.font.render(text, 1, (colour))
		textpos = text.get_rect()
		textpos.centerx = self.width / 2
		textpos.centery = self.height / 2
		self.background_store.blit(text, textpos)
		self.render = self.background_store

		if render:
			self.renderSurface.blit(self.background_store, self.borderRect)