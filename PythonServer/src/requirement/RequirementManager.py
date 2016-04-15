# coding=utf8
import sys

sys.path.append('..')
from tool.Util import Util
import json
from tool.DataOperation import DataOperation


class RequirementManager(Util):
    def __init__(self):
        pass

    # 添加一个需求
    def createRequirement(self, tokenID, info, merchandiseType):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            createTime = self.getCurrentTime()
            # 根据createTime+userID生成requirementID
            requirementID = self.getMD5String(createTime + userID)
            db = DataOperation()
            db.connect()
            sql = 'insert into requirement(requirementID, info, userID, merchandiseTypeID, publishedTime) values(\'%s\',\'%s\',\'%s\',\'%s\', now());' \
                  % (requirementID, info, userID, merchandiseType)
            db.operate(sql)
            db.close()
            return requirementID
        else:
            return False

    # 新增需求，需要学校，字段
    def createRequirementByCollege(self, jsonParam):
        param = json.loads(jsonParam)
        tokenID = param['tokenID']
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            publishedTime = self.getCurrentTime()
            requirementID = self.getMD5String(publishedTime + tokenID)
            info = param['info']
            merchandiseTypeID = param['merchandiseTypeID']
            collegeID = param['collegeID']
            cityID = param['cityID']

            sql = 'insert into requirement(requirementID, info, userID, merchandiseTypeID, publishedTime, collegeID, cityID) values(' \
                  '\'%s\', \'%s\', \'%s\', \'%s\', now(), \'%s\', \'%s\');' % (requirementID,
                                                                               info, userID, merchandiseTypeID, collegeID, cityID)
            db = DataOperation()
            db.connect()
            (ret, reason) = db.operate(sql)
            db.close()
            if False == ret:
                return (ret,reason)
            else:
                return (ret, requirementID)


    # 查询需求
    def searchRequirment(self, tokenID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            userID = self.getUserIDByToken(tokenID)
            db = DataOperation()
            db.connect()
            sql = 'select requirementID,info,userID,merchandiseTypeID from requirement where userID like \'%s\';' % userID

            cur = db.query(sql)
            if cur == None:
                db.close()
                return False

            resultlist = []
            for info in cur.fetchall():
                result = {}
                result['requirementID'] = info[0]
                result['info'] = info[1]
                result['userID'] = info[2]
                result['merchandiseType'] = info[3]
                resultlist.append(result)
            db.close()
            # [{"info": "james", "userID": "53f6dd617c1d318face609dfb563ad48", "requirementID": "11211b0f75f5af39500497a2aa51735b"},
            # {"info": "kobe", "userID": "53f6dd617c1d318face609dfb563ad48", "requirementID": "71e926ca360cf01b73b603cde8a73b72"},
            # {"info": "anthow", "userID": "53f6dd617c1d318face609dfb563ad48", "requirementID": "b415689f6caffb04c638610242fdc3af"}]
            return resultlist
        else:
            return False

    # 删除一个需求
    def deleteRequirment(self, tokenID, requirementID):
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'delete from requirement where requirementID like \'%s\';' % requirementID
            db.operate(sql)
            db.close()
            return True
        else:
            return False

    # 编辑一个需求
    def editRequirment(self, jsoninfo):
        result = json.loads(jsoninfo)
        info = result['info']
        tokenID = result['tokenID']
        requirementID = result['requirementID']
        merchandiseTypeID = result['merchandiseTypeID']
        collegeID = result['collegeID']
        cityID = result['cityID']
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] == 'success' and res['data'] == True:
            db = DataOperation()
            db.connect()
            sql = 'update requirement set info = \'%s\', merchandiseTypeID = \'%s\', publishedTime = now(), ' \
                  'collegeID = \'%s\', cityID = \'%s\' where requirementID like \'%s\';' % (info , merchandiseTypeID, requirementID, collegeID, cityID)
            db.operate(sql)
            db.close()
            return True
        else:
            return False

    # 获取所有需求
    def getAllRequirement(self, jsoninfo):
        param = json.loads(jsoninfo)
        tokenID = param['tokenID']
        startOffset = param['startOffset']
        pageCount = param['pageCount']
        searchKey = param['searchKey']
        merchandiseTypeID = param['merchandiseTypeID']
        cityID = param['cityID']
        collegeID = param['collegeID']
        # 首先判断一下这个token是否在有效期内
        res = json.loads(self.isTokenValidity(tokenID))
        if res['status'] != 'success':
            return False
        if '-1' == searchKey or -1 == searchKey:
            searchKey = ''
        if '0' == cityID:
            cityID = '%%'
        if '0' == collegeID:
            collegeID = '%%'

        sql = 'select requirementID, requirement.info, requirement.userID, requirement.merchandiseTypeID, userName, ' \
              'merchandiseTypeName, portraitPath, publishedTime ' \
              'from requirement, userInfo, merchandiseType ' \
              'where requirement.userID = userInfo.userID ' \
              'and requirement.merchandiseTypeID = merchandiseType.merchandiseTypeID ' \
              'and requirement.info like \'%%%s%%\' ' \
              'and requirement.merchandiseTypeID like \'%s\' ' \
              'and cityID like \'%s\' ' \
              'and collegeID like \'%s\' ' \
              'order by publishedTime desc limit %d, %d ' % (searchKey, merchandiseTypeID, cityID, collegeID, startOffset, pageCount)


        db = DataOperation()
        db.connect()
        cur = db.query(sql)
        if None == cur:
            db.close()
            return cur
        allReq = cur.fetchall()

        reqList = []
        for r in allReq:
            req = {}
            req['requirementID'] = r[0]
            req['info'] = r[1]
            req['userID'] = r[2]
            req['merchandiseTypeID'] = r[3]
            req['userName'] = r[4]
            req['merchandiseTypeName'] = r[5]
            req['portraitPath'] = r[6]
            req['publishedTime'] = str(r[7])
            reqList.append(req)

        return reqList

if __name__ == '__main__':
    rm = RequirementManager()
    # rm.createRequirement('c09bd67618d0eafda928f07280dd4cdc','kobe')
    # print rm.searchRequirment('c09bd67618d0eafda928f07280dd4cdc')
    # print rm.deleteRequirment('c09bd67618d0eafda928f07280dd4cdc', '2')
    result = {}
    result['info'] = 'kkkkkk'
    result['tokenID'] = 'c09bd67618d0eafda928f07280dd4cdc'
    result['requirementID'] ='21'
    jsoninfo = json.dumps(result)
    # print rm.editRequirment(jsoninfo)
