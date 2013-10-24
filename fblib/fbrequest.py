# #!/usr/bin/env python
# # encoding: utf-8
#
# Created by Kiran Panesar - 22/10/2013

import urllib
import fboauth
import json

class FBError(object):
	"""Class to return an error object if an FBRequestManager method fails"""

	def __init__(self, error_message, error_code):
		super(FBError, self).__init__()
		self.error_code = error_code
		self.error_message = error_message		

class FBRequestManager(object):
	""" Class to handle all requests to the Facebook API
		The calling controller should check whether the response is of type FBError
		to determine the success of the request.

		All methods are prefixed with "fb_" 
	"""
	def __init__(self, client_id, client_secret, redirect_uri):
		super(FBRequestManager, self).__init__()

		# Initialise the application with the data needed to authenticate the user
		self.client_id     = client_id
		self.client_secret = client_secret
		self.redirect_uri  = redirect_uri

		# Set up our OAuth manager with the authentication data
		# This class can be found in /fboatuh.py
		self.fb_oauth_manager = fboauth.FBOAuthManager(self.client_id, self.client_secret, self.redirect_uri)

	# Instance method to sign the user in
	def fb_authenticate_user(self):
		# Runs OAuth manager method to sign in
		self.fb_oauth_manager.fb_authenticate_user(self.client_id, self.redirect_uri, self.client_secret)

	# Sign the user out
	def fb_log_out(self):
		self.fb_oauth_manager.destroy_session()
		
	# Loads info on the currently-auth'd user
	def fb_load_info_for_current_user(self):
		# Load the saved access token and checks that it's still valid
		# If the user isn't auth'd, it will go and authenticate them 
		self.fb_oauth_manager.load_and_check_access_token()

		# Request the information for the user
		response = urllib.urlopen("https://graph.facebook.com/me?access_token="+self.fb_oauth_manager.access_token).read()
		
		# Parse out the error from the JSON response
		if error_from_json(json.loads(response)):
			return error_from_json(json.loads(response)) # If an error occurred, return the FBError object

		# Return the parsed JSON
		# Ideally we will implement an FBUser object to store the parsed JSON
		return json.loads(response)

	# Posts a status as the currently-auth'd
	def fb_post_message(self, status_message):
		# Load access token or authenticate user
		self.fb_oauth_manager.load_and_check_access_token()

		# Create the data to POST to the Facebook API
		data = {"access_token" : self.fb_oauth_manager.access_token, "message" : status_message}
		# Encode the POST data
		data = urllib.urlencode(data)

		# Make request to Facebook API
		response = urllib.urlopen("https://graph.facebook.com/me/feed", data).read()

		# Check for and return error. Will return None if request was successful
		return error_from_json(json.loads(response))

	# Simple method to check if the user is logged in
	def fb_is_user_authd(self):
		# Call FBOAuthManager method to check
		return self.fb_oauth_manager.is_user_logged_in()

# Parses the error object from the FB JSON response
def error_from_json(json_dict):
	json_error = None

	if json_dict != None:
		# If the JSON response contains an "error" object, return the FBError instance
		# with the message and code
		if "error" in json_dict:
			json_error = FBError(json_dict["error"]["message"], str(json_dict["error"]["code"]))

	return json_error