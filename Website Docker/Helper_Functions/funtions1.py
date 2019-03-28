import datetime
#-----------------------------------------------------------------------------
#HELPER FOR THE HELPERS
def connectCursor():
	connection = mysql.connector.connect(user='root', password='bluecrew', database='Aoc')
	cur = connection.cursor()
	return (connection,cur)

#-----------------------------------------------------------------------------
#GENERAL HELPER FUNCTIONS

def studentProgress(student):
	#this function will calculate how much time a student needs to graduate
	#returns a year that is the current year plus the number of years needed
	#to graduatate at the current rate
	#-----------------------------------
	#ASSUMTIONS MADE DURING THIS CALCULATION
	#1 - the student is taking for classes a semester
	#2 - the student has at least 3 of those classes each semester in their AOC
	#3 - all courses the student needs are being offered when they need/want them
	connection, cur = connectCursor()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	Total_NUM_to_complete = 0
	query = "SELECT AOC_id FROM Student_aoc WHERE Student_id = %s"
	values = (student,)
	cur.execute()
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	AOCID = ""
	for AOC_id in results:
		AOCID = AOC_id
	query = "SELECT NUM_to_complete FROM Requirements WHERE AOC_id = %s"
	values = (AOCID,)
	cur.execute()
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for NUM_to_complete in results:
		Total_NUM_to_complete += NUM_to_complete
	query = "SELECT NUM_completed FROM Requirements_completed WHERE Student_id = %s"
	values = (student,)
	cur.execute()
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for NUM_completed in results:
		Total_NUM_to_complete -= NUM_completed
	currentYear += (Total_NUM_to_complete/3)
	return currentYear

def aocInformation(AOC):
	#this function will grab all information attached to an AOC, including name
	#department, requirements, and courses for each requirement
	#returns a tuple
	connection, cur = connectCursor()
	query = "SELECT name FROM AOCs WHERE id = %s"
	values = (AOC,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	AOCname = ""

	for name in results:
		AOCname = name

	query = "SELECT * FROM Requirements WHERE AOC_id = %s"
	values = (AOC,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	tempReqList = []

	for id,name,AOC_id,NUM_to_complete in results:
		query = "SELECT Course_id FROM Courses_for_requirement WHERE Requirement_id = %s"
		values = (id,)
		cur.execute(query,values)
		results2 = cur.fetchall()
		connection.commit()
		cur.close()
		cur = connection.cursor()
		Courses_for_requirementList = []

		for Course_id in results2:
			query = "SELECT name,Department_id FROM Courses WHERE id = %s"
			values = (Course_id,)
			cur.execute()
			results3 = cur.fetchall()
			connection.commit()
			cur.close()
			cur = connection.cursor()

			for name,Department_id in results3:
				Courses_for_requirementList.append((name,Department_id))

		tempReqList.append((id,name,AOC_id,Courses_for_requirementList,NUM_to_complete))

	return (AOCname,tempReqList)

def grabAllCourses():
	#this function will return a list of tuples of all course names and Id numbers
	tempList = []
	connection, cur = connectCursor()
	query = "SELECT * FROM Courses"
	cur.execute(query,)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()

	for id,name,Department_id in results:
		tempList.append((id,name,Department_id))

	return tempList


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