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
			if 'agreement' in request.form:
				session['agreement'] = True
			else:
				session['agreement'] = False
			# session['agreement'] = request.form['agreement']
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
		if getProfessorProfile(student) != None:
			return redirect('/newAccount/Student')

		#try:
		newAccountCreation(session['name'],student,session['EGY'],session['AOC'],session['advisor'],session['agreement'],True)
		#except:
		#	return redirect('/newAccount/Student')
	
	student_name = getStudentProfile(student)[0][1]
	return render_template("StudentHomepage.html", Student=student, NAME=student_name, progress_sentece=progressSentence(student), 
		LOGOUT='http://www.ncfbluedream.com', ADDRESS='http://www.ncfbluedream.com')

def professorHomepage(professor):
	#global addr
	if getProfessorProfile(professor) == None:
		if getStudentProfile(professor) != None:
			return redirect('/newAccount/Professor')

		try:
			newAccountCreation(session['name'],professor,None,None,False)
		except:
			return redirect('/newAccount/Professor')
	
	professor_profile = getProfessorProfile(professor)
	professor_name = professor_profile[1]
	professor_id = professor_profile[0]

	return render_template("ProfessorHomepage.html", LOGOUT='http://www.ncfbluedream.com', 
		ADDRESS='http://www.ncfbluedream.com', Professor=professor, NAME=professor_name, adviseeList=adviseeInfo(professor_id))

@app.route('/<student>/studentAddCourse', methods=['GET', 'POST'])
def studentAddCourse(student):
	#global addr
	if request.method == 'POST':
		student_id = getStudentID(student)
		
		f = request.form
		courses = f.getlist('courseChoice[]')
		for course in courses:
			studentAddCourseSQL(student_id, course)

		return redirect('/'+student+'/studentProgressBreakdown')
	return render_template("StudentAddCoursePage.html", BACK='http://www.ncfbluedream.com'+"/"+student+"/homepage", 
		ADDRESS='http://www.ncfbluedream.com', CourseList=grabAllCourses())

@app.route('/<professor>/professorAddCourse', methods=['GET', 'POST'])
def professorAddCourse(professor):
	#global addr
	if request.method == 'POST':
		courseName = request.form['CourseName']
		addedOrNot = addProfessorCourse(courseName)
		if addedOrNot == True:
			return render_template("ProfessorAddCoursePage.html", BACK='http://www.ncfbluedream.com'+"/"+professor+"/homepage", Warning="Course added!")
		else:
			return render_template("ProfessorAddCoursePage.html", BACK='http://www.ncfbluedream.com'+"/"+professor+"/homepage", 
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
	return render_template("BrowseAOCs.html", BACK='http://www.ncfbluedream.com'+"/"+session['userEmail']+"/homepage",
		SoP = session['user_type'], AOCList=getAoCs())

@app.route('/<professor>/addAOC', methods=['GET', 'POST'])
def addAOC(professor, replace_id=None):
	#global addr
	if replace_id == None:
		aoc = {'NAME':'', 'REQS':[]}
	elif request.method != "POST":
		aoc_data = getAOC(replace_id)

		aoc = dict()
		aoc['NAME'] = aoc_data[1]
		
		reqs = dict()
		for req_data in aoc_data[2]:
			req = {'NAME': req_data[1], 'NUM': req_data[4], 'CLASSES': [course[0] for course in req_data[3]]}
			reqs.append(req)
		aoc['REQS'] = reqs

	if request.method == "POST":
		f = request.form

		# print(f)

		aoc = build_aoc_from_form(f)

		if f['action'] == 'add_requirement':
			aoc['REQS'].append({'NAME':'', 'NUM':0, 'CLASSES':[]})
		elif f['action'] != 'submit_form':
			aoc['REQS'][int(f['action'])-1]['COURSES'].append(-1)
		else:
			sqlAddAOC(aoc)
			return redirect('browseAOCs')

		print(aoc)

	return render_template("addAOCPage.html", BACK='http://www.ncfbluedream.com'+"/"+professor+"/homepage", 
		courses=grabAllCourses(), AOC_DATA=aoc)

@app.route('/FERPA')
def FERPA():
	return render_template("FERPA.html")

@app.route('/Welcome')
def Disclaimer():
	return render_template("DisclamerPage.html", StudentOrProfessor=session['user_type'])

@app.route('/AOCDetails/<SoP>/<AoC>', methods=['GET', 'POST'])
def AOCDetails(SoP, AoC):
	#global addr
	if request.method == 'POST':
		return redirect(url_for('.addAOC', professor=session['userEmail'], replace_id=AoC))
	return render_template("GeneralAOCDetailPage.html", ADDRESS='http://www.ncfbluedream.com', BACK='http://www.ncfbluedream.com'+'/browseAOCs', AOC=getAOC(AoC),
		StudentOrProfessor=SoP)

@app.route('/Edit/<AOC>')
def editAOC(AOC):
	#things and stuff here
	allAOC = getAOC(AOC)
	return render_template("EditAOCPage.html", BACK='http://www.ncfbluedream.com'+'/AOCDetails/Professor/'+AOC,
		AOC=allAOC)

@app.route('/<student>/studentProgressBreakdown', methods=['GET', 'POST'])
def studentProgressBreakdown(student, AOC="General Studies"):
	#global addr
	AOCListText = ""
	CoursesListText = ""
	LACListText = ""

	student_id = getStudentID(student)
	if request.method == 'POST':
		f = request.form
		checkedCourses = f.getlist('courses[]')
		checkedLACs = f.getlist('LACs[]')
		courses = set(checkedCourses) # remove duplicate courses
		LACs = set(checkedLACs)
		updateStudentClasses(student_id,courses)
		updateStudentLACs(student_id, LACs)
		# Drop courses and LACs
		# Add courses and LACs in list
	return render_template("StudentBreakdownPage.html", BACK='http://www.ncfbluedream.com'+"/"+student+"/homepage",
		progress_sentence=progressSentence(student), AOC_List=getStudentAOC(student), LACList=getLACProgress(student_id),
		email=session['userEmail'], Courses=getStudentCourses(student_id),AOCListText = AOCListText,
		AOC_Courses=AOCCourses(getStudentAOC(student)[0]),LACDic = LACRequirements(),CoursesListText = CoursesListText,
		LACListText = LACListText, Student=student)

if __name__ == "__main__":
	app.run()

#=========================================#
# Other Helper Functions                  #
#=========================================#

def build_aoc_from_form(f):
	print("Building AOC data...")
	name = f['AOC_name']
	print("Got AOC name...")

	if 'requirement_names[]' in f:
		req_names = f.getlist('requirement_names[]')
	else:
		req_names = []
	
	if 'courses[]' in f:
		req_courses = list(map(int, f.getlist('courses[]')))
	else:
		req_courses = []

	if 'courses_lens[]' in f:
		req_courses_lengths = list(map(int, f.getlist('courses_lens[]')))
	else:
		req_courses_lengths = []
	
	if 'nums_for_requirements[]' in f:
		req_nums = list(map(int, f.getlist('nums_for_requirements[]')))
	else:
		req_nums = []

	req_courses_parsed = list()
	courses_index = 0
	for num in req_courses_lengths:
		courses_for_req = list()

		# Oh no, I'm tapping into my inner C++ developer
		print("Loading courses...")
		print(num)
		while num > 0:
			print(req_courses[courses_index])
			courses_for_req.append(req_courses[courses_index])

			courses_index += 1
			num -= 1
		print("Finished loading courses...")

		print(courses_for_req)
		req_courses_parsed.append(courses_for_req)

	aoc = {'NAME':name, 'REQS':[]}

	for req_index in range(0, len(req_names)):
		req = {'NAME':req_names[req_index],'NUM':req_nums[req_index],'COURSES':req_courses_parsed[req_index]}
		aoc['REQS'].append(req)

	print("Finished building data...")

	return aoc

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
	return aocInformation(aoc)

def getAdvisors():
	return getAdvisorList()

def LACRequirements():
	return ["Math_proficiency","Divisional_coursework","Disiplinary_breadth","Diverse_perspective","Eight_liberal_art"]

def AOCCourses(AOC):
	list = []
	for requirement in AOC[2]:
		for courseList in requirement[3]:
			list += courseList
	return list

def courseId(course):
	courses = grabAllCourses()
	for Course in courses:
		if Course[1] == course:
			return Course[0]

def tryFormAOCCourses(student,course):
	student = getStudentID(student)
	try:
		add = request.form[course]
		if add == True:
			studentAddCourse(student,courseId(course))
		else:
			studentRemoveCourse(student,courseId(course))
	except:
		pass

def tryFormCourses(student,course):
	student = getStudentId(student)
	try:
		remove = request.form[course]
		studentRemoveCourse(student,courseId(course))
	except:
		pass

def tryFormLAC(student,LAC):
	student = getStudentID(student)
	try:
		LACvalue = request.form[LAC]
		updateStudentLACProgress(student,LAC,LACvalue)
	except:
		pass
