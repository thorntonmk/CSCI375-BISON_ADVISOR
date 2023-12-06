from firebase import firebase

db = firebase.database()

class CourseHistory:
    collection_name = "course_history"
    def __init__(self) -> None:
        self._studentid = ""
        self._course_id = ""
        self._assignment_total_score = 0
        self._midterm_total_score = 0
        self._final_total_score = 0
        self._year = ""
        self._semester = ""
    
    def setStudentId(self, id):
        self._studentid = id
        
    def setCourseId(self, id):
        self._course_id = id
    
    def setAssignmentTotal(self, total):
        self._assignment_total_score = total
    
    def setMidTermTotal(self, total):
        self._midterm_total_score = total
    
    def setFinalTotal(self, total):
        self._final_total_score = total
    
    def setYear(self, year):
        self._year = year
    
    def setSemester(self, semester):
        self._semester = semester
    
    def getStudentId(self):
        return self._studentid
    
    def getCourseId(self):
        return self._course_id
    
    def getAssignmentTotal(self):
        return self._assignment_total_score
    
    def getMidtermTotal(self):
        return self._midterm_total_score
    
    def getFinalTotal(self):
        return self._final_total_score
    
    def getYear(self):
        return self._year
    
    def getSemester(self):
        return self._semester
    
    
    def __str__(self) -> str:
        return f'{self._studentid}, course: {self._course_id}, year {self._year}, sem {self._semester}, total {self._assignment_total_score}, {self._midterm_total_score}, {self._final_total_score}'
    
    def saveData(self):
        exists = db.child(self.collection_name).order_by_child("student").equal_to(self._studentid).order_by_child("course").equal_to(self._course_id).get().each()
        if len(exists) > 0:
            raise ValueError("Student has done this course")
        try:
            db.child(self.collection_name).push({
                "student": self._studentid,
                "course": self._course_id,
                "assignmentTotal": self._assignment_total_score,
                "midtermTotal": self._midterm_total_score,
                "finalTotal": self._final_total_score,
                "year": self._year,
                "semester": self._semester
            })

            return self
        except:
            return False
        
    def getCoursesByStudent(student):
        try:
            courses = db.child(CourseHistory.collection_name).order_by_child("student").equal_to(student).get().each()
            if courses is None:
                return []
            courses_list = []
            for course in courses:
                c = {
                    "uid":course.key(),
                    "course": course.val()["course"],
                    "finalTotal": course.val()["finalTotal"],
                    "midtermTotal": course.val()["midtermTotal"],
                    "assignmentTotal": course.val()["assignmentTotal"],
                    "student": course.val()["student"],
                    "year": course.val()["year"],
                    "semester": course.val()["semester"]
                }
                courses_list.append(c)
            return courses_list
        except:
            return False
        
    def deleteStudentCourse(uid: str):
        try:
            db.child(CourseHistory.collection_name).child(uid).remove()
            return True
        except:
            return False
    
    