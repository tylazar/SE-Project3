from flask import Flask, session, render_template, redirect, request, url_for
import mysql.connector

from Helper_Functions import funtions1
from Helper_Functions.funtions1 import *

import datetime as dt

#app = Flask(__name__)

import sys
print(sys.path)
print(sys.version)

with open('/var/www/html/WebsiteDocker/keys', 'r') as f:
    ck = f.readline()[:-1]
    cs = f.readline()[:-1]

# print(ck)
# print(cs)

from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Change this

OAUTH = OAuth()
GOOGLE = OAUTH.remote_app('google',
						consumer_key=ck, # keeping off git for security
						consumer_secret=cs, # ditto
						request_token_params={'scope': 'email'},
						base_url='https://www.googleapis.com/oauth2/v1/',
						request_token_url=None,
						access_token_method='POST',
						access_token_url='https://accounts.google.com/o/oauth2/token',
						authorize_url='https://accounts.google.com/o/oauth2/auth',)


localhost_addr = 'http://127.0.0.1:5000'
server_addr = 'http://www.ncfbluedream.com'

addr = server_addr # Change this to serve on website or local

#=========================================#
# OAuth Functions                         #
#=========================================#

@GOOGLE.tokengetter
def get_google_token(token=None):
	return session.get('token')

#=========================================#
# Flask Pages for OAuth                   #
#=========================================#

@app.route('/<SoP>/authorize')
def oauth_google(SoP):
	#Page that redirects to Google's OAuth authorization page
	session['user_type'] = SoP
	return GOOGLE.authorize(callback=url_for('oauth_google_authorized', _external=True))

@app.route('/authorized')
def oauth_google_authorized():
	resp = GOOGLE.authorized_response()
	if resp is None:
		return redirect(url_for('/')) # Where to direct if the authorization fails
	else:
		# passed
		# print(resp)
		token = resp['access_token'] # "thing google uses to see if you are logged in"
		session['token'] = token

		user_info = GOOGLE.get('userinfo').data # "namesake"
		username = user_info['email']

		session['userEmail'] = username

		return redirect('/'+username+'/homepage') # Do normal string construction later on

	# do redirects here

#=========================================#
# Flask Pages                             #
#=========================================#

@app.route('/')
def landingPage():
	#stuff here
	#funtions1.connectionTest()
	session.clear()
	return render_template("LandingPage.html")

#@app.route('/login/<SoP>', methods=['GET', 'POST'])
#def loginPage(SoP):
#	#global addr
#	session.clear()
#	if request.method == 'POST':
#		session['userEmail'] = request.form['email']
#		session['user_type'] = SoP
#		return redirect('/'+request.form['email']+'/homepage')
#	return render_template("GeneralLogin.html", BACK='http://www.ncfbluedream.com', 
#		ADDRESS='http://www.ncfbluedream.com', StudentorProfessor=SoP)

@app.route('/newAccount/<SoP>', methods=['GET', 'POST'])
def newAccountPage(SoP):
	#global addr
	if request.method == 'POST':
		# session['userEmail'] = request.form['email']
		session['user_type'] = SoP
		if SoP == 'Student':
			session['EGY'] = request.form['ExpectedGraduationYear']
			session['AOC'] = request.form['AOC']
			session['agreement'] = request.form['agreement']
			session['advisor'] = request.form['advisor']
		session['name'] = request.form['name']
		return redirect('/FERPA')
	return render_template("GeneralNewAccount.html", BACK='http://www.ncfbluedream.com', 
		ADDRESS='http://www.ncfbluedream.com', StudentOrProfessor=SoP, AOCList=getAoCs(),
		AdvisorList=getAdvisors(), currentYear=dt.datetime.now().year)

@app.route('/<user>/homepage')
def userHomepage(user):
	if session['user_type'] == 'Student':
		return studentHomepage(user)
	elif session['user_type'] == 'Professor':
		return professorHomepage(user)

	return 'ERROR'

def studentHomepage(student):
	#global addr
	if getStudentProfile(student) == None:
		try:
			newAccountCreation(session['name'],student,session['EGY'],session['AOC'],True)
		except:
			return redirect('/newAccount/Student')
	return render_template("StudentHomepage.html", Student=student, progress_sentece=progressSentence(student), 
		LOGOUT='http://www.ncfbluedream.com', ADDRESS='http://www.ncfbluedream.com')

def professorHomepage(professor):
	#global addr
	if getProfessorProfile(professor) == None:
		try:
			newAccountCreation(session['name'],professor,None,None,False)
		except:
			return redirect('/newAccount/Professor')
	return render_template("ProfessorHomepage.html", LOGOUT='http://www.ncfbluedream.com', 
		ADDRESS='http://www.ncfbluedream.com', Professor=professor, adviseeList=getAdviseeList())

@app.route('/<student>/studentAddCourse')
def studentAddCourse(student):
	#global addr
	if request.method == 'POST':
		studentID = getStudentID(student)
		for x in range(1,20):
			courseID = request.form['courseChoice'+str(x)]
			studentAddCourse(studentID,courseID)
		redirect('/'+student+'/homepage')
	return render_template("StudentAddCoursePage.html", BACK='http://www.ncfbluedream.com'+"/"+student+"/homepage", 
		ADDRESS='http://www.ncfbluedream.com', CourseList=getCourses(student))

@app.route('/<professor>/professorAddCourse')
def professorAddCourse(professor):
	#global addr
	if request.method == 'POST':
		courseName = request.form['CourseName']
		addedOrNot = addProfessorCourse(courseName)
		if addedOrNot == True:
			redirect('/'+professor+'/homepage')
		else:
			render_template("ProfessorAddCoursePage.html", BACK='http://www.ncfbluedream.com'+"/"+professor+"/homepage", 
				Warning="That class already exsists")
	return render_template("ProfessorAddCoursePage.html", BACK='http://www.ncfbluedream.com'+"/"+professor+"/homepage", 
		Warning=None)

@app.route('/<student>/editProfile', methods=['GET', 'POST'])
def editStudentProfile(student):
	#global addr
	print('Loading student page')
	if request.method == 'POST':
		newName = request.form['name']
		newAOC = request.form['StudentAOC']
		newEGY = request.form['StudentGraduationYear']
		newAdvisor = request.form['Advisor']
		newAgreement = True if request.form.get('Agreement') else False
		studentID = getStudentID(student)
		print('POSTing new student info')
		updateStudentProfile(studentID,newName,newAdvisor,newEGY,newAOC,newAgreement)
	oldInfo = getStudentProfile(student)
	return render_template("EditStudentProfile.html", BACK='http://www.ncfbluedream.com'+"/"+student+"/homepage", 
		StudentName=getStudentName(student), AOCList=getAoCs(), currentYear=dt.datetime.now().year, 
		maxYear=dt.datetime.now().year+10, oldAOC=oldInfo[1][0], oldEGY=oldInfo[0][4], oldAdvisor=oldInfo[0][3], 
		oldAgreement=oldInfo[0][5], advisorList=getAdvisorList())

@app.route('/browseClasses')
def browseClasses():
	#global addr
	return render_template("BrowseCourses.html",CourseList=getCourseList())

@app.route('/browseAOCs', methods=['GET', 'POST'])
def browseAOCs():
	#global addr
	if request.method == 'POST':
		aoc = request.form['AOCs']
		return redirect('/AOCDetails/'+session['user_type']+'/'+aoc)
	return render_template("BrowseAOCs.html", BACK='http://www.ncfbluedream.com'+"/"+session['userEmail']+"/homepage", 
		AOCList=getAOCList())

@app.route('/<professor>/addAOC')
def addAOC(professor):
	#global addr
	return render_template("addAOCPage.html", BACK='http://www.ncfbluedream.com'+"/"+professor+"/homepage", 
		courses=getCourseList())

@app.route('/FERPA')
def FERPA():
	return render_template("FERPA.html")

@app.route('/Welcome')
def Disclaimer():
	return render_template("DisclamerPage.html", StudentOrProfessor=session['user_type'])

@app.route('/AOCDetails/<SoP>/<AOC>')
def AOCDetails(SoP, AOC):
	#global addr
	if request.method == 'POST':
		redirect('/Edit/'+AOC)
	return render_template("GeneralAOCDetailPage.html", BACK='http://www.ncfbluedream.com'+'/browseAOCs', AOC=AOC, 
		StudentorProfessor=SoP, requirements=getAOC(''))

@app.route('/Edit/<AOC>')
def editAOC(AOC):
	#things and stuff here
	allAOC = getAOC(AOC)
	return render_template("EditAOCPage.html", BACK='http://www.ncfbluedream.com'+'/AOCDetails/Professor/'+AOC, 
		AOC=allAOC)

# We will want to rename AOC_List to something like just AOC (but that would break the HTML as is)
@app.route('/<student>/studentProgressBreakdown')
def studentProgressBreakdown(student, AOC="General Studies"):
	#global addr
	return render_template("StudentBreakdownPage.html", BACK='http://www.ncfbluedream.com'+"/"+student+"/homepage", 
		progress_sentence=progressSentence(student), AOC_List=getStudentAOC(student), 
		LACList=getLACProgress(student), Courses=getCourses(student))

if __name__ == "__main__":
	app.run()



#=========================================#
# Dummy Functions                         #
#=========================================#

def getProgressSentence(student):
	return ["Bwee", "Bwee2"]

def getAOC(student):
	requirements = ["Intro to Programming Course", "Scheme", "C++", "Software Engineering"]
	return ["Computer Science", requirements]

def getLAC(student):
	return [('What goes', 'here?')]

def getCourses(student):
	return [(1,'Scheme'), (2,'Competitive Programming'), (3,'Intro to Pekes'), (4,'Advance Pekeonomics'), 
	(5,'Gender, Equality, & the Pekingese'), (6,'Pekesis')]

def getStudentName(student):
	studentProfile = getStudentProfile(student)
	studentName = studentProfile[0][1]
	return studentName

def getAOCList():
	return [("Computer Science",1), ("Biology",2), ("Political Science",3), ("Pekeology",4)]

def getAdviseeList():
	hts = ["Hunt Thomas Sparra", "Panting", "...no comment"]
	ys = ["Yourself", "Computer Science", "On Track"]
	return [hts, ys]

def getCourseList():
	return [(1,"Intro to Python"), (2,"Scheme"), (3,"Linear Algebra"), (4,"Intro to Buddhism"), (5,"Discrete Mathematics")]	

def progressSentence(studentEmail):
	studentProfile = getStudentProfile(studentEmail)
	studentID = studentProfile[0][0]
	studentProgressVar = getstudentProgress(studentID)
	studentAOC = studentProfile[1][1]
	expectedGraduationYear = studentProfile[0][4]
	string1 = "You have "
	string2 = "class(es) left to complete your AOC "
	string3 = ".\n You are "
	string4 = "on track to graduate by "
	variable1 = str(studentProgressVar[1])
	variable2 = studentAOC
	if studentProgressVar[0] <= expectedGraduationYear:
		variable3 = ""
	else:
		variable3 = "not "
	variable4 = str(expectedGraduationYear)
	finalString = string1+variable1+string2+variable2+string3+variable3+string4+variable4+"."
	return finalString

def getStudentAOC(studentEmail):
	studentProfile = getStudentProfile(studentEmail)
	AOCinfo = aocInformation(studentProfile[1][0])
	return [AOCinfo]

def getStudentID(studentEmail):
	studentProfile = getStudentProfile(studentEmail)
	ID = studentProfile[0][0]
	return ID

def getAOC(aoc):
	aocInformation(aoc)

def getAdvisors():
	return getAdvisorList()
