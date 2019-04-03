from flask import flask, session, render_template, redirect, request
import mysql.connector

from Helper_Functions import functions1
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

@app.route('/login/<SoP>')
def loginPage(SoP):
	#stuff here
	return render_template("generalLogin.html",StudentorProfessor=SoP)
	
@app.route('/newAccount/<SoP>')
def newAccountPage(SoP):
	#stuff here
	return render_template("generalNewAccount.html",StudentorProfessor=SoP)

@app.route('/<student>/homepage')
def studentHomepage(student):
	#stuff here
	return render_template("StudentHomepage.html",Student=student,progress_sentece=getProgressSentence(student))

@app.route('/<professor>/homepage')
def professorHomepage(professor):
	#stuff here
	return render_template("ProfessorHomepage.html",Professor=professor,adviseeList=getAdviseeList())

@app.route('/Student__AddCourse')
def studentAddCourse():
	#stuff here
	return render_template("StudentAddCoursePage.html",CourseList=getCourseList())

@app.route('/Professor__AddCourse')
def professorAddCourse():
	#stuff here
	return render_template("ProfessorAddCoursePage.html")

@app.route('/EditProfile/<student>')
def editStudentProfile(student):
	#stuff here
	return render_template("EditStudentProfile.html",StudentName=getStudentName(student),AOCList=getAOCList(),currentYear=datetime.datetime.now().year)

@app.route('/BrowseClasses')
def browseClasses():
	#stuff here
	return render_template("BrowseCourses.html",CourseList=getCourseList())

@app.route('/BrowseAOCs')
def browseAOCs():
	#stuff here
	return render_template("BrowseAOCs.html",AOCList=getAOCList())

@app.route('/<professor>/AddAOC')
def addAOC(professor):
	#stuff here
	return render_template("addAOCPage.html",courses=getCourseList())

@app.route('/FERPA')
def FERPA():
	#stuff here
	return render_template("FERPA.html")

@app.route('/AOCDetails/<SoP>/<AOC>')
def AOCDetails(SoP):
	#stuff here
	return render_template("generalAOCDetailPage.html",AOC=AOC,StudentorProfessor=SoP)

@app.route('/<student>/StudentProgressBreakdown')
def studentProgressBreakdown(student):
	#stuff here
	return render_template("StudentBreakdownPage.html",progress_sentence=getProgressSentence(student),AOC_List=getAOCList(),LACList=getLAC(student),Courses=getCourseList())

if __name__ == "__main__":
	app.run()
