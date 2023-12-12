from firebase import firebase
import calendar
import time
from datetime import datetime

db = firebase.database()

year = datetime.now().year
month = datetime.now().month
period = "Spring" if month >= 1 and month <=4 else "Fall" if month >= 9 and month <= 12 else "Summer"

class Settings:
    collection_name = "settings"
    def __init__(self) -> None:
        self._current_year = year
        self._current_semester = period

    
    def setCurrentYear(self, year):
        self._year = year
    
    def setCurrentSemester(self, current_semester):
        self._current_semester = current_semester


    def getCurrentYear(self) -> int:
        return self._current_year
    
    def getCurrentSemester(self) -> str:
        return self._current_semester
    
    
    
    def __str__(self) -> str:
        return f'year {self._current_year}, {self._current_semester} semester'
    
    def saveData(self):
        try:
            db.child(self.collection_name).update({
                "current_year": self._current_year,
                "current_semester": self._current_semester
            })

            return self
        except:
            return False
        
    def getSettings():
        settings = db.child(Settings.collection_name).get().val()
        if settings is None:
            sett = Settings()
            return sett
        sett = Settings()
        sett.setCurrentYear(settings["current_year"])
        sett.setCurrentSemester(settings["current_semester"])
        
        return sett
        
    
    