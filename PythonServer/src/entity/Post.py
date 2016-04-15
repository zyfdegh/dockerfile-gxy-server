class Post:
    def __init__(self,postID=None, merchandiseID=None, timeAndDate=None, userID=None):
        self._postID = postID
        self._merchandiseID = merchandiseID
        self._timeAndDate = timeAndDate
        self._userID = userID

    def getPostID(self):
        return self._postID

    def setPostID(self, postID):
        self._postID = postID

    def getMerchandiseID(self):
        return self._merchandiseID

    def setMerchandiseID(self, merchandiseID):
        self._merchandiseID = merchandiseID

    def gettimeAndDate(self):
        return self._timeAndDate

    def settimeAndDate(self,timeAndDate):
        self._timeAndDate = timeAndDate

    def getUserID(self):
        return self._userID

    def setUserID(self, userID):
        self._userID = userID

