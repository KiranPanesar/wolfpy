import sys, pygame
import lib.button as button
import engine

class GameOverScreen(object):
	"""docstring for GameOverScreen"""
	# if cabbage kills sheep, scenario = 0
	# if wolf kills sheep, scenario = 1
	def __init__(self, screen, scenario):
		super(GameOverScreen, self).__init__()
		self.screen = screen
		self.screen.fill((255, 255, 255))

	def show_screen(self):
		retry_button	  	=  button.Create(self.screen,(0,210,255), None, 300, "Try again", 300, 50, (255,255,255), 32, 2,(10,10,10),0)
		main_menu_button 	=  button.Create(self.screen,(0,210,255), None, 370, "Main Menu", 300, 50, (255,255,255), 32, 2,(10,10,10),0)

		self.screen.blit(retry_button.render,retry_button.rect)
		self.screen.blit(main_menu_button.render,main_menu_button.rect)

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if main_menu_button.rect.collidepoint(pos):
						print "Main menu clicked"
						game_engine = engine.GameEngine()
						game_engine.title_screen()
					elif retry_button.rect.collidepoint(pos):
						print "Rety button clicked"
						game_engine = engine.GameEngine()
						game_engine.start_game()

			pygame.display.flip()