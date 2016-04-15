# coding=utf8
import json
import sys

sys.path.append("..")

from TaskGettingImpll import TaskGettingImpll
from tool.RYClient import RYClient
from tool.DataOperation import DataOperation


class TaskGettingImpllNotification(TaskGettingImpll):
    def __init__(self, tag, collegeID):
        TaskGettingImpll.__init__(self, tag, collegeID)

    def getTask(self, tokenID, taskID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        workerID = self.getUserIDByToken(tokenID)
        sql = 'update workerTask set workerID = \'%s\', status = \'1\' where taskID like \'%s\';' % (workerID, taskID)
        db = DataOperation()
        db.connect()
        sqlUserID = 'select userID from workerTask where taskID like \'%s\';' % taskID
        cur = db.query(sqlUserID)
        if None != cur:
            userID = cur.fetchone();
            if None != userID:
                userID = userID[0]
                ryClient = RYClient()
                ryClient.publishMessage(workerID, userID, "您的 %s 服务,编号： %s ,已经被工作人员 %s 抢单，正在派送中" % (self._tagDic[self._tag], taskID, userID))

        db.operate(sql)
        db.close()
        return True


