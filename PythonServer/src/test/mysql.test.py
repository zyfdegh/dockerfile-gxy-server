# coding=utf8
import MySQLdb
import urllib2
import urllib
import json
import poster as poster
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
orderID = 'bb8aed1fe0c73413b4dcad17be37fbf1'
TOKEN_ID = 'b34c9a27008ab4f26dabd63b395751ee'
MERCHANDISE_ID = '431f52cf622de979fca2619d06d48876'
USER_ID = '75d45e053d0c2b6009a1d6c8577e3158'
expressID = '53c01dc577076ef65c85a2a68954af3c'
LOCALHOST = '127.0.0.1'
REMOTE = '121.43.111.75'


def fun():
    try:
        conn = MySQLdb.connect(host='192.168.1.102', user='root', passwd='root', db='secondhand', port=3306)
        cur = conn.cursor()

        value = ['3', '电脑', '1234']

        cur.execute('insert into requirement values(%s,%s,%s)', value)
        conn.commit()
        cur.close()
        conn.close()
    except MySQLdb.Error, e:
        print "Mysql Error %d: %s" % (e.args[0], e.args[1])


# 注册
def register():
    data = {}
    data['tel'] = '15062225372'
    data['password'] = '123'
    url = 'http://%s:5000/register/' % LOCALHOST
    post_data = urllib.urlencode(data)
    # 鎻愪氦锛屽彂閫佹暟鎹�
    req = urllib2.urlopen(url, post_data)
    # 鑾峰彇鎻愪氦鍚庤繑鍥炵殑淇℃伅
    content = req.read()
    print(content)


# 发布产品信息
def post():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/post_merchandise/'
    imgList = []
    imgList.append('file1')
    imgList.append('file2')
    info = {}
    info['name'] = 'zhulklllllll'
    info['age'] = '2555555'

    merchandiseInfo = {}
    merchandiseInfo['userID'] = '1234'
    merchandiseInfo['title'] = 'cameEEEEEEEEEEEra'
    merchandiseInfo['description'] = 'Nine'
    merchandiseInfo['merchandiseTypeID'] = '0'
    merchandiseInfo['price'] = 20
    merchandiseInfo['incomePrice'] = 60
    merchandiseInfo['carriage'] = 6
    merchandiseInfo['matching'] = True
    merchandiseInfo['college'] = 'Nanjing University'
    merchandiseInfo['location'] = 'Nanjing'
    merchandiseInfo['recommendation'] = True
    merchandiseInfo['swap'] = True
    merchandiseInfo['inspection'] = True
    merchandiseInfo['tokenID'] = TOKEN_ID
    merchandiseInfo['city'] = '南京'

    params = {'file1': open("D:/workspace/SecondHand/Secondhand/Pictures/images/text_xiaoguo.png", "rb"),
              'file2': open(u"D:/workspace/SecondHand/Secondhand/Pictures/images/广场1_05.png", "rb"),
              'merchandiseInfo': json.dumps(merchandiseInfo), 'imgList': json.dumps(imgList)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print result.read()


# 获取产品信息列表
def get_merchandise_list():
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
    upload_url = 'http://%s:5000/get_merchandise_list/' % REMOTE

    merchandiseInfo = {}

    params = {'merchandiseInfo': json.dumps(data)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 增加查询商品详情
def get_merchandise_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_merchandise_detail/'
    params = {'merchandiseID': MERCHANDISE_ID, 'tokenID': ''}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 修改商品接口
def update_merchandise():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/update_merchandise_info/'

    info = {}
    info['title'] = 'Hello'
    info['description'] = 'hhhhh'
    info['classification'] = '0'
    info['price'] = 13
    info['incomePrice'] = 60
    info['carriage'] = 6
    info['matching'] = True
    info['college'] = 'Nanjing University'
    info['location'] = 'Nanjing'
    info['recommendation'] = True
    info['inspection'] = True
    info['swap'] = True
    info['merchandiseID'] = '3edb9669fc702e53df7048d618c12e40'
    info['publishedTime'] = '2015-07-09'
    info['tokenID'] = '646877eb74094da28df1aef7ade08a02'
    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 登录
def login():
    data = {}
    data['tel'] = '15062225371'
    data['password'] = '123'
    url = 'http://%s:5000/login/' % REMOTE
    post_data = urllib.urlencode(data)
    req = urllib2.urlopen(url, post_data)
    content = req.read()
    print(content)


# 编辑上传
def upload():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5000/upload/' % LOCALHOST
    data = {}
    data['gender'] = 1
    data['userName'] = 'zero'
    data['info'] = 'student'
    data['tokenID'] = 'aaaaaa'
    data['residence'] = '南京'
    params = {'file': open("C:/Users/Public/Pictures/Sample Pictures/771724.jpg", "rb"), 'data': json.dumps(data),
              "isFile": "1"}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 创建地址
def addaddress():
    data = {}
    data['tel'] = '15062225371'
    data['addressName'] = 'nanjing'
    data['isdefault'] = True
    data['province'] = 'jiangsu'
    data['city'] = 'nanjing'
    data['area'] = 'nanligong'
    data['description'] = '200hao'
    data['zipCode'] = '210000'
    url = 'http://127.0.0.1:5000/add_address/'
    post_data = urllib.urlencode(data)
    req = urllib2.urlopen(url, post_data)
    content = req.read()
    print(content)


# 编辑地址
def editaddress():
    opener = poster.streaminghttp.register_openers()
    data = {}
    data['addressName'] = 'nanjing'
    data['addressID'] = 'd37e4451a202df16f709dac7dd1f2e6b'
    data['tel'] = '15062225371'
    data['province'] = 'beijing'
    data['city'] = 'beijing'
    data['area'] = 'area'
    data['description'] = 'beijing'
    data['zipCode'] = '123456'
    data['isdefault'] = True
    data['tokenID'] = '07a67cd855df48a464ed2c9192a9fa13'
    url = 'http://127.0.0.1:5000/editaddress/'
    params = {'data': json.dumps(data)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(url, datagen, headers)
    result = urllib2.urlopen(request)
    content = result.read()
    print(content)


# 发布一个快递代拿
def create_express():
    expressInfo = {}

    expressInfo['expressID'] = '123'
    expressInfo['expressName'] = 'Firset'
    expressInfo['userID'] = '1234'
    expressInfo['receiver'] = 'zero'
    expressInfo['tel'] = '15062225371'
    expressInfo['expressCompany'] = 'Shunfeng'
    expressInfo['expressAddress'] = 'South Gate'
    expressInfo['expressGetAddress'] = 'Library'
    expressInfo['expressNum'] = 'slkjsdfl'
    expressInfo['logisticsID'] = '1'
    expressInfo['tokenID'] = TOKEN_ID
    j = json.dumps(expressInfo)

    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/add_express/'

    params = {'data': json.dumps(expressInfo)}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 删除快递代拿信息
def delete_express():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/delete_express/'
    data = {}
    data['expressID'] = '2e79daea28e4551fc87cf70c236b7035'
    data['tokenID'] = '646877eb74094da28df1aef7ade08a02'
    params = {'data': json.dumps(data)}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 查询代拿信息
def search_express():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/search_express/'
    params = {'tokenID': '3b79479aadab031edeecde9bd5d42e94'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 删除地址
def deleteaddress():
    data = {}
    data['tokenID'] = '07a67cd855df48a464ed2c9192a9fa13'
    data['addressID'] = 'd37e4451a202df16f709dac7dd1f2e6b'
    upload_url = 'http://127.0.0.1:5000/deleteaddress/'
    post_data = urllib.urlencode(data)
    req = urllib2.urlopen(upload_url, post_data)
    content = req.read()
    print(content)


# 查询地址
def search_address():
    data = {}
    data['tokenID'] = TOKEN_ID
    upload_url = 'http://127.0.0.1:5000/search_address/'
    post_data = urllib.urlencode(data)
    req = urllib2.urlopen(upload_url, post_data)
    content = req.read()
    print(content)


# 生成订单
def generate_order():
    info = {}
    info['orderState'] = 'paid'
    info['sellerID'] = USER_ID
    info['buyerID'] = USER_ID
    info['tokenID'] = TOKEN_ID
    info['merchandiseID'] = MERCHANDISE_ID

    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5000/generate_order/' % REMOTE

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取订单列表
def get_order_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_order_list/'

    params = {'tokenID': '646877eb74094da28df1aef7ade08a02'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 修改订单状态
def update_order_status():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/update_order_list/'

    params = {'tokenID': '646877eb74094da28df1aef7ade08a02', 'status': 'paid'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 删除订单
def delete_order():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/delete_order/'

    params = {'tokenID': '3b79479aadab031edeecde9bd5d42e94', 'orderID': '851e3e44701f00729f29a7528cd48e91'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 通过OrderID获取商品信息
def get_merchandise_by_order():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_merchandise_by_order/'

    params = {'tokenID': '3b79479aadab031edeecde9bd5d42e94', 'orderID': 'dff7daa611569c91f37d6e520d95a11f'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取学校
def get_colleges():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_colleges/'

    params = {'tokenID': '646877eb74094da28df1aef7ade08a02', 'orderID': '60f36455919596b59a85fa8ec9a35298'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取排序方法列表
def get_sort_list():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_sort_list/'

    params = {'tokenID': '646877eb74094da28df1aef7ade08a02', 'orderID': '60f36455919596b59a85fa8ec9a35298'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取商品类型列表
def get_merchandise_type():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_merchandise_type/'

    params = {'tokenID': '646877eb74094da28df1aef7ade08a02', 'orderID': '60f36455919596b59a85fa8ec9a35298'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取我买到的
def get_my_bought():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5000/get_bought_list/' % REMOTE

    params = {'tokenID': TOKEN_ID, 'orderID': orderID}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取我卖出的
def get_my_sold():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_sold_list/'

    params = {'tokenID': '646877eb74094da28df1aef7ade08a02', 'orderID': 'bb8aed1fe0c73413b4dcad17be37fbf1'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 发布需求
def post_requirement():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/add_requirement/'

    params = {'tokenID': '09cfdba555de24ec3d06fa88b63d49ac', 'info': 'ccccc', 'merchandiseTypeID': '0'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 查询一个需求
def get_requirement():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/search_requirement/'

    params = {'tokenID': '09cfdba555de24ec3d06fa88b63d49ac', 'info': 'ccccc', 'merchandiseTypeID': '0'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 查询我的收藏
def get_my_favorite():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/search_favorite/'

    params = {'tokenID': TOKEN_ID}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取主页的图片
def get_pics():
    upload_url = 'http://127.0.0.1:5000/get_pics/'
    req = urllib2.urlopen(upload_url)
    content = req.read()
    print(content)


# 删除快递代发
def delete_express_post():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/delete_express_post/'
    params = {'tokenID': TOKEN_ID, 'expressPostID': 'cb764500411a17cbbedcaad3e5f1d4f8'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 发布快递代发
def create_express_post():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/create_express_post/'

    info = {}
    info['tokenID'] = TOKEN_ID
    info['expressName'] = 'xxx'
    info['tel'] = '15062225371'
    info['userName'] = '朱世杰'
    info['expressCompany'] = '申通'
    info['receiverCity'] = '北京'
    info['isOverWeight'] = False
    info['addressInfo'] = '南京大学北门'
    info['logisticsID'] = '1'

    params = {'data': json.dumps(info)}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 查询快递代拿代发列表
def get_express_all():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_express_all/'
    params = {'tokenID': TOKEN_ID}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 查询我的代发详细信息
def get_express_post_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_express_post_detail/'
    params = {'tokenID': TOKEN_ID, 'expressPostID': 'aefa6595d828f298990db7b4f4b40b0c'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 查询我的代拿详细信息
def get_express_get_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_express_get_detail/'
    params = {'tokenID': TOKEN_ID, 'expressGetID': '1f26082a3290df024a19cba8c4c65fad'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取账户信息
def get_account():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_account/'
    params = {'tokenID': TOKEN_ID, 'expressGetID': '1f26082a3290df024a19cba8c4c65fad'}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取城市列表
def get_city():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_city/'
    params = {}
    datagen, headers = poster.encode.multipart_encode(params)

    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 查询默认地址详情
def search_address_default_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/search_address_default_detail/'
    params = {'tokenID': 'cec57ea8762a28045ace4dd0a083ee2e'}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 商品浏览次数
def search_count():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/search_count/'
    params = {'merchandiseID': MERCHANDISE_ID}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 我的发布
def get_my_post():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_my_post/'
    params = {'tokenID': TOKEN_ID}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 获取用户详细信息
def get_user_detail():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/get_user_detail/'
    params = {'tokenID': TOKEN_ID}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())


# 发布产品信息
def post():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5000/post_merchandise/' % REMOTE
    imgList = []
    imgList.append('file1')
    imgList.append('file2')
    info = {}
    info['name'] = 'zhulklllllll'
    info['age'] = '2555555'

    merchandiseInfo = {}
    merchandiseInfo['userID'] = '1234'
    merchandiseInfo['title'] = 'cameEEEEEEEEEEEra'
    merchandiseInfo['description'] = 'Nine'
    merchandiseInfo['merchandiseTypeID'] = '0'
    merchandiseInfo['price'] = 20
    merchandiseInfo['incomePrice'] = 60
    merchandiseInfo['carriage'] = 6
    merchandiseInfo['matching'] = True
    merchandiseInfo['college'] = 'Nanjing University'
    merchandiseInfo['location'] = 'Nanjing'
    merchandiseInfo['recommendation'] = True
    merchandiseInfo['swap'] = True
    merchandiseInfo['inspection'] = True
    merchandiseInfo['tokenID'] = TOKEN_ID
    merchandiseInfo['city'] = '0'

    params = {'file1': open("D:/workspace/SecondHand/Secondhand/Pictures/images/text_xiaoguo.png", "rb"),
              'file2': open(u"D:/workspace/SecondHand/Secondhand/Pictures/images/广场1_05.png", "rb"),
              'merchandiseInfo': json.dumps(merchandiseInfo), 'imgList': json.dumps(imgList)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print result.read()


# 查询快递的状态
def search_logistics():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/search_logistics/'
    params = {'orderID': orderID, 'tokenID': TOKEN_ID}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())

# 增加单号(从订单里面进的)
def createLogisticsNo1():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/create_number_from_order/'
    params = {'tokenID': TOKEN_ID,'expressCompany':'','expressnum':'','orderID':''}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())

# 增加单号(从快递代发进的)
def createLogisticsNo2():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/create_number_from_post/'
    params = {'tokenID': TOKEN_ID,'expressCompany':'','expressnum':'','expressPostID':''}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())
    

# 根据商品的名字查询商品信息
def search_merchandise_by_name():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://127.0.0.1:5000/search_merchandise_by_name/'
    params = {'tokenID': '', 'merchandiseName': 'ca'}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())

# 查询支持的快递公司
def get_logistics_company():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5000/get_logistics_company/' % REMOTE
    params = {}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())

# 设置快递状态
def set_express_status():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5000/set_express_status/' % REMOTE
    status = {}
    status['expressID'] = expressID
    status['expressStatusID'] = '0'
    status['tokenID'] = TOKEN_ID
    params = {'status': json.dumps(status)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())

# 获取快递状态
def get_express_status():
    opener = poster.streaminghttp.register_openers()
    upload_url = 'http://%s:5000/get_express_status/' % REMOTE
    status = {}
    status['expressID'] = expressID
    status['expressStatusID'] = '0'
    status['tokenID'] = TOKEN_ID
    params = {'status': json.dumps(status)}
    datagen, headers = poster.encode.multipart_encode(params)
    request = urllib2.Request(upload_url, datagen, headers)
    result = urllib2.urlopen(request)
    print(result.read())



if __name__ == "__main__":
    # register()
    # login()
    # upload()
    # addaddress()
    # editaddress()
    # deleteaddress()
    # search_address()
    # get_merchandise_list()
    # get_merchandise_detail()
    # update_merchandise()
    # generate_order()
    # get_order_list()
    # update_order_status()
    # delete_order()
    # post()
    # create_express()
    # delete_express()
    # search_express()
    # get_colleges()
    # get_merchandise_type()
    # get_my_bought()
    # get_my_sold()
    # post_requirement()
    # get_requirement()
    # get_my_favorite()
    # get_merchandise_type()
    # create_express_post()
    # delete_express_post()
    # get_express_all()
    # get_express_post_detail()
    # get_express_get_detail()
    # get_account()
    # get_city()
    # search_address_default_detail()
    # search_count()
    # get_my_post()
    # get_user_detail()
    # search_logistics()
    # createLogisticsNo1()
    # createLogisticsNo2()
    # get_logistics_company()
    set_express_status()