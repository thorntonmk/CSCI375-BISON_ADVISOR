from firebase import firebase
import sys
sys.path.append("./")

from models.CourseHistory import CourseHistory
from models.Settings import Settings

db = firebase.database()

class Course:
    collection_name = "courses"
    def __init__(self) -> None:
        self._code = ""
        self._name = ""
        self._prerequisites = []
    
    def setCode(self, code):
        self._code = code
    
    def setName(self, name):
        self._name = name

    def setPrerequisites(self, prerequisites):
        self._prerequisites = prerequisites

    def getCode(self) -> str:
        return self._code
    
    def getName(self) -> str:
        return self._name
    
    def getPrerequisites(self) -> list:
        return self._prerequisites
    
    def __str__(self) -> str:
        return f'{self._code}:{self._name}, prereqs:{self._prerequisites}'
    
    def saveCourse(self):
        try:
            db.child(self.collection_name).child(self._code).set({
                "code": self._code,
                "name": self._name,
                "prerequisites": self._prerequisites
            })

            return self
        except:
            return False
        
    def getCourseByCode(code):
        try:
            response = db.child(Course.collection_name).child(code).get().val()
            course = Course
            course.setCode(response.get("code"))
            course.setName(response.get("name"))
            course.setPrerequisites(response.get("prerequisites"))

            return course
        except:
            return False
    
    def getCourses():
        courses = db.child(Course.collection_name).get().val()
        courses_list = []
        for k, v in courses.items():
            course = Course()
            course.setCode(v.get("code"))
            course.setName(v.get("name"))
            if "prerequisites" in v:
                course.setPrerequisites(v.get("prerequisites"))
            
            courses_list.append(course)

            return courses_list
    
    def courses_to_json() -> list:
        courses = db.child(Course.collection_name).get().each()
        if courses is None:
            return []
        courses_list = []
        for course in courses:
            if "prerequisistes" in course.val():
                c = {}
                c["code"] = course.val()["code"]
                c["name"] = course.val()["name"]
                c["prerequisites"] = ','.join(course.val()["prerequisites"])

                courses_list.append(c)
            else:
                courses_list.append(course.val())
        return courses_list
    
    def delete_course(course_code: str):
        try:
            deleted = db.child(Course.collection_name).child(course_code).remove()
            print(deleted)
            return True
        except:
            return False
    
    def register_student_for_course(student_id: str, course_id: str, prereqs: list):
        #check if prerequisites are met
        for prereq in prereqs:
            exists = db.child(CourseHistory.collection_name).order_by_child("student").equal_to(student_id).order_by_child("course").equal_to(prereq).get().each()
            print(str(exists))
            if len(exists) == 0:
                return f'Prerequisite {prereq} not met'
        # check if student has done it and save if not
        settings = Settings.getSettings()
        courseH = CourseHistory()
        courseH.setStudentId(student_id)
        courseH.setCourseId(course_id)
        courseH.setYear(str(settings.getCurrentYear()))
        courseH.setSemester(settings.getCurrentSemester())
        courseH.setAssignmentTotal(0)
        courseH.setMidTermTotal(0)
        courseH.setFinalTotal(0)

        try:
            courseH.saveData()
            return True
        except ValueError as e:
            print(e)
            return "Student has done this course"