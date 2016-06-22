# coding=utf8
import sys
import logging
sys.path.append('..')
import hashlib
import time
import json
from tool.DataOperation import DataOperation
class Util:
    def __init__(self):
        pass

    def getMD5String(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def getCurrentTime(self):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        currentTime = time.strftime(ISOTIMEFORMAT, time.localtime())
        return currentTime

    def datetimeToString(self, dateTime):
        ISOTIMEFORMAT = '%Y-%m-%d'
        currentTime = time.strftime(ISOTIMEFORMAT, dateTime)
        return str(currentTime)

    def getUserIDByToken(self,tokenID):
        sql = 'select userID from token where tokenID like \'%s\';' % tokenID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            return False
        result = cur.fetchone()
        db.close()
        if result == None:
            return False
        return result[0]

    def getUserNameByUserID(self,userID):
        sql = 'select userName from userInfo where userID like \'%s\';' %userID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            return False
        result = cur.fetchone()
        return result[0]

    def getUserIDByUserName(self,userName):
        sql = 'select userID from userInfo where userName like \'%s\';' %userName
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            return False
        result = cur.fetchone()
        return result[0]

    def isTokenValidity(self,tokenID):
        sql = 'select createtime from token where tokenID like \'%s\';' % tokenID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        createtime = cur.fetchone()
        if createtime == None:
            result = {}
            result['status'] = 'error'
            result['data'] = 'INVALID TOKENID'
            db.close()
	    logging.warning("Utils %s",result['status'])
            return json.dumps(result)
        else:
            sql = 'select timestampdiff(DAY,\'%s\',now());' % createtime
            cur = db.query(sql)
            timeDiff = cur.fetchone()
            db.close()
            result = {}
            result['status'] = 'success'
	    logging.warning("Utils %s",result['status'])
            if timeDiff[0] >= 30:
                result['data'] = False
                return json.dumps(result)
            else:
                result['data'] = True
                return json.dumps(result)
	logging.warning("Utils %s",result['status'])

    def generateID(self, value):
        currentTime = self.getCurrentTime()
        resultID = self.getMD5String(value.join(str(currentTime)))
        return resultID

if __name__ == '__main__':
    pass
