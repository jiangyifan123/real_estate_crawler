import threading
from utils.LogTools.CustomLog import logDebug
from multiprocessing import Process

class SpiderHandler(object):
    def run(self):
        pass


class SpiderTask(threading.Thread):
    @classmethod
    def key(cls):
        raise NotImplementedError

    @classmethod
    def description(cls):
        return ""

    @classmethod
    def run(self):
        print(f"run task {self.key()}")
        if not hasattr(self, '_taskList'):
            self._taskList = []
        self._threadList = []
        for task in self._taskList:
            subTask = task()
            self._threadList.append(subTask)
            subTask.run()


class SpiderTaskManager:
    def __init__(self) -> None:
        self._taskList = {}

    def register(self, task):
        if task.key() not in self._taskList:
            self._taskList[task.key()] = task

    def unregister(self, task):
        del self._taskList[task.key()]

    def runAllTask(self):
        for taskKey, task in self._taskList.items():
            logDebug(f"creating task {taskKey}")
            p = Process(target=task.run)
            p.start()