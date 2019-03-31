from flask import flask, session, render_template, redirect, request
import mysql.connector

from Helper_Functions import functions1
import datetime as dt

app = Flask(__name__)

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
	return render_template("ProfessorAddCoursePage.html",Department=getDepartment(professor))

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
	return render_template("addAOCPage.html",Department=getDepartment(professor),courses=getCourseList())

@app.route('/FERPA')
def FERPA():
	#stuff here
	return render_template("FERPA.html")

@app.route('/AOCDetails/<SoP>/<AOC>')
def AOCDetails(SoP):
	#stuff here
	return render_template("generalAOCDetailPage.html",AOC=AOC,Department=department,StudentorProfessor=SoP)

@app.route('/<student>/StudentProgressBreakdown')
def studentProgressBreakdown(student):
	#stuff here
	return render_template("StudentBreakdownPage.html",progress_sentence=getProgressSentence(student),AOC_List=getAOCList(),LACList=getLAC(student),Courses=getCourseList())

if __name__ == "__main__":
	app.run()
