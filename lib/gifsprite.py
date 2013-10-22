#Import Pygame
import pygame, os

"""
Gif Sprite Class - Daniel Koehler

	Initiate in the form:
		fooGif = GifSprite(['farmer.v1.1.png', 'farmer.v1.2.png'], xcord, ycord)
		fooGifGroup = pygame.sprite.Group(goatGif)
	Draw in loop in the form:
		Sets states:  e.g. goatGif.setFlip(1) or goatGif.update()
		Then blitz Group: fooGifGroup.draw(screen)
"""
class GifSprite(pygame.sprite.Sprite):
	def __init__(self,passedImageses,x,y):
		super(GifSprite, self).__init__()
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
		self.rect = pygame.Rect(0, 0, x, y)


	def load_image(name):
	    fullname = os.path.join('data', name)
	    # Still slightly unsure of try-excpection statments, thought implimenting one here might be useful for null resources in terms of debugging Tuesday.
	    try:
	        image = pygame.image.load(fullname)
	    except pygame.error, message:
	        print 'Cannot load image:', name
	        raise SystemExit, message
	    image = image.convert()
	    return image, image.get_rect()

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