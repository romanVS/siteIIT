#-*- coding: utf-8 -*
from google.appengine.api import users
from google.appengine.ext import db

class UserForum(db.Model):
	idUser = db.IntegerProperty()
	loginGoogle = db.StringProperty(multiline=True)
	loginForum = db.StringProperty(multiline=True)
	position = db.StringProperty(multiline=True)
	name = db.StringProperty(multiline=True)
	lastName = db.StringProperty(multiline=True)

def getIdUser(googleName):
	usersForum = db.GqlQuery("SELECT * FROM UserForum")
	for tmp_user in usersForum:
		if (tmp_user.loginGoogle == googleName):
			return tmp_user.idUser

def getIdUserForum(loginForum):
	usersForum = db.GqlQuery("SELECT * FROM UserForum")
	for tmp_user in usersForum:
		if (tmp_user.loginForum == loginForum):
			return tmp_user.idUser

def getUserById(idUser):
	usersForum = db.GqlQuery("SELECT * FROM UserForum")
	for tmp_user in usersForum:
		if (tmp_user.idUser == idUser):
			return tmp_user

def isAdmin(googleName):
	usersForum = db.GqlQuery("SELECT * FROM UserForum")
	for tmp_user in usersForum:
		if (tmp_user.loginGoogle == googleName and tmp_user.position == "admin"):
			return True
	return False

def isUser(googleName,idUser):
	usersForum = db.GqlQuery("SELECT * FROM UserForum")
	for tmp_user in usersForum:
		if (tmp_user.loginGoogle == googleName and tmp_user.idUser == idUser):
			return True
	return False
	
def autorization(path):
		greetings = ""
		
		if users.get_current_user():
			
			isUser = False
			usersForum = db.GqlQuery("SELECT * FROM UserForum")
			userForum = UserForum()
			
			for tmp_user in usersForum:
				if (tmp_user.loginGoogle == users.get_current_user().nickname()):
					isUser = True
			if (isUser == False):
				if (usersForum):
					userForum.idUser = usersForum.count() + 1	
				else:
					userForum.idUser = 1
				userForum.loginGoogle = users.get_current_user().nickname()
				userForum.loginForum = None
				userForum.position = 'user'
				userForum.name = None
				userForum.lastName = None	
				userForum.put()
			
			idUser = getIdUser(users.get_current_user().nickname())
			greetings += ("<a href='/user?id=%s'> %s</a>&nbsp;&nbsp;&nbsp;<a href=\"%s\">выйти</a>" 
			% (idUser, users.get_current_user().nickname(), users.create_logout_url(path)))
				
		else:
			greetings += ("<a href=\"%s\">Войти на сайт" % users.create_login_url(path))
			
		return greetings








