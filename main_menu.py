import sys, pygame
import lib.button
import engine
import settings

class MainMenuScreen(object):
	"""docstring for MainMenuScreen"""
	def __init__(self, screen):
		super(MainMenuScreen, self).__init__()
		self.screen = screen
	
	def show_screen(self):
		self.screen.fill((255, 255, 255))
		startBtn = lib.button.Create(self.screen,(0,210,255), None, 180, "Start Game", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		settingBtn = lib.button.Create(self.screen,(0,210,255), None, 250, "Settings", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		
		pygame.display.flip()

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if startBtn.rect.collidepoint(pos):
						self.start_game()
					if settingBtn.rect.collidepoint(pos):
						self.settings()
	def settings(self):
		settings_screen = settings.SettingsScreen(self.screen)
		settings_screen.show_screen()

	def start_game(self):
		game_screen = engine.GameEngine(self.screen)
		game_screen.start_game()