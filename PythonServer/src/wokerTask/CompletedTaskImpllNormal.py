# coding=utf8
import json
import sys
sys.path.append("..")

from CompletedTaskImpll import CompletedTaskImpll
from tool.DataOperation import DataOperation


class CompletedTaskImpllNormal(CompletedTaskImpll):
    def __init__(self, tag, collegeID):
        CompletedTaskImpll.__init__(self, tag, collegeID)

    def getCompletedTaskList(self, tokenID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        workerID = self.getUserIDByToken(tokenID)
        sql = 'select taskID, workerID, status, userName, userTel, takeTime, toAddress, fromTime, fromAddress  from workerTask where tag = %d and ' \
              ' collegeID like \'%s\' and status like \'%s\' and workerID like \'%s\';' % (self._tag, self._collegeID, self._status, workerID)
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return cur
        allResult = cur.fetchall()
        db.close()
        taskList = []
        for t in allResult:
            task = {}
            task['taskID'] = t[0]
            task['workerID'] = t[1]
            task['status'] = t[2]
            task['userName'] = t[3]
            task['userTel'] = t[4]
            task['takeTime'] = str(t[5])    # post:取货时间,inspection:验货时间,get:送货时间
            task['toAddress'] = t[6]        # 送货地点
            task['fromTime'] = t[7]         # 取货时间
            task['fromAddress'] = t[8]      # 取货地点，验货地点
            taskList.append(task)

        return taskList
