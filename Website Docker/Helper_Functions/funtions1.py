#-----------------------------------------------------------------------------
#GENERAL HELPER FUNCTIONS

def studentProgress(student):
	#this function will calculate how much time a student needs to graduate
	#returns a year that is the current year plus the number of years needed
	#to graduatate at the current rate

def aocInformation(AOC):
	#this function will grab all information attached to an AOC, including name
	#department, requirements, and courses for each requirement
	#returns a tuple

def grabAllCourses():
	#this function will return a list of tuples of all course names and Id numbers


#-----------------------------------------------------------------------------
#LOGIN PAGE

def loginAuthentication(username,password):
	#this function will authenticate whether a user has a correct username and
	#password pair
	#returns a boolean


#-----------------------------------------------------------------------------
#CREATE NEW ACCOUNT PAGE

def newAccountAuthentication(name,username,studentOrProfessor):
	#this function will authenticate whether that username and name are currently being used
	#in either students or professors, the variable studentOrProfessor is a boolean
	#returns a boolean

def newAccountCreation(username,password,name,email,studentOrProfessor):
	#this function will create the new account in either student or professors
	#the variable studentOrProfessor is a boolean
	#this function returns nothing


#-----------------------------------------------------------------------------
#STUDENT HOMEPAGE

def studentInformation(student):
	#this function will grab all information pertaining to a student
	#returns a tuple of said information


#-----------------------------------------------------------------------------
#PROFESSOR HOMEPAGE

def adviseeInfo(professor):
	#this function will grab all pertinant information from students who have the given
	#professor as an advisor
	#returns a list of tuples for this information


#-----------------------------------------------------------------------------
#STUDENT BREAKDOWN PAGE

def getLACProgress(student):
	#this function will grab all the information for that student and return the tuple of 
	#that information

def getStudentCourses(student):
	#this function will grab all courses the student has taken and return them in a list of
	#tuples with the course name and course Id

def updateStudentAOCProgress(student,progress):
	#this function will update a students progress in aoc requirements
	#returns nothing


#-----------------------------------------------------------------------------
#STUDENT ADD COURSE PAGE

#-----------------------------------------------------------------------------
#PROFESSOR ADD COURSE PAGE

#-----------------------------------------------------------------------------
#EDIT STUDENT PROFILE PAGE

#-----------------------------------------------------------------------------
#BROWSE CLASSES PAGE

#-----------------------------------------------------------------------------
#BROWSE AOCS PAGE

#-----------------------------------------------------------------------------
#STUDENT AOC DETAIL PAGE

#-----------------------------------------------------------------------------
#PROFESSOR AOC DETAIL PAGE

#-----------------------------------------------------------------------------
#ADD AOC PAGE

#-----------------------------------------------------------------------------
#EDIT AOC PAGE
