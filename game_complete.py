import sys, pygame
import lib.button as button
import main_menu
import fblib.fbrequest as fbrequest
import lib.message_popup as message_popup

class GameCompletedScreen(object):
	"""
		Class for the screen shown when the user sucessfully completes the game
	"""
	# Init function passes the main screen and the time they took to complete the game
	def __init__(self, screen, time_taken):
		super(GameCompletedScreen, self).__init__()

		self.screen = screen # Setup the screen
		self.time_taken = time_taken # Store their time takes

		# Setup FB manager
		self.fb_manager = fbrequest.FBRequestManager("641940845850673", "f322228ac31f51e7dd4fb54a341ec00d", "http://kiranpanesar.com/river_adventure/auth_user.html")

	# Method to show the screen
	def show_screen(self):

		# Set up transluscent background for screen
		background_surface = pygame.Surface((900,480))  
		background_surface.set_alpha(128)               
		background_surface.fill((255,255,255))           
		self.screen.blit(background_surface, (0,0)) 
		
		# Load image to be overlayed
		image_file_string = None
		image_file_string = "./img/Win.png"

		# Prepare image
		image = pygame.image.load(image_file_string).convert_alpha()
		image_rect = image.get_rect()

		# Render image
		self.screen.blit(image, image_rect)		

		# Set up button
		share_button	  	=  button.Create(self.screen,(0,210,255), None, 200, "Share Score", 300, 50, (255,255,255), 32, 2,(10,10,10),1)
		main_menu_button 	=  button.Create(self.screen,(0,210,255), None, 270, "Main Menu", 300, 50, (255,255,255), 32, 2,(10,10,10),1)

		# Loop to grab user input
		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
						sys.exit()
				# If they clicked, grab the mouse position
				# and run clicked button's method
				elif event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					if main_menu_button.rect.collidepoint(pos):
						# Show the main menu
						menu = main_menu.MainMenuScreen(self.screen)
						menu.show_screen()
					elif share_button.rect.collidepoint(pos):
						# Share score to facebook
						self.share_score()

			pygame.display.flip()

	def share_score(self):
		# Create message to be shared
		share_message = "I've just completed River Crossing Adventure in "+ str(self.time_taken) + " seconds!"

		# Create callback function (run when pop up message closes)
		def callback():
			# Run the FB manager request to actually send the message
			# Remember, if the user isn't auth'd, this will also authenticate them
			response = self.fb_manager.fb_post_message(share_message)

			# Check if an error occurred
			if type(response) is fbrequest.FBError:
				# Show a pop up detailing the error
				error_popup = message_popup.MessagePopUp("Could Not Share - An Error Occurred", response.error_message, "Dismiss")
				error_popup.show()
			else:
				# If no error, show success message
				success_popup = message_popup.MessagePopUp("Post Successfully Shared!", "Your message has been shared to Facebook!", "Dismiss")
				success_popup.show()

		# Show pop up to confirm the user wants to share this
		confirm_share = message_popup.MessagePopUp("Sharing To Facebook", "Message to be shared: \n"+share_message, "Publish!", callback)
		confirm_share.show()