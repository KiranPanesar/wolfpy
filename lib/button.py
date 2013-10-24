import pygame

class Create(pygame.Surface):
	def __init__(self, surface, background, x,y, text, width, height, colour, fontSize, border, borderColour, render):
		self.surface = None
		self.background = None	
		self.x = None
		self.y = None
		self.text = None
		self.width = None
		self.height = None
		self.colour = None
		self.fontSize = None
		self.border = None
		self.borderColour = None
		self.rect = None
		self.changeProperty(surface, background, x,y, text, width, height, colour, fontSize, border, borderColour)
		if render:
			self.renderSelf()
		# Create container border surface
		
	def changeProperty(self, surface = None, background= None, x= None,y= None, text= None, width= None, height= None, colour= None, fontSize= None, border= None, borderColour= None):
		if surface != None:
			self.surface = surface
		if background != None:
			self.background = background
		if x != None:	
			self.x = x
		if y != None:
			self.y = y
		if text != None:
			self.text = text
		if width != None:
			self.width = width
		if height != None:
			self.height = height
		if colour != None:
			self.colour = colour
		if fontSize != None:
			self.fontSize = fontSize
		if border != None:
			self.border = border
		if borderColour != None:
			self.borderColour = borderColour

	def change_text(self, text):
		self.text = text
		self.renderSelf()

	def renderSelf(self):
		pygame.font.init()
		border_surface = pygame.Surface((self.width,self.height))
		border_surface.fill((self.borderColour))
		border_surface_rect = border_surface.get_rect()
		if self.x != None:
			border_surface_rect.left = self.x
		else:
			border_surface_rect.centerx = self.surface.get_rect().centerx
		border_surface_rect.top = self.y
		# Create container border surface
		render = pygame.Surface((self.width -(self.border * 2),self.height -(self.border * 2)))
		render.fill((self.background))

		self.rect =  render.get_rect()
		self.rect.top = self.border
		self.rect.left = self.border
		# Let's blit these two!
		border_surface.blit(render, self.rect)
		self.rect = border_surface_rect
		self.font = pygame.font.Font(None, self.fontSize)
		
		text = self.font.render(self.text, 1, (self.colour))
		textpos = text.get_rect()
		textpos.centerx = self.width / 2
		textpos.centery = self.height / 2
		
		border_surface.blit(text, textpos)
		self.render = border_surface
		self.surface.blit(border_surface, border_surface_rect)
