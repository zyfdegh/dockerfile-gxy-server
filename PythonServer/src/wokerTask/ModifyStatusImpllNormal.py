# coding=utf8
import json
import sys

sys.path.append("..")

from TaskGettingImpll import TaskGettingImpll
from tool.RYClient import RYClient
from tool.DataOperation import DataOperation
from ModifyStatusImpll import ModifyStatusImpll

class ModifyStatusImpllNormal(ModifyStatusImpll):
    def __init__(self, tag, collegeID):
        ModifyStatusImpll.__init__(self, tag, collegeID)

    def modifyInspectionStatus(self, tokenID, taskID, status):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return (False)

        sql = 'update workerTask set status = \'%s\' where taskID like \'%s\';' % (status, taskID)
        db = DataOperation()
        db.connect()
        (ret, reason) = db.operate(sql)
        db.close()

        return (ret, reason)