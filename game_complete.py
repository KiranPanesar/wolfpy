import sys, pygame
import lib.button as button
import main_menu
import fblib.fbrequest as fbrequest

class GameCompletedScreen(object):
	"""docstring for GameCompletedScreen"""
	def __init__(self, screen, time_taken):
		super(GameCompletedScreen, self).__init__()
		self.screen = screen
		self.time_taken = time_taken
		self.fb_manager = fbrequest.FBRequestManager("641940845850673", "f322228ac31f51e7dd4fb54a341ec00d", "http://COPY-AND-PASTE-INTO-THE-GAME.com")

	def show_screen(self):
		background_surface = pygame.Surface((900,480))  
		background_surface.set_alpha(128)               
		background_surface.fill((255,255,255))           
		self.screen.blit(background_surface, (0,0)) 
		
		share_button	  	=  button.Create(self.screen,(0,210,255), None, 200, "Share Score", 300, 50, (255,255,255), 32, 2,(10,10,10),0)
		main_menu_button 	=  button.Create(self.screen,(0,210,255), None, 270, "Main Menu", 300, 50, (255,255,255), 32, 2,(10,10,10),0)

		self.screen.blit(share_button.render,share_button.rect)
		self.screen.blit(main_menu_button.render,main_menu_button.rect)

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if main_menu_button.rect.collidepoint(pos):
						print "Main menu clicked"
						menu = main_menu.MainMenuScreen(self.screen)
						menu.show_screen()
					elif share_button.rect.collidepoint(pos):
						print "share button clicked"
						self.fb_manager.fb_post_message("I've just completed River Crossing Adventure in "+ str(self.time_taken) + " seconds!")

			pygame.display.flip()

	def share_score(self):
		pass