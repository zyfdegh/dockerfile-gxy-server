class Requirement:
    def __init__(self,requirementID=None, info=None, userID=None):
        self._requirementID = requirementID
        self._info = info
        self._userID = userID

    def getRequirementID(self):
        return self._requirementID

    def setRequirementID(self,requirementID):
        self._requirementID = requirementID

    def getInfo(self):
        return self._info

    def setInfo(self, info):
        self._info = info

    def getUesrID(self):
        return self._userID

    def setUserID(self,userID):
        self._userID = userID
