
class SpiderTask:
    def key(self):
        raise NotImplementedError

    def description(self):
        return ""

    def run(self):
        pass


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
            task.run()