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

		# Initialise properties
		self.images = []  # Sprites will have multiple states (i.e., images) they can flip between
		self.index = 0    # Set the current image to be the first one 
		self.flip = False # Sets whether the Sprite should 'turn around' on the screen next refresh

		# Loop through the resources we have been passed
		# Add them to the images array
		for image in passedImages:
			self.images.append(self.load_image(image))
			if  self.flip == 0:
				self.image = self.images[self.index]
			else:
				self.image = pygame.transform.flip(self.images[self.index], 1, 0)
		
		# Set up frame for sprite
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y

		# Set up the sprite group
		self.group = pygame.sprite.Group(self)

	# Used the load the image from disk
	def load_image(self,name):
	    fullname = os.path.join('img', name)

	    # Try and load the image, return error message if failed
	    try:
	        image = pygame.image.load(fullname).convert_alpha()
	    except pygame.error, message:
	        print 'Cannot load image:', name
	        raise SystemExit, message
	    return image

	# Set the current sprite position and flip state
	def postion(self, left, top, flip):
		self.flip = flip # set flip state

		# Pick which image to display
		if self.flip == 0:
			self.image = self.images[self.index]
		else:
			self.image = pygame.transform.flip(self.images[self.index], 1, 0)
		
		# Update sprite position
		self.rect.left = left
		self.rect.top = top

	# Used to switch to next image in sprite group
	def update(self):
		self.index += 1 # increment image index

		# Set index to 0 if it's over the limit
		if self.index >= len(self.images):
			self.index = 0

		# If we shouldn't flip, just draw the image
		if self.flip == 0:
			self.image = self.images[self.index]
		else:
			# Else, flip around and draw
			self.image = pygame.transform.flip(self.images[self.index], 1, 0)

	# Used to set if the image should flip and instantly redraw
	def setFlip(self, flip):
		
		self.flip = flip
		# If it shouldn't flip, set the image
		if self.flip == 0:
			self.image = self.images[self.index]
		else:
			# else, flip the sprite around and draw
			self.image = pygame.transform.flip(self.images[self.index], 1, 0)
			
	# Used to draw the image for the provided index
	def setImage(self, index):
		if self.flip == 0:
			self.image = self.images[index]
		else:
			self.image = pygame.transform.flip(self.images[index], 1, 0)