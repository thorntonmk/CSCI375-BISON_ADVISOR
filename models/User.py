
from firebase import firebase

auth = firebase.auth()
db = firebase.database()

class User:
    collection_name = "users"

    def __init__(self):
        self._uid = ""
        self._fName = ""
        self._lName = ""
        self._phone = ""
        self._email = ""
        self._role = ""
        self._password = ""
        self._notifications = []
        self._appointments=[]
        self._courses = []

    def setUid(self, uid):
        self._uid = uid

    def setFName(self, name):
        self._fName = name
    

    def setLName(self, name):
        self._lName = name
    

    def setPhone(self, phone):
        self._phone = phone
    

    def setEmail(self, email):
        self._email = email
    
    def setPassword(self, password):
        self._password = password
    

    def setRole(self, role):
        self._role = role
    
    def setNotifications(self, notifications):
        self._notifications = notifications
    

    def setAppointments(self, appointments):
        self._appointments = appointments
    
    def setCourses(self, courses):
        self._courses = courses

    def getUid(self) -> str:
        return self._uid
    
    def getFName(self) -> str:
        return self._fName
    
    def getLName(self) -> str:
        return self._lName
    
    def getRole(self) -> str:
        return self._role
    
    def getCourses(self) -> list:
        return self._courses
    
    def createUser(self):
        try:
            us = auth.create_user_with_email_and_password(email=self._email, password=self._password)
            userid = us.get("localId")
            #save password
            db.child(self.collection_name).child(userid).set({
                "fName": self._fName,
                "lName": self._lName,
                "email": self._email,
                "phone": self._phone,
                "role": self._role,
                "notifications": self._notifications,
                "appointments": self._appointments,
                "courses": self._courses
            })
            #save to realtime db
            return self
        except:
            #Email already exists
            return False
    
    def getUser(uid):
        user = db.child(User.collection_name).child(uid).get().val()
        if user is not None:
            us = User()
            us.setUid(uid)
            us.setFName(user["fName"])
            us.setLName(user["lName"])
            us.setEmail(user["email"])
            us.setPhone(user["phone"])
            us.setRole(user["role"])
            if "appointments" in user:
                us.setAppointments(user["appointments"])
            if "notifications" in user:
                us.setNotifications(user["notifications"])
            if "courses" in user:
                us.setCourses(user["courses"])

            return us
        else:
            raise ValueError("Provided uid does not exist")
        
    def getAllUsers():
        users = db.child(User.collection_name).get().each()

        userList = []
        for u in users:
            c = {}
            c["uid"] = u.key()
            c["fName"] = u.val()["fName"]
            c["lName"] = u.val()["lName"]
            c["email"] = u.val()["email"]
            c["phone"] = u.val()["phone"]
            c["role"] = u.val()["role"]
            if "appointments" in u.val():
                c["appointments"] = u.val()["appointments"]
            if "notifications" in u.val():
                c["notifications"] = u.val()["notifications"]
            if "courses" in u.val():
                c["courses"] = u.val()["courses"]

            userList.append(c)

        return userList
    
    def login(email, password):
        try:
            result = auth.sign_in_with_email_and_password(email, password)
            return result.get("localId")
        except:
            return False
    
    def get_current_user_details(st):
        if "current_user_id" not in st.session_state:
            return None
        else:
            uid = st.session_state["current_user_id"]
            userInfo = db.child(User.collection_name).child(uid).get().val()
            user = User()
            user.setUid(uid)
            user.setFName(userInfo['fName'])
            user.setLName(userInfo['lName'])
            user.setEmail(userInfo['email'])
            user.setPhone(userInfo['phone'])
            user.setRole(userInfo['role'])
            if "appointments" in userInfo:
                user.setAppointments(userInfo['appointments'])
            if "notifications" in userInfo:
                user.setNotifications(userInfo['notifications'])
            if "courses" in userInfo:
                user.setCourses(userInfo["courses"])


            return user
    
    def get_students() -> list:
        students = db.child(User.collection_name).order_by_child("role").equal_to("Student").get().each()
        if students is None:
            return []
        students_list = []
        for student in students:
            c = {}
            c["uid"] = student.key()
            c["fName"] = student.val()["fName"]
            c["lName"] = student.val()["lName"]
            c["email"] = student.val()["email"]
            c["phone"] = student.val()["phone"]
            c["role"] = student.val()["role"]
            if "appointments" in student.val():
                c["appointments"] = student.val()["appointments"]
            if "notifications" in student.val():
                c["notifications"] = student.val()["notifications"]
            if "courses" in student.val():
                c["courses"] = student.val()["courses"]

            students_list.append(c)
        return students_list
    
    def updateUser(uid, json):
        try:
            db.child(User.collection_name).child(uid).update(json)
            return True
        except:
            return False
    
    def send_password_reset_email(email):
        auth.send_password_reset_email(email)
            
            
