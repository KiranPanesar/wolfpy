from Tkinter import *

class ErrorPopUp(object):
	"""docstring for ErrorPopUp"""
	def __init__(self, error_title, error_message, button_text):
		super(ErrorPopUp, self).__init__()
		self.error_title = error_title
		self.error_message = error_message
		self.button_text = button_text
	
	def show(self):
		def callback():
			master.destroy()

		master = Tk()
		master.title(self.error_title)
		w = Label(master, text=self.error_message)
		w.pack()
		b = Button(master, text=self.button_text, width=10, command=callback)
		b.pack()
		mainloop()