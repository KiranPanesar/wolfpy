import urllib

class FBRequestManager(object):
	"""docstring for FBRequestManager"""
	def __init__(self, access_token):
		super(FBRequestManager, self).__init__()
		self.access_token = access_token
	def fb_post_message(self, status_message):
		data = {"access_token" : self.access_token, "message" : status_message}
		data = urllib.urlencode(data)
		print data
		response = urllib.urlopen("https://graph.facebook.com/1071692196/feed", data)
		print response.info()