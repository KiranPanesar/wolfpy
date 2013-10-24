# #!/usr/bin/env python
# # encoding: utf-8
#
# Created by Kiran Panesar - 22/10/2013

import webbrowser
import csv
import time
import os

from Tkinter import *

class FBOAuthManager(object):
	""" Class to handle the requesting, storing and checking of the Facebook access token
		(Used to authenticate the current user)
	"""
	def __init__(self, client_id, client_secret, redirect_uri):
		super(FBOAuthManager, self).__init__()

		# Initial the current access token and expirery time
		self.access_token = None
		self.access_token_expirery_epoch = 0
		
		# Set up the data needed for authentication
		self.client_id     = client_id
		self.client_secret = client_secret
		self.redirect_uri  = redirect_uri
		
		# Load any saved access token from the data store
		self.load_access_token()

	# Instance method to sign the user in using OAuth
	# Parameters are optional, will default to current instance's properties if params are None
	#	1) Web browser launches with authentication URL for the app
	# 	2) User signs in, user pastes access token URL into pop up
	# 	3) Application parses out access token
	def fb_authenticate_user(self, client_id=None, redirect_uri=None, client_secret=None):
		# Default to properties if the parameters aren't provided
		if client_id == None:
			client_id = self.client_id
		if client_secret == None:
			client_secret = self.client_secret
		if redirect_uri == None:
			redirect_uri = self.redirect_uri

		# Create the URL string to request the user to sign in
		# Docs for this found at http://developers.facebook.com/docs/facebook-login/
		url_string = "https://www.facebook.com/dialog/oauth?client_id="+client_id+"&redirect_uri="+redirect_uri+"&response_type=token&scope=publish_actions"

		# Create Tkinter object to show pop up
		master = Tk()

		# Create callback function for if the user confirms they want to sign in
		def confirm_log_in():
			master.destroy()
			log_in()
		
		# Run the logic to log in
		def log_in():
			# University computers only allow apps to open in IE.
			# So check if IE exists and open request string in that, if it doesn't, open in default.
			if os.path.isfile('c:\program files\internet explorer\iexplore.exe'):
				print "IE"
				browser = webbrowser.get('c:\program files\internet explorer\iexplore.exe')
				browser.open(url_string)
			else:
				print "custom"
				webbrowser.open(url_string)

			# Create pop up box to enter the resulting login URL (used to parse out the access token)
			master = Tk()
			master.title("Sign Into Facebook")

			# Add text box to pop up
			e = Entry(master, width=50)
			e.pack()

			e.focus_set()
			e.insert(0,"")

			# Callback block to parse out the access_token from the URL
			def callback_block():
				# If text was entered
			    if len(e.get()) > 0:
			    	# Parse out the access token from the URL
			    	# This needs to be perfected a bit
			    	url_string = e.get()
			    	self.access_token = url_string[url_string.find("=")+1:url_string.find("&expires_in")]
			    	expiration_epoch = url_string[url_string.find("&expires_in=")+12:]

			    	# Save the access token and expirery data to disk
			    	self.save_access_token(self.access_token, expiration_epoch)

			    # Close pop up
			    master.destroy()

			# Add sign in button to pop up
			b = Button(master, text="Sign In!", width=10, command=callback_block)
			b.pack()
			# Show pop up
			mainloop()

		# Show pop up giving steps to sign in
		master.title("Steps to Sign In")
		w = Label(master, text="1) Log in using the browser window which will appear.\n2)Copy the URL that is loaded\n3)Paste back into the game\nAnd you're done!")
		w.pack()

		# Create button to callback to the confirm_log_in() function (defined line 54)
		b = Button(master, text="Got it!", width=10, command=confirm_log_in)
		b.pack()
		mainloop()

	# Instance method to sign the user out
	def destroy_session(self):
		# Reset the properties
		self.access_token = None
		self.access_token_expirery_epoch = 0

		# Clear the CSV file containing the token data
		csv_file_name = "./fblib/token_data.csv"
		csv_file = open(csv_file_name, "w+")
		csv_file.close()

	# Loads the access token (if available). If not, authenticate the user.
	def load_and_check_access_token(self):
		if self.has_access_token_expired():
			self.fb_authenticate_user()
		else:
			self.load_access_token()

	# Check if the access token has expired
	def has_access_token_expired(self):
		# Expirery epoch (UNIX time) checked against current time
		return self.access_token_expirery_epoch <= time.time()

	# Check if the user is logged in
	def is_user_logged_in(self):
		# If the access token doesn't exist, return False
		if self.access_token == None:
			return False
		else:
			return True

	# Loads the access token from the disk
	def load_access_token(self):
		# Creates path to CSV file
		with open('./fblib/token_data.csv', 'rb') as csvfile:
			csv_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
			# Grab the access token and expirery epoch
			for row in csv_reader:
				self.access_token = row[0]
				self.access_token_expirery_epoch = row[1]

	# Save the access token to the disk
	def save_access_token(self, access_token, expirery_epoch):
		# Find/create the CSV to store
		with open("./fblib/token_data.csv", "w+") as csv_file:
			csv_writer = csv.writer(csv_file, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			expiration_epoch = int(expirery_epoch) + int(time.time())
			# Store the access token
			csv_writer.writerow([access_token, expiration_epoch])
		
		# Load token to ensure success
		self.load_access_token
