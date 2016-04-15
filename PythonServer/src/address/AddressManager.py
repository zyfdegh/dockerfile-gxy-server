# coding=utf8
import sys

sys.path.append("..")
from tool.Util import Util
from stoken.TokenManager import TokenManager
from tool.DataOperation import DataOperation
import json


class AddressManager(Util):
    def __init__(self):
        pass

    def createAddress(self, addressName, tokenID, tel, province, city, area, description, zipCode, isdefault, userName):

        # 客户端记录一下创建地址的ID 以便以后操作使用
        createtime = self.getCurrentTime()
        addressID = self.getMD5String(createtime)
        userID = self.getUserIDByToken(tokenID)
        db = DataOperation()
        db.connect()
        if userID == None:
            db.close()
            return None
        if isdefault == 1:
            sqltem = 'update address set isdefault = 0;'
            db.operate(sqltem)
        sql = 'insert into address(addressID,userID,addressName,tel,province,city,area,description,zipCode,isdefault,userName)' \
              ' values(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%s,\'%s\');' \
              ' ' % (
                  addressID, userID, addressName, tel, province, city, area, description, zipCode, isdefault, userName)

        db.operate(sql)
        db.close()
        # 传给客户端保存
        return addressID

    def editAddress(self, jsoninfo):
        result = json.loads(jsoninfo)
        addressName = result['addressName']
        addressID = result['addressID']
        tel = result['tel']
        province = result['province']
        city = result['city']
        area = result['area']
        description = result['description']
        zipCode = result['zipCode']
        isdefault = result['isdefault']
        tokenID = result['tokenID']
        userName = result['userName']
        # 首先判断一下这个token是否在有效期内
        tokenManager = TokenManager()
        res = json.loads(tokenManager.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            if isdefault == 1:
                sqltem = 'update address set isdefault = 0 where userID like \'%s\';' % userID
                db.operate(sqltem)

            sql = 'update address set addressName = \'%s\' , tel = \'%s\' , province = \'%s\' , city=\'%s\' ,area =\'%s\',description = \'%s\',' \
                  ' zipCode = \'%s\' , isdefault = %d, userName = \'%s\' where addressID like \'%s\' and userID like \'%s\';' % (
                      addressName, tel, province, city, area, description, zipCode, isdefault, userName, addressID, userID)
            db.operate(sql)
            db.close()
            return True
        else:
            return False

    # 设置为默认地址
    def setDefaultAddress(self, tokenID, addressID):
        # 首先判断一下这个token是否在有效期内
        tokenManager = TokenManager()
        res = json.loads(tokenManager.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            sqllist = []
            sqltemp = 'update address set isdefault = \'0\' where  userID like \'%s\';' % userID
            sql = 'update address set isdefault = \'1\' where addressID like \'%s\' and userID like \'%s\';' % (addressID,userID)
            sqllist.append(sqltemp)
            sqllist.append(sql)
            db.multiOperate(sqllist)
            db.close()
            return True
        else:
            return False

    # 查询默认地址详情
    def searchAddressDefaultDetail(self, tokenID):
        # 首先判断一下这个token是否在有效期内
        tokenManager = TokenManager()
        res = json.loads(tokenManager.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            sql = 'select addressID,userID,addressName,' \
                  'isDefault,province,city,area,description,zipCode,' \
                  'tel,userName from address where isdefault = 1 and userID like \'%s\';' % userID
            print sql
            cur = db.query(sql)
            if cur == None:
                db.close()
                return False
            info = cur.fetchone()
            if info == None:
                db.close()
                return None

            db.close()
            result = {}
            result['addressID'] = info[0]
            result['userID'] = info[1]
            result['addressName'] = info[2]
            result['isdefault'] = info[3]
            result['province'] = info[4]
            result['city'] = info[5]
            result['area'] = info[6]
            result['description'] = info[7]
            result['zipCode'] = info[8]
            result['tel'] = info[9]
            result['userName'] = info[10]
            return result
        else:
            return False

    def deleteAddress(self, tokenID, addressID):
        # 首先判断一下这个token是否在有效期内
        tokenManager = TokenManager()
        res = json.loads(tokenManager.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'delete from address where addressID like \'%s\';' % addressID
            (ret, reason) = db.operate(sql)
            db.close()
            return ret
        else:
            return False

    def searchAddress(self, tokenID):
        # 首先判断一下这个token是否在有效期内
        # tokenManager = TokenManager()
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            sql = 'select addressID,userID,addressName,' \
                  'isDefault,province,city,area,description,zipCode,' \
                  'tel,userName  from address where userID like \'%s\';' % userID
            cur = db.query(sql)
            if cur == None:
                db.close()
                return False

            resultlist = []
            for info in cur.fetchall():
                result = {}
                result['addressID'] = info[0]
                result['addressName'] = info[2]
                result['isdefault'] = info[3]
                result['province'] = info[4]
                result['city'] = info[5]
                result['area'] = info[6]
                result['description'] = info[7]
                result['zipCode'] = info[8]
                result['tel'] = info[9]
                result['userName'] = info[10]
                resultlist.append(result)
            db.close()
            return resultlist
        else:
            return False


if __name__ == '__main__':
    addressManager = AddressManager()
