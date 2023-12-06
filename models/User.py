
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

    def getUid(self) -> str:
        return self._uid
    
    def getFName(self) -> str:
        return self._fName
    
    def getLName(self) -> str:
        return self._lName
    
    def getRole(self) -> str:
        return self._role
    
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
            
            
