import pygame

class Create(pygame.Surface):
	def __init__(self, surface, background, x,y, text, width, height, colour, fontSize, border, borderColour):

		pygame.font.init()

		self.render = pygame.Surface((width,height))
		self.render.fill(background)

		self.rect =  self.render.get_rect()
		self.rect.centerx = x
		self.rect.top = y

		font = pygame.font.Font(None, fontSize)
		
		text = font.render(text, 1, (colour))
		textpos = text.get_rect()
		textpos.centerx = width / 2
		textpos.centery = height / 2

		self.render.blit(text, textpos)
		surface.blit(startBtn.render, startBtn.rect)
	def setActive(self):
		pass
	def serInactive(self):
		pass