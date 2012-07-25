#-*- coding: utf-8 -*-

import os
import random

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
		
class Error404Page(webapp.RequestHandler):
	def get(self):
		number = random.choice('1234')
		template_values = {
					'number' : number
		}
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/static'), 'error404.html')
		self.response.out.write(template.render(path, template_values))		
		
		
		
application = webapp.WSGIApplication(
                                     [
										('/.*', Error404Page)
								     ],
                                     debug=False)

def main():
	run_wsgi_app(application)
	
if __name__ == "__main__":
	main()
