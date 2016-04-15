# coding=utf8
import sys

sys.path.append('..')
from tool.DataOperation import DataOperation
from tool.Util import Util
import json
from tool.RYClient import RYClient

class ExpressManager(Util):
    def __init__(self):
        pass

    def createExpress(self, jsonExpressInfo):

        expressInfo = json.loads(jsonExpressInfo)
        tokenID = expressInfo['tokenID']

        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        userID = self.getUserIDByToken(tokenID)

        tel = expressInfo['tel']
        expressCompany = expressInfo['expressCompany']
        collegeID = expressInfo['collegeID']
        # 送货地址
        expressAddress = expressInfo['expressAddress']
        receiver = expressInfo['receiver']
        expressName = expressInfo['expressName']
        # 拿货地址
        expressGetAddress = expressInfo['expressGetAddress']
        # 送货时间
        takeTime = expressInfo['takeTime']
        # 取货时间
        getTime = expressInfo['getTime']

        publishedTime = self.getCurrentTime()
        # logisticsID = expressInfo['logisticsID']

        expressID = self.generateID(str(expressName).join(tel))
        sql = 'insert into expressinfo(expressID, expressName, userID, receiver,' \
              ' tel, collegeID, expressAddress, publishedTime, logisticsID, expressGetAddress, expressCompany, takeTime, getTime)' \
              ' values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\',\'%s\',\'%s\',\'%s\',\'%s\', \'%s\', \'%s\', \'%s\');' % \
              (expressID, expressName, userID, receiver, tel, collegeID, expressAddress,
               publishedTime, 
               expressID, 
               expressGetAddress, 
               expressCompany, 
               str(takeTime),
               getTime)

        db = DataOperation()
        db.connect()
        db.operate(sql)

        db.close()

        return expressID

    def deleteExpressInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        expressID = info['expressID']
        tag = info['tag']
        # 0代表代拿，1代表代发
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        if tag == '0':
            sql = 'delete from expressinfo where expressID like \'%s\';' % expressID
        elif tag == '1':
            sql = 'delete from expresspost where expressPostID like \'%s\';' % expressID
        db = DataOperation()
        db.connect()
        db.operate(sql)

        db.close()
        return True

    # 快递查询
    def searchExpress(self, tokenID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            # sql = 'select * from expressinfo where userID like \'%s\';' % userID
            sql = 'select expressAll.expressID, tel, logisticsID, publishedTime, collegeID, expressNum, userName ,tag, takeTime, expressStatusID, companyName' \
                  ' from expressAll, expressState, logisticsCompany' \
                  ' where expressAll.expressID = expressState.expressID '\
                  ' and logisticsCompany.logisticsCompanyID = expressAll.expressCompany and userID like' \
                  ' \'%s\';' % userID
            cur = db.query(sql)
            if cur == None:
                db.close()
                return False

            resultlist = []
            for info in cur.fetchall():
                result = {}
                result['expressID'] = info[0]
                result['tel'] = info[1]
                result['logisticsID'] = info[2]
                result['publishedTime'] = str(info[3])
                result['collegeID'] = info[4]
                result['expressNum'] = info[5]
                result['userName'] = info[6]
                result['tag'] = info[7]
                result['takeTime'] = str(info[8])
                result['expressStatusID'] = info[9]
                result['expressName'] = info[10]
                resultlist.append(result)
            db.close()
            return resultlist
        else:
            return False

    # 发布快递代发
    def createExpressPost(self, jsonExpressInfo):
        expressInfo = json.loads(jsonExpressInfo)
        tokenID = expressInfo['tokenID']
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        userID = self.getUserIDByToken(tokenID)
        expressPostName = expressInfo['expressName']
        tel = expressInfo['tel']
        expressPostID = self.generateID(tel)
        userName = expressInfo['userName']
        # expressCompany = expressInfo['expressCompany']
        collegeID = expressInfo['collegeID']
        receiverCity = expressInfo['receiverCity']
        isOverWeight = expressInfo['isOverWeight']
        addressInfo = expressInfo['addressInfo']
        takeTime = expressInfo['takeTime']
        publishedTime = str(self.getCurrentTime())

        sql = 'insert into expressPost(expressPostID, userName, tel, collegeID, receiverCity,' \
              'isOverWeight, addressInfo, publishedTime, userID, logisticsID, takeTime, expressCompany)' \
              ' values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', %s, \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' % \
              (expressPostID, userName, tel, collegeID, receiverCity, isOverWeight, addressInfo, publishedTime,
               userID, expressPostID, takeTime, '0')
        db = DataOperation()
        db.connect()
        db.operate(sql)
        db.close()
        return expressPostID

    # 删除快递代发
    def deleteExpressPost(self, tokenID, expressPostID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'delete from expressPost where expressPostID like \'%s\';' % expressPostID
            db.operte(sql)
            db.close()
            return True
        else:
            return False

    # 修改快递代发信息
    def updateExpressPostInfo(self, jsonExpressInfo):
        expressinfo = json.loads(jsonExpressInfo)
        tokenID = expressinfo['tokenID']
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            expressPostID = expressinfo['expressPostID']
            userName = expressinfo['userName']
            tel = expressinfo['tel']
            # expressCompany = expressinfo['expressCompany']
            collegeID = expressinfo['collegeID']
            receiverCity = expressinfo['receiverCity']
            isOverWeight = expressinfo['isOverWeight']
            addressInfo = expressinfo['addressInfo']
            publishedTime = expressinfo['publishedTime']
            takeTime = expressinfo['takeTime']
            sql = 'update expressPost set userName = \'%s\',tel = \'%s\',collegeID=\'%s\',receiverCity=\'%s\',isOverWeight = %d , addressInfo = \'%s\' ' \
                  ' takeTime = \'%s\' where expressPostID like \'%s\';' % (
                userName, tel, collegeID, receiverCity, isOverWeight, addressInfo, publishedTime, expressPostID, str(takeTime))
            db.operte(sql)
            db.close()
            return True
        else:
            return False

    # 查询快递代发信息列表
    def getExressAllList(self, tokenID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            sql = 'select expressID, publishedTime, tel, logisticsID, expressCompany, expressNum, userName, tag, collegeID, takeTime' \
                  ' from expressAll where userID like \'%s\';' % userID
            db = DataOperation()
            db.connect()
            cur = db.query(sql)
            if None == cur:
                db.close()
                return False
            allResult = cur.fetchall()

            resultlist = []
            for i in list(allResult):
                result = {}
                result['expressID'] = i[0]
                result['publishedTime'] = str(i[1])
                result['tel'] = i[2]
                result['logisticsID'] = i[3]
                result['expressCompany'] = i[4]
                result['expressNum'] = i[5]
                result['userName'] = i[6]
                result['tag'] = i[7]
                result['collegeID'] = i[8]
                result['takeTime'] = i[9]
                resultlist.append(result)
            db.close()
            return resultlist
        else:
            return False

    # 查询快递代发详情
    def getExpressPostInfo(self, tokenID, expressPostID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'select expressPostID,userName,tel,expressCompany,receiverCity,' \
                  'isOverWeight,addressInfo,publishedTime,userID,logisticsID,expressNum,takeTime,' \
                  ' logisticsCompany.companyName, cityName' \
                  ' from expresspost, logisticsCompany, city  where ' \
                  ' expressPost.expressCompany = logisticsCompany.logisticsCompanyID and '\
                  ' expressPost.receiverCity = city.cityID and expressPostID like \'%s\';' % expressPostID
            cur = db.query(sql)
            if None == cur:
                db.close()
                return False
            result = cur.fetchone()
            if None == result:
                db.close()
                return False
            res = {}
            res['expressPostID'] = result[0]
            res['userName'] = result[1]
            res['tel'] = result[2]
            res['expressCompany'] = result[12]
            res['receiverCity'] = result[13]
            res['isOverWeight'] = result[5]
            res['addressInfo'] = result[6]
            res['publishedTime'] = str(result[7])
            res['userID'] = result[8]
            res['logisticsID'] = result[9]
            res['expressNum'] = result[10]
            res['takeTime'] = str(result[11])
            if None == res['expressNum']:
                res['companyName'] = 'NULL'
            else:
                sqlComName = 'select companyName from logistics, logisticsCompany where' \
                             ' logistics.logisticsCompanyID = logisticsCompany.logisticsCompanyID' \
                             ' and logistics.logisticsNum like \'%s\';' % res['expressNum']
                curComName = db.query(sqlComName)
                if None == curComName:
                    res['companyName'] = 'NULL'
                else:
                    companyName = curComName.fetchone()
                    if None == companyName:
                        res['companyName'] = 'NULL'
                    else:
                        res['companyName'] = companyName

            #res['companyName'] = result[11]
            db.close()
            return res
        else:
            return False

    # 查询快递代拿详情
    def getExpressGetInfo(self, tokenID, expressGetID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()

            sql = 'select expressName,userID,receiver,tel,expressCompany,expressAddress,' \
                  ' expressNum,publishedTime,expressInfo.logisticsID,expressGetAddress,companyName,expressInfo.collegeID,expressInfo.takeTime '\
                  ' from expressInfo,logisticsCompany,logistics where logistics.logisticsID = expressInfo.logisticsID' \
                  ' and logistics.logisticsCompanyID = logisticsCompany.logisticsCompanyID ' \
                  ' and expressID like \'%s\';' % expressGetID
            cur = db.query(sql)
            if None == cur:
                db.close()
                return cur
            result = cur.fetchone()
            if result == None:
                pass
            res = {}
            res['expressName'] = result[0]
            res['userID'] = result[1]
            res['receiver'] = result[2]
            res['tel'] = result[3]
            res['expressCompany'] = result[4]
            res['expressAddress'] = result[5]
            res['expressNum'] = result[6]
            res['publishedTime'] = str(result[7])
            res['logisticsID'] = result[8]
            res['expressGetAddress'] = result[9]
            res['companyName'] = result[10]
            res['collegeID'] = result[11]
            res['takeTime'] = str(result[12])
            db.close()
            return res
        else:
            return False

    # 增加单号(从订单里面进的)
    def createLogisticsNo1(self, tokenID, expressCompany, expressnum, orderID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            # 通过orderID查询logisticsID
            sqltemp = 'select logisticsID from  merchandiseorder where orderID like \'%s\';' % orderID
            curtemp = db.query(sqltemp)
            if None == curtemp:
                db.close()
                return False
            logisticsID = curtemp.fetchone()[0]
            # 通过logisticsID更新快递表的单号
            sql = 'update logistics set company = \'%s\' , logisticsnum = \'%s\' where logisticsID like \'%s\';' % (
                expressCompany, expressnum, logisticsID)

            sqlMsg = 'select buyerID, sellerID from merchandiseOrder where orderID like \'%s\';' % orderID
            curMsg = db.query(sqlMsg)
            if None != curMsg:
                retMsg = curMsg.fetchone()
                if None != retMsg:
                    buyerID = retMsg[0]
                    sellerID = retMsg[1]
                    ryClient = RYClient()
                    ryClient.publishMessage(sellerID, buyerID, "您的商品已经发货，请及时查看。快递单号 %s " % expressnum)

            db.operate(sql)
            db.close()
            return True
        else:
            return False

    # 增加单号(从快递代发进的)
    def createLogisticsNo2(self, tokenID, expressCompany, expressnum, expressPostID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            # 通过expressPostID查询logisticsID
            sqltemp = 'select logisticsID from  expresspost where  expressPostID like \'%s\';' % expressPostID
            curtemp = db.query(sqltemp)
            if None == curtemp:
                db.close()
                return False
            logisticsID = curtemp.fetchone()[0]

            sql = 'update expresspost, logistics set expresspost.expressCompany = \'%s\', expresspost.expressnum = \'%s\' ,logistics.company = \'%s\', ' \
                  'logistics.logisticsnum = \'%s\' where expresspost.logisticsID like \'%s\' and logistics.logisticsID like \'%s\'' % (
                      expressCompany, expressnum, expressCompany, expressnum, logisticsID, logisticsID)
            db.operate(sql)
            db.close()
            return True
        else:
            return False

    # 查询快递的状态
    def searchLogistics(self, orderID, tokenID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'select merchandise.merchandiseID, merchandiseName, currentPrice, path, logisticsNum, companyName, abbr, logisticsCompany.imgPath' \
                  ' from merchandise, imgPath, merchandiseOrder,logistics, logisticsCompany '\
                  ' where merchandise.merchandiseID = imgPath.merchandiseID '\
                  ' and merchandise.merchandiseID = merchandiseOrder.merchandiseID' \
                  ' and merchandiseOrder.logisticsID = logistics.logisticsID' \
                  ' and logistics.company = logisticsCompany.logisticsCompanyID '\
                  ' and orderID like \'%s\';' % orderID
            cur = db.query(sql)
            if None == cur:
                db.close()
                return None
            resultData = cur.fetchall()
            logistics ={}
            img = []
            for l in resultData:
                if len(img) <= 0:
                    logistics['merchandiseID'] = l[0]
                    logistics['merchandiseName'] = l[1]
                    logistics['currentPrice'] = l[2]
                    img.append(l[3])
                    logistics['merchandiseImgPath'] = img
                    logistics['logisticsNum'] = l[4]
                    logistics['companyName'] = l[5]
                    logistics['abbr'] = l[6]
                    logistics['logisticsCompanyImgPath'] = l[7]
                else:
                    img.append(l[3])
            db.close()
            return logistics

        else:
            return False

    # 查询快递公司信息
    def getLogisticsCompanyInfo(self):
        sql = 'select logisticsCompanyID, companyName, abbr, imgpath from logisticsCompany'
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return cur
        allResult = cur.fetchall()
        db.close()
        companys = []
        for l in allResult:
            info = {}
            info['companyID'] = l[0]
            info['companyName'] = l[1]
            info['abbr'] = l[2]
            info['imgPath'] = l[3]
            companys.append(info)
        return companys

    # 设置快递状态
    def setExpressStatus(self, jsonInfo):
        info = json.loads(jsonInfo)
        expressID = info['expressID']
        expressStatusID = info['expressStatusID']
        tokenID = info['tokenID']
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            #sql = 'insert into expressState(expressID, expressStatusID, modifyTime) values (\'%s\', \'%s\', now())' % \
            #      (expressID, expressStatusID)
            sql = 'update expressState set expressStatusID = \'%s\', modifyTime = now()' \
                  ' where expressID like \'%s\';' % (expressStatusID, expressID)
            db.operate(sql)
            db.close()
            return True
        return False

    # 获取快递状态
    def getExpressStatus(self, jsonInfo):
        info = json.loads(jsonInfo)
        expressID = info['expressID']
        tokenID = info['tokenID']
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'select expressID, expressStatusID, modifyTime from expressState where expressID like \'%s\';' % expressID
            cur = db.query(sql)
            if None == cur:
                db.close()
                return cur
            status = cur.fetchone()
            db.close()
            if None == status:
                return status

            resultData = {}
            resultData['expressID'] = status[0]
            resultData['expressStatusID'] = status[1]
            resultData['modifyTime'] = str(status[2])

            return resultData
        return None



if __name__ == '__main__':
    m = ExpressManager()
    tokenID = '646877eb74094da28df1aef7ade08a02'
    expressGetID = '1f26082a3290df024a19cba8c4c65fad'
    orderID = 'bb8aed1fe0c73413b4dcad17be37fbf1'
    j = '{\"tel\": \"15062225371\", \"expressCompany\": \"Shunfeng\", \"expressID\": \"123\", \"userID\": \"1234\", \"expressAddress\": \"South Gate\", \"receiver\": \"zero\", \"expressName\": \"First\"}'
    j = '{\"tel\": \"15062225371\", \"expressCompany\": \"yuantong\",\"expressAddress\": \"Nanjing\", \"receiver\": \"zero\", \"expressName\": \"First\",\"tokenID\":\"c09bd67618d0eafda928f07280dd4cdc\"}'
    # info = m.searchExpress(tokenID)
    userID = m.getUserIDByToken(tokenID)
    # print userID
    # info = m.getExpressDetailInfo('6dfd070a615d8fc69c8f80e4ce9667a9', 'aefa6595d828f298990db7b4f4b40b0c')
    # res = {}
    # res['status'] = 'SUCCESS'
    # res['data'] = info
    # print json.dumps(res)
    # print info
    # print m.getExpressGetInfo(tokenID, expressGetID)
    # m.createLogisticsNo1(tokenID, 'shenfeng', '111110', 'dff7daa611569c91f37d6e520d95a11f')
    m.searchLogistics(orderID, tokenID)
