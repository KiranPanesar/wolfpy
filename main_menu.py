import sys, pygame
import lib.button
import engine
import settings
import lib.message_popup as message_popup
import lib.alert_view as alert_view

class MainMenuScreen(object):
	"""
		Class for showing the Main menu
	"""
	def __init__(self, screen):
		super(MainMenuScreen, self).__init__()
		
		# Set up screen
		self.screen = screen

		# Set up blue background image
		self.background = pygame.image.load('./img/Background.png').convert_alpha()
		
		# Set up characters overlay image
		self.background_overlay = pygame.image.load('./img/Title-Screen.png').convert_alpha()

	# Method to actually show the screen
	def show_screen(self):
		# Draw the background images
		self.screen.blit(self.background, (0, 0)) # Draw First!
		self.screen.blit(self.background_overlay, (0, 0)) # Draw First!
		
		# Draw the buttons
		start_button = lib.button.Create(self.screen,(0,210,255), None, 180, "Start Game", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		setting_button = lib.button.Create(self.screen,(0,210,255), None, 250, "Settings", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		info_button = lib.button.Create(self.screen,(0,210,255), None, 320, "How To Play", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		
		# Render changes to screen
		pygame.display.flip()

		# Loop to catch user input
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				# If the user clicks, grab mouse position
				# Run the clicked button's method
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if start_button.rect.collidepoint(pos):
						self.start_game()
					if setting_button.rect.collidepoint(pos):
						self.settings()
					if info_button.rect.collidepoint(pos):
						self.show_instructions()
	
	# Starts the game
	def start_game(self):
		game_screen = engine.GameEngine(self.screen)
		game_screen.start_game()

	# Opens settings menu
	def settings(self):
		settings_screen = settings.SettingsScreen(self.screen)
		settings_screen.show_screen()

	# Shows instruction menu
	def show_instructions(self):
		instructions_popup = message_popup.MessagePopUp("Instructions", "The aim of the game is to get all the characters across to the other side. Your boat only has room for one extra object. \n\nThe sheep will get eaten by the wolf or the mutant cabbage if you, the farmer, leave either of them together.\n\nUse the arrow keys to move around and click to move a character.", "Got it!")
		instructions_popup.show()