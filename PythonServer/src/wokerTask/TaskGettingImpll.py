# coding=utf8
import json
import sys

sys.path.append("..")

from tool.Util import Util


class TaskGettingImpll(Util):
    def __init__(self, tag, collegeID):
        self._tag = tag
        self._status = 0
        self._collegeID = collegeID

        self._tagDic = {}
        self._tagDic[0] = '快递代拿'
        self._tagDic[1] = '快递代发'
        self._tagDic[2] = '验货服务'

    def getTask(self, tokenID, taskID):
        pass
