# coding=utf8
import sys

sys.path.append("..")

import os
import json
import unittest
import logging
from user.rong import ApiClient

class RYClient:
    def __init__(self):
        os.environ.setdefault('rongcloud_app_key', self.getAppKey())
        os.environ.setdefault('rongcloud_app_secret', self.getAppSecret())
        logging.basicConfig(level=logging.INFO)
        self._ryapi = ApiClient()
        self._paths = 'http://121.43.111.75:5000/static/'

    def getAppKey(self):
        return "m7ua80gbuf2am"

    def getAppSecret(self):
        return "3EyhxJXCKnMB"

    def publishMessage(self, fromUserID, toUserID, content, objectName='RC:TxtMsg'):
        result = self._ryapi.message_publish(
            from_user_id=fromUserID,
            to_user_id=toUserID,
            object_name=objectName,
            content=json.dumps({"content":content}),
            push_content='thisisapush',
            push_data='aa')

        return result['code']

    def getRYToken(self, userID, name, portait):
        action = 'user/getToken'
        params = {}
        params['userId'] = userID
        params['name'] = name
        params['portraitUri'] = portait
        # print(json.dumps(params))
        return self._ryapi.user_get_token(userID, name, portait)
