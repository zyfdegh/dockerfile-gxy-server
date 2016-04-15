class Spread:
    def __init__(self, spreadID=None, price=None, timeAndDate=None, userID=None):
        self._spreadID = spreadID
        self._price = price
        self._timeAndDate = timeAndDate
        self._userID = userID

    def getUserID(self):
        return self._userID

    def setUserID(self, userID):
        self._userID = userID

    def gettimeAndDate(self):
        return self._timeAndDate

    def settimeAndDate(self, timeAndDate):
        self._timeAndDate = timeAndDate

    def getPrice(self):
        return self._price

    def setPrice(self, price):
        self._price = price

    def getSpreadID(self):
        return self._spreadID

    def setSpreadID(self, spreadID):
        self._spreadID = spreadID