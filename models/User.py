
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
                "appointments": self._appointments
            })
            #save to realtime db
            return self
        except:
            #Email already exists
            return False
    
    def getUser(self, uid):
        user = self.ref.child(uid).get()
        if user is not None:
            self._uid = uid
            self._fName = user["fName"]
            self._lName = user["lName"]
            self._email = user["email"]
            self._phone = user["phone"]
            self._role = user["role"]
            self._appointments = user["appointments"]
            self._notifications = user["notifications"]

            return self
        else:
            raise ValueError("Provided uid does not exist")
        
    def getAllUsers(self):
        users = self.ref.get()

        userList = []
        for u in users:
            user = User()
            user.setFName(u["fName"])
            user.setLName(u["lName"])
            user.setEmail(u["email"])
            user.setPhone(u["phone"])
            user.setRole(u["role"])
            user.setAppointments(u["appointments"])
            user.setNotifications(u["notifications"])
    
    def login(email, password):
        try:
            result = auth.sign_in_with_email_and_password(email, password)
            return result.get("localId")
        except:
            return False
    
    def get_current_user_details(st):
        uid = st.session_state["current_user_id"]
        if not uid:
            return None
        else:
            userInfo = db.child(User.collection_name).child(uid).get().val()
            user = User()
            user.setUid(uid)
            user.setFName(userInfo['fName'])
            user.setLName(userInfo['lName'])
            user.setEmail(userInfo['email'])
            user.setPhone(userInfo['phone'])
            user.setRole(userInfo['role'])
            user.setAppointments(userInfo['appointments'])
            user.setNotifications(userInfo['notifications'])

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

            students_list.append(c)
        return students_list
            
            
