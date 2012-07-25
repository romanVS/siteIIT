#-*- coding: utf-8 -*-

import os
import cgi
import time
import methods
import re 

from datetime import datetime, timedelta
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.api import users
from google.appengine.ext import db

# Форум ##############################################

class ForumPage(webapp.RequestHandler):
	def get(self):
		if (self.request.get('page')):
			pagePost = True

			try:
				page = int(self.request.get('page'))
			except:
				pagePost = False
			if (pagePost):
				greetings = methods.autorization("/forum?page=1")
		
				if users.get_current_user():
					isLogin = True
				else:
					isLogin = False
			
				topicsQuery = db.GqlQuery("SELECT * FROM Topic ORDER BY dateTopic DESC")
				for topic in topicsQuery:
					user = methods.getUserById(topic.idAuthor)
					if (user.loginForum):
						topic.author = user.loginForum
						topic.put()

		
	
				countPages = int(topicsQuery.count()/20)
				if (topicsQuery.count()%20):
					countPages += 1
		
				topicsOnPage = []
				startTopic = page * 20 - 19
				endTopic = startTopic + 19
				count = 1
				for topic in topicsQuery:
					if (count >= startTopic and count <= endTopic):
						topicsOnPage.append(topic)
					count += 1
			
				countPages = int(topicsQuery.count() / 20)
				if (topicsQuery.count() % 20):
					countPages += 1

				visibleAllPages = []
				visibleStartPages = []
				visibleMiddlePages = []
				visibleEndPages = []

				if countPages < 10:
					for count in range(countPages):
						visibleAllPages.append(count + 1)
					visibleStartSeparator = False
					visibleEndSeparator = False

				elif (page < 6):
					if (page < 3):
						for pageForum in range(3):
							visibleStartPages.append(pageForum + 1)
					else:
						for pageForum in range(page + 1):
							visibleStartPages.append(pageForum + 1)
					visibleStartSeparator = False
					visibleEndSeparator = True
					visibleEndPages.append(countPages - 2)
					visibleEndPages.append(countPages - 1)
					visibleEndPages.append(countPages)
			
				elif (page > countPages - 5):
					visibleStartPages.append(1)
					visibleStartPages.append(2)
					visibleStartPages.append(3)
					visibleStartSeparator = True
					visibleEndSeparator = False
					if (page > countPages - 2):
						visibleEndPages.append(countPages - 2)
						visibleEndPages.append(countPages - 1)
						visibleEndPages.append(countPages)
					else:
						visibleEndPages.append(page - 1)
						visibleEndPages.append(page)
						count = page + 1
						while count <= countPages:
							visibleEndPages.append(count)
							count += 1
				else:	
					visibleStartPages.append(1)
					visibleStartPages.append(2)
					visibleStartPages.append(3)
					visibleStartSeparator = True
					visibleMiddlePages.append(page - 1)
					visibleMiddlePages.append(page)
					visibleMiddlePages.append(page + 1)
					visibleEndSeparator = True
					visibleEndPages.append(countPages - 2)
					visibleEndPages.append(countPages - 1)
					visibleEndPages.append(countPages)

				template_values = {
							'isLogin' : isLogin,
		      					'greetings': greetings,
							'topics': topicsOnPage,
							'countPages' : countPages, 
							'visibleAllPages' : visibleAllPages,
							'visibleStartPages' : visibleStartPages,
							'visibleStartSeparator' : visibleStartSeparator,
							'visibleMiddlePages' : visibleMiddlePages,
							'visibleEndPages' : visibleEndPages,
							'visibleEndSeparator' : visibleEndSeparator
		      				   }
		
				path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'forum.html')
				self.response.out.write(template.render(path, template_values))
			else:
				self.redirect('/forum?page=1')
		else:
			self.redirect('/forum?page=1')
#Топик############################################################################################################################
class Topic(db.Model):
	idTopic = db.IntegerProperty()
	author = db.StringProperty(multiline=True)
	idAuthor = db.IntegerProperty()
	nameTopic = db.StringProperty(multiline=True)
	dateTopic = db.StringProperty(multiline=True)

class CreateTopicPage(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			greetings = methods.autorization("/forum?page=1")
			template_values = {
	 					'greetings': greetings
	      				   }
			path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'createtopic.html')
			self.response.out.write(template.render(path, template_values))
		else:
			self.redirect('/forum?page=1')

class CreateTopic(webapp.RequestHandler):
	def post(self):
		if users.get_current_user():

			queryLastTopic = db.Query(Topic)
			queryLastTopic.order("-idTopic")
			lastTopic = queryLastTopic.get()
	    		nameTopicFromPost = re.sub('<[^>]*>', '', self.request.get('nameTopic'))
			if (nameTopicFromPost):
				topic = Topic()
				if lastTopic:		
					topic.idTopic = lastTopic.idTopic + 1
				else:
					topic.idTopic = 1

				topic.author = users.get_current_user().nickname()
				topic.idAuthor = methods.getIdUser(users.get_current_user().nickname())
	    			topic.nameTopic = nameTopicFromPost
				topic.dateTopic = datetime.now().strftime('%d.%m.%y %H:%M')
				messageFromPost = re.sub('<[^>]*>', '', self.request.get('message')).replace('\n','<br />')
				if (messageFromPost):
					message = Message()
					message.idMessage = 1
					message.Row = 1
					message.idTopic = topic.idTopic
					message.author = users.get_current_user().nickname()
					message.idAuthor = methods.getIdUser(users.get_current_user().nickname())
					message.message = messageFromPost
					message.dateMessage = datetime.now().strftime('%d.%m.%y %H:%M')	
			    		
					message.put()
					topic.put()
	
					self.redirect('/topic?idTopic=%s&topicPage=1' % topic.idTopic)
				else:
					self.redirect('/errorCreateTopic')	
			else:
				self.redirect('/errorCreateTopic')

		else:
			self.redirect('/forum?page=1')

class ErrorCreateTopic(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			greetings = methods.autorization("/forum?page=1")
			template_values = {
	 					'greetings': greetings
	      				   }
			path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'errorCreateTopic.html')
			self.response.out.write(template.render(path, template_values))
		else:
			self.redirect('/forum?page=1')
class TopicPage(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			greetings = methods.autorization("/topic?idTopic=1&topicPage=1")

			if (self.request.get('idTopic') and self.request.get('topicPage')):

				idTopic = self.request.get('idTopic')
				topicPagePost = True

				try:				
					topicPage = int(self.request.get('topicPage'))
					topicQuery = db.GqlQuery("SELECT * FROM Topic WHERE idTopic = %s" % idTopic)
				except:
					topicPagePost = False
				
				if topicPagePost:

					topic = topicQuery.get()	
			    		
					user = methods.getUserById(topic.idAuthor)
					if (user.loginForum):
						topic.author = user.loginForum
						topic.put()

					messagesQuery = db.GqlQuery("SELECT * FROM Message WHERE idTopic = %s ORDER BY idMessage" % idTopic)
					if (messagesQuery.count() != 0):

						for message in messagesQuery:
							user = methods.getUserById(message.idAuthor)
							if (user.loginForum):
								message.author = user.loginForum
								message.put()
							if(methods.isUser(users.get_current_user().nickname(), message.idAuthor)):
								message.isAuthor = True
								message.put()
							else:
								message.isAuthor = False
								message.put()
				
					else:
						countPages = 1;

					messagesOnPage = []
					startMessage = topicPage * 20 - 19
					endMessage = startMessage + 19
					count = 1
					for message in messagesQuery:
						if (count >= startMessage and count <= endMessage):
							messagesOnPage.append(message)
						count += 1
			
					countPages = int(messagesQuery.count() / 20)
					if (messagesQuery.count() % 20):
						countPages += 1
		

					visibleAllPages = []
					visibleStartPages = []
					visibleMiddlePages = []
					visibleEndPages = []

					if countPages < 10:
						for count in range(countPages):
							visibleAllPages.append(count + 1)
						visibleStartSeparator = False
						visibleEndSeparator = False
					elif (topicPage < 6):
						if (topicPage < 3):
							for page in range(3):
								visibleStartPages.append(page + 1)
						else:
							for page in range(topicPage + 1):
								visibleStartPages.append(page + 1)
						visibleStartSeparator = False
						visibleEndSeparator = True
						visibleEndPages.append(countPages - 2)
						visibleEndPages.append(countPages - 1)
						visibleEndPages.append(countPages)
			
					elif (topicPage > countPages - 5):
						visibleStartPages.append(1)
						visibleStartPages.append(2)
						visibleStartPages.append(3)
						visibleStartSeparator = True
						visibleEndSeparator = False
						if (topicPage > countPages - 2):
							visibleEndPages.append(countPages - 2)
							visibleEndPages.append(countPages - 1)
							visibleEndPages.appealend(countPages)
						else:
							visibleEndPages.append(topicPage - 1)
							visibleEndPages.append(topicPage)
							count = topicPage + 1
							while count <= countPages:
								visibleEndPages.append(count)
								count += 1
					else:	
						visibleStartPages.append(1)
						visibleStartPages.append(2)
						visibleStartPages.append(3)
						visibleStartSeparator = True
						visibleMiddlePages.append(topicPage - 1)
						visibleMiddlePages.append(topicPage)
						visibleMiddlePages.append(topicPage + 1)
						visibleEndSeparator = True
						visibleEndPages.append(countPages - 2)
						visibleEndPages.append(countPages - 1)
						visibleEndPages.append(countPages)

					admin = methods.isAdmin(users.get_current_user().nickname())
					template_values = {
								'greetings' : greetings,
								'admin' : admin,
			      					'messages': messagesOnPage,
								'topic': topic,
								'visibleAllPages' : visibleAllPages,
								'visibleStartPages' : visibleStartPages,
								'visibleStartSeparator' : visibleStartSeparator,
								'visibleMiddlePages' : visibleMiddlePages,
								'visibleEndPages' : visibleEndPages,
								'visibleEndSeparator' : visibleEndSeparator
							  }

					path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'topic.html')
					self.response.out.write(template.render(path, template_values))

				else:
					self.redirect('/forum?page=1')
			else:
				self.redirect('/forum?page=1')
		else:
			self.redirect('/forum?page=1')

#Сообщение########################################################################################################################
class Message(db.Model):
	Row = db.IntegerProperty()
	idMessage = db.IntegerProperty()
	idTopic = db.IntegerProperty()
	author = db.StringProperty(multiline=True)
	idAuthor = db.IntegerProperty()
	message = db.TextProperty()
	dateMessage = db.StringProperty(multiline=True)
	isAuthor =  db.BooleanProperty()

class AddMessage(webapp.RequestHandler):
	def post(self):
		if users.get_current_user():

			idTopic = self.request.get('idTopic')
			
			queryLastMessage = db.Query(Message)
			queryLastMessage.order("-idMessage")
			lastMessage = queryLastMessage.get()
			
			messagesQuery = db.GqlQuery("SELECT * FROM Message WHERE idTopic=%s" % idTopic)
		
			if(messagesQuery.count() != 0): 
				topicPage = int(messagesQuery.count() / 20)
				if (messagesQuery.count() % 20):
					topicPage += 1
				messageFromPost = re.sub('<[^>]*>', '', self.request.get('message')).replace('\n','<br />')	
				if(messageFromPost):
	
					message = Message()
					message.idMessage = lastMessage.idMessage + 1

					if(lastMessage.Row == 1):
						message.Row = 2
					else:
						message.Row = 1

					message.idTopic = int(idTopic)
					message.author = users.get_current_user().nickname()
					message.idAuthor = methods.getIdUser(users.get_current_user().nickname())
					message.message =  messageFromPost
					message.dateMessage = datetime.now().strftime('%d.%m.%y %H:%M')	
				    	message.put()

			
		    			
					self.redirect('/topic?idTopic=%s&topicPage=%s' % (idTopic, topicPage))
				else:
					self.redirect('/errorAddMessage?idTopic=%s&topicPage=%s' % (idTopic, topicPage))
			else:
				messageFromPost = re.sub('<[^>]*>', '', self.request.get('message')).replace('\n','<br />')
				if(messageFromPost):
					message = Message()
					message.idMessage = 1
					message.Row = 1
					message.idTopic = int(idTopic)
					message.author = users.get_current_user().nickname()
					message.idAuthor = methods.getIdUser(users.get_current_user().nickname())
					message.message = messageFromPost
					message.dateMessage = datetime.now().strftime('%d.%m.%y %H:%M')	
				    		
					message.put()
					self.redirect('/topic?idTopic=%s&topicPage=1' % idTopic)

				else:
					self.redirect('/errorAddMessage?idTopic=%s&topicPage=%s' % (idTopic, topicPage))
		else:
			self.redirect('/error')

class ErrorAddMessage(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():

			idTopic = self.request.get('idTopic')
			topicPage = self.request.get('topicPage')
			greetings = methods.autorization("/forum?page=1")
		
			template_values = {
							'idTopic':idTopic,
		      					'topicPage':topicPage,
							'greetings': greetings
					  }

			path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'errorAddMessage.html')
			self.response.out.write(template.render(path, template_values))
		else:
			self.redirect('/error')

class EditMessage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/editMessage")
		idTopic = self.request.get('idTopic')
		idMessage = self.request.get('idMessage')

		if(idTopic and idMessage):
				messageQuery = db.GqlQuery("SELECT * FROM Message WHERE idTopic=%s AND idMessage=%s" % (idTopic, idMessage))
				for message in messageQuery:
					if(methods.getIdUser(users.get_current_user().nickname()) == message.idAuthor):
						messageText = message.message.replace('<br />','\n')
	
						template_values = {
									'messageText': messageText,
									'idTopic': idTopic,
									'idMessage': idMessage,
									'greetings': greetings
								  }
			
						path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'editMessage.html')
						self.response.out.write(template.render(path, template_values))
					else:
						self.redirect('/error')

class ActionEditMessage(webapp.RequestHandler):
	def post(self):
		idTopic = self.request.get('idTopic')
		idMessage = self.request.get('idMessage')
		messageText = self.request.get('message').replace('\n','</br>')

		if(idTopic and idMessage and messageText):
			messageQuery = db.GqlQuery("SELECT * FROM Message WHERE idTopic=%s AND idMessage=%s" % (idTopic, idMessage))
			for message in messageQuery:
				if(methods.getIdUser(users.get_current_user().nickname()) == message.idAuthor):
					
					message.message = messageText
					message.put()
			
					
					self.redirect('/successEditMessage?idTopic=%s' % idTopic)
				else:
					self.redirect('/error')
		else:	
			self.redirect('/successEditMessage?idTopic=%s' % idTopic)

class ActionDeleteMessage(webapp.RequestHandler):
	def get(self):
		
		idTopic = self.request.get('idTopic')
		idMessage = self.request.get('idMessage')
    		
		if(idTopic and idMessage):
			messageQuery = db.GqlQuery("SELECT * FROM Message WHERE idTopic=%s AND idMessage=%s" % (idTopic, idMessage))
			for message in messageQuery:
				if(methods.getIdUser(users.get_current_user().nickname()) == message.idAuthor):
				
					message.delete()
			
					self.redirect('/successDeleteMessage?idTopic=%s' % idTopic)
				else:
					self.redirect('/error')
		else:
			self.redirect('/error')

class SuccessEditMessage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/successEditMessage")
		idTopic = self.request.get('idTopic')
			
		template_values = {
					'greetings': greetings,
					'idTopic': idTopic
				  }

		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'successEditMessage.html')
		self.response.out.write(template.render(path, template_values))

class SuccessDeleteMessage(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/successDeleteMessage")
		idTopic = self.request.get('idTopic')
			
		template_values = {
					'greetings': greetings,
					'idTopic': idTopic
				  }

		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'successDeleteMessage.html')
		self.response.out.write(template.render(path, template_values))
#####################################################################################################################################
class User(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/forum?page=1")
		idPost = True
		try:
			userById = db.GqlQuery("SELECT * FROM UserForum WHERE idUser = %s" % self.request.get('id'))
		except:
			idPost = False
		if (idPost and userById.count() != 0):
			for userForum in userById:
				loginGoogle = userForum.loginGoogle
				login = userForum.loginForum
				position = userForum.position
				name = userForum.name
				lastName = userForum.lastName
				if users.get_current_user():
					isUser = methods.isUser(users.get_current_user().nickname(), int(self.request.get('id')))
					admin =  methods.isAdmin(users.get_current_user().nickname())
				else:
					self.redirect('/')
			
			template_values = {
						'admin' : admin,
						'isUser': isUser,
						'greetings': greetings,
						'loginGoogle': loginGoogle,
						'login': login,
						'position': position,
						'name': name,
						'lastName': lastName
					  }

			path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'user.html')
			self.response.out.write(template.render(path, template_values))
		else:
			self.redirect('/')

class SaveChanges(webapp.RequestHandler):
	def post(self):
		if users.get_current_user():
			isUser = methods.isUser(users.get_current_user().nickname(), methods.getIdUser(self.request.get('loginGoogle')))
			loginExist = True

			if (isUser):		
				queryLoginExist = db.GqlQuery("SELECT * FROM UserForum ")
				for userForum in queryLoginExist:

					if (userForum.loginForum == self.request.get('login')):
						loginExist = False
				if loginExist:
					query = db.GqlQuery("SELECT * FROM UserForum WHERE idUser = %s" % methods.getIdUser(self.request.get('loginGoogle')))
					for userForum in query:
						idUser = userForum.idUser

						if self.request.get('login'):
							userForum.loginForum = re.sub('<[^>]*>', '',self.request.get('login'))
						else:
							userForum.loginForum = None
			
						if self.request.get('name'):
							userForum.name = re.sub('<[^>]*>', '',self.request.get('name'))
						else:
							userForum.name = None

						if self.request.get('lastName'):
							userForum.lastName = re.sub('<[^>]*>', '',self.request.get('lastName'))
						else:
							userForum.lastName = None

						userForum.put()

					self.redirect('/user?id=%s' % idUser)
				else:
					self.redirect('/errorLoginExist')
			else:
				self.redirect('/')

class ErrorLoginExist(webapp.RequestHandler):
	def get(self):
				
		greetings = methods.autorization("/")
		template_values = {
      					'greetings': greetings
      				   }
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'errorLoginExist.html')
		self.response.out.write(template.render(path, template_values))	
#####################################################################################################################################
class AdminPanel(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/admin")
		if users.get_current_user():
			admin = methods.isAdmin(users.get_current_user().nickname())
			if (admin):
				template_values = {
							'greetings': greetings
						  }

				path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'admin.html')
				self.response.out.write(template.render(path, template_values))
			else:
				self.redirect('/error')
		else:
			self.redirect('/')

class AddAdmin(webapp.RequestHandler):
	def get(self):
		greetings = methods.autorization("/admin")
		error = self.request.get('error')
		userPost  = self.request.get('user')	
		if users.get_current_user():
			admin =  methods.isAdmin(users.get_current_user().nickname())
			if (admin):
				template_values = {
							'userPost':userPost,
							'error':error,
							'greetings': greetings
						  }
		
		
				path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'addAdmin.html')
				self.response.out.write(template.render(path, template_values))
			else:
				self.redirect('/error')
		else:
			self.redirect('/')

class SearchUser(webapp.RequestHandler):
	def post(self):
		if users.get_current_user():
			admin =  methods.isAdmin(users.get_current_user().nickname())
			if (admin):
				login = self.request.get('login')
				loginForum = None
				error = None
				
				query = db.GqlQuery("SELECT * FROM UserForum WHERE loginForum='%s'" % login)
				queryGoogle = db.GqlQuery("SELECT * FROM UserForum WHERE loginGoogle='%s'" % login)
				if (query.count() != 0):
					for user in query:
						loginForum = user.loginForum
						self.redirect('/addAdmin?user=%s' % loginForum)
					
			
				elif (queryGoogle.count() != 0):
					for user in queryGoogle:
						if (user.loginForum != None):
							loginForum = user.loginForum
						else:
							loginForum = user.loginGoogle

						self.redirect('/addAdmin?user=%s' % loginForum)			
				else:
						error = "This user doesn't exist"	
						self.redirect('/addAdmin?error=%s' % error)
						
				
			else:
				self.redirect('/error')
		else:
			self.redirect('/')

class ActionAddAdmin(webapp.RequestHandler):
	def post(self):
		if users.get_current_user():
			admin =  methods.isAdmin(users.get_current_user().nickname())
			if (admin):

				User = methods.getUserById(methods.getIdUser(self.request.get('login')))
		
				if User:
					User.position = "admin"
					User.put()
					self.redirect('/user?id=%s' % methods.getIdUser(self.request.get('login'))) 
		 		
				else:
					User = methods.getUserById(methods.getIdUserForum(self.request.get('login')))
					User.position = "admin"
					User.put()
					self.redirect('/user?id=%s' % methods.getIdUserForum(self.request.get('login')))
			else:
				self.redirect('/error')
		else:
			self.redirect('/')

class New(db.Model):
	idNew = db.IntegerProperty()
	textNew = db.TextProperty()
	dateNew = db.StringProperty(multiline=True)

class NewsPage(webapp.RequestHandler):
	def get(self):
		admin = False
		if users.get_current_user():
			admin =  methods.isAdmin(users.get_current_user().nickname())
				
		query = db.GqlQuery("SELECT * FROM New ORDER by dateNew DESC")
		greetings = methods.autorization("/")
		template_values = {
					'admin': admin,
      					'greetings': greetings,
					'news': query
      				   }
		path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates'), 'news.html')
		self.response.out.write(template.render(path, template_values))	

class AddNews(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			admin =  methods.isAdmin(users.get_current_user().nickname())
			if (admin):
		
				greetings = methods.autorization("/forum?page=1")

				template_values = {
							'greetings': greetings
						  }

				path = os.path.join(os.path.join(os.path.dirname(__file__), 'templates/forum'), 'addNews.html')
				self.response.out.write(template.render(path, template_values))
		else:
			self.redirect('/error')

class ActionAddNews(webapp.RequestHandler):
	def post(self):
		if users.get_current_user():
			admin =  methods.isAdmin(users.get_current_user().nickname())
			if (admin):

				query = db.GqlQuery("SELECT * FROM New")
				queryLastNew = db.Query(New)
				queryLastNew.order("-idNew")
				lastNew = queryLastNew.get()

				new = New()

				if (query.count() == 0):
					new.idNew = 1		
				else:
					new.idNew = lastNew.idNew + 1
		
				new.textNew = self.request.get('textNew').replace('\n','</br>')
				new.dateNew = datetime.now().strftime('%d.%m.%y %H:%M')	
				new.put()

				self.redirect('/')
		else:
			self.redirect('/error')

class ActionDeleteNews(webapp.RequestHandler):
	def get(self):
		if users.get_current_user():
			admin =  methods.isAdmin(users.get_current_user().nickname())
			if (admin):
				idNew = self.request.get('idNew')
				query = db.GqlQuery("SELECT * FROM New WHERE idNew = %s" % idNew)
				for new in query:
					new.delete()
				self.redirect('/')

		else:
			self.redirect('/error')

#########################################################
		
application = webapp.WSGIApplication(
                                     [							('/', NewsPage),
											('/forum', ForumPage),
											('/createTopic', CreateTopicPage),
											('/actionCreateTopic', CreateTopic),
											('/topic', TopicPage),
											('/addMessage', AddMessage),
											('/editMessage', EditMessage),
											('/successEditMessage', SuccessEditMessage),
											('/actionEditMessage', ActionEditMessage),
											('/actionDeleteMessage', ActionDeleteMessage),
											('/successDeleteMessage', SuccessDeleteMessage),
											('/errorCreateTopic', ErrorCreateTopic),	
											('/errorAddMessage', ErrorAddMessage),
											('/user', User),
											('/saveChanges', SaveChanges),
											('/addNews', AddNews),
											('/actionAddNews', ActionAddNews),
											('/actionDeleteNews', ActionDeleteNews),
											('/admin', AdminPanel),
											('/addAdmin', AddAdmin),
											('/searchUser', SearchUser),
											('/actionAddAdmin', ActionAddAdmin),
											('/errorLoginExist', ErrorLoginExist)
								     ],
                                     debug=True)

def main():
	run_wsgi_app(application)
	
if __name__ == "__main__":
	main()
