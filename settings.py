import sys, pygame
import lib.button
import main_menu
import fblib.fbrequest as fbrequest

class SettingsScreen(object):
	"""docstring for SettingsScreen"""
	def __init__(self, screen):
		super(SettingsScreen, self).__init__()
		self.screen = screen
		self.sound = True
		self.fb_manager = fbrequest.FBRequestManager("641940845850673", "f322228ac31f51e7dd4fb54a341ec00d", "http://kiranpanesar.com/river_adventure/auth_user.html")

	def show_screen(self):
		self.background = pygame.image.load('./img/Background.png').convert_alpha()
		self.screen.blit(self.background, (0,0))
		backBtn =  lib.button.Create(self.screen,(0,210,255), 20, 20, "Back", 60, 30, (255,255,255), 24, 2,(10,10,10),1)
		soundBtn =  lib.button.Create(self.screen,(0,210,255), None, 180, "Toggle Sound (On)", 300, 50, (255,255,255), 32, 2,(10,10,10),0)
		self.fb_toggle_button =  lib.button.Create(self.screen,(0,210,255), None, 250, "Facebook Log In", 300, 50, (255,255,255), 32, 2,(10,10,10),1)

		if self.fb_manager.fb_is_user_authd():
			print self.fb_manager.fb_oauth_manager
			self.fb_toggle_button.change_text("Log Out")
		
		if pygame.mixer.music.get_busy():
			soundBtn.change_text("Toggle Sound (On)")
		else:
			soundBtn.change_text("Toggle Sound (Off)")	

		sound_rect = soundBtn.rect

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if backBtn.rect.collidepoint(pos):
						self.title_screen()
					elif sound_rect.collidepoint(pos): # Cords Same
						if self.sound == 1:
							self.sound = 0
							pygame.mixer.music.stop()
							soundBtn.change_text("Toggle Sound (Off)")	
						else: 
							self.sound = 1
							pygame.mixer.music.play(-1)
							soundBtn.change_text("Toggle Sound (On)")	
					elif self.fb_toggle_button.rect.collidepoint(pos):
						self.toggle_user_login()
			pygame.display.flip()
	def title_screen(self):
		main_screen = main_menu.MainMenuScreen(self.screen)
		main_screen.show_screen()

		pass
	def toggle_user_login(self):
		print "Toggle"
		if self.fb_manager.fb_is_user_authd():
			print "logging out"
			self.fb_manager.fb_log_out()
			self.fb_toggle_button.change_text("Log In")
		else:
			print "logging in"
			self.fb_manager.fb_authenticate_user()
			self.fb_toggle_button.change_text("Log Out")