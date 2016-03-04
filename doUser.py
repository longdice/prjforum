import string, re, json
from bottle import redirect,template
from datetime import datetime
from bson.objectid import ObjectId

class userClass(object):
	def __init__(self, database):
		self.db = database
		self.user = database.user
		
	def checkLogin(self, username, password):
		query = self.user.find({'username':username, 'password':password})
		RESULT = list(query)
		if RESULT:
			return RESULT
		else:
			return 0
		
	def checkStatus(self,username):
		query = self.user.find({'username':username})
		RESULT = list(query)
		if RESULT:
			return RESULT
		
	def eqPassword(self,password,confPassword):
		if password!=confPassword:
			return 1
		else:
			return 0
	
	def checkUsername(self,username):
		query = self.user.find({'username':username})
		RESULT = list(query)
		if RESULT:
			return 1
		else:
			return 0

	def checkEmail(self,email):
		query = self.user.find({'email':email})
		RESULT = list(query)
		if RESULT:
			return 1
		else:
			return 0
			
	def insertUser(self, FirstName, LastName, Username, Email, Password, Phone, TypeUser):
		#dateRegister = datetime.now().strftime('%d-%m-%Y %H:%M:%S.%f')
		dateRegister = datetime.utcnow()
		images = ''
		query = self.user.save({'firstname':FirstName,'lastname':LastName,'username':Username,'email':Email,'password':Password,'phone':Phone,'images':images,'typeuser':TypeUser,'dateregister':dateRegister})
		if query:
			return 1
		else:
			return 0
	
	#member edit Images
	def editImages(self,ID,nameimages):
		RESULT = self.user.update({'_id': ObjectId(ID)},{'$set': {   'images': nameimages  }}, upsert=False, multi=False)
		if RESULT:
			return RESULT
		else:
			return 0
			
	#member edit Name
	def editName(self,ID,fistname,lastname):
		print "----------------------------------\n"
		RESULT = self.user.update({'_id': ObjectId(ID)},{'$set': {   'firstname': fistname, 'lastname' : lastname }}, upsert=False, multi=False)
		if RESULT:
			return RESULT
		else:
			return 0
			
	#member edit Email
	def editEmail(self,ID,newemail):
		RESULT = self.user.update({'_id': ObjectId(ID)},{'$set': {   'email': newemail  }}, upsert=False, multi=False)
		if RESULT:
			return RESULT
		else:
			return 0
			
	#member edit Password
	def editPassword(self,ID,newpassword):
		RESULT = self.user.update({'_id': ObjectId(ID)},{'$set': {   'password': newpassword  }}, upsert=False, multi=False)
		if RESULT:
			return RESULT
		else:
			return 0
			
	#member edit Phone
	def editPhone(self,ID,phonenumber):
		RESULT = self.user.update({'_id': ObjectId(ID)},{'$set': {   'phone': phonenumber  }}, upsert=False, multi=False)
		if RESULT:
			return RESULT
		else:
			return 0