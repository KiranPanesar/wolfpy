import pygame

class AlertView(object):
	"""Shows a pop up"""
	def __init__(self, popup_title, popup_message, popup_screen, dismiss_button_title, action_button_title, button_callback):
		super(AlertView, self).__init__()
		self.popup_title = popup_title
		self.popup_message  = popup_message
		self.screen = popup_screen
		self.dismiss_button_title = dismiss_button_title
		self.action_button_title = action_button_title
		self.button_callback = button_callback

	def show_popup(self):
		print "asdasd"
		pygame.font.init()
		background_store = self.screen.copy()
		font = pygame.font.Font(None, 15)
		title_label = font.render(self.popup_title, 1 (255,255,255))
		title_rect  = title_label.get_rect()
		title_label.centerx = self.screen.get_rect().width/2

		self.screen.blit(title_label, title_rect)
		pygame.display.flip()

		while 1:
			pass