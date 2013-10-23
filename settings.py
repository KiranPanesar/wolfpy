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
		self.screen.fill((255, 255, 255))
		backBtn =  lib.button.Create(self.screen,(0,210,255), 20, 20, "Back", 60, 30, (255,255,255), 24, 2,(10,10,10),1)
		soundBtnOn =  lib.button.Create(self.screen,(0,210,255), None, 180, "Toggle Sound (On)", 300, 50, (255,255,255), 32, 2,(10,10,10),0)
		soundBtnOff =  lib.button.Create(self.screen,(0,210,255), None, 180, "Toggle Sound (Off)", 300, 50, (255,255,255), 32, 2,(10,10,10),0)
		self.fb_toggle_button =  lib.button.Create(self.screen,(0,210,255), None, 250, "Facebook Log In", 300, 50, (255,255,255), 32, 2,(10,10,10),1)

		if self.fb_manager.fb_is_user_authd:
			self.fb_toggle_button.change_text("Log Out")
		
		if self.sound:
			self.screen.blit(soundBtnOn.render,soundBtnOn.rect)
		else:
			self.screen.blit(soundBtnOff.render,soundBtnOff.rect)
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if backBtn.rect.collidepoint(pos):
						self.title_screen()
					elif soundBtnOn.rect.collidepoint(pos): # Cords Same
						print "sound button"
						if self.sound == 1:
							self.sound = 0
							self.screen.blit(soundBtnOff.render,soundBtnOff.rect)
						else: 
							self.sound = 1
							self.screen.blit(soundBtnOn.render,soundBtnOn.rect)
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