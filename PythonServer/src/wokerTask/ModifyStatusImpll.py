# coding=utf8
import json
import sys

sys.path.append("..")

from tool.Util import Util


class ModifyStatusImpll(Util):
    def __init__(self, tag, collegeID):
        self._tag = tag
        self._status = 1
        self._collegeID = collegeID

    def modifyInspectionStatus(self, tokenID, taskID, status):
        pass