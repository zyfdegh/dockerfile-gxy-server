# coding=utf8
import json
import sys
from src.tool.RYClient import RYClient

sys.path.append("..")
from tool.Util import Util
from tool.DataOperation import DataOperation
from merchandise.MerchandiseManager import MerchandiseManager


class OrderManager(Util):
    def __init__(self):
        pass

    # 创建order表
    def createOrder(self, jsonInfo):
        # 创建订单的时间
        createTime = self.getCurrentTime()
        # 生成订单的ID
        orderID = self.getMD5String(createTime)
        data = json.loads(jsonInfo)
        tokenID = data['tokenID']

        merchandiseID = data['merchandiseID']
        orderState = data['orderState']
        addressID = data['addressID']
        alipayID = data['alipayID']

        logisticsID = orderID
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return (False, None, None)

        # 买家ID通过tokenID来获取，卖家ID通过商品ID来获取
        buyerID = self.getUserIDByToken(tokenID)
        sellerID = self.getUserIDByMerchandiseID(merchandiseID)

        sql = 'insert into merchandiseOrder(orderID, createTime, orderState, sellerID, buyerID, logisticsID, merchandiseID, addressID)' \
              ' values(\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' % \
              (orderID, self.getCurrentTime(), orderState, sellerID, buyerID, logisticsID, merchandiseID, addressID)
        db = DataOperation()
        db.connect()
        db.operate(sql)
        db.close()
        return (orderID, buyerID, sellerID)

    # 通过商品ID获取卖家ID
    def getUserIDByMerchandiseID(self, merchandiseID):
        sql = 'select userID from merchandise where merchandiseID like \'%s\';' % merchandiseID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            db.close()
            return  False

        userID = cur.fetchone()

        db.close()

        if None == userID:
            return False

        return userID[0]

    # 查询order表
    def getOrderList(self, tokenID, action):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        userID = self.getUserIDByToken(tokenID)
        sql = 'select orderID, createTime, orderState, sellerID, buyerID, company, state, merchandiseOrder.merchandiseID, location,' \
              ' currentPrice, oldPrice, merchandiseName, info, imgpath.path from ' \
              ' merchandiseOrder, logistics, merchandise, imgPath where imgPath.merchandiseID = merchandiseOrder.merchandiseID and' \
              ' %s = \'%s\' and ' \
              ' merchandiseOrder.merchandiseID = merchandise.merchandiseID and logistics.logisticsID = merchandiseOrder.orderID ' \
              ' ;' % (action, userID)
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            db.close()
            return False
        allResult = cur.fetchall()
        db.close()

        listOrders = []
        tmp = {}
        for d in allResult:
            orderInfo = {}
            if d[7] not in tmp.keys():
                orderInfo['orderID'] = d[0]
                orderInfo['createTime'] = str(d[1])
                orderInfo['orderState'] =d[2]
                orderInfo['sellerID'] = d[3]
                orderInfo['buyerID'] = d[4]
                orderInfo['company'] = d[5]
                orderInfo['state'] = d[6]
                orderInfo['merchandiseID'] = d[7]
                orderInfo['location'] = d[8]
                orderInfo['currentPrice'] = d[9]
                orderInfo['oldPrice'] = d[10]
                orderInfo['merchandiseName'] = d[11]
                orderInfo['info'] = d[12]
                imgList = []
                imgList.append(d[13])
                orderInfo['imgPath'] = imgList
                tmp[d[7]] = imgList
                listOrders.append(orderInfo)
            else:
                tmp[d[7]].append(d[13])

        return listOrders

    # 获取我买到的
    def getMyBought(self, tokenID):
        return self.getOrderList(tokenID, 'buyerID')

    # 获取我卖出的
    def getMySold(self, tokenID):
        return self.getOrderList(tokenID, 'sellerID')

    # 改变order的状态
    def changeOrderState(self, status, tokenID, orderID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        userID = self.getUserIDByToken(tokenID)
        sql = "update merchandiseOrder set orderstate = \'%s\' where buyerID = \'%s\' and orderID like \'%s\';" % (status, userID, orderID)
        db = DataOperation()
        db.connect()
        db.operate(sql)

        db.close()
        return True

    # 删除订单
    # 只有在未付款状态下才能被删除
    def deleteOrder(self, tokenID, orderID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        sql = 'delete from merchandiseOrder where orderID like \'%s\';' % orderID
        db = DataOperation()
        db.connect()
        db.operate(sql)
        db.close()
        return True

    # 通过merchandiseID 获取订单详情
    def getOrderDetailByMerchandiseID(self, tokenID, merchandiseID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        sql = 'select merchandiseName, currentPrice, oldPrice, visitedCount, sellerID, postedMerchandise.info,' \
               ' publishedTime, swap, autoShipment, inspection, college, merchandiseTypeName, matching,' \
               ' recommendation, status, userInfo.userName, address.addressID, address.userID,' \
               ' address.userName, address.tel, address.description, orderID, orderState, alipayID from merchandiseOrder, ' \
               ' postedMerchandise, merchandiseType, userInfo, address ' \
               ' where merchandiseOrder.merchandiseID=postedMerchandise.merchandiseID and ' \
               ' postedMerchandise.merchandiseTypeID = merchandiseType.merchandiseTypeID and ' \
               ' address.addressID = merchandiseOrder.addressID and ' \
               ' merchandiseOrder.merchandiseID like \'%s\';' % merchandiseID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return cur
        info = cur.fetchone()
        sqlImg = 'select path from imgpath where merchandiseID like \'%s\';' % merchandiseID
        curImg = db.query(sqlImg)
        if None == curImg:
            db.close()
            return curImg
        imgPathall = curImg.fetchone()
        db.close()
        
        if None == info:
            return info
        #info = info[0]
        resultData = {}
        resultData['merchandiseName'] = info[0]
        resultData['currentPrice'] = info[1]
        resultData['oldPrice'] = info[2]
        resultData['visitedCount'] = info[3]
        resultData['sellerID'] = info[4]
        resultData['info'] = info[5]
        resultData['publishedTime'] = str(info[6])
        resultData['swap'] = info[7]
        resultData['autoShipment'] = info[8]
        resultData['inspection'] = info[9]
        resultData['college'] = info[10]
        resultData['merchandiseTypeName'] = info[11]
        resultData['matching'] = info[12]
        resultData['recommendation'] = str(info[13])
        resultData['status'] = info[14]
        resultData['userName'] = info[15]
        resultData['addressID'] = info[16]
        resultData['addressUserID'] = info[17]
        resultData['addressUserName'] = info[18]
        resultData['tel'] = info[19]
        resultData['addressDescription'] = info[20]
        resultData['orderID'] = info[21]
        resultData['orderState'] = info[22]
        resultData['alipayID'] = info[23]
        imgList = []
        resultData['imgPath'] = imgList
        for i in imgPathall:
            imgList.append(i)
        return resultData
        
    # 更新支付宝ID
    def changeAlipayID(self, tokenID, orderID, alipayID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        db = DataOperation()
        db.connect()
        sql = 'update merchandiseOrder set alipayID = \'%s\' where orderID like \'%s\';' % (alipayID, orderID)
        db.operate(sql)
        db.close()
        return True

    # 取消订单
    def CancelOrder(self, tokenID, orderID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        userID = self.getUserIDByToken(tokenID)
        sql = 'delete from merchandiseOrder where buyerID like \'%s\' and orderID like \'%s\';' % (userID, orderID)
        db = DataOperation()
        db.connect()
        db.operate(sql)
        db.close()
        return True
    #提醒发货
    def remindDelivery(self, tokenID, sellerID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        userID = self.getUserIDByToken(tokenID)
        ryClient = RYClient()
        ryClient.publishMessage(userID, sellerID, "亲，还不发货，您的客官都着急了，赶紧发货，不要偷懒哦！")
        return True


if __name__ == '__main__':
    info = {}
    info['orderState'] = 'paid'
    info['sellerID'] = '1234'
    info['buyerID'] = '12345'
    info['tokenID'] = '646877eb74094da28df1aef7ade08a02'
    info['merchandiseID'] = '7386a44372c74030612d644fa3d2f885'
    orderManager = OrderManager()
    orderManager.createOrder(json.dumps(info))
    # print orderManager.getOrderList('646877eb74094da28df1aef7ade08a02')
    # orderManager.changeOrderState('completed', '646877eb74094da28df1aef7ade08a02')
    # orderManager.deleteOrder('646877eb74094da28df1aef7ade08a02', '30f33d4750e3c0ff68fa08c9f7915fff')
