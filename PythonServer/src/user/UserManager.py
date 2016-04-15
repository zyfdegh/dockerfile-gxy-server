# coding=utf8
import sys

sys.path.append("..")
from tool.Util import Util
from tool.DataOperation import DataOperation
from stoken.TokenManager import TokenManager
import json
import os
import unittest
import logging
from rong import ApiClient

app_key = "m7ua80gbuf2am"
app_secret = "3EyhxJXCKnMB"


class UserManager(Util):
    def __init__(self):
        os.environ.setdefault('rongcloud_app_key', app_key)
        os.environ.setdefault('rongcloud_app_secret', app_secret)
        logging.basicConfig(level=logging.INFO)
        self._ryapi = ApiClient()
        self._paths = 'http://121.43.111.75:5000/static/'

    def createUser(self, userID, userName, password, birthday, info, portrait, account, tel, email, gender):
        sql = 'insert into userinfo values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %f, \'%s\', \'%s\', %d);' % (
            userID, userName, password, birthday, info, portrait, account, tel, email, gender)
        db = DataOperation()
        db.connect()
        db.operate(sql)
        db.close()

    def getUserInfo(self, jsonInfo):
        params = json.loads(jsonInfo)
        tokenID = params['token']
        valid = self.isTokenValidity(tokenID)

        if 'error' == json.loads(valid)['status']:
            return (False, tokenID, tokenID)
        userID = self.getUserIDByToken(tokenID)
        return (True, tokenID, userID)

    def findPassWord(self,tel,pwd):
        db = DataOperation()
        db.connect()
        sqltel = 'select count(*) from userinfo where tel like \'%s\';' % tel
        cur = db.query(sqltel)
        #表明该用户并未注册，所以不存在找回密码
        if(cur == None):
            db.close()
            return False
        count = cur.fetchone()[0]
        #如果存在这个用户，就修改该条数据中的密码
        if(count > 0):
            sqlfind = 'update userinfo set password = \'%s\' where tel like \'%s\';' % (pwd,tel)
            db.operate(sqlfind)
            db.close()
            return True
    def createUserQuickly(self, tel, pwd):
        db = DataOperation()
        db.connect()
        sqltel = 'select count(*) from userinfo where tel like \'%s\';' % tel
        cur = db.query(sqltel)
        if cur == None:
            db.close()
            return False
        count = cur.fetchone()[0]
        # 说明这个手机号已经存在，不能重复注册
        if count > 0:
            db.close()
            return False
        userID = self.getMD5String(tel)
        userName = tel[0:3] + '****' + tel[-4:]
        portrait = 'default_portrait.png'
        sql = 'insert into userinfo(userID, password, tel, userName, portraitPath) values(\'%s\',\'%s\',\'%s\', \'%s\', \'%s\');' % (userID, pwd, tel, userName, portrait)
        db.operate(sql)
        db.close()
        return userID

    # 根据电话和密码来查找用户是否存在
    def searchUser(self, tel, pwd):
        userID = self.getMD5String(tel)
        sql = 'select userID,userName,portraitPath,tel from userinfo where userID like \'%s\' and password like \'%s\';' % (
            userID, pwd)
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            db.close()
            return (False, None, None)

        resultData = cur.fetchone()
        db.close()
        if None == resultData:
            return (False, None, None)

        # 判断用户表中是否有这条记录,个数
        count = int(cur.rowcount)
        if count > 0:
            # 代表有这个用户的记录
            userID = resultData[0]
            userName = resultData[1]
            portraitPath = resultData[2]
            # tel = resultData[3]
            ryToken = self.getRYToken(userID, userName, self._paths + portraitPath)
            return (1, userID, ryToken)
        else:
            # 代表没有这个用户的记录
            return (0, None, None)

    #通过UserID获取用户详细信息
    def getUserDetailInfoByUserID(self, userID, tokenID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        sql = 'select userName, birthday, info, portraitPath, account, tel, email, gender, residence '\
              'from userinfo where userID like \'%s\';' % userID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return cur
        data = cur.fetchone()
        db.close()
        if None == data:
            return data
        userInfo = {}
        userInfo['userName'] = data[0]
        userInfo['birthday'] = str(data[1])
        userInfo['info'] = data[2]
        userInfo['portraitPath'] = data[3]
        userInfo['account'] = data[4]
        userInfo['tel'] = data[5]
        userInfo['email'] = data[6]
        userInfo['gender'] = data[7]
        userInfo['residence'] = data[8]
        return userInfo

    def getRYToken(self, userID, name, portait):
        action = 'user/getToken'
        params = {}
        params['userId'] = userID
        params['name'] = name
        params['portraitUri'] = portait
        # print(json.dumps(params))
        return self._ryapi.user_get_token(userID, name, portait)
        # return self._ryapi.call_api(action, json.dumps(params))

    # 根据tokenID和userID来查询用户的详细信息
    def getUserDetail(self, tokenID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            sql = 'select userID,userName,birthday,info,portraitPath,account,tel,email,gender,residence from userinfo where userID like \'%s\';' % userID
            # cur.fetchone()--->内容如下
            # ('202cb962ac59075b964b07152d234b70', 'anthow', '123', None, 'student', 'D_pic.jpg2015-07-09 20:20:17', None, '15062225371', None, 1)
            cur = db.query(sql)
            if cur == None:
                db.close()
                return False

            allinfo = cur.fetchone()
            result = {}
            result['userID'] = allinfo[0]
            result['userName'] = allinfo[1]
            result['birthday'] = str(allinfo[2])
            result['info'] = allinfo[3]
            result['portraitPath'] = allinfo[4]
            result['account'] = allinfo[5]
            result['tel'] = allinfo[6]
            result['email'] = allinfo[7]
            result['gender'] = allinfo[8]
            result['residence'] = allinfo[9]
            db.close()
            return result
        else:
            return False

    # 编辑个人资料 返回上传照片的路径并保存到本地文件夹下
    def editUserInfo(self, jsonInfo, filename, isfile):
        # 解析json获取数据
        result = json.loads(jsonInfo)
        gender = result['gender']
        userName = result['userName']
        info = result['info']
        tokenID = result['tokenID']
        residence = result['residence']

        # 首先判断一下这个token是否在有效期内
        tokenManager = TokenManager()
        res = json.loads(tokenManager.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)

            db = DataOperation()
            db.connect()

            if isfile == '0':
                sql = 'update userinfo set gender = %d,userName = \'%s\', info = \'%s\',residence=\'%s\' where userID like \'%s\';' % \
                      (gender, userName, info, residence, userID)
                db.operate(sql)
                db.close()
                return True
            sql = 'update userinfo set portraitPath = \'%s\' ,gender = %d,userName = \'%s\', info = \'%s\',residence=\'%s\' where userID like \'%s\';' % \
                  (filename, gender, userName, info, residence, userID)
            db.operate(sql)
            db.close()
            return True
        else:
            return False

    # 获取账户余额
    def getAccount(self, tokenID):
        tokenManager = TokenManager()
        res = json.loads(tokenManager.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            sql = 'select account from userinfo where userID like \'%s\';' % userID
            db = DataOperation()
            db.connect()
            cur = db.query(sql)
            if None == cur:
                db.close()
                return False
            accountNum = cur.fetchone()

            db.close()
            return accountNum[0]

        return False

    # 修改账户余额
    def setAccount(self, tokenID, account):
        tokenManager = TokenManager()
        res = json.loads(tokenManager.isTokenValidity(tokenID))

        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            sql = 'update userinfo set account = \'%s\' where userID like \'%s\';' % (account, userID)
            db = DataOperation()
            db.connect()
            db.operate(sql)
            db.close()
            return True

        return False


if __name__ == '__main__':
    m = UserManager()
    # m.createUser('123dddddd', '朱世杰', '12dddd34', '1991-03-15', 'good', './img.png', 15.4, '15062225371',
    #             'ci20083333@126.com', 0)
    # m.searchUser('15062225371','12dddd34')
    # m.createUserQuickly('111','111')
    # sqltem = 'select userName , portraitPath from userinfo where userID like \'%s\';' % '1234'
    # db = DataOperation()
    # db.connect()
    # cur = db.query(sqltem)
    # print  cur.fetchall()[0]
    # print  m.getRYToken('53f6dd617c1d318face609dfb563ad48', 'aaaa', 'http://www.rongcloud.cn/images/logo.png')
