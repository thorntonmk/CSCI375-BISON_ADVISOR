from firebase import firebase

db = firebase.database()
storage = firebase.storage()

class Storage:
    folderpaths = ["files", "images", "video"]
    def __init__(self) -> None:
        self._name = ""
        self._folderpath = ""
        self._file = None

    
    def setName(self, name):
        self._name = name
    
    
    def setFolderPath(self, folderpath):
        self._folderpath = folderpath

    def setFile(self, file):
        self._file = file


    def getName(self) -> str:
        return self._name
    
    
    def getFolderPath(self) -> str:
        return self._folderpath
    
    def getFile(self):
        return self._file
    
    
    def __str__(self) -> str:
        return f'year {self._name}, a(n) {self._folderpath}'
    
    def saveData(self):
        try:
            storage.child(self._folderpath).child(self._name).put(self._file)

            return self
        except:
            return False
        
    def getFileUrl(folderpath, filename):
        return storage.child(folderpath).child(filename).get_url(None)
        
    
    