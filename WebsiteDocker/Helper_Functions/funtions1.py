import datetime
#-----------------------------------------------------------------------------
#HELPER FOR THE HELPERS
def connectCursor():
	'''
	returns the mysql connection and the cursor for further use
	'''
	connection = mysql.connector.connect(user='pythonUser', password='bluecrew', database='Aoc')
	cur = connection.cursor()
	return (connection,cur)

#-----------------------------------------------------------------------------
#GENERAL HELPER FUNCTIONS

def studentProgress(student):
	'''
	this function will calculate how much time a student needs to graduate
	returns a year that is the current year plus the number of years needed
	to graduatate at the current rate
	-----------------------------------
	ASSUMTIONS MADE DURING THIS CALCULATION
	1 - the student is taking for classes a semester
	2 - the student has at least 3 of those classes each semester in their AOC
	3 - all courses the student needs are being offered when they need/want them
	'''
	connection, cur = connectCursor()
	now = datetime.datetime.now()
	currentYear = int(now.year)
	Total_NUM_to_complete = 0
	query = "SELECT AOC_id FROM Student_aoc WHERE Student_id = %s"
	values = (student,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	AOCID = ""
	for AOC_id in results:
		AOCID = AOC_id
	query = "SELECT NUM_to_complete FROM Requirements WHERE AOC_id = %s"
	values = (AOCID,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for NUM_to_complete in results:
		Total_NUM_to_complete += NUM_to_complete
	query = "SELECT NUM_completed FROM Requirements_completed WHERE Student_id = %s"
	values = (student,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for NUM_completed in results:
		Total_NUM_to_complete -= NUM_completed
	currentYear += (Total_NUM_to_complete/3)
	return currentYear

def aocInformation(AOC):
	'''
	this function will grab all information attached to an AOC, including name
	department, requirements, and courses for each requirement
	returns a tuple
	'''
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
			query = "SELECT * FROM Courses WHERE id = %s"
			values = (Course_id,)
			cur.execute(query,values)
			results3 = cur.fetchall()
			connection.commit()
			cur.close()
			cur = connection.cursor()

			for id,name in results3:
				Courses_for_requirementList.append((id,name))

		tempReqList.append((id,name,AOC_id,Courses_for_requirementList,NUM_to_complete))

	return (AOCname,tempReqList)

def grabAllCourses():
	'''
	this function will return a list of tuples of all course names and Id numbers
	'''
	tempList = []
	connection, cur = connectCursor()
	query = "SELECT * FROM Courses"
	cur.execute(query,)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()

	for id,name in results:
		tempList.append((id,name))

	return tempList


#-----------------------------------------------------------------------------
#LOGIN PAGE

#doesn't look like this function is needed, covered by oauth
#def loginAuthentication(email):
	#this function will authenticate whether a user has a correct username and
	#password pair
	#returns a boolean


#-----------------------------------------------------------------------------
#CREATE NEW ACCOUNT PAGE

def newAccountAuthentication(email):
	'''
	this function will authenticate whether that username and name are currently being used
	in either students or professors
	returns a boolean
	'''
	connection, cur = connectCursor()
	query = "SELECT (SELECT email FROM Students) as student, (SELECT email FROM Professors) as professor"
	cur.execute(query,)
	results = cur.fetchall()
	connection.commit()
	cur.close()

	for student, professor in results:
		if (student or professor) == email:
			return False
	return True

def newAccountCreation(name,email,studentOrProfessor):
	'''
	this function will create the new account in either student or professors
	the variable studentOrProfessor is a boolean
	this function returns nothing
	'''
	if not newAccountAuthentication(email):
		return False
	connection, cur = connectCursor()
	query = "INSERT INTO %s (name,email) VALUES (%s,%s)"
	if studentOrProfessor:
		table = "Students"
	else:
		table = "Professors"
	values = (table,name,email)
	cur.execute(query,values)
	connection.commit()
	cur.close()


#-----------------------------------------------------------------------------
#STUDENT HOMEPAGE

def studentInformation(student):
	'''
	this function will grab all information pertaining to a student
	returns a tuple of said information
	'''
	calculatedGraduation = studentProgress(student)
	AOCname = ""
	AOCid = 0
	connection, cur = connectCursor()
	query = "SELECT AOC_id FROM Student_aoc WHERE Student_id = %s"
	values = (student,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()

	for AOC_id in results:
		AOCid = AOC_id

	query = "SELECT name FROM AOCs WHERE id = %s"
	values = (AOC_id,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()

	for name in results:
		AOCname = name

	numCompleted = 0

	query = "SELECT NUM_completed FROM Requirements_completed WHERE Student_id = %s"
	values = (student,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for NUM_completed in results:
		numCompleted -= NUM_completed

	numTotal = 0

	query = "SELECT NUM_to_complete FROM Requirements WHERE AOC_id = %s"
	values = (AOCID,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for NUM_to_complete in results:
		numTotal += NUM_to_complete


	numLeft = numTotal - numCompleted

	return (calculatedGraduation,AOCname,numLeft)


#-----------------------------------------------------------------------------
#PROFESSOR HOMEPAGE

def adviseeInfo(professor):
	'''
	this function will grab all pertinant information from students who have the given
	professor as an advisor
	returns a list of tuples for this information
	for students who have not agreed to give their inormation to their advisor they will appear
	but with their information said as simply [hidden]
	'''
	adviseeList = []
	connection, cur = connectCursor()
	query = "SELECT id, name, Agreed_to_advisee FROM Students WHERE advisor = %s"
	values = (professor,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()

	for id, name, Agreed_to_advisee in results:
		if Agreed_to_advisee == False:
			adviseeList.append((name,'[hidden]','[hidden]'))
		else:
			query = "SELECT AOC_id FROM Student_aoc WHERE Student_id = %s"
			values = (id,)
			cur.execute(query,values)
			results2 = cur.fetchall()
			connection.commit()
			cur.close()
			cur = connection.cursor()
			AOC_name = ""
			for AOC_id in results2:
				query = "SELECT name from AOCs WHERE id = %s"
				values = (AOC_id,)
				cur.execute(query,values)
				results3 = cur.fetchall()
				connection.commit()
				cur.close()
				cur = connection.cursor()
				for name in results3:
					AOC_name = name
			adviseeList.append((name,AOC_name,adviseeInfoHelper(id)))

	return adviseeList

def adviseeInfoHelper(student):
	'''
	this function basically does the same thing as the student progress function
	but instead of returning a year returns a percentage
	'''
	connection, cur = connectCursor()
	query = "SELECT AOC_id FROM Student_aoc WHERE Student_id = %s"
	values = (student,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	AOC_ID = 0
	totalNumber = 0
	completedNumber = 0
	for AOC_id in results:
		AOC_ID = AOC_id
	query = "SELECT id, NUM_to_complete FROM Requirements WHERE AOC_id = %s"
	values = (AOC_ID,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for id, NUM_to_complete in results:
		totalNumber += NUM_to_complete
		query = "SELECT NUM_completed FROM Requirements_completed WHERE Student_id = %s, Requirement_id = %s"
		values = (student,id)
		cur.execute(query,values)
		results2 = cur.fetchall()
		connection.commit()
		cur.close()
		cur = connection.cursor()
		for NUM_completed in results2:
			completedNumber += NUM_completed

	return float(float(completedNumber)/float(totalNumber))


#-----------------------------------------------------------------------------
#STUDENT BREAKDOWN PAGE

def getLACProgress(student):
	'''
	this function will grab all the information for that student and return the list of 
	tuples of that information
	'''
	connection, cur = connectCursor()
	tempList = [("Math_proficiency",False),("Divisional_coursework",False),("Disiplinary_breadth",False),("Diverse_perspective",False),("Eight_liberal_art",False)]
	query = "SELECT Math_proficiency, Divisional_coursework, Disiplinary_breadth, Diverse_perspective, Eight_liberal_art FROM LAC_Requirements WHERE Student_id = %s"
	values = (student,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()

	for Math_proficiency, Divisional_coursework, Disiplinary_breadth, Diverse_perspective, Eight_liberal_art in results:
		tempList[0][1] = Math_proficiency
		tempList[1][1] = Divisional_coursework
		tempList[2][1] = Disiplinary_breadth
		tempList[3][1] = Diverse_perspective
		tempList[4][1] = Eight_liberal_art

	return tempList


def getStudentCourses(student):
	'''
	this function will grab all courses the student has taken and return them in a list of
	tuples with the course name and course Id
	'''
	CoursesTaken = []
	connection, cur = connectCursor()
	query = "SELECT Course_id FROM Courses_completed WHERE Student_id = %s"
	values = (student,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()

	for Course_id in results:
		query = "SELECT * FROM Courses WHERE id = %s"
		values = (Course_id,)
		cur.execute(query,values)
		results2 = cur.fetchall()
		connection.commit()
		cur.close()
		cur = connection.cursor()
		for id,name,Department_id in results2:
			CoursesTaken.append((id,name,Department_id))

	return CoursesTaken

def updateStudentAOCProgress(student,requirement_id,requirement_progress):
	'''
	this function will update a students progress in aoc requirements
	returns nothing
	'''
	connection, cur = connectCursor()
	query = "UPDATE Requirements_completed SET NUM_completed = %s WHERE Student_id = %s AND Requirement_id = %s"
	values = (requirement_progress,student,requirement_id)
	cur.execute(query,values)
	connection.commit()
	cur.close()

def updateStudentLACProgress(student,LAC_requirement_column,LAC_progress):
	'''
	this function will update a students progress in LAC requirements
	returns nothing
	'''
	connection, cur = connectCursor()
	query = "UPDATE LAC_Requirements SET %s = %s WHERE Student_id = %s"
	values = (LAC_requirement_column,LAC_progress,student)
	cur.execute(query,values)
	connection.commit()
	cur.close()


#-----------------------------------------------------------------------------
#STUDENT ADD COURSE PAGE

def studentAddCourse(student,course):
	'''
	this function will add a course to a student's courses completed
	returns nothing
	'''
	connection, cur = connectCursor()
	query = "INSERT INTO Courses_completed (Student_id,Course_id) VALUES (%s,%s)"
	values = (student,course)
	cur.execute(query,values)
	connection.commit()
	cur.close()

#-----------------------------------------------------------------------------
#PROFESSOR ADD COURSE PAGE

def authenticateProfessorCourse(course_name):
	'''
	Check to see if submitted name is the same as any other Course in the table
	Args
		course_name: The name of the course to be checked
	Returns
		bool: If the course can be created
	'''
	connection, cur = connectCursor()
	query = "SELECT 1 FROM Courses WHERE Name=%s"
	values = (course_name)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()

	return len(results) == 0

def addProfessorCourse(course_name):
	'''
	Main function to submit new Course into the Courses table
	Args
		course_name: The name of the course to be checked
		department_name: The department that the professor creating the course belongs to
	Returns
		bool: If the course was created
	'''
	if not authenticateProfessorCourse(course_name):
		# Should we log something too?
		return False

	connection, cur = connectCursor()
	query = "INSERT INTO Courses (Name) VALUES (%s)"
	values = (course_name,)
	cur.execute(query,values)
	connection.commit()
	cur.close()
	return True

#-----------------------------------------------------------------------------
#EDIT STUDENT PROFILE PAGE
def getStudentProfile(studentEmail):
	'''
	Main function is to grab all info for a student’s “profile”,
	from the student table, student AOC table, and AOC table.
	Args
		studentEmail: The email of the student. This is used as
			a key for getting the student row.
	Returns
		student_row: [ID, name, email, advisor, graduation-year, agreed_to_advisee_info_trad]
		aoc_row: [ID, name, department-id]
	'''
	connection, cur = connectCursor()

	query = "SELECT 1 FROM Students WHERE Email=%s"
	values = (studentEmail,)
	cur.execute(query, values)
	student_row = cur.fetchall()[0]
	student_id = student_row[0]
	connection.commit()
	cur.close()
	cur = connection.cursor()

	query = "SELECT 1 FROM Student_aoc WHERE Student_id=%s"
	values = (student_id,)
	cur.execute(query, values)
	student_aoc_row = cur.fetchall()[0]
	aoc_id = student_aoc_row[1]
	connection.commit()
	cur.close()
	cur = connection.cursor()

	query = "SELECT 1 FROM AOCs WHERE id=%s"
	values = (aoc_id,)
	cur.execute(query, values)
	aoc_row = cur.fetchall()[1]

	connection.commit()
	cur.close()

	return student_row, aoc_row

def updateStudentProfile(student_id, name, advisor, graduation_year, aoc_id):
	'''
	Main function is to submit all info for a student’s “profile”,
	submits to the student table and student AOC table
	'''
	connection, cur = connectCursor()

	query = "UPDATE Student_aoc SET aoc_id=%s WHERE student_id=%s"
	values = (aoc_id, student_id)
	cur.execute()
	connection.commit()
	cur.close()
	cur = connection.commit()

	query = "UPDATE Students SET name=%s,advisor=%s,graduation_year=%s WHERE student_id=%s"
	values = (name, advisor, graduation_year, student_id)
	cur.execute()
	connection.commit()
	cur.close()

#-----------------------------------------------------------------------------
#BROWSE CLASSES PAGE

def getCourses():
	'''
	retuns a list of tuples of Course information from the Courses table
	'''
	connection, cur = connectionCurson()
	query = "SELECT * FROM Courses"
	cur.execute()
	ret = cur.fetchall()
	connection.commit()
	cur.close()

	return ret

#-----------------------------------------------------------------------------
#BROWSE AOCS PAGE

def getAoCs():
	'''
	retuns a list of tuples of AOC information from the AOC table
	'''
	connection, cur = connectionCurson()
	query = "SELECT * FROM AOCs"
	cur.execute()
	ret = cur.fetchall()
	connection.commit()
	cur.close()

	return ret

#-----------------------------------------------------------------------------
#AOC DETAIL PAGE
#will use the above function and simply grab the correct tuple needed for the AOC needed

#-----------------------------------------------------------------------------
#ADD AOC PAGE

def addAOC(AOC_name,Requirements):
	'''
	AOC_name is the name of the AOC, requirements is a list of tuples that hold information for each requirement
	this tuple is structure as such, (requirement_name,NUM_to_complete,[list of courses associated with said requirement])
	the list of courses is a list of tuples of ids and names, respectively
	this structure makes this function and the editAOC function a lot easier
	returns nothing
	'''
	connection, cur = connectCursor()
	query = "INSERT INTO AOCs (name) VALUES (%s)"
	values = (AOC_name,)
	cur.execute(query,values)
	connection.commit()
	cur.close()
	cur = connection.cursor()
	query = "SELECT id FROM AOCs WHERE name = %s"
	values = (AOC_name,)
	cur.execute(query,values)
	results = cur.fetchall()
	connection.commit()
	cur.close()
	cur = connection.cursor()
	AOC_id = 0

	for id in results:
		AOC_id = id

	for requirement in Requirements:
		query = "INSERT INTO Requirements (name,AOC_id,NUM_to_complete) VALUES (%s,%s,%s)"
		values = (requirement[0],AOC_id,requirement[1])
		cur.execute(query,values)
		connection.commit()
		cur.close()
		cur = connection.cursor()
		query = "SELECT id FROM Requirements WHERE name = %s AND AOC_id = %s"
		values = (requirement[0],AOC_id)
		cur.execute(query,values)
		results2 = cur.fetchall()
		connection.commit()
		cur.close()
		cur = connection.cursor()
		requirement_id = 0

		for id in results2:
			requirement_id = id

		for Course in requirement[2]:
			query = "INSERT INTO Courses_for_requirement (Requirement_id,Course_id) VALUES (%s,%s)"
			values = (requirement_id,Course[0])
			cur.execute(query,values)
			connection.commit()
			cur.close()


#-----------------------------------------------------------------------------
#EDIT AOC PAGE

def editAOC(AOC_name,AOC_id,oldRequirements,newRequirements):
	'''
	AOC_name is the name of the AOC, AOC_id is its id, requirements is a list of tuples that hold information for each requirement
	this tuple is structure as such, (requirement_name,NUM_to_complete,requirement_id,[list of courses associated with said requirement])
	the list of courses is a list of tuples of ids and names, respectively
	this structure makes this function and the addAOC function a lot easier
	'''
	connection, cur = connectCursor()
	query = "UPDATE AOCs SET name = %s WHERE id = %s"
	values = (AOC_name,AOC_id)
	cur.execute(query,values)
	connection.commit()
	cur.close()
	cur = connection.cursor()
	for x in range(len(newRequirements)):
		oldRequirement = oldRequirements[x]
		newRequirement = newRequirements[x]
		query = "UPDATE Requirements SET name = %s, NUM_to_complete = %s WHERE AOC_id = %s and name = %s"
		values = (newRequirement[0],newRequirement[1],AOC_id,oldRequirement[0])
		cur.execute(query,values)
		connection.commit()
		cur.close()
		cur = connection.cursor()
		query = "DELETE FROM Courses_for_requirement WHERE Requirement_id = %s"
		values = (oldRequirement[2],)
		cur.execute(query,values)
		connection.commit()
		cur.close()
		cur = connection.cursor()
		for Course in newRequirement[3]:
			query = "INSERT INTO Courses_for_requirement (Requirement_id,Course_id) VALUES (%s,%s)"
			values = (newRequirement[2],Course[0])
			cur.execute(query,values)
			connection.commit()
			cur.close()

