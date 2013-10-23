# #!/usr/bin/env python
# # encoding: utf-8
#
# Created by Kiran Panesar - 22/10/2013

import webbrowser
import csv
import time

from Tkinter import *

class FBOAuthManager(object):
	"""docstring for FBOAuthManager"""
	def __init__(self, client_id, client_secret, redirect_uri):
		super(FBOAuthManager, self).__init__()
		self.access_token = None
		self.access_token_expirery_epoch = 0
		
		self.client_id     = client_id
		self.client_secret = client_secret
		self.redirect_uri  = redirect_uri
		
		self.load_access_token()

	def fb_authenticate_user(self, client_id=None, redirect_uri=None, client_secret=None):
		if client_id == None:
			client_id = self.client_id
		if client_secret == None:
			client_secret = self.client_secret
		if redirect_uri == None:
			redirect_uri = self.redirect_uri

		urlString = "https://www.facebook.com/dialog/oauth?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=token&scope=publish_actions"

		master = Tk()

		def confirm_log_in():
			master.destroy()
			log_in()
			
		def log_in():
			webbrowser.open(urlString)

			master = Tk()
			master.title("Sign Into Facebook")

			e = Entry(master, width=50)
			e.pack()

			e.focus_set()
			e.insert(0,"")

			def callback_block():
			    if len(e.get()) > 0:
			    	# parse the url
			    	url_string = e.get()
			    	self.access_token = url_string[url_string.find("=")+1:url_string.find("&expires_in")]
			    	expiration_epoch = url_string[url_string.find("&expires_in=")+12:]
			    	self.save_access_token(self.access_token, expiration_epoch)

			    master.destroy()

			b = Button(master, text="Sign In!", width=10, command=callback_block)
			b.pack()

			mainloop()

		master.title("Steps to Sign In")
		w = Label(master, text="1) Log in using the browser window which will appear.\n2)Copy the URL that is loaded\n3)Paste back into the game\nAnd you're done!")
		w.pack()
		b = Button(master, text="Got it!", width=10, command=confirm_log_in)
		b.pack()
		mainloop()

	def destroy_session(self):
		self.access_token = None
		self.access_token_expirery_epoch = 0

		# Clear the CSV file containing the token data
		csv_file_name = "./fblib/token_data.csv"
		csv_file = open(csv_file_name, "w+")
		csv_file.close()

	def load_and_check_access_token(self):
		if self.has_access_token_expired():
			self.fb_authenticate_user()
		else:
			self.load_access_token()
	
	def has_access_token_expired(self):
		return self.access_token_expirery_epoch <= time.time()

	def is_user_logged_in(self):
		if self.access_token == None:
			return False
		else:
			return True

	def load_access_token(self):
		with open('./fblib/token_data.csv', 'rb') as csvfile:
			csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in csv_reader:
				self.access_token = row[0]
				self.access_token_expirery_epoch = row[1]

	def save_access_token(self, access_token, expirery_epoch):
		with open("./fblib/token_data.csv", "w+") as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			expiration_epoch = int(expirery_epoch) + int(time.time())

			csv_writer.writerow([access_token, expiration_epoch])
		self.load_access_token
