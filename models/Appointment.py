from firebase import firebase
import calendar
import time

db = firebase.database()

class Appointment:
    collection_name = "appointments"
    def __init__(self) -> None:
        self._uid = ""
        self._date = ""
        self._time = ""
        self._description = ""
        self._appointer = ""
        self._appointee = ""
        self._confirmed = ""
    
    def setUid(self, uid):
        self._uid = uid
    
    def setDate(self, datetime):
        self._datetime = datetime

    def setDescription(self, description):
        self._description = description
    
    def setAppointer(self, appointer):
        self._appointer = appointer

    def setAppointee(self, appointee):
        self._appointee = appointee

    def setConfirmed(self, confirmed):
        self._confirmed = confirmed
    
    def setTime(self, time):
        self._time = time

    def getUid(self) -> str:
        return self._uid
    
    def getDate(self) -> str:
        return self._datetime
    
    def getDescription(self) -> str:
        return self._description
    
    def getAppointee(self) -> str:
        return self._appointee
    
    def getAppointer(self) -> str:
        return self._appointer
    
    def getConfirmed(self) -> str:
        return self._confirmed
    
    def getTime(self) -> str:
        return self._time
    
    def __str__(self) -> str:
        return f'{self._description}. From {self._appointer}. to {self._appointee}. At {self._datetime}'
    
    def saveData(self):
        gmt = time.gmtime()
        ts = calendar.timegm(gmt)
        try:
            db.child(self.collection_name).push({
                "description": self._description,
                "date": self._datetime,
                "time": self._time,
                "appointer": self._appointer,
                "appointee": self._appointee,
                "confirmed": self._confirmed
            })

            return self
        except:
            return False
        
    def getAppointments(uid):
        received_appointments = db.child(Appointment.collection_name).order_by_child("appointee").equal_to(uid).get().each()
        sent_appointments = db.child(Appointment.collection_name).order_by_child("appointer").equal_to(uid).get().each()
        data = {}
        if len(received_appointments) == 0:
            data["received"] = []
        received_notifications_list = []
        for notf in received_appointments:
            c = {
                "uid": notf.key(),
                "description": notf.val()["description"],
                "date": notf.val()["date"],
                "time": notf.val()["time"],
                "appointer": notf.val()["appointer"],
                "appointee": notf.val()["appointee"],
                "confirmed": False if "confirmed" not in notf.val() else notf.val()["confirmed"]
            }
            received_notifications_list.append(c)
        data["received"] = received_notifications_list

        if len(sent_appointments) == 0:
            data["sent"] = []
        sent_notifications_list = []
        for notf in sent_appointments:
            c = {
                "uid": notf.key(),
                "description": notf.val()["description"],
                "date": notf.val()["date"],
                "time": notf.val()["time"],
                "appointer": notf.val()["appointer"],
                "appointee": notf.val()["appointee"],
                "confirmed": False if "confirmed" not in notf.val() else notf.val()["confirmed"]
            }
            sent_notifications_list.append(c)
        data["sent"] = sent_notifications_list
        return data
        
    def ConfirmAppointment(uid):
        try:
            db.child(Appointment.collection_name).child(uid).update({
                "confirmed": True
            })
            return True
        except:
            return False
    
    def deleteAppointment(uid: str):
        try:
            db.child(Appointment.collection_name).child(uid).remove()
            return True
        except:
            return False
    
    