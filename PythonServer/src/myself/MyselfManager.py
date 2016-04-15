# coding=utf8
import json
import sys

sys.path.append("..")
from tool.Util import Util
from tool.DataOperation import DataOperation
from merchandise.MerchandiseManager import MerchandiseManager
from requirement.RequirementManager import RequirementManager
from favorite.FavoriteManager import FavoriteManager
from express.ExpressManager import ExpressManager


class MyselfManager(Util):
    def __init__(self):
        pass

    def getCount(self, tokenID, sql):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            cur = db.query(sql)
            if cur == None:
                db.close()
                return False

            count = cur.fetchone()[0]
            db.close()
            return count
        else:
            return False

    # 获取对应的数量
    # 获取我发布的数量
    def getMyPostCount(self, tokenID):
        userID = self.getUserIDByToken(tokenID)
        sql = 'select count(*) from postedmerchandise where userID like \'%s\';' % userID
        return self.getCount(tokenID, sql)

    # 获取我卖出的数量
    def getMySoldCount(self, tokenID):
        userID = self.getUserIDByToken(tokenID)
        sql = 'select count(*) from merchandiseOrder where buyerID like \'%s\';' % userID
        return self.getCount(tokenID, sql)

    # 获取我买到的数量
    def getMyBought(self, tokenID):
        userID = self.getUserIDByToken(tokenID)
        sql = 'select count(*) from merchandiseOrder where sellerID like \'%s\';' % userID
        return self.getCount(tokenID, sql)

    # 获取我需求的数量
    def getMyRequirementCount(self, tokenID):
        userID = self.getUserIDByToken(tokenID)
        sql = 'select count(*) from requirement where userID like \'%s\';' % userID
        return self.getCount(tokenID, sql)

    # 获取我快递服务的数量
    def getMycourierCount(self, tokenID):
        userID = self.getUserIDByToken(tokenID)
        sql = 'select count(*) from logictics where userID like \'%s\';' % userID
        return self.getCount(tokenID, sql)

    # 获取我的收藏的数量
    def getMyFavoriteCount(self, tokenID):
        userID = self.getUserIDByToken(tokenID)
        sql = 'select count(*) from favorite where userID like \'%s\';' % userID
        return self.getCount(tokenID, sql)

    # 我的资料  ---->跳转到编辑个人资料的页面
    def getMyinfo(self, tokenID):
        userManager = UserManager()
        # 根据tokenID查找userID
        userID = self.getUserIDByToken(tokenID)
        result = userManager.getUserDetail(tokenID, userID)
        return result

    # 我的发布
    def getMypost(self, tokenID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        merchandiseManager = MerchandiseManager()
        userID = self.getUserIDByToken(tokenID)
        resultlist = merchandiseManager.getPostMerchandiseList(userID)
        '''db = DataOperation()
        db.connect()
        sqlmid = 'select merchandiseID from  postedmerchandise where userID like \'%s\';' % userID
        cur = db.query(sqlmid)
        if cur == None:
            return False
        mid = cur.fetchall()
        db.close()
        resultlist = []
        for merchandiseID in mid:
            result = merchandiseManager.getMerchandiseDetail(tokenID, merchandiseID)
            print(mid)
            print(result)
            resultlist.append(result)'''

        return resultlist

    # 我卖出的
    def getMysold(self):
        pass

    # 我买到的
    def getMybought(self):
        pass

    # 我需求的
    def getMyneeded(self, tokenID):
        requriementManager = RequirementManager()
        jsoninfo = requriementManager.searchRequirment(tokenID)
        return jsoninfo

    # 我的快递服务
    def getMycourier(self, tokenID):
        expressManager = ExpressManager()
        jsoninfo = expressManager.searchExpress(tokenID)
        return jsoninfo

    # 我的收藏
    def getMyfavorite(self, tokenID):
        favoriteManager = FavoriteManager()
        jsoninfo = favoriteManager.searchFavorite(tokenID)
        return jsoninfo


if __name__ == '__main__':
    mm = MyselfManager()
    sql = 'select * from userInfo where userID = \'202cb962ac59075b964b07152d234b70\''
    db = DataOperation()
    db.connect()
    db.close()
    tokenID = '5b38ff93107040d94a001bf08dbe3474'
    # sql = 'select count(*) from userInfo where userName = \'anthow\';'
    # cur = db.query(sql)
    # print cur.fetchone()[0]
    # print mm.getMyneeded('c09bd67618d0eafda928f07280dd4cdc')
    print mm.getMycourier(tokenID)
