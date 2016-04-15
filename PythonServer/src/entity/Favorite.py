class Favorite:
    def __init__(self,favoriteID=None, merchandiseID=None, userID=None, timeAndDate=None):
        self._favoriteID = favoriteID
        self._merchandiseID = merchandiseID
        self._userID = userID
        self._timeAndDate = timeAndDate

    def getFavoriteID(self):
        return self._favoriteID

    def setFavoriteID(self, favoriteID):
        self._favoriteID = favoriteID

    def getMerchandiseID(self):
        return self._merchandiseID

    def setMerchandiseID(self, merchandiseID):
        self._merchandiseID = merchandiseID

    def getUserID(self):
        return self._userID

    def setUserID(self, userID):
        self._userID = userID

    def gettimeAndDate(self):
        return self._timeAndDate

    def settimeAndDate(self, timeAndDate):
        self._timeAndDate = timeAndDate