# coding=utf8
import sys

sys.path.append("..")

from tool.RYClient import RYClient
from tool.Util import Util
from tool.DataOperation import DataOperation
from stoken.TokenManager import TokenManager
import json
import os
import unittest
import logging
from rong import ApiClient

app_key = "vnroth0krcwoo"
app_secret = "Ip5p2uLTIhV"

class WokerManager(Util):
    def __init__(self, adminID = None, adminPW = None):
        os.environ.setdefault('rongcloud_app_key', app_key)
        os.environ.setdefault('rongcloud_app_secret', app_secret)
        logging.basicConfig(level=logging.INFO)
        self._ryapi = ApiClient()
        self._paths = 'http://121.43.111.75:5000/static/'
        self._adminID = adminID
        self._adminPW = adminPW

    # 创建一个工作人员账户
    def createWorker(self, tel, pwd):

        db = DataOperation()
        db.connect()
        sqlAdmin = 'select adminID, adminPW from adminInfo where adminID like \'%s\' and adminPW like \'%s\';' % (self._adminID, self._adminPW)
        curAdmin = db.query(sqlAdmin)
        if None == curAdmin:
            db.close()
            return None
        adminInfo = curAdmin.fetchone()
        # 管理员密码错误
        if None == adminInfo or len(adminInfo<=0):
            db.close()
            return None

        sqltel = 'select count(*) from worker where tel like \'%s\';' % tel
        cur = db.query(sqltel)
        #查找数据库失败
        if cur == None:
            db.close()
            return False
        count = cur.fetchone()[0]
        #数据库中已存在该号码，说明已被注册过，故不能重复注册
        if count > 0:
            db.close()
            return False
        workerID = self.getMD5String(tel)
        workerName = tel[0:3] + '****' + tel[-4:]
        portraitPath = 'default_portrait.png'
        sql = 'insert into worker(workerID,password,tel,workerName,portraitPath) values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');' %(workerID,pwd,tel,workerName,portraitPath)
        db.operate(sql)
        db.close()
        return workerID
        
    # 更新工作人员账户信息
    def updateWorkerInfo(self, workInfo):
        jsoninfo = json.loads(workInfo)
        workerID = jsoninfo['workerID']
        workerName = jsoninfo['workerName']
        workerTag = jsoninfo['workerTag']
        superior = jsoninfo['superior']
        birthday = jsoninfo['birthday']
        info = jsoninfo['info']
        portraitPath = jsoninfo['portraitPath']
        account = jsoninfo['account']
        tel = jsoninfo['tel']
        email = jsoninfo['email']
        gender = jsoninfo['gender']
        residence = jsoninfo['residence']
        area = jsoninfo['area']
        primary = jsoninfo['primary']

        db = DataOperation()
        db.connect()

        sqlAdmin = 'select adminID, adminPW from adminInfo where adminID like \'%s\' and adminPW like \'%s\';' % (self._adminID, self._adminPW)
        curAdmin = db.query(sqlAdmin)
        if None == curAdmin:
            db.close()
            return None
        adminInfo = curAdmin.fetchone()
        # 管理员密码错误
        if None == adminInfo or len(adminInfo<=0):
            db.close()
            return None

        sql0 = 'select * from worker where tel like \'%s\'' % tel
        cur = db.query(sql0)
        allinfo = cur.fetchone()
        if None == allinfo:
            db.close()
            return False
        if 0 == allinfo[0]:
            db.close()
            return False

        sql = 'updata worker set workerName = \'%s\',workerTag = \'%s\',superior = \'%s\','\
        'birthday= \'%s\',info = \'%s\',portraitPath = \'%s\','\
        'account = \'%s\',tel = \'%s\',email = \'%s\',gender = \'%s\',residence = \'%s\',area = \'%s\',primary = \'%s\' where workerID like \'%s\';'%\
        (workerName,workerTag,superior,birthday,info,portraitPath,account,tel,email,gender,residence,area,primary,workerID)

        db.operate(sql)
        db.close()
        return True
        
    # 删除工作人员信息
    def deleteWorker(self, tel):
        db = DataOperation()
        db.connect()
        sqlAdmin = 'select adminID, adminPW from adminInfo where adminID like \'%s\' and adminPW like \'%s\';' % (self._adminID, self._adminPW)
        curAdmin = db.query(sqlAdmin)
        if None == curAdmin:
            db.close()
            return None
        adminInfo = curAdmin.fetchone()
        # 管理员密码错误
        if None == adminInfo or len(adminInfo<=0):
            db.close()
            return None
        sql0 = 'select count(*) from worker where tel like \'%s\';' % tel

        cur = db.query(sql0)
        a = cur.fetchone()
        if a == None:
            db.close()
            return False
        if a[0] == 0:
            db.close()
            return False
        
        sql1 = 'delete from worker where tel like \'%s\';' % tel
        db.operate(sql1)
        db.close()
        return True
        
    # 查询工作人员信息
    def searchWorker(self, tel, passwd):
        db = DataOperation()
        db.connect()
        sqltel = 'select workerID, workerName, password, workerTag, superior, birthday, info, portraitPath, account, tel, ' \
                 'email, gender, residence, area from worker where tel like \'%s\' and password like \'%s\';' % (tel, passwd)
        cur = db.query(sqltel)

        allinfo = cur.fetchone()
        if allinfo == None:
            db.close()
            return (False, None, None)
        if len(allinfo) == 0:
            db.close()
            return (None, None, None)

        ryClinet = RYClient()
        ryTokenID = ryClinet.getRYToken(allinfo, allinfo[1], allinfo[7]);
        result = {}
        result['workerID'] = allinfo[0]
        result['workerName'] = allinfo[1]
        # result['password'] = allinfo[2]
        result['workerTag'] = allinfo[3]
        result['superior'] = allinfo[4]
        result['birthday'] = str(allinfo[5])
        result['info'] = allinfo[6]
        result['portraitPath'] = allinfo[7]
        result['account'] = allinfo[8]
        result['tel'] = allinfo[9]
        result['email'] = allinfo[10]
        result['gender'] = allinfo[11]
        result['residence'] = allinfo[12]
        result['area'] = allinfo[13]
        db.close()
        workerID = allinfo[0]
        return (workerID, ryTokenID, result)

    #设置上级领导        telup:上级的电话号码，telmy自己的电话号码
    def setSuperior(self,telup,telmy):
        if telmy == telup:
            return False
        db = DataOperation()
        db.connect()

        sql0 = 'select count(*) from worker where tel like \'%s\';'%telmy
        cur = db.query(sql0)
        a = cur.fetchone()
        if a == None:
            db.close()
            return False
        if a[0] == 0:
            db.close()
            return False
        sql = 'update worker set superior = \'%s\' where tel like \'%s\';'%(telup,telmy)
        db.operate(sql)
        db.close()
        return True


if __name__ == '__main__':
    w = WokerManager('123','123')
    print w.searchWorker('11111')
    #print w.deleteWorker('11111')
