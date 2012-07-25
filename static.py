#-*- coding: utf-8 -*-

import os
import methods

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class CathedraPage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/cathedra")
			
		template_values = {
      					'greetings': greetings,
      				   }
		
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/static'), 'cathedra.html')
		self.response.out.write(template.render(path, template_values))	

class ContestPage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/contest")
		template_values = {
      					'greetings': greetings,
      				   }
		
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/static'), 'contest.html')
		self.response.out.write(template.render(path, template_values))	
		
class GamesPage(webapp.RequestHandler):
	def get(self, number):		
		greetings = methods.autorization("/games%s" % number)
		template_values = {
      					'greetings': greetings,
      				   }
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/games'), 'games%s.html' % number)
		self.response.out.write(template.render(path, template_values))
		
class ShedulePage(webapp.RequestHandler):
	def get(self, number):
		greetings = methods.autorization("/shedule%s" % number) 
		template_values = {
      					'greetings': greetings,
      				   }
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/shedule'), 'shedule%s.html' % number) 
		self.response.out.write(template.render(path, template_values))
		
class SearchPage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/search")
		template_values = {
      					'greetings': greetings,
      				   }
		
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/static'), 'search.html')
		self.response.out.write(template.render(path, template_values))		
		
class AboutPage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/about")
		template_values = {
      					'greetings': greetings,
      				   }
		
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/static'), 'about.html')
		self.response.out.write(template.render(path, template_values))
		
class SitemapPage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/sitemap")
		template_values = {
      					'greetings': greetings,
      				   }
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/static'), 'sitemap.html')
		self.response.out.write(template.render(path, template_values))	
		
class ForGoogle(webapp.RequestHandler):
	def get(self):
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/static'),'google8133ff8d2631c81f.html')
		self.response.out.write(template.render(path, None))
		
application = webapp.WSGIApplication(
                                     [
										('/cathedra', CathedraPage),
										('/contest', ContestPage),
										('/games(1||2)', GamesPage),
										('/shedule(1||2||3||4)', ShedulePage),
										('/about', AboutPage),
										('/sitemap', SitemapPage),
										('/search', SearchPage),
										('/google8133ff8d2631c81f.html',ForGoogle),
								     ],
                                     debug=False)

def main():
	run_wsgi_app(application)
	
if __name__ == "__main__":
	main()
