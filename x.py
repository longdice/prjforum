import pymongo, os, datetime
import json
from pymongo import MongoClient
from bottle import route, static_file, template, run, debug, request, redirect ,response
from datetime import datetime
from json import dumps
###########[Library sendiri]######
import doUser, doUploadClient , doMember, doForum, doComment
##################################

####### START Database ##############################
connection_string = "mongodb://localhost" 
connection = pymongo.MongoClient(connection_string)
database = connection.projek
#####################################################

#### START controller ##########################
controllerUser = doUser.userClass(database)
controlleruploadclient = doUploadClient.uploadClientClass(database)
controllerMember = doMember.memberClass(database)
controllerForum = doForum.forumClass(database)
controllerComment = doComment.commentClass(database)
#### END Controller ############################
#http://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_pyMongo_tutorial_installing.php
'''
http://www.gtsystem.eu/blog/2011/11/bottle-decorator-for-validate-query-parameters/
http://blog.mongolab.com/2013/04/thinking-about-arrays-in-mongodb/
db.forum.update({"_id" : ObjectId("56d033431cce9e1f20d4220b"),},{})

db.user.update({ "_id" : ObjectId("56cfecc51cce9e1a1c2e33fc")  },{ "Set" : { "username" :  "admin" ,"password":"admin123"}  })

komen
-----------
id 
timelineid
userid
komenat

timeline
----------
id
komenid []
auhor


'''


FirstName = "Irene"
LastName = "Safitri"
Username = "admin"
Email = "adminhacker@gmail.com"
Password ="admin123"
Phone = "086753422422"
typeuser = "admin"
resultSaveUser = controllerUser.insertUser(FirstName, LastName, Username, Email, Password, Phone, typeuser)
def get_db():
    client = MongoClient('localhost:27017')
    db = client.projek
    return db
'''
def find(db):
	id = str('56d033431cce9e1f20d4220b')
    q = db.forum.find({'_id' : ObjectId(id)})
	return q'''

def update_post(db):
	db.forum.update({"_id" : ObjectId("56d0bcc51cce9e49b8e9f148")},  { "$addToSet" : { "username2" :  "claudea" }})

def get_forum(db):
    return db.forum.find_one()
'''
if __name__ == "__main__":
	resultSaveUser = controllerUser.insertUser(FirstName, LastName, Username, Email, Password, Phone, typeuser)
    #db = get_db() 
    #add_post(db)
	#update_post(db)
    print "oke"#find(db)
'''	