from flask import Flask, session, render_template, redirect, request, url_for
# import mysql.connector

from Helper_Functions import funtions1

import datetime as dt

from flask_oauthlib.client import OAuth

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' # Change this

OAUTH = OAuth()
GOOGLE = OAUTH.remote_app('google',
						consumer_key='ASK_HUNT', # keeping off git for security
						consumer_secret='ASK_HUNT', # ditto
						request_token_params={'scope': 'email'},
						base_url='https://www.googleapis.com/oauth2/v1/',
						request_token_url=None,
						access_token_method='POST',
						access_token_url='https://accounts.google.com/o/oauth2/token',
						authorize_url='https://accounts.google.com/o/oauth2/auth',)


localhost_addr = 'http://127.0.0.1:5000'
server_addr = 'https://www.ncfbluedream.com'

addr = localhost_addr # Change this to serve on website or local

#=========================================#
# OAuth Functions                         #
#=========================================#

@GOOGLE.tokengetter
def get_google_token(token=None):
	return session.get('token')

#=========================================#
# Flask Pages for OAuth                   #
#=========================================#

@app.route('/authorize')
def oauth_google():
	'''
	Page that redirects to Google's OAuth authorization page
	'''
	return GOOGLE.authorize(callback=url_for('oauth_google_authorized', _external=True))

@app.route('/authorized')
def oauth_google_authorized():
	'''
	Page that is returned after authorization passes or fails
	'''
	resp = GOOGLE.authorized_response()
	if resp is None:
		return redirect(url_for('/')) # Where to direct if the authorization fails
	else:
		# passed
		print(resp)
		token = resp['access_token'] # "thing google uses to see if you are logged in"
		session['token'] = token

		user_info = GOOGLE.get('userinfo').data # "namesake"
		username = user_info['email']

		session['email'] = username

		return redirect('/'+username+'/homepage') # Do normal string construction later on

	# do redirects here

#=========================================#
# Flask Pages                             #
#=========================================#

@app.route('/')
def landingPage():
	#stuff here
	return render_template("LandingPage.html")

@app.route('/login/<SoP>', methods=['GET', 'POST'])
def loginPage(SoP):
	if request.method == 'POST':
		session['user'] = request.form['email']
		session['user_type'] = SoP
		return redirect('/'+request.form['email']+'/homepage')
	#stuff here
	return render_template("generalLogin.html", BACK=addr, ADDRESS=addr, StudentorProfessor=SoP)
	
@app.route('/newAccount/<SoP>', methods=['GET', 'POST'])
def newAccountPage(SoP):
	#stuff here
	if request.method == 'POST':
		session['user'] = request.form['email']
		session['user_type'] = SoP
		return redirect('/'+request.form['email']+'/homepage')
	return render_template("generalNewAccount.html", BACK=addr, ADDRESS=addr, StudentorProfessor=SoP)

@app.route('/<user>/homepage')
def userHomepage(user):
	if session['user_type'] == 'Student':
		return studentHomepage(user)
	elif session['user_type'] == 'Professor':
		return professorHomepage(user)

	return 'ERROR'

def studentHomepage(student):
	#stuff here
	return render_template("StudentHomepage.html",Student=student,progress_sentece=getProgressSentence(student), LOGOUT=addr, ADDRESS=addr)

def professorHomepage(professor):
	#stuff here
	return render_template("ProfessorHomepage.html", LOGOUT=addr, ADDRESS=addr, Professor=professor,adviseeList=getAdviseeList())

@app.route('/<student>/studentAddCourse')
def studentAddCourse(student):
	#stuff here
	return render_template("StudentAddCoursePage.html", BACK=addr+"/"+student+"/homepage", ADDRESS=addr, CourseList=getCourses(student))

@app.route('/<professor>/professorAddCourse')
def professorAddCourse(professor):
	#stuff here
	return render_template("ProfessorAddCoursePage.html", BACK=addr+"/"+professor+"/homepage")

@app.route('/<student>/editProfile')
def editStudentProfile(student):
	#stuff here
	return render_template("EditStudentProfile.html", BACK=addr+"/"+student+"/homepage",StudentName=getStudentName(student),AOCList=getAOCList(),currentYear=dt.datetime.now().year)

@app.route('/browseClasses')
def browseClasses():
	#stuff here
	return render_template("BrowseCourses.html",CourseList=getCourseList())

@app.route('/browseAOCs', methods=['GET', 'POST'])
def browseAOCs():
	#stuff here
	if request.method == 'POST':
		aoc = request.form['AOCs']
		return redirect('/AOCDetails/'+session['user_type']+'/'+aoc)
	return render_template("BrowseAOCs.html", BACK=addr+"/"+session['user']+"/homepage", AOCList=getAOCList())

@app.route('/<professor>/addAOC')
def addAOC(professor):
	#stuff here
	return render_template("addAOCPage.html", BACK=addr+"/"+professor+"/homepage", courses=getCourseList())

@app.route('/FERPA')
def FERPA():
	#stuff here
	return render_template("FERPA.html")

@app.route('/AOCDetails/<SoP>/<AOC>')
def AOCDetails(SoP, AOC):
	#stuff here
	return render_template("generalAOCDetailPage.html", BACK=addr+'/browseAOCs', AOC=AOC, StudentorProfessor=SoP, requirements=getAOC(''))

# We will want to rename AOC_List to something like just AOC (but that would break the HTML as is)
@app.route('/<student>/studentProgressBreakdown')
def studentProgressBreakdown(student, AOC="General Studies"):
	#stuff here
	return render_template("StudentBreakdownPage.html", BACK=addr+"/"+student+"/homepage", progress_sentence=getProgressSentence(student),AOC=getAOC(student),LACList=getLAC(student),Courses=getCourses(student))

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
	return ['Scheme', 'Competitive Programming', 'Intro to Pekes', 'Advance Pekeonomics', 'Gender, Equality, & the Pekingese', 'Pekesis']

def getStudentName(student):
	return "Hunt Sparra"

def getAOCList():
	return ["Computer Science", "Biology", "Political Science", "Pekeology"]

def getAdviseeList():
	hts = ["Hunt Thomas Sparra", "Panting", "...no comment"]
	ys = ["Yourself", "Computer Science", "On Track"]
	return [hts, ys]

def getCourseList():
	return ["Intro to Python", "Scheme", "Linear Algebra", "Intro to Buddhism", "Discrete Mathematics"]