from firebase import firebase
import calendar
import time

db = firebase.database()

class Notification:
    collection_name = "notifications"
    def __init__(self) -> None:
        self._uid = ""
        self._datetime = False
        self._message = ""
        self._priority = ""
        self._read = False
        self._sender = ""
        self._sendee = ""
    
    def setUid(self, uid):
        self._uid = uid
    
    def setDateTime(self, datetime):
        self._datetime = datetime

    def setMessage(self, message):
        self._message = message
    
    def setPriority(self, priority):
        self._priority = priority
    
    def setRead(self, read):
        self._read = read
    
    def setSender(self, sender):
        self._sender = sender

    def setSendee(self, sendee):
        self._sendee = sendee

    def getUid(self) -> str:
        return self._uid
    
    def getDateTime(self) -> str:
        return self._datetime
    
    def getMessage(self) -> str:
        return self._message
    
    def getSendee(self) -> str:
        return self._sendee
    
    def getSender(self) -> str:
        return self._sender
    
    def getRead(self) -> bool:
        return self._read
    
    def getPriority(self) -> str:
        return self._priority
    
    def __str__(self) -> str:
        return f'{self._message}. From {self._sender}. to {self._sendee}. At {self._datetime}'
    
    def saveData(self):
        gmt = time.gmtime()
        ts = calendar.timegm(gmt)
        try:
            db.child(self.collection_name).push({
                "message": self._message,
                "datetime": ts if not self._datetime else self._datetime,
                "priority": self._priority,
                "read": False if not self._read else self._read,
                "sender": self._sender,
                "sendee": self._sendee
            })

            return self
        except:
            return False
        
    def getNotifications(uid):
        received_notifications = db.child(Notification.collection_name).order_by_child("sendee").equal_to(uid).get().each()
        sent_notifications = db.child(Notification.collection_name).order_by_child("sender").equal_to(uid).get().each()
        data = {}
        if len(received_notifications) == 0:
            data["received"] = []
        received_notifications_list = []
        for notf in received_notifications:
            c = {
                "uid": notf.key(),
                "message": notf.val()["message"],
                "priority": notf.val()["priority"],
                "datetime": notf.val()["datetime"],
                "read": notf.val()["read"],
                "sender": notf.val()["sender"],
                "sendee": notf.val()["sendee"],
            }
            received_notifications_list.append(c)
        data["received"] = received_notifications_list

        if len(sent_notifications) == 0:
            data["sent"] = []
        sent_notifications_list = []
        for notf in sent_notifications:
            c = {
                "uid": notf.key(),
                "message": notf.val()["message"],
                "priority": notf.val()["priority"],
                "datetime": notf.val()["datetime"],
                "read": notf.val()["read"],
                "sender": notf.val()["sender"],
                "sendee": notf.val()["sendee"],
            }
            sent_notifications_list.append(c)
        data["sent"] = sent_notifications_list
        return data
        
    
    def MarkAsRead(uid):
        try:
            db.child(Notification.collection_name).child(uid).update({
                "read": True
            })
            return True
        except:
            return False
    
    def deleteNotification(uid: str):
        try:
            db.child(Notification.collection_name).child(uid).remove()
            return True
        except:
            return False
    
    