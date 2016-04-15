class Logistics:
    def __init__(self,logisticsID=None, company=None, state=None, location=None):
        self._logisticsID = logisticsID
        self._company = company
        self._state = state
        self._location = location

    def getLogisticsID(self):
        return self._logisticsID

    def setLogisticsID(self, logisticsID):
        self._logisticsID = logisticsID

    def getCompany(self):
        return self._company

    def setCompany(self, company):
        self._company = company

    def getState(self):
        return self._state

    def setState(self, state):
        self._state = state

    def getLocation(self):
        return self._location

    def setLocation(self, location):
        self._location = location



