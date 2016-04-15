class ExpressInfo:
    '''
    expressID nvarchar(100) comment '',
    expressName nvarchar(1000) comment '',
    userID nvarchar(100) comment '',
    receiver nvarchar(1000) comment '',
    tel nvarchar(100) comment '',
    expressCompany nvarchar(100) comment '',
    expressAddress nvarchar(1000) comment '',
    '''
    def __init__(self, expressID = None, expressName = None, userID = None, receiver = None, tel = None, expressCompany = None, expressAddress = None):
        self._expressID = expressID
        self._expressName = expressName
        self._userID = userID
        self._receiver = receiver
        self._tel = tel
        self._expressCompany = expressCompany
        self._expressAddress = expressCompany

    def setExpressID(self, expressID):
        self._expressID = expressID

    def getExpressID(self):
        return self._expressID

    def setExpressName(self, expressName):
        self._expressName = expressName

    def getExpressName(self):
        return self._expressName

    def setUserID(self, userID):
        self._userID = userID

    def getUserID(self):
        return self._userID

    def setReceiver(self, receiver):
        self._receiver = receiver

    def getReceiver(self):
        return self._receiver

    def setTel(self, tel):
        self._tel = tel

    def getTel(self):
        return self._tel

    def setExpressCompany(self, expressCompany):
        self._expressCompany = expressCompany

    def getExpressCompany(self):
        return self._expressCompany

    def setExpressAddress(self, expressAddress):
        self._expressAddress = expressAddress

    def getExpressAddress(self):
        return self._expressAddress
