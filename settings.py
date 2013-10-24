import sys, pygame
import lib.button
import main_menu
import fblib.fbrequest as fbrequest

class SettingsScreen(object):
	"""
		Class for showing the Settings screen
	"""
	def __init__(self, screen):
		super(SettingsScreen, self).__init__()
		self.screen = screen # Set up screen
		self.sound = True    # Set sound default to "on"

		# Initialise the FB manager
		self.fb_manager = fbrequest.FBRequestManager("641940845850673", "f322228ac31f51e7dd4fb54a341ec00d", "http://kiranpanesar.com/river_adventure/auth_user.html")

	# Instance method to show the screen
	def show_screen(self):
		# Set up image background
		self.background = pygame.image.load('./img/Background.png').convert_alpha()
		self.screen.blit(self.background, (0,0))

		# Create buttons for going back, toggling sound and toggling Facebook
		backBtn =  lib.button.Create(self.screen,(0,210,255), 20, 20, "Back", 60, 30, (255,255,255), 24, 2,(10,10,10),1)
		self.soundBtn =  lib.button.Create(self.screen,(0,210,255), None, 180, "Toggle Sound (On)", 300, 50, (255,255,255), 32, 2,(10,10,10),0)
		self.fb_toggle_button =  lib.button.Create(self.screen,(0,210,255), None, 250, "Facebook Log In", 300, 50, (255,255,255), 32, 2,(10,10,10),1)

		# If the Facebook user is logged in, change the button to log out
		if self.fb_manager.fb_is_user_authd():
			self.fb_toggle_button.change_text("Log Out")
		
		# Checks if a sound is currently playing, alters button title appropriately
		if pygame.mixer.music.get_busy():
			self.soundBtn.change_text("Toggle Sound (On)")
		else:
			self.soundBtn.change_text("Toggle Sound (Off)")	

		# Loop to catch the user's input
		while 1:
			for event in pygame.event.get():
				# If they hit escape, quit.
				if event.type == pygame.QUIT:
						sys.exit()
				# If they have clicked, grab the mouse position
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					# If they've clicked the back button, go to the main screen
					if backBtn.rect.collidepoint(pos):
						self.title_screen()
					# If they've clicked the sound button, toggle sound
					elif self.soundBtn.rect.collidepoint(pos):
						self.toggle_sound()
					# If they've clicked the FB button, toggle Facebook
					elif self.fb_toggle_button.rect.collidepoint(pos):
						self.toggle_user_login()
			# Render display
			pygame.display.flip()

	# Instance method loads the main screen (equvilient of going back)
	def title_screen(self):
		main_screen = main_menu.MainMenuScreen(self.screen)
		main_screen.show_screen()

	def toggle_sound(self):
		if self.sound == 1:
			self.sound = 0
			pygame.mixer.music.stop()
			self.soundBtn.change_text("Toggle Sound (Off)")	
		else: 
			self.sound = 1
			pygame.mixer.music.play(-1)
			self.soundBtn.change_text("Toggle Sound (On)")	

	# Toggling the user login stae
	def toggle_user_login(self):
		# If the user is logged in, log them out and change button text
		if self.fb_manager.fb_is_user_authd():
			self.fb_manager.fb_log_out()
			self.fb_toggle_button.change_text("Log In")
		else:
			# If not auth'd, log them in and change button text
			self.fb_manager.fb_authenticate_user()
			self.fb_toggle_button.change_text("Log Out")