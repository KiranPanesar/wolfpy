#Import Pygame
import pygame, os

"""
Gif Sprite Class - Daniel Koehler

	Initiate in the form:
		fooGif = GifSprite(['Farmer Walk Animation 01a.png', 'Farmer Walk Animation 02a.png'], xcord, ycord)
		fooGifGroup = pygame.sprite.Group(goatGif)
	Draw in loop in the form:
		Sets states:  e.g. goatGif.setFlip(1) or goatGif.update()
		Then blitz Group: fooGifGroup.draw(screen)
"""
class Create(pygame.sprite.Sprite):
	def __init__(self,passedImages,x,y):
		super(Create, self).__init__()
		self.images = []
		self.index = 0
		self.flip = False
		# Loop through the resources we have been passed
		for image in passedImages:
			self.images.append(self.load_image(image))
			if  self.flip == 0:
				self.image = self.images[self.index]
			else:
				self.image = pygame.transform.flip(self.images[self.index], 1, 0)
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.group = pygame.sprite.Group(self)


	def load_image(self,name):
	    fullname = os.path.join('img', name)
	    # Still slightly unsure of try-excpection statments, thought implimenting one here might be useful for null resources in terms of debugging Tuesday.
	    try:
	        image = pygame.image.load(fullname).convert_alpha()
	    except pygame.error, message:
	        print 'Cannot load image:', name
	        raise SystemExit, message
	    return image

	def postion(self, left, top, flip):
		self.flip = flip
		if self.flip == 0:
			self.image = self.images[self.index]
		else:
			self.image = pygame.transform.flip(self.images[self.index], 1, 0)
		self.rect.left = left
		self.rect.top = top

	def update(self):
		self.index += 1
		if self.index >= len(self.images):
			self.index = 0
		if self.flip == 0:
			self.image = self.images[self.index]
		else:
			self.image = pygame.transform.flip(self.images[self.index], 1, 0)

	def setFlip(self, flip):
		self.flip = flip
		if self.flip == 0:
			self.image = self.images[self.index]
		else:
			self.image = pygame.transform.flip(self.images[self.index], 1, 0)
	def setImage(self, index):
		if self.flip == 0:
			self.image = self.images[index]
		else:
			self.image = pygame.transform.flip(self.images[index], 1, 0)