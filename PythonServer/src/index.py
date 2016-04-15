# coding=utf8
import os
import os.path
from flask import Flask, request, url_for
from address.AddressManager import AddressManager
import sys

sys.path.append('..')

from tool.RYClient import RYClient
from user.WorkerManager import WokerManager
from wokerTask.TaskExpressGetManger import TaskExpressGetManager
from wokerTask.TaskExpressPostManger import TaskExpressPostManager
from wokerTask.TaskInspectionManger import TaskInspectionManager

from user.UserManager import UserManager
from stoken.TokenManager import TokenManager
from werkzeug.utils import secure_filename
from merchandise.MerchandiseManager import MerchandiseManager
from express.ExpressManager import ExpressManager
from order.OrderManager import OrderManager
from favorite.FavoriteManager import FavoriteManager
from requirement.RequirementManager import RequirementManager
from myself.MyselfManager import MyselfManager
import json
from PIL import Image

app = Flask(__name__)

# 定义一个上传文件的全局路径
UPLOAD_FOLDER = '/opt/Secondhand/Server/Server/src/static'
# UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# 发布商品
@app.route('/post_merchandise/', methods=['POST', 'GET'])
def post_merchandise():
    result = {}
    result['status'] = 'FAILED'
    result['data'] = 'NULL'
    if request.method == 'POST':
        imgListJson = request.form['imgList']
        merchandiseInfo = request.form['merchandiseInfo']
        imgList = json.loads(imgListJson)
        merchandiseManager = MerchandiseManager()

        # 图片上传时的所有参数
        imgPathList = []
        fileDict = {}
        for img in imgList:
            # 根据名称来获取文件对象并保存
            imgFile = request.files[img]

            if imgFile and allowed_file(imgFile.filename):
                filename = secure_filename(imgFile.filename)
                fileDict[filename] = imgFile
                imgPathList.append(filename)
        merchandiseID = merchandiseManager.createMerchandise(merchandiseInfo, imgPathList)
        if False == merchandiseID:
            result['data'] = 'Bad tokenID'
            return json.dumps(result)
        WIDTH = 240
        HEIGHT = 240
        for i in imgPathList:
            filePathOrigin = 'merchandise/%s/origin/%s' % (merchandiseID, i)
            merchandisePath = os.path.join(app.config['UPLOAD_FOLDER'], 'merchandise')
            if not os.path.isdir(merchandisePath):
                os.makedirs(merchandisePath)
            merchandiseIDPath = os.path.join(merchandisePath, merchandiseID)
            if not os.path.isdir(merchandiseIDPath):
                os.makedirs(merchandiseIDPath)
            merchandiseOriginPath = os.path.join(merchandiseIDPath, 'origin')
            if not os.path.isdir(merchandiseOriginPath):
                os.makedirs(merchandiseOriginPath)
            merchandiseThumbPath = os.path.join(merchandiseIDPath, 'thumbnail')
            if not os.path.isdir(merchandiseThumbPath):
                os.makedirs(merchandiseThumbPath)
            imgFile = fileDict[i]
            originImg = os.path.join(merchandiseOriginPath, i)
            imgFile.save(originImg)
            # 生成一份缩略图
            thumbnailpath = 'merchandise/%s/thumbnail/%s' % (merchandiseID, i)
            img = Image.open(originImg)
            img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
            imgThumbNail = os.path.join(merchandiseThumbPath, i)
            img.save(imgThumbNail)

        result['status'] = 'SUCCESS'
        result['data'] = merchandiseID
    return json.dumps(result)


# 查询发布产品的列表
@app.route('/get_merchandise_list/', methods=['POST', 'GET'])
def get_merchandise_list():
    result = {}
    result['status'] = 'FAILED'
    result['data'] = 'NULL'
    if request.method == 'POST':
        data = request.form['merchandiseInfo']
        merchandiseManager = MerchandiseManager()
        resultData = merchandiseManager.getMerchandiseInfoBriefList(data)
        if False == resultData:
            result['data'] = 'Bad tokenID'
        elif None == resultData:
            result['data'] = 'No data'
        else:
            result['status'] = 'SUCCESS'
            result['data'] = resultData
        return json.dumps(result)


@app.route('/get_posted_merchandise_detail/', methods=['POST', 'GET'])
def get_posted_merchandise_detail():
    result = {}
    result['status'] = 'FAILED'
    result['data'] = 'NULL'
    if request.method == 'POST':
        data = request.form['merchandiseInfo']
        merchandiseManager = MerchandiseManager()
        resultData = merchandiseManager.getPostedMerchandiseDetail(data)
        if False == resultData:
            result['data'] = 'Bad tokenID'
        elif None == resultData:
            result['data'] = 'No data'
        else:
            result['status'] = 'SUCCESS'
            result['data'] = resultData
        return json.dumps(result)

# 查询单个商品详情
@app.route('/get_merchandise_detail/', methods=['POST', 'GET'])
def get_merchandise_detail():
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        merchandiseID = request.form['merchandiseID']
        merchandiseManager = MerchandiseManager()
        info = merchandiseManager.getMerchandiseDetail(tokenID, merchandiseID)
        if False == info:
            data['status'] = 'FAILED'
            data['data'] = 'NULL'
            return json.dumps(data)

        data['data'] = info
        data['status'] = 'SUCCESS'
        return json.dumps(data)
    else:
        pass


# 更新商品信息
@app.route('/update_merchandise_info/', methods=['POST', 'GET'])
def update_merchandise_info():
    if request.method == 'POST':
        data = request.form['data']
        imgList = request.form['imgList']
        merchandiseManager = MerchandiseManager()
        

        imgModificationList = {}
        addList = []
        deleteList = []
        imgModificationList['add'] = addList
        imgModificationList['delete'] = deleteList
        for i in imgList:
            if '0' == i['action']:
                # 根据名称来获取文件对象并保存
                imgFile = request.files[i['img']]
                if imgFile and allowed_file(imgFile.filename):
                    filename = secure_filename(imgFile.filename)
                    # filename = merchandiseManager.getMD5String(str(merchandiseManager.getCurrentTime()).join(filename))
                    imgFile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    addList.append(filename)
            else:
                delFileName = request.files[i['img']]
                if os.path.isfile(delFileName):
                    os.remove(delFileName)
                    deleteList.append(delFileName)

        result = merchandiseManager.updateMerchandiseInfo(data, imgModificationList)
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        if False == result:
            resultData['data'] = 'Bad TokenID'
            return json.dumps(resultData)
        resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)


# 发布快递代拿
@app.route('/add_express/', methods=['POST', 'GET'])
def add_express():
    expressManager = ExpressManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        expressInfo = request.form['data']
        expressID = expressManager.createExpress(expressInfo)
        if False == expressID:
            data['data'] = 'Bad tokenID'
            return json.dumps(data)

        data['status'] = 'SUCCESS'
        data['data'] = expressID
        return json.dumps(data)


# 删除快递代拿信息
@app.route('/delete_express/', methods=['POST', 'GET'])
def delete_express():
    expressManager = ExpressManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        expressInfo = request.form['data']

        if True == expressManager.deleteExpressInfo(expressInfo):
            data['status'] = 'SUCCESS'
        return json.dumps(data)


# 查询快递
@app.route('/search_express/', methods=['POST', 'GET'])
def search_express():
    expressManager = ExpressManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        jsonlist = expressManager.searchExpress(tokenID)
        if jsonlist != None and jsonlist != False:
            data['status'] = 'SUCCESS'
            data['data'] = jsonlist
        return json.dumps(data)


# 注册
@app.route('/register/', methods=['POST', 'GET'])
def register():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        tel = request.form['tel']
        pwd = request.form['password']

        userID = userManager.createUserQuickly(tel, pwd)
        if userID != None and userID != False:
            data['status'] = 'SUCCESS'
            data['data'] = userID

    else:
        pass
    return json.dumps(data)


# 登录
@app.route('/login/', methods=['POST', 'GET'])
def login():
    userManager = UserManager()
    tokenManager = TokenManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        tel = request.form['tel']
        pwd = request.form['password']
        # 判断用户是否存在
        (status, userID, ryToken) = userManager.searchUser(tel, pwd)
        if status == 1:
            # 代表这个用户存在
            # 登录成功后便为这个用户创建一个token
            # userID是由密码MD5而来的
            userID = userManager.getMD5String(tel)
            tokenID = tokenManager.createToken(userID)
            resultData = {}
            resultData['tokenID'] = tokenID
            resultData['ryTokenID'] = ryToken
            data['status'] = 'SUCCESS'
            data['data'] = resultData
            return json.dumps(data)
        else:
            # 代表这个用户不存在
            # return 'ERROR TEL OR PASSWORD'
            data['data'] = 'ERROR TEL OR PASSWORD'
            return json.dumps(data)
    else:
        pass


# 编辑上传
@app.route('/upload/', methods=['POST', 'GET'])
def upload():
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    userManager = UserManager()
    newfilepath = None
    WIDTH = 240
    HEIGHT = 240
    if request.method == 'POST':
        jsonInfo = request.form['data']
        (ret, tokenID, userID) = userManager.getUserInfo(jsonInfo)

        isfile = request.form['isFile']
        if isfile == '1':
            imgfile = request.files['file']
            if imgfile and allowed_file(imgfile.filename):
                filename = secure_filename(imgfile.filename)
                currentTime = userManager.getCurrentTime()
                filePostPix = str(filename).split('.')
                newfilepath = userManager.getMD5String(currentTime + tokenID)
                newfilepath = newfilepath + '.' + filePostPix[-1]
                # 将上传的高清大图放到hd_portrait目录下
                newfilepathorign = 'portrait/%s/hd_portrait/%s' % (userID, newfilepath)
                imgfile.save(os.path.join(app.config['UPLOAD_FOLDER'], newfilepathorign))
                # 生成一份缩略图
                thumbnailpath = 'portrait/%s/thumbnail_portrait/%s' % (userID, newfilepath)
                img = Image.open(newfilepath)
                img = img.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
                img.save(os.path.join(app.config['UPLOAD_FOLDER'], thumbnailpath))
        else:
            pass
    else:
        pass
    # 获取编辑是否成功
    result = userManager.editUserInfo(jsonInfo, newfilepath, isfile)
    if result == True:
        data['status'] = 'SUCCESS'
    # 返回json格式
    return json.dumps(result)


# 查询用户信息
@app.route('/get_user_detail/', methods=['POST', 'GET'])
def get_user_detail():
    userManager = UserManager()
    data = {}
    data['status'] = 'FAILED'
    data['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        jsoninfo = userManager.getUserDetail(tokenID)
        if jsoninfo != None and jsoninfo != False:
            data['status'] = 'SUCCESS'
            data['data'] = jsoninfo
        return json.dumps(data)
    else:
        pass


# 创建地址
@app.route('/add_address/', methods=['POST', 'GET'])
def add_address():
    addressManager = AddressManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':

        data = request.form['data']
        data = json.loads(data)

        tokenID = data['tokenID']
        tel = data['tel']
        addressName = data['addressName']
        isdefault = data['isdefault']
        province = data['province']
        city = data['city']
        area = data['area']
        description = data['description']
        zipCode = data['zipCode']
        userName = data['userName']

        addressID = addressManager.createAddress(addressName, tokenID, tel, province, city, area, description, zipCode,
                                                 isdefault, userName)
        if addressID != None and addressID != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = addressID
        return json.dumps(resultData)
    else:
        pass


# 编辑地址
@app.route('/edit_address/', methods=['POST', 'GET'])
def edit_address():
    addressManager = AddressManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        jsoninfo = request.form['data']
        data = addressManager.editAddress(jsoninfo)
        if data == True:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)
    else:
        pass


# 删除地址
@app.route('/delete_address/', methods=['POST', 'GET'])
def delete_address():
    addaddress = AddressManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        addressID = request.form['addressID']
        data = addaddress.deleteAddress(tokenID, addressID)
        if data == True:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)
    else:
        pass


@app.route('/search_address/', methods=['POST', 'GET'])
def search_address():
    addaddress = AddressManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        info = addaddress.searchAddress(tokenID)
        if info != None and info != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = info
        return json.dumps(resultData)
    else:
        pass


# 生成订单
@app.route('/generate_order/', methods=['POST', 'GET'])
def generate_order():
    if request.method == 'POST':
        data = request.form['data']
        orderManager = OrderManager()
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        (orderID, buyerID, sellerID) = orderManager.createOrder(data)
        if False == orderID:
            resultData['data'] = 'Bad tokenID'
        ryClient = RYClient()
        ryClient.publishMessage(buyerID, sellerID, "您发布的商品已经被下单了，赶快到我卖出的里面看下吧！")
        resultData['status'] = 'SUCCESS'
        resultData['data'] = orderID
        return json.dumps(resultData)

# 取消订单
@app.route('/cancel_order/', methods=['POST','GET'])
def cancel_order():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        orderID = request.form['orderID']
        # merchandiseID = request.form['merchandiseID']
        orderManager = OrderManager()
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        ret = orderManager.CancelOrder(tokenID, orderID)
        if False == ret:
            resultData['data'] = 'Bad tokenID'

        resultData['status'] = 'SUCCESS'
        resultData['data'] = 'NULL'

        return json.dumps(resultData)

# 更新订单里的支付宝ID
@app.route('/update_alipay_id/', methods = ['POST', 'GET'])
def update_alipay_id():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        alipayID = request.form['alipayID']
        orderID = request.form['orderID']
        orderManager = OrderManager()
        ret = orderManager.changeAlipayID(tokenID, orderID, alipayID)
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        if False == ret:
            resultData['data'] = 'Bad tokenID'
        else:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)



# 增加一个我的收藏
@app.route('/add_favorite/', methods=['POST', 'GET'])
def add_favorite():
    favoriteManager = FavoriteManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        merchandiseID = request.form['merchandiseID']
        favoriteID = favoriteManager.createFavorite(tokenID, merchandiseID)
        if favoriteID != None or favoriteID != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = favoriteID
        return json.dumps(resultData)

    else:
        pass


# 删除一个收藏表
@app.route('/delete_favorite/', methods=['POST', 'GET'])
def delete_favorite():
    favoriteManager = FavoriteManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        merchandiseID = request.form['merchandiseID']
        data = favoriteManager.deleteFavorite(tokenID, merchandiseID)
        if True == data:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)
    else:
        pass


# 获取收藏列表
@app.route('/search_favorite/', methods=['POST', 'GET'])
def search_favorite():
    favoriteManager = FavoriteManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        jsonlist = favoriteManager.searchFavorite(tokenID)
        if jsonlist != None and jsonlist != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = jsonlist
        return json.dumps(resultData)

    else:
        pass


# 查询订单列表
@app.route('/get_order_list/', methods=['POST', 'GET'])
def get_order_list():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        orderManager = OrderManager()

        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        orderList = orderManager.getOrderList(tokenID)
        if False == orderList:
            resultData['status'] = 'FAILED'
            resultData['data'] = 'Bad tokenID'

        resultData['status'] = 'SUCCESS'
        resultData['data'] = orderList

        return json.dumps(resultData)


# 我买到的
@app.route('/get_bought_list/', methods=['POST', 'GET'])
def get_bought_list():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        orderManager = OrderManager()

        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        orderList = orderManager.getMyBought(tokenID)
        if False == orderList:
            resultData['status'] = 'FAILED'
            resultData['data'] = 'Bad tokenID'

        resultData['status'] = 'SUCCESS'
        resultData['data'] = orderList
        return json.dumps(resultData)


# 我卖出的
@app.route('/get_sold_list/', methods=['POST', 'GET'])
def get_sold_list():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        orderManager = OrderManager()

        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        orderList = orderManager.getMySold(tokenID)
        if False == orderList:
            resultData['status'] = 'FAILED'
            resultData['data'] = 'Bad tokenID'

        resultData['status'] = 'SUCCESS'
        resultData['data'] = orderList

        return json.dumps(resultData)


# 修改订单状态
@app.route('/update_order_status/', methods=['POST', 'GET'])
def update_order_status():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        status = request.form['status']
        orderID = request.form['orderID']
        orderManager = OrderManager()
        result = orderManager.changeOrderState(status, tokenID, orderID)
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        if False == result:
            resultData['data'] = 'Bad tokenID'

        resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)


# 删除订单
@app.route('/delete_order/', methods=['POST', 'GET'])
def delete_order():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        orderID = request.form['orderID']
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        orderManager = OrderManager()
        result = orderManager.deleteOrder(tokenID, orderID)
        if False == result:
            resultData['data'] = 'Bad tokenID'

        resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)


# 添加一个需求
@app.route('/add_requirement/', methods=['POST', 'GET'])
def add_requirement():
    requirementManager = RequirementManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'

    if request.method == 'POST':
        tokenID = request.form['tokenID']
        info = request.form['info']
        merchandiseType = request.form['merchandiseTypeID']
        requirementID = requirementManager.createRequirement(tokenID, info, merchandiseType)
        if requirementID != None and requirementID != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = requirementID
        return json.dumps(resultData)

    else:
        pass

# 添加一个需求，需要指定城市和学校
@app.route('/add_requirement_by_college/', methods=['POST', 'GET'])
def add_requirement_by_college():
    requirementManager = RequirementManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'

    if request.method == 'POST':
        params = request.form['params']
        (ret, requirementID) = requirementManager.createRequirementByCollege(params)
        if False == ret:
            resultData['data'] = requirementID
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = requirementID
        return json.dumps(resultData)

# 删除一个需求
@app.route('/delete_requirement/', methods=['POST', 'GET'])
def delete_requirement():
    requirementManager = RequirementManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'

    if request.method == 'POST':
        tokenID = request.form['tokenID']
        requirementID = request.form['requirementID']
        data = requirementManager.deleteRequirment(tokenID, requirementID)
        if True == data:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)
    else:
        pass


# 编辑一个需求
@app.route('/edit_requirement/', methods=['POST', 'GET'])
def edit_requirement():
    requirementManager = RequirementManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        jsoninfo = request.form['data']
        data = requirementManager.editRequirment(jsoninfo)
        if True == data:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)
    else:
        pass

# 按页查询所有需求
@app.route('/search_requirement_by_page/', methods=['POST', 'GET'])
def search_requirement_by_page():
    requirementManager = RequirementManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        param = request.form['param']
        reqList = requirementManager.getAllRequirement(param)
        if False == reqList or None == reqList:
            resultData['data'] = 'Bad tokenID or bad search'
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = reqList
        return json.dumps(resultData)


# 查询所有需求
@app.route('/search_requirement/', methods=['POST', 'GET'])
def search_requirement():
    requirementManager = RequirementManager()
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        jsonlist = requirementManager.searchRequirment(tokenID)
        if jsonlist != None and jsonlist != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = jsonlist
        return json.dumps(resultData)
    else:
        pass


# 获取所支持的学校列表
@app.route('/get_colleges/', methods=['POST', 'GET'])
def get_colleges():
    if request.method == 'POST':
        merchandiseManager = MerchandiseManager()
        data = {}
        data['status'] = 'SUCCESS'
        data['data'] = merchandiseManager.getCollegeInfo()
        return json.dumps(data)

# 通过城市获取城市列表,tag 0时该接口返回该城市所有的大学，否则返回只支持的大学
@app.route('/get_colleges_by_city/', methods=['POST', 'GET'])
def get_colleges_by_city():
    if request.method == 'POST':
        merchandiseManager = MerchandiseManager()
        data = {}
        data['status'] = 'FAILED'
        data['data'] = 'NULL'
        params = request.form['params']
        cityList = merchandiseManager.getCollegeListByCity(params)
        if False == cityList or None == cityList:
            data['data'] = 'Bad token or bad sql query'
        else:
            data['status'] = 'SUCCESS'
            data['data'] = cityList
        return json.dumps(data)

# 获取排序类型列表
@app.route('/get_sort_list/', methods=['POST', 'GET'])
def get_sort_list():
    if request.method == 'POST':
        merchandiseManager = MerchandiseManager()
        data = {}
        data['status'] = 'SUCCESS'
        data['data'] = merchandiseManager.getSortType()
        return json.dumps(data)


# 获取商品类型列表
@app.route('/get_merchandise_type/', methods=['POST', 'GET'])
def get_merchandise_type():
    if request.method == 'POST':
        merchandiseManager = MerchandiseManager()
        data = {}
        data['status'] = 'SUCCESS'
        data['data'] = merchandiseManager.getMerchandiseType()
        return json.dumps(data)


# 通过OrderID查询商品信息
@app.route('/get_merchandise_by_order/', methods=['POST', 'GET'])
def get_merchandise_by_order():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        tokenID = request.form['tokenID']
        orderID = request.form['orderID']
        merchandiseManager = MerchandiseManager()
        merchandiseInfo = merchandiseManager.getMerchandiseByOrderID(tokenID, orderID)
        if False == resultData:
            resultData['data'] = 'Bad tokenID'
        elif -1 == resultData:
            resultData['data'] = 'Bad orderID'
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = merchandiseInfo

        return json.dumps(resultData)

# 获取商品的详情，及订单状态
@app.route('/get_merchandise_order_state/', methods=['POST', 'GET'])
def get_merchandise_order_state():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        orderManager = OrderManager()
        tokenID = request.form['tokenID']
        merchandiseID = request.form['merchandiseID']
        orderInfo = orderManager.getOrderDetailByMerchandiseID(tokenID, merchandiseID)
        if False == orderInfo:
            resultData['status'] = 'FAILED'
            resultData['data'] = 'Bad tokenID'
        elif None == orderInfo:
            resultData['data'] = 'NULL'
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = orderInfo
        return json.dumps(resultData)
         

# 删除快递代发
@app.route('/delete_express_post/', methods=['POST', 'GET'])
def delete_express_post():
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    expressManager = ExpressManager()
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        expressPostID = request.form['expressPostID']
        tag = request.form['tag']
        info = expressManager.deleteExpressInfo(tokenID, expressPostID, tag)
        if info == True:
            resultData['status'] = 'SUCCESS'
    return json.dumps(resultData)


# 发布快递代发消息
@app.route('/create_express_post/', methods=['POST', 'GET'])
def create_express_post():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        expressInfo = request.form['data']
        expressManager = ExpressManager()
        expressPostID = expressManager.createExpressPost(expressInfo)
        if False == expressPostID:
            resultData['data'] = 'Bad tokenID'

        resultData['status'] = 'SUCCESS'
        resultData['data'] = expressPostID
        return json.dumps(resultData)


# 查询快递代拿代发列表
@app.route('/get_express_all/', methods=['POST', 'GET'])
def get_express_all():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        tokenID = request.form['tokenID']
        expressManager = ExpressManager()
        result = expressManager.getExressAllList(tokenID)

        if result != None and result != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = result
    return json.dumps(resultData)


# 查询我的代发详细信息
@app.route('/get_express_post_detail/', methods=['POST', 'GET'])
def get_express_post_detail():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        tokenID = request.form['tokenID']
        expressPostID = request.form['expressPostID']
        expressManager = ExpressManager()
        result = expressManager.getExpressPostInfo(tokenID, expressPostID)
        if result != None and result != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = result
    return json.dumps(resultData)


# 查询我的代拿详细信息
@app.route('/get_express_get_detail/', methods=['POST', 'GET'])
def get_express_get_detail():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        tokenID = request.form['tokenID']
        expressGetID = request.form['expressGetID']
        expressManager = ExpressManager()
        result = expressManager.getExpressGetInfo(tokenID, expressGetID)
        if result != None and result != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = result
    return json.dumps(resultData)


# 增加单号(从订单里面进的)
@app.route('/create_number_from_order/', methods=['POST', 'GET'])
def create_number_from_order():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        tokenID = request.form['tokenID']
        expressCompany = request.form['expressCompany']
        expressnum = request.form['expressnum']
        orderID = request.form['orderID']
        expressManager = ExpressManager()
        result = expressManager.createLogisticsNo1(tokenID, expressCompany, expressnum, orderID)
        if result == True:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)


# 增加单号(从代发里面进的)
@app.route('/create_number_from_post/', methods=['POST', 'GET'])
def create_number_from_post():
    if request.method == 'POST':
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        tokenID = request.form['tokenID']
        expressCompany = request.form['expressCompany']
        expressnum = request.form['expressnum']
        expressPostID = request.form['expressPostID']
        expressManager = ExpressManager()
        result = expressManager.createLogisticsNo2(tokenID, expressCompany, expressnum, expressPostID)
        if result == True:
            resultData['status'] = 'SUCCESS'
        return json.dumps(resultData)


# 获取账户余额
@app.route('/get_account/', methods=['POST', 'GET'])
def get_account():
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        userManager = UserManager()
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        account = userManager.getAccount(tokenID)

        if None == account:
            resultData['data'] = 'No data'
        elif False == account:
            resultData['data'] = 'Bad tokenID'
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = account

        return json.dumps(resultData)


# 获取城市列表
@app.route('/get_city/', methods=['POST', 'GET'])
def get_city():
    if request.method == 'POST':
        merchandiseManager = MerchandiseManager()

        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        cityList = merchandiseManager.getCityList()
        if None == cityList:
            resultData['data'] = 'No data'
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = cityList

        return json.dumps(resultData)


# 查询默认地址详情
@app.route('/search_address_default_detail/', methods=['POST', 'GET'])
def search_address_default_detail():
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    if request.method == 'POST':
        addressManager = AddressManager()
        tokenID = request.form['tokenID']
        addressInfo = addressManager.searchAddressDefaultDetail(tokenID)
        if addressInfo != None and addressInfo != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = addressInfo
        return json.dumps(resultData)
    else:
        pass

# 删去我的发布
@app.route('/delete_my_post/',methods=['POST','GET'])
def delete_my_post():
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    merchandiseManager = MerchandiseManager()
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        merchandiseID = request.form['merchandiseID']
        postInfo = merchandiseManager.deleteMerchandise(tokenID,merchandiseID)
        if postInfo != None and postInfo != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = postInfo
        return json.dumps(resultData)
    else:
        pass

# 我的发布
@app.route('/get_my_post/', methods=['POST', 'GET'])
def get_my_post():
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    myselfManager = MyselfManager()
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        postInfo = myselfManager.getMypost(tokenID)
        if postInfo != None and postInfo != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = postInfo
        return json.dumps(resultData)
    else:
        pass


# 查询快递的状态
@app.route('/search_logistics/', methods=['GET', 'POST'])
def search_logistics():
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    expressManager = ExpressManager()
    if request.method == 'POST':
        orderID = request.form['orderID']
        tokenID = request.form['tokenID']
        info = expressManager.searchLogistics(orderID, tokenID)
        if info != None and info != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = info
        return json.dumps(resultData)
    else:
        pass

# 根据商品的名字或者描述查询商品信息
@app.route('/search_merchandise_by_name/',methods=['POST','GET'])
def search_merchandise_by_name():
    resultData = {}
    resultData['status'] = 'FAILED'
    resultData['data'] = 'NULL'
    merchandiseManager = MerchandiseManager()
    if request.method == 'POST':
        tokenID = request.form['tokenID']
        merchandiseName = request.form['merchandiseName']
        info = merchandiseManager.searchMerchandiseByName(tokenID,merchandiseName)
        if info != None and info != False:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = info
        return json.dumps(resultData)
    else:
        pass

# 获取支持的快递公司接口
@app.route('/get_logistics_company/', methods = ['POST', 'GET'])
def get_logistics_company():
    if request.method == 'POST':
        expressManager = ExpressManager()
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        if None == expressManager or False == expressManager:
            return json.dumps(resultData)
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = expressManager.getLogisticsCompanyInfo()
            return json.dumps(resultData)


# 设置快递状态
@app.route('/set_express_status/', methods = ['POST', 'GET'])
def set_express_status():
    if request.method == 'POST':
        expressManager = ExpressManager()
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        jsonStatus = request.form['status']
        ret = expressManager.setExpressStatus(jsonStatus)
        if None == ret or False == ret:
            return json.dumps(resultData)
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = jsonStatus
            return json.dumps(resultData)

# 获取快递状态信息
@app.route('/get_express_status/', methods = ['POST', 'GET'])
def get_express_status():
    if request.method == 'POST':
        expressManager = ExpressManager()
        resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        jsonStatus = request.form['status']
        ret = expressManager.getExpressStatus(jsonStatus)
        if None == ret or False == ret:
            return json.dumps(resultData)
        else:
            resultData['status'] = 'SUCCESS'
            resultData['data'] = jsonStatus
            return json.dumps(resultData)

# 获取商品是否被锁定
@app.route('/get_merchandise_freeze_state/', methods = ['POST', 'GET'])
def get_merchandise_freeze_state():
    if request.method == 'POST':
        merchandiseID = request.form['merchandiseID']
        merchandiseManager = MerchandiseManager()
        isFreeze = merchandiseManager.isMerchandiseFrozen(merchandiseID)
       	resultData = {}
        resultData['status'] = 'FAILED'
        resultData['data'] = 'NULL'
        if None == isFreeze:
            return json.dumps(resultData)
        resultData['status'] = 'SUCCESS'
        resultData['data'] = isFreeze
        return json.dumps(resultData)

# 精品推荐
@app.route('/set_recommendation/', methods = ['POST', 'GET'])
def set_recommendation():
    if request.method == 'POST':
        info = request.form['info']
        merchandiseManager = MerchandiseManager()
        ret = merchandiseManager.setRecommendation(info)
        resultData = {}
        resultData['status'] = 'SUCCESS'
        resultData['data'] = ret
        return json.dumps(resultData)

# 查询广场里的商品
@app.route('/get_recommendated_merchandise_list/', methods = ['POST', 'GET'])
def get_recommendated_merchandise_list():
    result = {}
    result['status'] = 'FAILED'
    result['data'] = 'NULL'
    if request.method == 'POST':
        data = request.form['merchandiseInfo']
        merchandiseManager = MerchandiseManager()
        resultData = merchandiseManager.getMerchandiseInfoBriefList(data, True)
        if False == resultData:
            result['data'] = 'Bad tokenID'
        elif None == resultData:
            result['data'] = 'No data'
        else:
            result['status'] = 'SUCCESS'
            result['data'] = resultData
        return json.dumps(result)

# 通过UserID获取用户信息
@app.route('/get_user_by_id/', methods = ['POST', 'GET'])
def get_user_by_id():
    result = {}
    result['status'] = 'FAILED'
    result['data'] = 'NULL'
    if request.method == 'POST':
        userManager = UserManager()
        userID = request.form['userID']
        tokenID = request.form['tokenID']
        info = userManager.getUserDetailInfoByUserID(userID, tokenID)
        if None == info:
            return json.dumps(result)
        elif False == info:
           result['data'] = 'Bad tokenID'
           return json.dumps(result)
        result['status'] = 'SUCCESS'
        result['data'] = info
        return json.dumps(result)

# 工作人员注册
@app.route('/worker_register/', methods=['POST', 'GET'])
def worker_register():
    if(request.method == 'POST'):
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        tel = request.form['tel']
        pwd = request.form['password']
        adminID = request.form['adminID']
        adminPW = request.form['adminPW']
        workerManager = WokerManager(adminID, adminPW)
        allResult = workerManager.createWorker(tel,pwd)
        if(False == allResult):
            return json.dumps(result)
        else:
            workerID = allResult
            result['status'] = 'SUCCESS'
            result['data'] = workerID
            return json.dumps(result)
    else:
        pass

# 工作人员登录
@app.route('/worker_login/', methods=['POST', 'GET'])
def worker_login():
    if(request.method == 'POST'):
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        tel = request.form['tel']
        pwd = request.form['password']
        workerManager = WokerManager()
        (workerID, ryTokenID, workerInfo) = workerManager.searchWorker(tel, pwd)
        tokenManager = TokenManager()
        #判断用户是否存在
        # (status,userID,ryToken) = userManager.searchUser(tel,pwd)

        if(workerID != False and workerID != None):
            #代表这个用户存在
            #登录成功后便为这个用户创建一个token
            #userID由密码MD5而来的
            toKenID = tokenManager.createToken(workerID)
            resultData  = {}
            resultData['tokenID'] = toKenID
            resultData['ryTokenID'] = ryTokenID
            resultData['workerInfo'] = workerInfo
            result['status'] = 'SUCCESS'
            result['data'] = resultData
            return json.dumps(result)
        else:
            # 代表这个用户不存在
            # return 'ERROR TEL OR PASSWORD'
            result['data'] = 'ERROR TEL OR PASSWORD'
            return json.dumps(result)
    else:
        pass


# 工作人员修改信息
@app.route('/worker_update_info/', methods=['POST', 'GET'])
def worker_update_info():
    if(request.method == 'POST'):
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        wokerInfo = request.form['wokerInfo']
        adminID = request.form['adminID']
        adminPW = request.form['adminPW']
        wokerManager = WokerManager(adminID, adminPW)
        allresult = wokerManager.updateWorkerInfo(wokerInfo)
        if(allresult == False):
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = 'True'
            return json.dumps(result)
    else:
        pass

# 删除工作人员
@app.route('/delete_worker/', methods=['POST', 'GET'])
def delete_worker():
    if(request.method == 'POST'):
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        tel = request.form['tel']
        adminID = request.form['adminID']
        adminPW = request.form['adminPW']
        wokerManager = WokerManager(adminID, adminPW)
        allresult = wokerManager.deleteWorker(tel)
        if(allresult == False):
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = 'True'
            return json.dumps(result)
    else:
        pass

# 工作人员获取该区域内的快递代拿信息
@app.route('/worker_get_expressinfo/', methods=['POST', 'GET'])
def worker_get_expressinfo():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        taskExpressGetManager = TaskExpressGetManager(0, collegeID)
        allResult = taskExpressGetManager.getAllTaskList()
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)

    else:
        pass

# 工作人员获取该区域内的快递代发信息
@app.route('/worker_get_express_post/', methods=['POST', 'GET'])
def worker_get_express_post():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        taskExpressPostManager = TaskExpressPostManager(1,collegeID)
        allResult = taskExpressPostManager.getAllTaskList()
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)

    else:
        pass

# 工作人员获取验货信息
@app.route('/worker_get_inspect_info/', methods=['POST', 'GET'])
def worker_get_inspect_info():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        taskInspectionManager = TaskInspectionManager(2,collegeID)
        allResult = taskInspectionManager.getAllTaskList()
        if allResult == None:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)
    else:
        pass
# 工作人员抢单,快递代拿
@app.route('/worker_take_express_get/', methods=['POST', 'GET'])
def worker_take_express_get():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskID = request.form['taskID']
        taskExpressGetManager = TaskExpressGetManager(0,collegeID)
        allResult = taskExpressGetManager.getTask(tokenID, taskID)
        if False == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = 'True'
            return json.dumps(result)
    else:
        pass

# 工作人员抢单,快递代代发
@app.route('/worker_take_express_post/', methods=['POST', 'GET'])
def worker_take_express_post():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskID = request.form['taskID']
        taskExpressPostManager = TaskExpressPostManager(1,collegeID)
        allResult = taskExpressPostManager.getTask(tokenID, taskID)
        if False == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = 'True'
            return json.dumps(result)
    else:
        pass

# 工作人员抢单,验货
@app.route('/worker_take_inspection/', methods=['POST', 'GET'])
def worker_take_inspection():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskID = request.form['taskID']
        taskInspectionManager = TaskInspectionManager(2,collegeID)
        allResult = taskInspectionManager.getTask(tokenID, taskID)
        if False == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = 'True'
            return json.dumps(result)
    else:
        pass

# 工作人员验货反馈
@app.route('/worker_feedback/', methods=['POST', 'GET'])
def worker_feedback():
    pass

# 工作人员， 查询正在派送的快递代拿
@app.route('/worker_doing_expressinfo/', methods=['POST', 'GET'])
def worker_doing_expressinfo():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskExpressGetManager = TaskExpressGetManager(0, collegeID)
        allResult = taskExpressGetManager.getDoingTaskList(tokenID)
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)
    else:
        pass

# 工作人员， 查询正在派送的快递代发
@app.route('/worker_doing_expresspost/', methods=['POST', 'GET'])
def worker_doing_expresspost():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskExpressPostManager = TaskExpressPostManager(1, collegeID)
        allResult = taskExpressPostManager.getDoingTaskList(tokenID)
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)
    else:
        pass


# 工作人员， 查询正在派送的验货
@app.route('/worker_doing_inspection/', methods=['POST', 'GET'])
def worker_doing_inspection():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskInspectionManager = TaskInspectionManager(2, collegeID)
        allResult = taskInspectionManager.getDoingTaskList(tokenID)
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)
    else:
        pass

# 工作人员， 查询已完成的快递代拿
@app.route('/worker_completed_expressinfo/', methods=['POST', 'GET'])
def worker_completed_expressinfo():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskExpressGetManager = TaskExpressGetManager(0, collegeID)
        allResult = taskExpressGetManager.getCompletedTaskList(tokenID)
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)
    else:
        pass

# 工作人员， 查询已完成的快递代发
@app.route('/worker_completed_expresspost/', methods=['POST', 'GET'])
def worker_completed_expresspost():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskExpressPostManager = TaskExpressPostManager(1, collegeID)
        allResult = taskExpressPostManager.getCompletedTaskList(tokenID)
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)
    else:
        pass

# 工作人员， 查询已完成的验货
@app.route('/worker_completed_inspection/', methods=['POST', 'GET'])
def worker_completed_inspection():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        collegeID = request.form['collegeID']
        tokenID = request.form['tokenID']
        taskInspectionManager = TaskInspectionManager(2, collegeID)
        allResult = taskInspectionManager.getCompletedTaskList(tokenID)
        if None == allResult:
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = allResult
            return json.dumps(result)
    else:
        pass
# 提醒发货   remind_delivery
@app.route('/remind_delivery/', methods=['POST', 'GET'])
def remind_delivery():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        tokenID = request.form['tokenID']
        sellerID = request.form['sellerID']
        manager = OrderManager()
        if manager.remindDelivery(tokenID, sellerID):
            result['status'] = 'SUCCESS'
            result['data'] = 'True'
            return json.dumps(result)
        else:
            return json.dumps(result)
    else:
        pass

# 修改任务专题
@app.route('/modify_task_status/', methods = ['POST', 'GET'])
def modify_task_status():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        tokenID = request.form['tokenID']
        taskID = request.form['taskID']
        status = request.form['status']

        inspectionManager = TaskInspectionManager()
        (ret, reason) = inspectionManager.modifyTaskStatus(tokenID, taskID, status)
        if False == ret:
            result['data'] = reason
        else:
            result['status'] = 'SUCCESS'
        return json.dumps(result)

#购买服务费用
@app.route('/service_price/', methods=['POST', 'GET'])
def service_price():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        tokenID = request.form['tokenID']
        merchandisemanager =  MerchandiseManager()
        info = merchandisemanager.servicePrice(tokenID)
        if(info == None):
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = info
            return json.dumps(result)
    else:
        pass

#找回密码
@app.route('/find_pwd/', methods=['POST', 'GET'])
def find_pwd():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        tel = request.form['tel']
        pwd = request.form['password']
        usermanager = UserManager()
        info = usermanager.findPassWord(tel,pwd)
        if(info == False):
            return json.dumps(result)
        else:
            result['status'] = 'SUCCESS'
            result['data'] = info
            return json.dumps(result)
    else:
        pass

# 快递服务支付接口
@app.route('/express_pay/', methods = ['POST', 'GET'])
def express_pay():
    if request.method == 'POST':
        result = {}
        result['status'] = 'FAILED'
        result['data'] = 'NULL'
        params = request.form['param']
        inspectionManager = TaskInspectionManager()
        (ret, reason) = inspectionManager.pay(params)

        if False == ret:
            result['data'] = reason
        else:
            result['status'] = 'SUCCESS'
        return json.dumps(result)




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
