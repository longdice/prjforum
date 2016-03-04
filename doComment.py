import pymongo,string, re,json
from bottle import redirect,template
from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient
import doUser

connection_string = "mongodb://localhost" 
connection = pymongo.MongoClient(connection_string)
dbs = connection.projek
#--------------------------------[CONTROLLER]-------------------------------------#
controllerUser = doUser.userClass(dbs)
#-----------------------------------------------------------------------------------------#
class commentClass(object):
	def __init__(self, database):
		self.db = database
		self.comment = database.comment
		
	def countCommentbyforum(self, forumid):
		query = self.comment.find({'objectID_forum':forumid}).count()
		if query:
			return query
		else:
			0

	def selectCommentbyforum(self, forumid):
		l=[]
		user_image = []
		imagepersonal = []
		for each_name in self.comment.find({'objectID_forum' : ObjectId(forumid)}):
			user_image = controllerUser.checkStatus(each_name['username2'])
			for each_nameimage in user_image:
				l.append({'_id':each_name['_id'],'username1':each_name['username1'], 'username2':each_name['username2'], 'comment_date':each_name['comment_date'], 'type_comment':each_name['type_comment'], 'comment_content':each_name['comment_content'],'objectID_timeline':each_name['objectID_timeline'],'imagepersonal':each_nameimage['images']})
		return l
		
	def postComment(self, forumid, username1, username2, reply, type):
		datepost = datetime.now().strftime('%d-%m-%Y')
		query = self.comment.save({'objectID_forum' : ObjectId(forumid),'objectID_timeline' : '','username1' : username1,'username2':username2,'comment_content':reply,'comment_date':datepost,'type_comment':type})
		if query:
			return 1
		else:
			return 0