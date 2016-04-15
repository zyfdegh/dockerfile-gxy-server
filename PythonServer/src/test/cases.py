# coding=utf8
import MySQLdb
import urllib2
import urllib
import json
import poster as poster
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
TOKEN_ID = 'beb6b5d38f82e3edf0250a486189fdd4'
MERCHANDISE_ID = '00acfae81c15891b6b08ddcdb820da8b'

# 测试获取商品列表
# 1,正常登录，tokenID正确，获取商品列表结果正确
# 2，
def get_merchandise_list_normal():
    data = {}
    data['college'] = '0'
    data['merchandiseType'] = '书籍旧刊'
    data['merchandiseType'] = '0'
    data['sortType'] = '0'
    data['pageCount'] = 10
    data['tokenID'] = TOKEN_ID
    data['start'] = 0
    data['city'] = '0'

    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://121.43.111.75:5000/get_merchandise_list/'

    merchandiseInfo = {}

    params = {'merchandiseInfo': json.dumps(data)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    expect_json = '{"status": "SUCCESS", "data": [{"userName": "\u7fa4\u9b54\u4e71\u821e", "portraitPath": "9ffe51067f20a386d30dbbe466a1bca2.jpg", "publishedTime": "2015-07-25 17:43:49", "oldPrice": 800.0, "merchandiseID": "a2ff7f01ee591b28a827771b3738443a", "favorite": null, "imgPath": ["1437817421584.jpg"], "currentPrice": 800.0, "info": "\u8003\u8651", "college": "0", "shipmentPrice": null, "merchandiseName": "\u54c8\u4f26\u88e4", "merchandiseTypeName": "\u4e66\u7c4d\u65e7\u520a"}]}'
    assert (result.read() == expect_json)
    # print(result.read())

if __name__ == "__main__":
    get_merchandise_list_normal()