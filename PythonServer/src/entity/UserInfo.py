class UserInfo:
    def __init__(self, userID=None, userName=None,password=None,email=None,  gender=None, addressID=None, info=None, imgPath=None, account=None, tel=None):
        self._userID = userID
        self._email = email
        self._userName = userName
        self._password = password
        self._gender = gender
        self._addressID = addressID
        self._info = info
        self._imgPath = imgPath
        self._account = account
        self._tel = tel

    def getUserID(self):
        return self._userID

    def setUserID(self, userID):
        self._userID = userID

    def getEmail(self):
        return self._email

    def setEmail(self, email):
        self._email = email

    def getUserName(self):
        return self._userName

    def setUserName(self, userName):
        self._userName = userName

    def getPassword(self):
        return self._password

    def setPassword(self,password):
        self._password = password

    def getGender(self):
        return self._gender

    def setGender(self, gender):
        self._gender = gender

    def getAddressID(self):
        return self._addressID

    def setAddressID(self, addressID):
        self._addressID = addressID

    def getInfo(self):
        return self._info

    def setInfo(self, info):
        self._info = info

    def getImgPath(self):
        return self._imgPath

    def setImgPath(self, imgPath):
        self._imgPath = imgPath

    def getAccount(self):
        return self._account

    def setAccount(self, account):
        self._account = account

    def getTel(self):
        return self._tel

    def setTel(self, tel):
        self._tel = tel
