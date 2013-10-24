# #!/usr/bin/env python
# # encoding: utf-8
#
# Created by Kiran Panesar - 23/10/2013

from Tkinter import *

class MessagePopUp(object):
	"""
		Class to show a simple Tkinter popup in only two lines of code
	"""
	# Initialise the object with a title, message, button text and callback action
	def __init__(self, popup_title, popup_message, button_text, button_action = None):
		super(MessagePopUp, self).__init__()
		self.popup_title = popup_title
		self.popup_message = popup_message
		self.button_text = button_text
		self.button_action = button_action
	
	# Instance method to show the popuyp
	def show(self):
		# Create callback function to run after Tkinter popup is dismissed
		def callback():
			# Close the pop up
			master.destroy()

			# If a callback action has been provided, run it
			if self.button_action != None:
				self.button_action()

		# Create a Tkinter instance
		master = Tk()

		# Set popup title
		master.title(self.popup_title)

		# Set up popup message and add it to the popup
		w = Label(master, text=self.popup_message)
		w.pack()

		# Set up button (with title and callback) and add it to the popup
		b = Button(master, text=self.button_text, width=10, command=callback)
		b.pack()
		mainloop()