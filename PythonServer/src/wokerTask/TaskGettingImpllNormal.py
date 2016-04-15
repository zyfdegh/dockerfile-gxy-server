# coding=utf8
import json
import sys

sys.path.append("..")

from wokerTask.TaskGettingImpll import TaskGettingImpll
from tool.DataOperation import DataOperation


class TaskGettingImpllNormal(TaskGettingImpll):

    def getTask(self, tokenID, taskID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        workerID = self.getUserIDByToken(tokenID)
        sql = 'update workerTask set workerID = \'%s\' where taskID like \'%s\';' % (workerID, taskID)
        db = DataOperation()
        db.connect()
        db.operate(sql)
        db.close()
        return True