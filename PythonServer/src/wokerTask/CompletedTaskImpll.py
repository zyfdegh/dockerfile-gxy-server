# coding=utf8
import json
import sys

sys.path.append("..")

from tool.Util import Util


class CompletedTaskImpll(Util):
    def __init__(self, tag, collegeID):
        self._tag = tag
        self._status = 2
        self._collegeID = collegeID

    def getCompletedTaskList(self, tokenID):
        pass