import sys, pygame
import lib.button
import engine
import settings
import lib.message_popup as message_popup

class MainMenuScreen(object):
	"""docstring for MainMenuScreen"""
	def __init__(self, screen):
		super(MainMenuScreen, self).__init__()
		self.screen = screen
		self.background = pygame.image.load('./img/Background.png').convert_alpha()

	def show_screen(self):
		self.screen.blit(self.background, (0, 0)) # Draw First!
		startBtn = lib.button.Create(self.screen,(0,210,255), None, 180, "Start Game", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		settingBtn = lib.button.Create(self.screen,(0,210,255), None, 250, "Settings", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		info_button = lib.button.Create(self.screen,(0,210,255), None, 320, "How To Play", 300, 50, (255,255,255), 32, 2,(10,10,10),1);

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
					if info_button.rect.collidepoint(pos):
						self.show_instructions()
	def start_game(self):
		game_screen = engine.GameEngine(self.screen)
		game_screen.start_game()

	def settings(self):
		settings_screen = settings.SettingsScreen(self.screen)
		settings_screen.show_screen()

	def show_instructions(self):
		instructions_popup = message_popup.MessagePopUp("Instructions", "The aim of the game is to get all the characters across to the other side. Your boat only has room for one extra object. \n\nThe sheep will get eaten by the wolf or the mutant cabbage if you, the farmer, leave either of them together them together.\n\nUse the arrow keys to move around and click to move a character.", "Got it!")
		instructions_popup.show()