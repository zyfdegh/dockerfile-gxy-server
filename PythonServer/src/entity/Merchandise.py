class Merchandise:
    def __init__(self, merchandiseID=None, merchandiseName=None, currentPrice=None, oldPrice=None, imgPath=None
                 , visitedCount=None, userID=None, info=None, publishedTime=None, swap=None, autoShipment=None, inspection=None):
        self._merchandiseID = merchandiseID
        self._merchandiseName = merchandiseName
        self._currentPrice = currentPrice
        self._oldPrice = oldPrice
        self._imgPath = imgPath
        self._visitedCount = visitedCount
        self._userID = userID
        self._info = info
        self._publishedTime = publishedTime
        self._swap = swap
        self._autoShipment = autoShipment
        self._inspection = inspection
    def getMerchandiseID(self):
        return self._merchandiseID

    def setMerchandiseID(self, merchandiseID):
        self._merchandiseID = merchandiseID

    def getMerchandiseName(self):
        return self._merchandiseName

    def setMerchandiseName(self, merchandiseName):
        self._merchandiseName = merchandiseName

    def getCurrentPrice(self):
        return self._currentPrice

    def setCurrentPrice(self, currentPrice):
        self._currentPrice = currentPrice

    def getOldPrice(self):
        return self._oldPrice

    def setOldPrice(self, oldPrice):
        self._oldPrice = oldPrice

    def getImgPath(self):
        return self._imgPath

    def setImgPath(self, imgPaht):
        self._imgPath = imgPaht

    def getVisitedCount(self):
        return self._visitedCount

    def setVisitedCount(self, visitedCount):
        self._visitedCount = visitedCount

    def getUserID(self):
        return self._userID

    def setUserID(self, userID):
        self._userID = userID

    def getInfo(self):
        return self._info

    def setInfo(self, info):
        self._info = info

    def getPublishedTime(self):
        return self._publishedTime

    def setPublishedTime(self, publishedTime):
        self._publishedTime = publishedTime

    def isSwap(self):
        return self._swap

    def setSwap(self, swap):
        self._swap = swap

    def isAutoShipment(self):
        return self._autoShipment

    def setAutoShipment(self, autoShipment):
        self._autoShipment = autoShipment

    def isInspection(self):
        return self._inspection

    def setInspection(self, inspection):
        self._inspection = inspection

