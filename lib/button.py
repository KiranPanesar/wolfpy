import pygame

class Create(pygame.Surface):
	'''
		Class to easily create a pygame button
	'''
	
	# Initialise button with various properties
	def __init__(self, surface, background, x,y, text, width, height, colour, fontSize, border, borderColour, render):
		
		# Set all properties to None
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

		# Update properties to their real values
		self.changeProperty(surface, background, x,y, text, width, height, colour, fontSize, border, borderColour)
		
		# 'render' parameter specifies whether the button should be automatically rendered
		# If render = 1, render the button
		if render:
			self.renderSelf()
		
	# Used to update the properties
	def changeProperty(self, surface = None, background= None, x= None,y= None, text= None, width= None, height= None, colour= None, fontSize= None, border= None, borderColour= None):
		# Checks if each param is None before updating
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

	# Change the text of the button
	def change_text(self, text):
		self.text = text
		self.renderSelf()

	# Used to draw the button on the screen
	def renderSelf(self):
		# Initialise font
		pygame.font.init()

		# Draw border for button on screen
		border_surface = pygame.Surface((self.width,self.height))
		border_surface.fill((self.borderColour))
		border_surface_rect = border_surface.get_rect()
		
		# If an x-coordinate has been specified, set it
		# else center button
		if self.x != None:
			border_surface_rect.left = self.x
		else:
			border_surface_rect.centerx = self.surface.get_rect().centerx
		
		# Set button's start y-coordinate
		border_surface_rect.top = self.y
		
		# Create container border surface
		render = pygame.Surface((self.width -(self.border * 2),self.height -(self.border * 2)))
		render.fill((self.background))

		# Set up button's main frame
		self.rect =  render.get_rect()
		self.rect.top = self.border
		self.rect.left = self.border

		# Blit background to screen
		border_surface.blit(render, self.rect)
		self.rect = border_surface_rect
		
		# Set up font
		self.font = pygame.font.Font(None, self.fontSize)
		
		# Create text label
		text = self.font.render(self.text, 1, (self.colour))
		textpos = text.get_rect()
		textpos.centerx = self.width / 2
		textpos.centery = self.height / 2
		
		# Blit text label to border
		border_surface.blit(text, textpos)
		self.render = border_surface

		# Blit the final button to screen
		self.surface.blit(border_surface, border_surface_rect)
