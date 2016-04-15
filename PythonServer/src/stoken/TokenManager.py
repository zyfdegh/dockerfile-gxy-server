# coding=utf8
import sys
sys.path.append("..")
from  datetime import *
import time
from tool.Util import Util
from tool.DataOperation import DataOperation
import json


class TokenManager(Util):
    def __init__(self):
        pass

    def createToken(self, userID):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        createTime = time.strftime(ISOTIMEFORMAT, time.localtime())
        tokenID = self.getMD5String(userID.join(createTime))
        sql1 = 'delete from token where userID like \'%s\';' % userID
        sql2 = 'insert into token values(\'%s\',\'%s\',\'%s\', %d);' % (tokenID, userID, createTime, 100)
        sqllist = [sql1, sql2]
        # sql.join('insert into stoken values(\'%s\',\'%s\',\'%s\', %d);' % (tokenID, userID,createTime, 100))
        db = DataOperation()
        db.connect()
        # db.operate(sql)
        db.multiOperate(sqllist)
        db.close()
        return tokenID

    def searchToken(self, tokenID):
        sql = 'select * from stoken where tokenID=\'%s\';' % tokenID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            db.close()
            return False

        # 判断token表中是否有这条记录,个数
        count = int(cur.rowcount)
        if count > 0:
            # 代表有这个token的记录
            db.close()
            return 1
        else:
            # 代表没有这个token的记录
            db.close()
            return 0
        db.close()

if __name__ == '__main__':
    m = TokenManager()
    #m.createToken('1234')
    print(m.isTokenValidity('646877eb74094da28df1aef7ade08a02'))
