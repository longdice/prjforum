import string

class uploadClientClass(object):
	def __init__(self, database):
		self.db = database
		self.projectClient = database.projectClient
		
	def summTotProjectbyClient(self,username):
		query = self.projectClient.find({'username1':username}).count()
		if query==0:
			return 0
		else:
			return query
			
	def summTotProjectbyMember(self,username):
		query = self.projectClient.find({'username2':username}).count()
		if query==0:
			return 0
		else:
			return query
			
	def showUnTake(self):
		l=[]
		for each_name in self.projectClient.find({'username2':'NULL'}):
			l.append({'_id':each_name['_id'],'idProject':each_name['idProject'], 'ProjectName':each_name['ProjectName'], 'ContactPerson':each_name['ContactPerson'], 'ProjectFee':each_name['ProjectFee'], 'Deadline':each_name['Deadline']})
		return l
		
	def showTake(self,username2):
		l=[]
		for each_name in self.projectClient.find({'username2':username2}):
			l.append({'idProject':each_name['idProject'], 'ProjectName':each_name['ProjectName'],'Deadline':each_name['Deadline']})
		return l
	
	def takeProject(self,idProject,username2):
		query = self.projectClient.update({'idProject':idProject}, {'$set':{'username2':username2,'Status':'TAKE'}})
		if query:
			return 1
			
	def findIDProject(self,idProject):
		query = self.projectClient.find({'idProject':idProject})
		RESULT=list(query)
		if RESULT:
			return 1
		else:
			return 0
	
	def deleteProject(self,idProject):
		query = self.projectClient.remove({'idProject':idProject})
		if query:
			return 1
		else:
			return 0
			
	def selectProject(self,username):
		query = self.projectClient.find({'username1':username})
		RESULT=list(query)
		if RESULT:
			return RESULT
		else:
			return 0
	
	def memberUploadProject(self,idProject,username,jwbanprojek):
		query = self.projectClient.update({'idProject':idProject}, {'$set':{'namefileproject':jwbanprojek}})
		if query:
			return 1
		else:
			return 0
	
	def selectProjectSolved(self,username):
		query = self.projectClient.find({"Status" : "TAKE","username1" : username})
		RESULT=list(query)
		if RESULT:
			return RESULT
		else:
			return 0

	def acceptProject(self,idProject):
		query = self.projectClient.update({'idProject':idProject}, {'$set':{'DeclineStatus':"Approved"}})
		if query:
			return 1
		else:
			return 0

	def declineProject(self,idProject):
		query = self.projectClient.update({'idProject':idProject}, {'$set':{'DeclineStatus':"Decline"}})
		if query:
			return 1
		else:
			return 0
			
	def insertProject(self,ContactPerson, ProjectName, ProjectFee, Deadline, idProject, username1, username2="NULL"):
		self.projectClient.save({'ContactPerson':ContactPerson, 'ProjectName':ProjectName, 'ProjectFee':ProjectFee, 'Deadline':Deadline, 'idProject':idProject, 'username1':username1, 'username2':username2,'Approvaladmin':'','Status':'UNTAKE','DeclineStatus':'','namefileproject':''})