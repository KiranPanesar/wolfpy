import pygame, os, sys
import button

class AlertView(object):
	"""Shows a pop up"""
	def __init__(self,backing_screen, button_callback, popup_title = "", popup_message = "", action_button_title = "Okay", msg_1 = "", msg_2 = "", msg_3 = "", msg_4 = ""):
		super(AlertView, self).__init__()
		self.popup_title = popup_title
		self.popup_message  = popup_message
		self.screen = backing_screen
		self.action_button_title = action_button_title
		self.button_callback = button_callback
		self.messages = []
		if msg_1 != "":
			self.messages.append(msg_1)
		if msg_2 != "":
			self.messages.append(msg_2)
		if msg_3 != "":
			self.messages.append(msg_3)
		if msg_4 != "":
			self.messages.append(msg_4)
		print self.messages

	def show_popup(self):
		pygame.font.init()
		background_store = self.screen.copy()

		background_surface = pygame.Surface((500,280))  
		background_surface.set_alpha(235)               
		background_surface.fill((255,255,255))           
		
		
		#Render Cross
		font = pygame.font.Font(None, 20)
		exit_label = font.render("X", 1, (6,6,6))
		exit_label_rect  = exit_label.get_rect()
		exit_label_rect.left = 680
		exit_label_rect.top = 110
		self.screen.blit(background_surface, (200,100)) 
		self.screen.blit(exit_label, exit_label_rect)

		font = pygame.font.Font(None, 20)
		#Render Message
		for idx, message in enumerate(self.messages):
			title_label = font.render(message, 1, (6,6,6))
			title_rect  = title_label.get_rect()
			title_rect.left = 250
			title_rect.top = 150 + ((idx + 1) * 30)
			self.screen.blit(title_label, title_rect)

		
		startBtn = button.Create(self.screen,(0,210,255), None, 310, "Okay", 300, 50, (255,255,255), 32, 2,(10,10,10),1);
		pygame.display.flip()

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				elif event.type == pygame.MOUSEBUTTONUP:
						pos = pygame.mouse.get_pos()
						if exit_label_rect.collidepoint(pos):
							self.screen.blit(background_store, (0,0))
							pygame.display.flip()
							break
						elif startBtn.rect.collidepoint(pos):
							self.screen.blit(background_store, (0,0))
							pygame.display.flip()
							self.button_callback()
							break


