import json
import MySQLdb
import sys
from datetime import date, datetime

sys.path.append('..')
from tool.DataOperation import DataOperation

if __name__ == '__main__':
    a = True
    rf = {}
    rf['status'] = 'error'
    rf['data'] = 'INVALID TOKENID'
    # print json.dumps(rf)

    '''db = DataOperation()
    db.connect()
    sql = 'select * from token where userID = \'%s\';' % '1234\'; \nselect * from token where \'1\'=\'1'
    print sql
    cur = db.query(sql)
    print cur'''
    # s = 'name = ?' ?('james')
    # print s
    # result = {}
    # result['gender'] = '1'
    # result['userName'] = 'james'
    # result['info'] = 'player'
    # result['tokenID'] = 'xxxxxxxxxxxx'
    # print json.dumps(result)
    '''result = {}
    result['addressName'] = 'xxx'
    result['addressID'] = 'xxx'
    result['tel']= 'xxx'
    result['province']= 'xxx'
    result['city']= 'xxx'
    result['area']= 'xxx'
    result['description']= 'xxx'
    result['zipCode']= 'xxx'
    result['isdefault']= 1
    result['tokenID']= 'xxx'''
    # print json.dumps(result)
    '''result = {}
    result['info'] = 'kkkkkk'
    result['tokenID'] = 'c09bd67618d0eafda928f07280dd4cdc'
    result['requirementID'] = '21'
    # print json.dumps(result)
    # j = '{\\"tel\\": \\"15062225371\\",\\"receiver\\":\\"zero\\",\\"expressName\\": \\"First\\",\\"tokenID\\":\\"c09bd67618d0eafda928f07280dd4cdc\\"}'
    # print json.loads(j)
    jsonarr = '[{\"favoriteID\": \"177b2655a38d07680c40c42ab418acf3\", \"merchandiseID\": \"1\", \"userID\": \"53f6dd617c1d318face609dfb563ad48\", \"timeAndDate\": \"2015-07-13 17:39:55\"},{\"favoriteID\": \"1da1cdfe68d75628e5e71c77edd130e9\", \"merchandiseID\": \"2\", \"userID\": \"53f6dd617c1d318face609dfb563ad48\", \"timeAndDate\": \"2015-07-13 17:40:20\"},{\"favoriteID\": \"62916d2229e6eadf4af2d74ec250757d\", \"merchandiseID\": \"3\", \"userID\": \"53f6dd617c1d318face609dfb563ad48\", \"timeAndDate\": \"2015-07-13 17:40:23\"}]'
    rs = {}
    rs['status'] = 'success'
    rs['data'] = jsonarr
    # print json.dumps(rs)'''
    res = {}
    t = [[5, 6], [1, 2], [3, 4]]
    t1 = [1, 2, 3]
    list = []
    tel = '15651758376'
    s = tel[0:4] + '****' + tel[-4:]
    print s


def __default(obj):
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    else:
        raise TypeError('%r is not JSON serializable' % obj)
