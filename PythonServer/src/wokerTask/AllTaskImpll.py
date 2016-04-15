# coding=utf8
import json
import sys

sys.path.append("..")

from tool.Util import Util


class AllTaskImpll(Util):
    def __init__(self, tag=0, collegeID=0):
        self._tag = tag
        self._status = 0
        self._collegeID = collegeID

    def getAllTaskList(self):
        pass
