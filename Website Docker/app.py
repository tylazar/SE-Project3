from flask import Flask, session, render_template, redirect, request
import mysql.connector

from Helper_Functions import funtions1
import datetime as dt

app = Flask(__name__)

@app.route('/')
def landingPage():
	#stuff here
	pass

@app.route('/login/<SoP>')
def loginPage(SoP):
	#stuff here
	pass
	
@app.route('/newAccount/<SoP>')
def newAccountPage(SoP):
	#stuff here
	pass

@app.route('/<student>/homepage')
def studentHomepage(student):
	#stuff here
	pass

@app.route('/<professor>/homepage')
def professorHomepage(professor):
	#stuff here
	pass

@app.route('/Student__AddCourse')
def studentAddCourse():
	#stuff here
	pass

@app.route('/Professor__AddCourse')
def professorAddCourse():
	#stuff here
	pass

@app.route('/EditProfile/<student>')
def editStudentProfile(student):
	#stuff here
	pass

@app.route('/EditProfile/<professor>')
def editProfessorProfile(professor):
	#stuff here
	pass

@app.route('/BrowseClasses')
def browseClasses():
	#stuff here
	pass


if __name__ == "__main__":
	app.run()
