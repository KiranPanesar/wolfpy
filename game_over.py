import sys, pygame
import lib.button as button

class GameOverScreen(object):
	"""docstring for GameOverScreen"""
	def __init__(self, screen):
		super(GameOverScreen, self).__init__()

	def show_screen(self):
		self.screen.fill((255, 255, 255))
		
		retry_button	  	=  button.Create(self.screen,(0,210,255), None, 180, "Try again", 300, 50, (255,255,255), 32, 2,(10,10,10),0)
		main_menu_button 	=  button.Create(self.screen,(0,210,255), None, 180, "Main Menu", 300, 50, (255,255,255), 32, 2,(10,10,10),0)

		self.screen.blit(retry_button.render,retry_button.rect)
		self.screen.blit(main_menu_button.render,main_menu_button.rect)

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()


			pygame.display.flip()

		