class Order:
    def __init__(self, orderID=None, timeAndDate=None, state=None, userID=None, sellerID=None, buyerID=None, logisticsID=None,  merchandiseID=None):
        self._orderID = orderID
        self._timeAndDate = timeAndDate
        self._state = state
        self._sellerID = sellerID
        self._buyerID = buyerID
        self._logisticsID = logisticsID
        self._merchandiseID = merchandiseID

    def getOrderID(self):
        return self._orderID

    def setOrderID(self, orderID):
        self._orderID = orderID

    def getTimeStamp(self):
        return self._timeAndDate

    def setTimeStamp(self, timeAndDate):
        self._timeAndDate = timeAndDate

    def getState(self):
         return self._state

    def setState(self, state):
         self._state = state


    def getSellerID(self):
        return self._sellerID

    def setSellerID(self, sellerID):
        self._sellerID = sellerID

    def getBuyerID(self):
        return self._buyerID

    def setBuyerID(self, buyerID):
        self._buyerID = buyerID

    def getLogisticsID(self):
        return self._logisticsID

    def setLogisticsID(self, logisticsID):
        self._logisticsID = logisticsID

    def getMerchandiseID(self):
        return self._merchandiseID

    def setMerchandiseID(self, merchandiseID):
        self._merchandiseID = merchandiseID
