class Token:
    def __init__(self, tokenID=None, userID=None, createTime=None, validity=None):
        self._tokenID = tokenID
        self._userID = userID
        self._createTime = createTime
        self._validity = validity

    def getTokenID(self):
        return self._tokenID

    def getUserID(self):
        return self._userID

    def setUserID(self, userID):
        self._userID = userID

    def getCreateTime(self):
        return self._createTime

    def setCreateTime(self, createTime):
        self._createTime = createTime

    def getValidity(self):
        return self._validity

    def setValidity(self, validity):
        self._validity = validity
