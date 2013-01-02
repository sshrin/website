import webapp2
import cgi
import jinja2
import os

from google.appengine.api import users
from google.appengine.ext import db

jinja_environment = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Message(db.Model):
	message = db.StringProperty()

def create_message(message_text):
	message = Message()
	message.message = message_text
	db.put(message)

def get_message():
	message_key = db.Key.from_path('Message', 'message')
	message = db.get(message_key)
	if message is None:
		return "No message stored yet."
	else:
		return message.message

def get_messages():
	messages = db.Query(Message).run()
	return messages
	# message_string = ''
	# for message in messages:
	# 	message_string = message_string + message.message + '<br><hr>'
	# return message_string	

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	user = users.get_current_user()

    	if user:
    		template_values = {
    			"messages" : get_messages()
    		}

    		template = jinja_environment.get_template('index.html')
    		self.response.write(template.render(template_values))
    		# output = """
    		# <html>
    		# 	<body>
    		# 	    <h1>Hi {0}!</h1>
    		# 		<form action="/guest" method="post">
    		# 	      	<input type="text" name="content">
    		# 	      	<br>
    		# 	      	<input type="submit" value="Submit">
    		# 	    </form>
    		# 	    <br><hr><br>
    		# 	    The current values are: {1}
    		# 	</body>
    		# </html>
    	 # 	"""
    	 # 	self.response.write(output.format(user.email(), get_messages()))
    	else:
    		self.redirect(users.create_login_url(self.request.uri))

class GuestHandler(webapp2.RequestHandler):
	def post(self):
		create_message(cgi.escape(self.request.get('content')))
		self.redirect('/')
		#self.response.write('<html><body>' + cgi.escape(self.request.get('content')) + '</body></html>')

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/guest', GuestHandler)
], debug=True)