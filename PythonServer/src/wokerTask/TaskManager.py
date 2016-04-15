# coding=utf8
import json
import sys
from AllTaskImpll import AllTaskImpll
from DoingTaskImpll import DoingTaskImpll
from CompletedTaskImpll import CompletedTaskImpll
from TaskGettingImpll import TaskGettingImpll
from ModifyStatusImpll import ModifyStatusImpll

sys.path.append("..")
from tool.Util import Util


class TaskManager(Util):
    def __init__(self, tag=0, collegeID=0):
        self._allListImpll = AllTaskImpll(tag, collegeID)
        self._doingImpll = DoingTaskImpll(tag, collegeID)
        self._completedImpll = CompletedTaskImpll(tag, collegeID)
        self._taskGettingImpll = TaskGettingImpll(tag, collegeID)
        self._modifyStatusImpll = ModifyStatusImpll(tag, collegeID)

    def getAllTaskList(self):
        return self._allListImpll.getAllTaskList()
        
    def getDoingTaskList(self, tokenID):
        return self._doingImpll.getDoingTaskList(tokenID)
        
    def getCompletedTaskList(self, tokenID):
        return self._completedImpll.getCompletedTaskList(tokenID)

    def getTask(self, tokenID, taskID):
        return self._taskGettingImpll.getTask(tokenID, taskID)

    def modifyTaskStatus(self, tokenID, taskID, status):
        return self._modifyStatusImpll.modifyInspectionStatus(tokenID, taskID, status)
