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
class forumClass(object):
	def __init__(self, database):
		self.db = database
		self.forum = database.forum
	
	def selectForum(self,typepost):
		l=[]
		user_image = []
		imagepersonal = []
		for each_name in self.forum.find({"typepost" : typepost}):
			user_image = controllerUser.checkStatus(each_name['username1'])
			for each_nameimage in user_image:
				l.append({'_id':each_name['_id'],'username1':each_name['username1'], 'username2':each_name['username2'], 'datepost':each_name['datepost'], 'typepost':each_name['typepost'], 'forum_tittle':each_name['forum_tittle'],'forum_content':each_name['forum_content'],'imagepersonal':each_nameimage['images']})
			#l.append({'_id':each_name['_id'],'username1':each_name['username1'], 'username2':each_name['username2'], 'datepost':each_name['datepost'], 'typepost':each_name['typepost'], 'forum_tittle':each_name['forum_tittle'],'forum_content':each_name['forum_content']})
		return l

	def updateuser(self,id,username2,type):#jika ada user yang komen
		query = self.forum.update({"_id" : ObjectId(id) ,"typepost" : type },  { "$addToSet" : { "username2" :  username2 }})
		result = list(query)
		if result:
			return result
		else:
			return 0

	def countcomment(self,id):#jika ada user yang komen
		query = self.forum.find({"_id" : ObjectId("56d042c41cce9e1b9c257fcb")}).count()
		result = list(query)
		if result:
			return result
		else:
			return 0
			
	def checkDataForum(self,title,type):
		l=[]
		query = self.forum.find({'forum_tittle' : title,'typepost' : type})
		result = list(query)
		if result:
			user_image = controllerUser.checkStatus(result[0]['username1'])
			l.append({'_id':result[0]['_id'],'username1':result[0]['username1'],'username2':result[0]['username2'],'forum_content':result[0]['forum_content'],'forum_tittle':result[0]['forum_tittle'],'datepost':result[0]['datepost'],'typepost':result[0]['typepost'],'photoauthor':user_image[0]['images']})
			return l
		else:
			return 0

	def createForum(self,title,description,username,typeforum):
		datepost = datetime.now().strftime('%d-%m-%Y')
		query = self.forum.save({'username1':username,'username2':[],'datepost':datepost,'typepost':typeforum,'forum_tittle':title,'forum_content':description})
		if query:
			return query
		else:
			return 0