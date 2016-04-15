# coding=utf8
import json
import sys

sys.path.append("..")

from tool.Util import Util


class DoingTaskImpll(Util):
    def __init__(self, tag, collegeID):
        self._tag = tag
        self._status = 1
        self._collegeID = collegeID

    def getDoingTaskList(self, tokenID):
        pass