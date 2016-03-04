import pymongo,string, re,json
from bottle import redirect,template
from datetime import datetime
from bson.objectid import ObjectId
import doUser

connection_string = "mongodb://localhost" 
connection = pymongo.MongoClient(connection_string)
dbs = connection.projek
#--------------------------------[CONTROLLER]-------------------------------------#
controllerUser = doUser.userClass(dbs)
#-----------------------------------------------------------------------------------------#
class memberClass(object):
	def __init__(self, database):
		self.db = database
		self.timeline = database.timeline

	def selectdataTimeline(self,username,status):
		query = self.timeline.find({'username1':username, "status" : status})
		result = list(query)
		if result:
			return result
		else:
			return 0
			
	def selectalldataTimeline(self,status):
		query = self.timeline.find({ "status" : status})
		result = list(query)
		if result:
			return result
		else:
			return 0
	
	def checkarticle(self,title,type):
		l=[]
		query = self.timeline.find({'Article_title' : title,'typePost' : type})
		result = list(query)
		if result:
			user_image = controllerUser.checkStatus(result[0]['username1'])
			l.append({'_id':result[0]['_id'],'username1':result[0]['username1'],'Article_title':result[0]['Article_title'],'datepost':result[0]['datepost'],'username2':result[0]['username2'],'Post_content':result[0]['Post_content'],'images':result[0]['images'],'status':result[0]['status'],'typePost':result[0]['typePost'],'photoauthor':user_image[0]['images']})
			return l
		else:
			return 0

	def checktimeline(self,id):
		l=[]
		query = self.timeline.find({'_id' : ObjectId(id)})
		result = list(query)
		if result:
			user_image = controllerUser.checkStatus(result[0]['username1'])
			l.append({'_id':result[0]['_id'],'username1':result[0]['username1'],'Article_title':result[0]['Article_title'],'datepost':result[0]['datepost'],'username2':result[0]['username2'],'Post_content':result[0]['Post_content'],'images':result[0]['images'],'status':result[0]['status'],'typePost':result[0]['typePost'],'photoauthor':user_image[0]['images']})
			return l
		else:
			return 0

	def updateuser(self,id,username2,type):#jika ada user yang komen
		query = self.timeline.update({"_id" : ObjectId(id) ,"typePost" : type },  { "$addToSet" : { "username2" :  username2 }})
		result = list(query)
		if result:
			return result
		else:
			return 0

	def insertPosting(self,post_content,username,nameimages,typepost,article):
		datepost = datetime.now().strftime('%d-%m-%Y')
		status = "Active"
		self.timeline.save({'username1':username, 'username2':[], 'datepost':datepost, 'typePost':typepost, 'Article_title':article, 'Post_content':post_content, 'images':nameimages, 'status':status})