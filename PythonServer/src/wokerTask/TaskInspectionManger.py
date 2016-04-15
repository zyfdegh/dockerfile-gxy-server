# coding=utf8
import json
import sys

sys.path.append("..")
from AllTaskImpllNormal import AllTaskImpllNormal
from CompletedTaskImpllNormal import CompletedTaskImpllNormal
from DoingTaskImpllNormal import DoingTaskImpllNormal
from TaskGettingImpllNotification import TaskGettingImpllNotification
from ModifyStatusImpllNormal import ModifyStatusImpllNormal
from tool.DataOperation import DataOperation

sys.path.append("..")

from TaskManager import TaskManager

class TaskInspectionManager(TaskManager):
    def __init__(self, tag=2, collegeID=0):
        TaskManager.__init__(self, tag, collegeID)
        self._allListImpll = AllTaskImpllNormal(tag, collegeID)
        self._doingImpll = DoingTaskImpllNormal(tag, collegeID)
        self._completedImpll = CompletedTaskImpllNormal(tag, collegeID)
        self._taskGettingImpll = TaskGettingImpllNotification(tag, collegeID)
        self._modifyStatusImpll = ModifyStatusImpllNormal(tag, collegeID)

    def pay(self, jsonParam):
        params = json.loads(jsonParam)
        tokenID = params['tokenID']
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return (False)

        taskID = params['taskID']
        price = params['price']

        sql = 'update workerTask set price = %s where taskID like \'%s\';' % (price, taskID)
        db = DataOperation()
        db.connect()
        (ret, reason) = db.operate(sql)
        db.close()
        return (ret, reason)
