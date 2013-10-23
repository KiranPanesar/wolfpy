# #!/usr/bin/env python
# # encoding: utf-8
#
# Created by Kiran Panesar - 23/10/2013

from Tkinter import *

class MessagePopUp(object):
	"""docstring for MessagePopUp"""
	def __init__(self, popup_title, popup_message, button_text, button_action):
		super(MessagePopUp, self).__init__()
		self.popup_title = popup_title
		self.popup_message = popup_message
		self.button_text = button_text
		self.button_action = button_action
	
	def show(self):
		def callback():
			master.destroy()
			if self.button_action != None:
				self.button_action()

		master = Tk()
		master.title(self.popup_title)
		w = Label(master, text=self.popup_message)
		w.pack()
		b = Button(master, text=self.button_text, width=10, command=callback)
		b.pack()
		mainloop()