# coding=utf8
import json
import sys

sys.path.append('..')
from tool.Util import Util
from tool.CJsonEncoder import CJsonEncoder
from tool.DataOperation import DataOperation


class FavoriteManager(Util):
    def __init__(self):
        pass

    # 创建一个收藏表
    def createFavorite(self, tokenID, merchandiseID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            createTime = self.getCurrentTime()
            favoriteID = self.getMD5String(createTime + userID)
            sql = 'insert into favorite values(\'%s\',\'%s\',\'%s\',\'%s\');' % (
                favoriteID, merchandiseID, userID, createTime)
            print sql
            db = DataOperation()
            db.connect()
            db.operate(sql)
            db.close()
            return favoriteID
        else:
            return False

    # 查询收藏表
    def searchFavorite(self, tokenID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            sql = 'select favoriteID, favorite.merchandiseID, postedMerchandise.userID, timeAndDate, ' \
                  'portraitPath, userName, currentPrice, oldPrice, postedMerchandise.info, ' \
                  'imgPath.path from favorite, userInfo, postedMerchandise, imgPath' \
                  ' where postedMerchandise.userID = userinfo.userID and favorite.merchandiseID= postedMerchandise.merchandiseID' \
                  ' and postedMerchandise.merchandiseID = imgPath.merchandiseID and favorite.userID like \'%s\';' % userID
            print sql
            cur = db.query(sql)
            if None == cur:
                db.close()
                return False
            resultlist = []
            resultData = cur.fetchall()
            

            temp = {}
            for info in resultData:
                if info[1] not in temp.keys():
                    result = {}
                    result['favoriteID'] = info[0]
                    result['merchandiseID'] = info[1]
                    result['userID'] = info[2]
                    result['timeAndDate'] = str(info[3])
                    result['portraitPath'] = info[4]
                    result['userName'] = info[5]
                    result['currentPrice'] = info[6]
                    result['oldPrice'] = info[7]
                    result['info'] = info[8]
                    imgList = []
                    imgList.append(info[9])
                    temp[info[1]] = imgList
                    result['path'] = imgList
                    resultlist.append(result)
                else:
                    temp[info[1]].append(info[9])
            db.close()
            # [{"favoriteID": "177b2655a38d07680c40c42ab418acf3", "merchandiseID": "1", "userID": "53f6dd617c1d318face609dfb563ad48", "timeAndDate": "2015-07-13 17:39:55"},
            # {"favoriteID": "1da1cdfe68d75628e5e71c77edd130e9", "merchandiseID": "2", "userID": "53f6dd617c1d318face609dfb563ad48", "timeAndDate": "2015-07-13 17:40:20"},
            # {"favoriteID": "62916d2229e6eadf4af2d74ec250757d", "merchandiseID": "3", "userID": "53f6dd617c1d318face609dfb563ad48", "timeAndDate": "2015-07-13 17:40:23"}]
            return resultlist
        else:
            return False

    # 删除一个收藏表
    def deleteFavorite(self, tokenID, merchandiseID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'delete from favorite where merchandiseID like \'%s\';' % merchandiseID
            print sql
            db.operate(sql)
            db.close()
            return True
        else:
            return False


if __name__ == '__main__':
    fm = FavoriteManger()
    favotiteID = '1'
    tokenID = 'c09bd67618d0eafda928f07280dd4cdc'
    merchandiseID = '3'
    # print fm.createFavorite(tokenID,merchandiseID)
    # print fm.searchFavorite(tokenID)
    # print fm.deleteFavorite(tokenID,favotiteID)
