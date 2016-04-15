# coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf8')

from tool.Util import Util
import json
from tool.DataOperation import DataOperation
from address.AddressManager import AddressManager


class MerchandiseManager(Util):
    def __init__(self):
        self._sortTypes = self.getSupportedSortType()
        self._college = self.getSupportedCollege()
        self._merchandiseType = self.getSupportedMerchandiseType()
        self._citys = self.getSupportCity()

        self._favoriteDict = {}

    def setSortType(self, sortType):
        if '3' == sortType:
            self._sortTypes['type'] = 'asc'
        else:
            self._sortTypes['type'] = 'desc'

    # 获取支持的商品类型
    def getSupportedMerchandiseType(self):
        types = {}
        db = DataOperation()
        db.connect()

        sql = 'select * from merchandiseType'
        cur = db.query(sql)
        if None == cur:
            db.close()
            return None

        result = cur.fetchall()
        db.close()

        for r in result:
            types[r[0]] = r[1]
        types['0'] = '%%'
        types['ALL'] = '%%'
        return types

    # 获取支持的城市
    def getSupportCity(self):
        citys = {}
        db = DataOperation()
        db.connect()

        sql = 'select cityID, cityName from city;'
        cur = db.query(sql)
        if None == cur:
            db.close()
            return None

        result = cur.fetchall()
        db.close()
        for c in result:
            citys[c[0]] = c[1]
        citys['0'] = '%%'
        citys['ALL'] = '%%'
        return citys

    # 获取支持的大学名称
    def getSupportedCollege(self):
        types = {}
        db = DataOperation()
        db.connect()

        sql = 'select * from collegeInfo'
        cur = db.query(sql)
        if None == cur:
            db.close()
            return None

        result = cur.fetchall()
        db.close()
        for r in result:
            types[r[0]] = r[1]
        types['0'] = '%%'
        types['ALL'] = '%%'
        return types

    # 获取支持的筛选排序名称
    def getSupportedSortType(self):
        types = {}
        db = DataOperation()
        db.connect()

        sql = 'select * from sortType'
        cur = db.query(sql)
        if None == cur:
            db.close()
            return None
        result = cur.fetchall()
        db.close()

        # for r in result:
        #     types[r[0]] = r[1]
        types['ALL'] = '%%'
        types['价格降序'] = 'currentPrice'
        types['价格升序'] = 'currentPrice'
        types['发布时间'] = 'publishedTime'
        types['综合排序'] = 'publishedTime'
        types['ALL'] = 'publishedTime'
        types['0'] = 'publishedTime'
        types['1'] = 'publishedTime'
        types['2'] = 'currentPrice'
        types['3'] = 'currentPrice'
        return types

    # jsonInfo :
    # {
    #    "userID" : "123"
    #   "title" : "相机"
    #    "description" : "九成新。。。。。"
    #    "classification": 0,
    #    "price": 10,
    #    "incomePrice": 60,
    #    "carriage": 6,
    #    "macthing": true,
    #    "college": "Nanjing University",
    #    "location": "Nanjing",
    #    "recommendation": true,
    #    "swap":True
    #    "inspection": true
    # }
    #
    def createMerchandise(self, jsonInfo, imgList):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']  # 登录信息，tokenID
        title = info['title']  # 商品名称
        description = info['description']  # 详细描述
        merchandiseTypeID = info['merchandiseTypeID']  # 分类
        price = info['price']  # 想卖价格
        incomePrice = info['incomePrice']  # 买时价格
        carriage = info['carriage']  # 运费
        matching = info['matching']  # 匹配卖货
        college = info['college']  # 大学
        location = info['location']  # 位置
        recommendation = info['recommendation']  # 精品推荐
        inspection = info['inspection']  # 第三方验货
        swap = info['swap']  # 是否支持物物交换
        city = info['city']  # 城市
        currentTime = self.getCurrentTime()
        merchandiseID = self.generateMerchandiseID(currentTime + tokenID)

        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        userID = self.getUserIDByToken(tokenID)
        sqlList = []


        for img in imgList:
            sqlImg = 'insert into imgPath(imgPathID, path, merchandiseID) values(\'%s\', \'%s\', \'%s\');' \
                     % (self.generateID(img), img, merchandiseID)
            sqlList.append(sqlImg)
        sql = 'insert into merchandise(merchandiseID, merchandiseName, currentPrice, oldPrice, userID, info,' \
              ' publishedTime, swap, inspection, college, merchandiseTypeID, matching, recommendation, city) values(' \
              ' \'%s\', \'%s\', %f, %f, \'%s\', \'%s\', \'%s\', %s, %s, \'%s\', \'%s\', %s, %s, \'%s\');' % \
              (merchandiseID, title, price, incomePrice, userID, description, currentTime, swap,
               inspection, college, merchandiseTypeID, matching, recommendation, city)
        db = DataOperation()
        db.connect()
        sqlList.append(sql)

        db.multiOperate(sqlList)
        db.close()

        return merchandiseID

    # 更新商品详情
    def updateMerchandiseInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']  # 登录信息，tokenID
        title = info['title']  # 商品名称
        description = info['description']  # 详细描述
        classification = info['classification']  # 分类
        price = info['price']  # 想卖价格
        incomePrice = info['incomePrice']  # 买时价格
        carriage = info['carriage']  # 运费
        matching = info['matching']  # 匹配卖货
        college = info['college']  # 大学
        location = info['location']  # 位置
        recommendation = info['recommendation']  # 精品推荐
        inspection = info['inspection']  # 第三方验货
        swap = info['swap']  # 是否支持物物交换
        merchandiseID = self.generateMerchandiseID(title)
        publishedTime = info['publishedTime']
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        userID = self.getUserIDByToken(tokenID)
        sql = 'update merchandise set merchandiseName = \'%s\', currentPrice = %f, oldPrice = %f, userID = \'%s\', ' \
              ' info = \'%s\', publishedTime = \'%s\', swap = %s, inspection = %s, college = \'%s\',' \
              ' merchandiseTypeID = \'%s\', matching = %s, recommendation = %s;' % \
              (title, price, incomePrice, userID,
               description, publishedTime, swap, inspection, college,
               classification, matching, recommendation)

        sqlImgAdd = 'insert into imgPath(imgPathID, path, merchandiseID) values'
        addList = imgList['add']
        deleteList = imgList['delete']
        sqlImgAdd = ''
        sqlList = []
        sqlList.append(sql)
        for addImg in addList:
            if addImg != addList[-1]:
                sqlImgAdd = sqlImgAdd + "(\'%s\', \'%s\', \'%s\')," % (self.generateID(i['img']), addImg, merchandiseID)
            else:
                sqlImgAdd = sqlImgAdd + "(\'%s\', \'%s\', \'%s\');" % (self.generateID(i['img']), addImg, merchandiseID)
        
        sqlList.append(sqlImgAdd)
        for delImg in deleteList:
            if delImg != deleteList[-1]:
                sqlImgDel = 'delete from imgPath where merchandiseID like \'%s\' and path like \'%s\';'  % (merchandiseID, delImg);
                sqlImgDelList.append(sqlImgDel)
        
        
        db = DataOperation()
        db.connect()
        #db.operate(sql)
        db.multiOperate(sqlList)

        db.close()
        return True

    # 生成图片操作sql
    def generateSql(self, imgDic):
        sqlAdd = 'insert into imgPath(imgPathID, path, merchandiseID) values()'

    # 生成商品ID
    def generateMerchandiseID(self, merchandiseName):
        '''currentTime = self.getCurrentTime()
        merchandiseID = self.getMD5String(merchandiseName.join(str(currentTime)))'''
        return self.generateID(str(merchandiseName))

    # 获取我关注的商品列表
    def getMyFavoriteList(self, userID):
        # if len(self._favoriteDict) > 0:
        #     return self._favoriteDict
        sqlFavorite = 'select merchandiseID from favorite where userID like \'%s\';' % userID
        db = DataOperation()
        db.connect()
        cur = db.query(sqlFavorite)
        if None == cur:
            db.close()
            return None
        allResult = cur.fetchall()

        for m in allResult:
            self._favoriteDict[m[0]] = True
        db.close()
        return self._favoriteDict

    # 获取商品信息列表
    def getMerchandiseInfoBriefList(self, jsonInfo, isRecomm = False):
        # 解析jsonInfo
        # info = json.loads(jsonInfo)
        # data = info['data']
        data = json.loads(jsonInfo)
        college = data['college']
        merchandiseType = data['merchandiseType']
        sortType = data['sortType']
        pageCount = data['pageCount']
        tokenID = data['tokenID']
        start = data['start']
        city = data['city']
        valid = self.isTokenValidity(tokenID)
        userID = ''
        if 'error' == json.loads(valid)['status']:
            valid = False
        else:
            valid = True
            userID = self.getUserIDByToken(tokenID)

        # self.setSortType(sortType)
        # if college == 'ALL':
        #    college = '%%'
        # if merchandiseType == 'ALL':
        #   merchandiseType = '%%'
        # if None == city or 'ALL' == city:
        #    city = '%%'
        self.setSortType(sortType)
        sortAction = self._sortTypes['type']
        sortType = self._sortTypes[sortType]
        merchandiseType = self._merchandiseType[merchandiseType]
        college = self._college[college]
        city = self._citys[city]
        # sortTypes = {}
        # sortTypes['currentPrice'] = 'currentPrice'
        # sortTypes['publishedTime'] = 'publishedTime'
        condition = ''
        if True == isRecomm:
            condition = ' and recommendation is true '
        else:
            condition = ' '
        db = DataOperation()
        db.connect()
        sql = 'select merchandiseName, college, merchandiseID, currentPrice, ' \
              'merchandiseType, merchandiseList.userName, merchandiseList.portraitPath, publishedTime, ' \
              'favorite, imgPath, merchandiseList.info, oldPrice, shipmentPrice ,userID from merchandiseList where ' \
              ' merchandiseID in (select merchandiseID' \
              ' from (select merchandiseID from merchandiseList '\
              'where merchandiseType like \'%s\' and city like \'%s\' and college like \'%s\' ' \
              ' and freeze is false %s group by merchandiseID order by %s %s limit %d, %d) as t) order by %s %s;' % (merchandiseType, 
               city, college, condition, sortType, sortAction, start, pageCount, sortType, sortAction)
        # (merchandiseType, city, self._sortTypes[sortType], self._sortTypes['type'], pageCount, 10)
        cur = db.query(sql)
        if None == cur:
            db.close()
            return False
        allresult = cur.fetchall()
        db.close()
        # 最后返回的list
        l = []
        # merchandiseID 作为Key存储Imglist
        temp = {}
        favoriteAssitant = {}

        for i in list(allresult):
            res = {}
            # if temp[i[2]] == None:
            # 如果已经merchandiseID存在，直接往里面的imgList里添加图片
            if i[2] not in temp.keys():
                res['merchandiseName'] = i[0]
                res['college'] = i[1]
                res['merchandiseID'] = i[2]
                res['currentPrice'] = i[3]
                res['merchandiseTypeName'] = i[4]
                res['userName'] = i[5]
                res['portraitPath'] = i[6]
                res['publishedTime'] = str(i[7])
                res['favorite'] = i[8]
                res['info'] = i[10]
                res['oldPrice'] = i[11]
                res['shipmentPrice'] = i[12]
                res['userID'] = i[13]
                imgList = []
                imgList.append(i[9])
                res['imgPath'] = imgList
                temp[i[2]] = imgList
                l.append(res)
                favoriteAssitant[i[2]] = res
            else:
                temp[i[2]].append(i[9])
        
        if True == valid:
            favoriteMList = self.getMyFavoriteList(userID)
            if None != favoriteMList:
                # for m in favoriteMList:
                #    favoriteAssitant[m]['favorite'] = True
                for m in favoriteAssitant.keys():
                    if self._favoriteDict.has_key(m):
                        favoriteAssitant[m]['favorite'] = '1'
        return l

    # 获取发布商品信息列表
    def getPostMerchandiseList(self, userID):
        db = DataOperation()
        db.connect()
        sql = 'select merchandiseName,currentPrice,oldPrice, visitedCount,info,publishedTime,swap,autoShipment,inspection,college,matching,' \
              ' recommendation,status, city,shipmentPrice,merchandiseID from postedmerchandise where userID like \'%s\' and status not like \'deleted\';' % userID
        cur = db.query(sql)
        if None == cur:
            db.close()
            return False
        l = []
        for info in cur.fetchall():
            res = {}
            img = []
            res['merchandiseName'] = info[0]
            res['currentPrice'] = info[1]
            res['oldPrice'] = info[2]
            res['visitedCount'] = info[3]
            res['info'] = info[4]
            res['publishedTime'] = str(info[5])
            res['swap'] = info[6]
            res['autoShipment'] = info[7]
            res['inspection'] = info[8]
            res['college'] = info[9]
            res['matching'] = info[10]
            res['recommendation'] = info[11]
            res['status'] = info[12]
            res['city'] = info[13]
            res['shipmentPrice'] = info[14]
            res['merchandiseID'] = info[15]
            merchandiseID = info[15]
            sqlImg = 'select path from imgpath where merchandiseID like \'%s\';' % merchandiseID
            curImg = db.query(sqlImg)
            for i in curImg.fetchall():
                img.append(i[0])
            res['imgList'] = img
            l.append(res)
        db.close()
        return l

    # 获取商品信息详情
    def getMerchandiseDetail(self, tokenID, merchandiseID):
        self.updateCount(merchandiseID)
        valid = self.isTokenValidity(tokenID)
        sql = ''
        resultInfo = ''
        islogin = json.loads(valid)['status']
        favorite = '0'
        favoriteCount = None
        if 'success' == islogin:
            sql = 'select merchandise.merchandiseID, merchandise.merchandiseName, merchandise.currentPrice, merchandise.oldPrice, merchandise.visitedCount, ' \
                   'merchandise.userID, merchandise.info, merchandise.publishedTime, merchandise.swap, merchandise.autoShipment, merchandise.inspection, merchandise.college, ' \
                   'merchandise.merchandiseTypeID, merchandise.matching, merchandise.recommendation, path, userInfo.userName, userInfo.portraitPath, ' \
                   'residence,merchandise.shipmentPrice,collegeInfo.collegeName from merchandise, imgPath, ' \
                   'userInfo, collegeInfo where merchandise.college = collegeInfo.collegeID and ' \
                   'userInfo.userID = merchandise.userID and imgPath.merchandiseID = merchandise.merchandiseID and merchandise.merchandiseID = \'%s\';' % merchandiseID
            addressManager = AddressManager()
            resultInfo = addressManager.searchAddressDefaultDetail(tokenID)
            favorite = '0'
        else:
            sql = 'select merchandise.merchandiseID, merchandise.merchandiseName, merchandise.currentPrice, merchandise.oldPrice, merchandise.visitedCount, ' \
                  'merchandise.userID, merchandise.info, merchandise.publishedTime, merchandise.swap, merchandise.autoShipment, merchandise.inspection, merchandise.college, ' \
                  'merchandise.merchandiseTypeID, merchandise.matching, merchandise.recommendation, path, userInfo.userName, userInfo.portraitPath, ' \
                  'residence,merchandise.shipmentPrice, collegeInfo.collegeName from merchandise, imgPath, ' \
                  'userInfo, collegeInfo where merchandise.college = collegeInfo.collegeID and ' \
                  'userInfo.userID = merchandise.userID and imgPath.merchandiseID = merchandise.merchandiseID and merchandise.merchandiseID = \'%s\';' % merchandiseID  
            # userID = self.getUserIDByToken(tokenID)
            resultInfo = 'Not found'
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return False
        allResult = cur.fetchall()
        if 'success' == islogin:
            sqlFavorite = 'select count(*) from favorite where merchandiseID like \'%s\';' % merchandiseID
            cur = db.query(sqlFavorite)
            if None == cur:
                db.close()
                favorite = '0'
            favoriteCount = cur.fetchone()
            if None == favoriteCount:
                favorite = '0'
            favorite = favoriteCount[0]
        sqlFreeze = 'select freeze from merchandiseList where merchandiseID like \'%s\';' % merchandiseID
        curFreese = db.query(sqlFreeze)
        isFreeze = '0'
        if None != curFreese:
            isFreeze = curFreese.fetchone()
            if None != isFreeze:
                isFreeze = isFreeze[0]
        isBought = '0'
        if 'success' == islogin:
            sqlBuyID = 'select buyerID from merchandiseOrder where merchandiseID like \'%s\';' % merchandiseID
            curBuy = db.query(sqlBuyID)
            if None != curBuy:
                buyerID = curBuy.fetchone()
                userID = self.getUserIDByToken(tokenID)
                if None != buyerID and buyerID[0] == userID:
                    isBought = '1'
            
        db.close()
        
        resultData = {}
        imgList = []
        for result in allResult:
            if len(resultData) <= 0:
                resultData['merchandiseID'] = result[0]
                resultData['merchandiseName'] = result[1]
                resultData['currentPrice'] = result[2]
                resultData['oldPrice'] = result[3]
                resultData['visitedCount'] = result[4]
                resultData['userID'] = result[5]
                resultData['info'] = result[6]
                resultData['publishedTime'] = str(result[7])
                resultData['swap'] = result[8]
                resultData['autoShipment'] = result[9]
                resultData['inspection'] = result[10]
                resultData['college'] = result[20]
                resultData['merchandiseTypeID'] = result[12]
                resultData['matching'] = result[13]
                resultData['recommendation'] = result[14]
                resultData['userName'] = result[16]
                resultData['portraitPath'] = result[17]
                resultData['residence'] = result[18]
                resultData['shipmentPrice'] = result[19]
                resultData['defaultAddress'] = resultInfo
                resultData['imgList'] = imgList

                resultData['favorite'] = favorite
                imgList.append(result[15])
                resultData['isFreeze'] = isFreeze
                resultData['isBought'] = isBought
            else:
                imgList.append(result[15])
        return resultData


    # 删除商品信息
    def deleteMerchandise(self, tokenID, merchandiseID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        sql = 'delete from merchandise where merchandiseID like \'%s\' and merchandiseID not in (select merchandiseID from merchandiseOrder);' % merchandiseID
        sqlOrder = 'select merchandiseID from merchandiseOrder where merchandiseID like \'%s\';' % merchandiseID
        db = DataOperation()
        db.connect()
        cur = db.query(sqlOrder)
        if None != cur:
            orderID = cur.fetchone()
            if None != orderID:
                db.close()
                return False
        db.operate(sql)
        db.close()
        return True


    # 通过订单获取商品信息
    def getMerchandiseByOrderID(self, tokenID, orderID):
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False

        sql = 'select merchandiseName, currentPrice, oldPrice, visitedCount, userID, info,' \
              ' publishedTime, swap, autoShipment, inspection, college, merchandiseTypeName, matching,' \
              ' recommendation, status from merchandiseOrder, postedMerchandise, merchandiseType ' \
              'where merchandiseOrder.merchandiseID=postedMerchandise.merchandiseID and ' \
              'postedMerchandise.merchandiseTypeID = merchandiseType.merchandiseTypeID and orderID like \'%s\';' % orderID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return False
        result = cur.fetchone()
        db.close()
        info = {}
        info['merchandiseName'] = result[0]
        info['currentPrice'] = result[1]
        info['oldPrice'] = result[2]
        info['visitedCount'] = result[3]
        info['userID'] = result[4]
        info['info'] = result[5]
        info['publishedTime'] = str(result[6])
        info['swap'] = result[7]
        info['autoShipment'] = result[8]
        info['inspection'] = result[9]
        info['college'] = result[10]
        info['merchandiseTypeName'] = result[11]
        info['matching'] = result[12]
        info['recommendation'] = result[13]
        info['status'] = result[14]
        return info


    # 获取大学信息
    def getCollegeInfo(self):
        sql = "select * from collegeInfo;"
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            db.close()
            return False
        allresult = cur.fetchall()
        db.close()

        collegeList = []
        for c in allresult:
            info = {}
            info['collegeID'] = c[0]
            info['collegeName'] = c[1]
            collegeList.append(info)
        return collegeList

    # 通过城市获取城市列表,该接口返回该城市所有的大学
    def getCollegeListByCity(self, jsonParams):
        params = json.loads(jsonParams)
        tokenID = params['tokenID']
        cityID = params['cityID']
        tag = params['tag']

        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        condition = ''
        if '1' == tag or 1 == tag:
            condition = 'and isSupport = true'
        else:
            condition = ''

        sql = 'select collegeID, collegeName, cityID, isSupport from collegeInfo ' \
              'where cityID like \'%s\' %s;' % (cityID, condition)
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return cur

        allCollege = cur.fetchall()
        collegeList = []
        for c in allCollege:
            college = {}
            college['collegeID'] = c[0]
            college['collegeName'] = c[1]
            college['cityID'] = c[2]
            college['isSupport'] = c[3]
            collegeList.append(college)

        return collegeList

    # 获取排序方式
    def getSortType(self):
        sql = 'select * from sortType;'
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            db.close()
            return False

        allresult = cur.fetchall()
        db.close()

        sortList = []
        for s in allresult:
            sortInfo = {}
            sortInfo['sortTypeInfo'] = s[0]
            sortInfo['sortTypeName'] = s[1]
            sortList.append(sortInfo)

        return sortList


    # 获取商品分类
    def getMerchandiseType(self):
        sql = 'select * from merchandiseType;'
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if cur == None:
            db.close()
            return False
        allresult = cur.fetchall()
        db.close()

        merchandiseList = []
        for m in allresult:
            info = {}
            info['merchandiseTypeID'] = m[0]
            info['merchandiseTypeName'] = m[1]
            info['imgpath'] = m[2]
            merchandiseList.append(info)

        return merchandiseList


    # 获取支持的城市列表
    def getCityList(self):
        sql = 'select * from city;'
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return False
        allResult = cur.fetchall()
        db.close()
        cityList = []
        for c in allResult:
            info = {}
            info['cityID'] = c[0]
            info['cityName'] = c[1]
            cityList.append(info)
        return cityList


    # 商品浏览次数
    def updateCount(self, merchandiseID):
        db = DataOperation()
        db.connect()
        sql = 'update merchandise set visitedCount = visitedCount+1 where merchandiseID like \'%s\';' % merchandiseID
        db.operate(sql)
        db.close()
		
    # 根据上商品的名字查询
    def searchMerchandiseByName(self, tokenID, merchandiseName):
        valid = self.isTokenValidity(tokenID)
        islogin = json.loads(valid)['status']
        db = DataOperation()
        db.connect()
        sql = 'select merchandiselist.merchandiseID,merchandiselist.merchandiseName,currentPrice,oldPrice,visitedCount,userInfo.userName,' \
              'merchandiselist.info,publishedTime,swap,autoShipment,inspection,college,merchandiseType,' \
              'matching,recommendation,city,imgPath,userInfo.portraitPath,favorite,shipmentPrice,userInfo.userID ' \
              'from merchandiselist,userInfo,imgPath where userInfo.userName =  merchandiselist.userName ' \
              'and imgPath.merchandiseID = merchandiselist.merchandiseID and imgPath.path = merchandiselist.imgPath and ' \
              'merchandiseName like \'%%%s%%\' or merchandiselist.info like \'%%%s%%\' group by merchandiselist.merchandiseID,merchandiselist.imgPath;' % (merchandiseName,merchandiseName)
        cur = db.query(sql)
        if cur == None:
            db.close()
            return False
        info = cur.fetchall()
        db.close()
        l = []
        temp = {}
        for i in info:
            result = {}
            if i[0] not in temp.keys():
                imgList = []
                temp[i[0]] = imgList
                result['merchandiseID'] = i[0]
                result['merchandiseName'] = i[1]
                result['currentPrice'] = i[2]
                result['oldPrice'] = i[3]
                result['visitedCount'] = i[4]
                result['userName'] = i[5]
                result['info'] = i[6]
                result['publishedTime'] = str(i[7])
                result['swap'] = i[8]
                result['autoShipment'] = i[9]
                result['inspection'] = i[10]
                result['college'] = i[11]
                result['merchandiseType'] = i[12]
                result['matching'] = i[13]
                result['recommendation'] = i[14]
                result['city'] = i[15]
                result['imgList'] = imgList
                imgList.append(i[16])
                result['portraitPath'] = i[17]
                if 'success' == islogin:
                    result['favorite'] = i[18]
                else:
                    result['favorite'] = '0'
                result['shipmentPrice'] = i[19]
                result['userID'] = i[20]
                l.append(result)
            else:
                temp[i[0]].append(i[16])
        return l

    def servicePrice(self,tokenID):
        sql = 'select recommendPrice,matchPrice,inspectPrice from allPrices where userID like \'%s\';' % tokenID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        allinfo = cur.fetchone()
        if(allinfo == None):
            db.close()
            return None
        if(len(allinfo) == 0):
            db.close()
            return None
        result = {}
        result['recommendPrice'] = allinfo[0]
        result['matchPrice'] = allinfo[1]
        result['inspectPrice'] = allinfo[2]
        db.close()
        return result

    def isMerchandiseFrozen(self, merchandiseID):
        sql = 'select freeze from merchandiseList where merchandiseID like \'%s\';' % merchandiseID
        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return cur
        isFreeze = cur.fetchone()
        if None == isFreeze:
            db.close()
            return False
        db.close()
        return isFreeze[0]
    
    def setRecommendation(self, jsonInfo):
        info = json.loads(jsonInfo)
        merchandiseID = info['merchandiseID']
        tokenID = info['info']
        valid = self.isTokenValidity(tokenID)
        if 'error' == json.loads(valid)['status']:
            return False
        sql = 'update merchandise set recommendation = true where merchandiseID like \'%s\';' % merchandiseID
        db = DataOperation()
        db.connect()
        db.operate(sql)
        db.close()
        return True

if __name__ == '__main__':
    m = MerchandiseManager()
    # jsonInfo = '{\"status\": \"SUCCESS\", \"data\": {\"merchandiseType\": \"Daily\", \"sortType\":\"currentPrice\",\"pageCount\": 10, \"merchandiseID\": 1, \"start\": 0, \"currentPrice\": 100, \"college\": \"Nanjing\", \"merchandiseName\": \"camera\"}}'
    # m.getMerchandiseInfoBriefList(jsonInfo)

    # jsonInfo = '{\"tokenID\":\"646877eb74094da28df1aef7ade08a02\",\"title\":\"camera\",\"description\":\"jjjj\",\"classification\":0,\"price\":10,\"incomePrice\":60,\"carriage\":6,\"matching\":\"True\",\"college\":\"Nanjing University\",\"location\":\"Nanjing\",\"recommendation\":\"True\",\"swap\":\"True\",\"inspection\":\"True\"}'
    # m.createMerchandise(jsonInfo, None)

    # m.getMerchandiseDetail('e848f20e2f6faf351b77bb03dd3dd06c', '917f7565dace69250a6997fc801661f3')

    # jsonInfo = '{\"publishedTime\": \"2015-07-09\", \"tokenID\": \"646877eb74094da28df1aef7ade08a02\", \"title\": \"Hello\", \"description\": \"hhhhh\", \"classification\": \"0\", \"price\": 13, \"merchandiseID\": \"3edb9669fc702e53df7048d618c12e40\", \"incomePrice\": 60, \"carriage\": 6, \"college\": \"Nanjing University\", \"location\": \"Nanjing\", \"recommendation\": \"true\", \"inspection\": \"true\", \"matching\": \"true\", \
    # \"swap\": \"true\"}'
    # m.updateMerchandiseInfo(jsonInfo)
    # m.deleteMerchandise('646877eb74094da28df1aef7ade08a02', '7386a44372c74030612d644fa3d2f885')

    print m.getSupportedCollege()
    print m.getSupportedMerchandiseType()
    s = m.getSupportedSortType()
