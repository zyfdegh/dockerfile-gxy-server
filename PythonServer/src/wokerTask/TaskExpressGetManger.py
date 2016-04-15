# coding=utf8
import json
import sys
from AllTaskImpllNormal import AllTaskImpllNormal
from CompletedTaskImpllNormal import CompletedTaskImpllNormal
from DoingTaskImpllNormal import DoingTaskImpllNormal
from TaskGettingImpllNotification import TaskGettingImpllNotification

sys.path.append("..")

from TaskManager import TaskManager

class TaskExpressGetManager(TaskManager):
    def __init__(self, tag=0, collegeID=0):
        self._allListImpll = AllTaskImpllNormal(tag, collegeID)
        self._doingImpll = DoingTaskImpllNormal(tag, collegeID)
        self._completedImpll = CompletedTaskImpllNormal(tag, collegeID)
        self._taskGettingImpll = TaskGettingImpllNotification(tag, collegeID)
