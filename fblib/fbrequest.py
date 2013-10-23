# #!/usr/bin/env python
# # encoding: utf-8
#
# Created by Kiran Panesar - 22/10/2013

import urllib
import fboauth
import json

class FBError(object):
	"""docstring for FBError"""
	def __init__(self, error_message, error_code):
		super(FBError, self).__init__()
		self.error_code = error_code
		self.error_message = error_message		

class FBRequestManager(object):
	"""docstring for FBRequestManager"""
	def __init__(self, client_id, client_secret, redirect_uri):
		super(FBRequestManager, self).__init__()
		self.client_id     = client_id
		self.client_secret = client_secret
		self.redirect_uri  = redirect_uri

		self.fb_oauth_manager = fboauth.FBOAuthManager(self.client_id, self.client_secret, self.redirect_uri)

	# Used to sign the user in 
	def fb_authenticate_user(self):
		self.fb_oauth_manager.fb_authenticate_user(self.client_id, self.redirect_uri, self.client_secret)

	def fb_log_out(self):
		self.fb_oauth_manager.destroy_session()
		
	# Loads info on the currently-auth'd user
	def fb_load_info_for_current_user(self):
		self.fb_oauth_manager.load_and_check_access_token()
		response = urllib.urlopen("https://graph.facebook.com/me?access_token="+self.fb_oauth_manager.access_token).read()
		
		if error_from_json(json.loads(response)):
			return error_from_json(json.loads(response))

		return json.loads(response)

	# Posts a status as the currently-auth'd
	def fb_post_message(self, status_message):
		self.fb_oauth_manager.load_and_check_access_token()
		data = {"access_token" : self.fb_oauth_manager.access_token, "message" : status_message}
		data = urllib.urlencode(data)
		response = urllib.urlopen("https://graph.facebook.com/me/feed", data).read()

		return error_from_json(json.loads(response))

	def fb_is_user_authd(self):
		return self.fb_oauth_manager.is_user_logged_in


def error_from_json(json_dict):
	json_error = None
	if json_dict != None:
		if "error" in json_dict:
			json_error = FBError(json_dict["error"]["message"], str(json_dict["error"]["code"]))

	return json_error