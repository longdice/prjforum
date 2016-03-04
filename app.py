import pymongo, os, datetime,time
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


######## Memasukkan BOOTSRAP ####################
@route('/css/app/<filename>')
def js_static(filename):
	return static_file(filename, root='./css/app/')

@route('/css/fonts/<filename>')
def js_static(filename):
	return static_file(filename, root='./css/fonts/')

@route('/js/vendor/maps/google/jquery-ui-map/addons/<filename>')
def js_static(filename):
	return static_file(filename, root='./js/vendor/maps/google/jquery-ui-map/addons/')

@route('/js/vendor/maps/google/jquery-ui-map/ui/<filename>')
def js_static(filename):
	return static_file(filename, root='./js/vendor/maps/google/jquery-ui-map/ui/')

@route('/css/vendor/<filename>')
def js_static(filename):
	return static_file(filename, root='./css/vendor/')
	
@route('/js/vendor/<filename>')
def js_static(filename):
	return static_file(filename, root='./js/vendor/')
	
@route('/js/app/<filename>')
def js_static(filename):
	return static_file(filename, root='./js/app/')

@route('/temp/<filename>')
def js_static(filename):
	return static_file(filename, root='./temp/')
	
@route('/images/people/<filename>')
def js_static(filename):
	return static_file(filename, root='./images/people/')

@route('/images/people/110/<filename>')
def js_static(filename):
	return static_file(filename, root='./images/people/110/')	

@route('/images/timeline/<filename>')
def js_static(filename):
	return static_file(filename, root='./images/timeline/')
################################################

######## START VIEW #########
def checkLogin():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	RESULT = controllerUser.checkStatus(datacookies)	
	return RESULT

@route('/')
def index():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		if TYPE == 'member':
			RESULT2 = controllerMember.selectdataTimeline(username,"Active") #ambil data timeline
			return template('home-member',STATUS=0,type=TYPE,name=FULLNAME,dataposting=RESULT2,images= IMAGE)
		if TYPE == 'client':
			return template('home-client',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
		if TYPE == 'admin':
			return template('home-admin',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return template('index',dict(ERR=RESULT))

@route('/loginProses', method =["POST" , "GET"])
def login():
	username = request.forms.get('username')
	password = request.forms.get('password')
	
	RESULT = controllerUser.checkLogin(username, password)
	if request.method == 'POST':
		if RESULT == 0:
			return template('index',dict(ERR=RESULT))
		else:
			TYPE = RESULT[0]['typeuser']
			FISTNAME = RESULT[0]['firstname']
			LASTNAME = RESULT[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			response.set_cookie("cookiesuser", username, secret='test123',expires=(int(time.time()) + 3600))
			if TYPE == "member": 
				return redirect('/homemember')
			if TYPE == "client":
				return redirect('/clienthome')
			if TYPE == "admin":
				return redirect('/adminhome')
	else:
		return redirect('/')

@route('/registerClient', method='POST')
def registerClient():
	RESULT = 1
	temp_user = ""
	temp_pass = ""
	FirstName = request.forms.get('txtName')
	LastName = request.forms.get('txtLastname')
	Username= request.forms.get('txtUsername')
	Email = request.forms.get('txtEmail')
	Password = request.forms.get('txtPassword')
	ReTypePass = request.forms.get('txtRetypePassword')
	Phone = request.forms.get('txtPhoneNumber')
	Agree = str(request.forms.get('txtAgree'))
	typeuser = request.forms.get('txtTypeUser')
	
	resultPassword = controllerUser.eqPassword(Password,ReTypePass)
	resultSameUsername = controllerUser.checkUsername(Username)
	
	if resultPassword==1 or resultSameUsername==1:
		return template('registerClient',dict(ERR=1))
	else:
		resultSaveUser = controllerUser.insertUser(FirstName, LastName, Username, Email, Password, Phone, typeuser)
		#resultSaveUser = 1 #mode debug
		if resultSaveUser==1:
			if typeuser == "client":
				redirect('/homemember')
			else:
				return template("signUpHacker",temp_user=Username,temp_pass=Password)
		else:
			return redirect("/registerClient")     #gagal save
		
@route('/Securityquestion' ,method =["GET"])
def Securityquestion():
	data_temp= ""
	return template('signUpHacker',data_temp)
#bagian home admin
@route('/adminhome')
def adminhome():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		return template('home-admin',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return redirect('/')

@route('/manageclient')
def manageclient():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		return template('manageclient',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return redirect('/')
@route('/manageproject')
def manageproject():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		return template('manageproject',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return redirect('/')

@route('/managetimeline')
def managetimeline():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		return template('managetimeline',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return redirect('/')

@route('/manageforumgeneral')
def manageforumgeneral():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		return template('managegeneral',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return redirect('/')

@route('/manageforumdefence')
def manageforumdefence():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		return template('manageforumdefence',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return redirect('/')

@route('/manageforumzeroday')
def manageforumdefence():
	RESULT = 1
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	TYPE = ''
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)
		TYPE = RESULT[0]['typeuser']
		username = str(RESULT[0]['username'])
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		return template('manageforumzeroday',STATUS=0,name=FULLNAME,type=TYPE,images= IMAGE)
	else:
		return redirect('/')
#----------------------------------------------------------------------------------------------------------------------------------------------------
#bagian home client 
@route('/clienthome')
def clientRegitration():
	status = ''
	status = checkLogin()
	if str(status) == 'None':
		redirect('/')
	else:
		username = str(status[0]['username'])
		typeuser = str(status[0]['typeuser'])
		FISTNAME = status[0]['firstname']
		LASTNAME = status[0]['lastname']
		IMAGE = status[0]['images']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)			
		return template('home-client',STATUS=0,name=FULLNAME,type=typeuser,images= IMAGE)	

@route('/clientdownload')
def clientdownload():
	status = ''
	status = checkLogin()
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if str(status) == 'None':
		redirect('/')
	else:
		username = str(status[0]['username'])
		typeuser = str(status[0]['typeuser'])
		FISTNAME = status[0]['firstname']
		LASTNAME = status[0]['lastname']
		IMAGE = status[0]['images']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)		
		RESULT = controlleruploadclient.selectProjectSolved(username)  #ambil data user
		'''print "-------------------------------------\n"
		print RESULT
		print "-------------------------------------\n"'''
		#TYPE = "member"
		return template('downloadClient',STATUS = 0,name=FULLNAME,type=typeuser,dataproject=RESULT,images= IMAGE)

@route('/EditProfileClient' ,method =["POST" , "GET"])
def EditProfileClient():
	ERR = ''
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "client"
		ID = RESULT[0]['_id']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		EMAIL = RESULT[0]['email']
		PHONE = RESULT[0]['phone']
		PASSWORD = RESULT[0]['password']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		print "-------------------------------------------------\n"
		if request.method == 'POST':
			type = request.forms.get('type')
			
			if type== "uploadimage": #jika uploadimage
				path = request.forms.get('path')
				upload = request.files.get('upload')
				if upload:
					name, ext = os.path.splitext(upload.raw_filename)
					if ext not in ('.jpeg','.png','.jpg'):
						return template('editprofile-client',STATUS = 'File extension not allowed.',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
					else:
						nameimages = upload.raw_filename
						upload.raw_filename = nameimages
						upload.save(path)
						controllerUser.editImages(ID,nameimages)
						return redirect('/EditProfileMember')
				else:
					return template('editprofile-client',STATUS = 'Images must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
			
			if type == "editname": #jika editname
				fistname = request.forms.get('fistname')
				lastname = request.forms.get('lastname')
				if fistname == '' or lastname =='':
					return template('editprofile-client',STATUS = 'Name must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					controllerUser.editName(ID,fistname,lastname)
					return template('editprofile-client',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)

			if type == "editemail": #jika editemail
				newemail = request.forms.get('newemail')
				if newemail == '':
					return template('editprofile-client',STATUS = 'Email must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					controllerUser.editEmail(ID,newemail)
					return template('editprofile-client',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)

			if type == "editpassword": #jika editpassword
				oldpassword = request.forms.get('oldpassword')
				newpassword = request.forms.get('newpassword')
				renewpassword = request.forms.get('renewpassword')
				
				if oldpassword == '' or newpassword =='' or renewpassword == '':
					return template('editprofile-client',STATUS = 'Password must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					if eqPassword(newpassword,renewpassword) == 1:
						return template('editprofile-client',STATUS = 'Renew password must be same with New Password',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
					else:
						controllerUser.editPassword(ID,newpassword)
					return template('editprofile-client',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
			
			if type == "editphone": #jika editphone
				phonenumber = request.forms.get('phonenumber')
				if phonenumber == '':
					return template('editprofile-client',STATUS = 'Phone must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					controllerUser.editPhone(ID,phonenumber)
					return template('editprofile-client',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
			#print type
		else:
			return template('editprofile-client',STATUS = ERR,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')
 
@route('/deleteproject' ,method =["POST"])
def deleteproject():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		if request.method == 'POST':
			idProject = request.forms.get('idProject')
			controlleruploadclient.deleteProject(idProject) 
			os.remove("temp/"+idProject)
			redirect('/clientdownload')
		else:
			redirect('/clientdownload')
	else:
		redirect('/')

@route('/declineproject' ,method =["POST"])
def declineproject():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		if request.method == 'POST':
			idProject = request.forms.get('idProject')
			controlleruploadclient.declineProject(idProject) 
			redirect('/clientdownload')
		else:
			redirect('/clientdownload')
	else:
		redirect('/')

@route('/acceptproject',method =["POST"])
def acceptproject():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		if request.method == 'POST':
			idProject = request.forms.get('idProject')
			controlleruploadclient.acceptProject(idProject) 
			redirect('/clientdownload')
		else:
			redirect('/clientdownload')
	else:
		redirect('/')

@route('/UploadProjectClient' ,method =["POST" , "GET"])
def uploadProjectClient():
	error = ""
	if request.method == 'POST':
		ContactPerson = request.forms.get('ContactPerson')
		ProjectName = request.forms.get('ProjectName')
		ProjectFee = request.forms.get('ProjectFee')
		Deadline= request.forms.get('day') + '/' + request.forms.get('month') + '/' + request.forms.get('year')
		upload = request.files.get('upload')
		path = request.forms.get('hide')
		username = request.get_cookie("cookiesuser", secret='test123')
		RESULT = controllerUser.checkStatus(username)
		TYPE = str(RESULT[0]['typeuser'])
		IMAGE = RESULT[0]['images']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		
		jumlahProjek = controlleruploadclient.summTotProjectbyClient(username)
		jumlahProjek = jumlahProjek + 1
		idProject = username + str(jumlahProjek)
					
		name, ext = os.path.splitext(upload.raw_filename)
		
		if ext not in ('.doc','.pdf','.jpeg','.png','.jpg'):
			return template('home-client',STATUS=2, name=FULLNAME, type=TYPE)
		else:
			idProject =  idProject + ext
			print "-----------------------------------------------------------------------------------------------\n"
			print idProject
			upload.raw_filename = idProject
			upload.save(path)
			controlleruploadclient.insertProject(ContactPerson, ProjectName, ProjectFee, Deadline, idProject, username)
			return template('home-client',STATUS=1, name=FULLNAME,type=TYPE,images= IMAGE)	
	else:	
		redirect('/clienthome')

@route('/timelinecontent')
def timelinecontent():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		id = request.GET.get("id")
		if str(id) == "":
			return redirect('/homemember')
		else:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			timelineid = request.forms.get("timelineid")
			if request.method == 'POST':
				return "post"
			else:
				resdatakonten = controllerMember.checktimeline(id)
				if resdatakonten == 0:
					return redirect('/homemember')
				else:
					timelineid = resdatakonten[0]['_id']
					resdatakomen = controllerComment.selectCommentbyforum(timelineid)#sohai
					return template('timelinecontent',type=TYPE,name=FULLNAME,images=IMAGE,resdatakonten=resdatakonten,resdatakomen=resdatakomen,error=0)
	else:
		return redirect('/')

@route('/postreplytimeline' ,method =["POST" , "GET"])
def postreplytimeline():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		if request.method == 'POST':
			reply = request.forms.get("reply")
			id = request.forms.get("timelineid")
			type = request.forms.get("type")
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			timelineid = request.forms.get("timelineid")

			resdatakonten = controllerMember.checktimeline(id)
			if str(reply) == "":
				if resdatakonten == 0:
					return redirect('/')
				else:
					timelineid = resdatakonten[0]['_id']
					resdatakomen = controllerComment.selectCommentbyforum(timelineid)#sohai
				return template('articlecontent',type=TYPE,name=FULLNAME,images=IMAGE,resdatakonten=resdatakonten,resdatakomen=resdatakomen,error='Reply mustbe filled')
			else:
				timelineid = request.forms.get("timelineid")
				username1 = request.forms.get("username1")
				username2 = USERNAME
				type = request.forms.get("type")
				resdatakonten = controllerComment.postComment(timelineid,username1,username2,reply,type)
				resupdate = controllerMember.updateuser(timelineid,username2,type)
				print resupdate
				url = '/timelinecontent?id='+str(timelineid)
				redirect(url)
		else:
			return redirect('/')
	else:
		return redirect('/')

#------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#bagian home-member
@route('/homemember')
def homemember():
	ERR = 0
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)		
		RESULT2 = controllerMember.selectalldataTimeline("Active") #ambil data timeline
		print "------------------------------------------------"
		return template('home-member',STATUS = ERR,type=TYPE,name=FULLNAME,images=IMAGE,dataposting=RESULT2)
	else:
		return redirect('/')

@route('/updatestatus' ,method =["POST" , "GET"])
def updatestatus():
	ERR = 0
	if request.method == 'POST':
		datacookies = request.get_cookie("cookiesuser", secret='test123')
		RESULT = controllerUser.checkStatus(datacookies)
		nameimages = ''
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)	
		RESULT2 = controllerMember.selectdataTimeline(USERNAME,"Active") #ambil data timeline
		
		post_content = request.forms.get('message')
		path = request.forms.get('hide')
		upload = request.files.get('upload')
		location = request.forms.get('location')
		
		if post_content: #JIKA POST NYA GK KOSONG
			if upload:   #JIKA UPLOAD GAMBAR
				name, ext = os.path.splitext(upload.raw_filename)
				if ext not in ('.jpeg','.png','.jpg'):
					return template('home-member',STATUS = 1,type=TYPE,name=FULLNAME,images=IMAGE,dataposting=RESULT2)
				else:
					nameimages = upload.raw_filename
					upload.raw_filename = nameimages
					upload.save(path)
			controllerMember.insertPosting(post_content,USERNAME,nameimages,typepost="timeline",article="")
			if location == "homemember":
				return redirect('/homemember')
			else:
				return redirect('/profilemember')
		else:
			if location == "homemember":
				return redirect('/homemember')
			else:
				return redirect('/profilemember')
	else:
		return redirect('/')
#bagian artikel
@route('/postarticle',method =["POST" , "GET"])
def postarticle():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)	
		if request.method == 'POST':
			title = request.forms.get('title')
			description = request.forms.get('description')
			if str(title) == "":
				return template('postarticle',error=1,status="Title must be filled!!!",type=TYPE,name=FULLNAME,images=IMAGE)
			elif str(description) == "":
				return template('postarticle',error=1,status="Description must be filled!!!",type=TYPE,name=FULLNAME,images=IMAGE)
			else:
				controllerMember.insertPosting(description,USERNAME,nameimages="",typepost="article",article=title)
				url = '/articlecontent?title='+str(title)+'&type=article'
				redirect(url)
		else:
			return template('postarticle',error=0,status="",type=TYPE,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')

@route('/articlecontent', method =["POST" , "GET"])
def articlecontent():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		title = request.GET.get("title")
		type = request.GET.get("type")
		if str(title) == "" or str(type) == "":
			return redirect('/homemember')
		else:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			articleid = request.forms.get("articleid")
			if request.method == 'POST':
				return "post"
			else:
				resdatakonten = controllerMember.checkarticle(str(title),str(type))
				if resdatakonten == 0:
					return redirect('/homemember')
				else:
					articleid = resdatakonten[0]['_id']
					resdatakomen = controllerComment.selectCommentbyforum(articleid)#sohai
					return template('articlecontent',type=TYPE,name=FULLNAME,images=IMAGE,resdatakonten=resdatakonten,resdatakomen=resdatakomen,error=0)
	else:
		return redirect('/')	

@route('/postreplyarticle', method =["POST" , "GET"])
def postreplyarticle():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		if request.method == 'POST':
			reply = request.forms.get("reply")
			title = request.forms.get("title")
			type = request.forms.get("type")
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			articleid = request.forms.get("articleid")

			resdatakonten = controllerMember.checkarticle(str(title),str(type))
			if str(reply) == "":
				if resdatakonten == 0:
					return redirect('/')
				else:
					articleid = resdatakonten[0]['_id']
					resdatakomen = controllerComment.selectCommentbyforum(articleid)#sohai
				return template('articlecontent',type=TYPE,name=FULLNAME,images=IMAGE,resdatakonten=resdatakonten,resdatakomen=resdatakomen,error='Reply mustbe filled')
			else:
				articleid = request.forms.get("articleid")
				username1 = request.forms.get("username1")
				username2 = USERNAME
				type = request.forms.get("type")
				resdatakonten = controllerComment.postComment(articleid,username1,username2,reply,type)
				resupdate = controllerMember.updateuser(articleid,username2,type)
				print resupdate
				url = '/articlecontent?title='+str(title)+'&type='+str(type)
				redirect(url)
		else:
			return redirect('/')
	else:
		return redirect('/')
#bagian profile
@route('/EditProfileMember' ,method =["POST" , "GET"])
def EditProfileMember():
	ERR = ''
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		ID = RESULT[0]['_id']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		EMAIL = RESULT[0]['email']
		PHONE = RESULT[0]['phone']
		PASSWORD = RESULT[0]['password']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		print "-------------------------------------------------\n"
		if request.method == 'POST':
			type = request.forms.get('type')
			
			if type== "uploadimage": #jika uploadimage
				path = request.forms.get('path')
				upload = request.files.get('upload')
				if upload:
					name, ext = os.path.splitext(upload.raw_filename)
					if ext not in ('.jpeg','.png','.jpg'):
						return template('editprofile-member',STATUS = 'File extension not allowed.',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
					else:
						nameimages = upload.raw_filename
						upload.raw_filename = nameimages
						upload.save(path)
						controllerUser.editImages(ID,nameimages)
						return redirect('/EditProfileMember')
				else:
					return template('editprofile-member',STATUS = 'Images must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
			
			if type == "editname": #jika editname
				fistname = request.forms.get('fistname')
				lastname = request.forms.get('lastname')
				if fistname == '' or lastname =='':
					return template('editprofile-member',STATUS = 'Name must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					controllerUser.editName(ID,fistname,lastname)
					return template('editprofile-member',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)

			if type == "editemail": #jika editemail
				newemail = request.forms.get('newemail')
				if newemail == '':
					return template('editprofile-member',STATUS = 'Email must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					controllerUser.editEmail(ID,newemail)
					return template('editprofile-member',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)

			if type == "editpassword": #jika editpassword
				oldpassword = request.forms.get('oldpassword')
				newpassword = request.forms.get('newpassword')
				renewpassword = request.forms.get('renewpassword')
				
				if oldpassword == '' or newpassword =='' or renewpassword == '':
					return template('editprofile-member',STATUS = 'Password must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					if eqPassword(newpassword,renewpassword) == 1:
						return template('editprofile-member',STATUS = 'Renew password must be same with New Password',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
					else:
						controllerUser.editPassword(ID,newpassword)
					return template('editprofile-member',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
			
			if type == "editphone": #jika editphone
				phonenumber = request.forms.get('phonenumber')
				if phonenumber == '':
					return template('editprofile-member',STATUS = 'Phone must be filled',type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
				else:
					controllerUser.editPhone(ID,phonenumber)
					return template('editprofile-member',STATUS = 1,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
			#print type
		else:
			return template('editprofile-member',STATUS = ERR,type=TYPE,firstname = FISTNAME,lastname=LASTNAME,phone=PHONE,email=EMAIL,password=PASSWORD,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')

@route('/profilemember')
def profilemember():
	ERR = 0
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		EMAIL    = RESULT[0]['email']
		PHONE    = RESULT[0]['phone']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)		
		RESULT2 = controllerMember.selectdataTimeline(USERNAME,"Active") #ambil data timeline
		listProjectTake = controlleruploadclient.showTake(USERNAME) #ambil data Project
		totalprojekbymember = controlleruploadclient.summTotProjectbyMember(USERNAME) #hitung total projeknya
		return template('profile-member',dict(listProjectTake=listProjectTake),totalprojekbymember=totalprojekbymember,STATUS = ERR,type=TYPE,name=FULLNAME,email=EMAIL,phone=PHONE,images=IMAGE,dataposting=RESULT2)
#belom
@route('/showfollowing')
def showfollowing():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)		
		return template('showfollowing',type=TYPE,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')
#belom
@route('/showfollowers')
def showFollowers():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		IMAGE = RESULT[0]['images']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)		
		return template('showfollowers',type=TYPE,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')
		
@route('/projectmember')   #show list projek 
def projectmember():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		return redirect('/listproject')
	else:
		return redirect('/')

@route('/listproject') #show list projek 
def projectmember():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		
		listProjectUnTake = controlleruploadclient.showUnTake()
		return template('project-member',dict(listProjectUnTake=listProjectUnTake),type=TYPE,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')

@route('/resultproject')
def resultproject():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		listProjectTake = controlleruploadclient.showTake(datacookies)
		RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
		TYPE = "member"
		USERNAME = RESULT[0]['username']
		FISTNAME = RESULT[0]['firstname']
		LASTNAME = RESULT[0]['lastname']
		FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		IMAGE = RESULT[0]['images']
		'''print "------------------------------------------\n"
		print listProjectTake
		print "------------------------------------------\n"'''
		return template('upload-member',dict(listProjectTake=listProjectTake),error ="",type=TYPE,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')

@route('/takeit', method="POST")
def takeProjectProses():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		idProject = request.forms.get('idProject')
		RESULT = controlleruploadclient.takeProject(idProject,datacookies)
		#IMAGE = str(RESULT[0]['images'])	
		if RESULT == 1:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			listProjectUnTake = controlleruploadclient.showUnTake()
		return redirect('/listproject')#return template('project-member',dict(listProjectUnTake=listProjectUnTake),type=TYPE,name=FULLNAME,images=IMAGE)
	else:
		return redirect('/')

@route('/uploadresultproject', method =["POST" , "GET"])
def uploadresultproject():
	if request.method == 'POST':
		datacookies = request.get_cookie("cookiesuser", secret='test123')
		if datacookies:
			idproject = request.forms.get('idproject')
			path	  = request.forms.get('path')
			upload = request.files.get('upload')
			listProjectTake = controlleruploadclient.showTake(datacookies)
			RESULT = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			username = RESULT[0]['username']
			FISTNAME = RESULT[0]['firstname']
			LASTNAME = RESULT[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			IMAGE = RESULT[0]['images']
			
			if upload:
				name, ext = os.path.splitext(upload.raw_filename)
				if ext not in ('.doc','.docx'):
					return template('upload-member',dict(listProjectTake=listProjectTake),error=1,type=TYPE,name=FULLNAME,images=IMAGE)
				else:
					jwbanprojek = username + str(upload.raw_filename)
					controlleruploadclient.memberUploadProject(idproject,username,jwbanprojek)
					upload.raw_filename = jwbanprojek
					upload.save(path)
					return template('upload-member',dict(listProjectTake=listProjectTake),error=0,type=TYPE,name=FULLNAME,images=IMAGE)
			else:
				return template('upload-member',dict(listProjectTake=listProjectTake),error=1,type=TYPE,name=FULLNAME,images=IMAGE)
		else:
			return redirect('/')
	else:
		return redirect('/')

@route('/clientRegistration')
def clientRegitration():
	ERR = 0
	return template('registerClient', dict(ERR=ERR))
#------------------------------------------ FORUM ----------------------------------------------------#
@route('/forumGeneral')
def forumGeneral():
	resdataforum = ""
	user_image = []
	imagepersonal = []
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		idProject = request.forms.get('idProject')
		RESULT = controlleruploadclient.takeProject(idProject,datacookies)
		#IMAGE = str(RESULT[0]['images'])	
		if RESULT == 1:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			
			resdataforum = controllerForum.selectForum("forumgeneral")
		print "-----------------------------------------"
		print resdataforum
		print "-----------------------------------------"
		return template('forumGeneral',type=TYPE,name=FULLNAME,images=IMAGE,resdataforum=resdataforum)
	else:
		return redirect('/')

@route('/forumDefence') #gambar belom berubah
def forumDefence():
	resdataforum = ""
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		idProject = request.forms.get('idProject')
		RESULT = controlleruploadclient.takeProject(idProject,datacookies)
		#IMAGE = str(RESULT[0]['images'])	
		if RESULT == 1:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			resdataforum = controllerForum.selectForum("forumdefence")
		return template('forumDefence',type=TYPE,name=FULLNAME,images=IMAGE,resdataforum=resdataforum)
	else:
		return redirect('/')

@route('/forumZeroDay') #gambar belom berubah
def forumZeroDay():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		idProject = request.forms.get('idProject')
		RESULT = controlleruploadclient.takeProject(idProject,datacookies)
		#IMAGE = str(RESULT[0]['images'])	
		if RESULT == 1:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			resdataforum = controllerForum.selectForum("forumzeroday")
		return template('forumZeroDay',type=TYPE,name=FULLNAME,images=IMAGE,resdataforum=resdataforum)
	else:
		return redirect('/')

@route('/postreply', method =["POST" , "GET"])
def postreply():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		if request.method == 'POST':
			reply = request.forms.get("reply")
			title = request.forms.get("title")
			type = request.forms.get("type")
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)			
			if str(reply) == "":
				resdatakonten = controllerForum.checkDataForum(str(title),str(type))
				if resdatakonten == 0:
					return redirect('/forumGeneral')
				else:
					forumid = resdatakonten[0]['_id']
					resdatakomen = controllerComment.selectCommentbyforum(forumid)#sohai
				return template('forumcontent',type=TYPE,name=FULLNAME,images=IMAGE,resdatakonten=resdatakonten,resdatakomen=resdatakomen,error='Reply mustbe filled')
			else:
				forumid = request.forms.get("forumid")
				username1 = request.forms.get("username1")
				username2 = USERNAME
				type = request.forms.get("type")
				resdatakonten = controllerComment.postComment(forumid,username1,username2,reply,type)
				resupdate = controllerForum.updateuser(forumid,username2,type) 
				url = '/forumcontent?title='+str(title)+'&type='+str(type)
				redirect(url)
		else:
			return redirect('/')
	else:
		return redirect('/')

@route('/forumcontent', method =["POST" , "GET"])
def forumcontent():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		title = request.GET.get("title")
		type = request.GET.get("type")
		if str(title) == "" or str(type) == "":
			return redirect('/forumGeneral')
		else:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			USERNAME = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
			forumid = request.forms.get("forumid")
			if request.method == 'POST':
				return "post"
			else:
				resdatakonten = controllerForum.checkDataForum(str(title),str(type))
				if resdatakonten == 0:
					return redirect('/forumGeneral')
				else:
					forumid = resdatakonten[0]['_id']
					resdatakomen = controllerComment.selectCommentbyforum(forumid)#sohai
					print resdatakomen
					return template('forumcontent',type=TYPE,name=FULLNAME,images=IMAGE,resdatakonten=resdatakonten,resdatakomen=resdatakomen,error=0)
	else:
		return redirect('/')		

@route('/newthreadforum', method=["POST","GET"])
def newthreadforum():
	error = 0
	title = ""
	description = ""
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		idProject = request.forms.get('idProject')
		RESULT = controlleruploadclient.takeProject(idProject,datacookies)
		if RESULT == 1:
			RESULT2 = controllerUser.checkStatus(datacookies)  #ambil data user
			TYPE = "member"
			username = RESULT2[0]['username']
			IMAGE = RESULT2[0]['images']
			FISTNAME = RESULT2[0]['firstname']
			LASTNAME = RESULT2[0]['lastname']
			FULLNAME = str(FISTNAME) + " " + str(LASTNAME)
		if request.method == 'POST':
			typeforum = request.forms.get('typeforum')
			if typeforum =="":
				redirect('/forumGeneral')
			else:
				title = request.forms.get('title')
				description = request.forms.get('description')				
				if title == "":
					return template('newthreadforum',error=1,status="You must be filled the title",typeforum=typeforum,type=TYPE,name=FULLNAME,images=IMAGE)
				elif description == "":
					return template('newthreadforum',error=1,status="You must be filled the description",typeforum=typeforum,type=TYPE,name=FULLNAME,images=IMAGE)
				else:
					if str(title) =="None" and str(description) == "None":
						return template('newthreadforum',error=0,status="",typeforum=typeforum,type=TYPE,name=FULLNAME,images=IMAGE)
					else: 
						controllerForum.createForum(title,description,username,typeforum)
						if typeforum == "forumgeneral":
							redirect('/forumGeneral')
						if typeforum == "forumdefence":
							redirect('/forumDefence')
						if typeforum == "forumzeroday":
							redirect('/forumZeroDay')							
			return template('newthreadforum',error=0,status="",typeforum=typeforum,type=TYPE,name=FULLNAME,images=IMAGE)
		else:
			redirect('/forumGeneral')
	else:
		return redirect('/')



@route('/forgotpssword', method =["POST" , "GET"])
def logout():
	error = 0
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	if datacookies:
		redirect("/")
	else:
		if request.method == 'POST':
			emailforget = request.forms.get('emailforget')
			if emailforget:
				res = controllerUser.checkEmail(emailforget)
				if res == 0:
					return template('forgotpass',error=0,status='Your email not register')
				return template('forgotpass',error=1,status ='Successfully check your email for get confirmation.')
			else:
				return template('forgotpass',error=0,status='Email must be filled')
		else:
			return template('forgotpass',error='',status='')

@route('/logout')
def logout():
	datacookies = request.get_cookie("cookiesuser", secret='test123')
	response.set_cookie("cookiesuser", datacookies , secret='test123', max_age=0)
	return template('index',dict(ERR=1))
	
###### END PROSES #########################################################################

		
#run server
debug(True)
run(host='localhost', port=8080)
#run(host='192.168.1.104', port=8080)