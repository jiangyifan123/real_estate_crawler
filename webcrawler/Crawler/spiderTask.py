import threading
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)


class SpiderTask(threading.Thread):
    @classmethod
    def key(cls):
        raise NotImplementedError

    @classmethod
    def description(cls):
        return ""

    @classmethod
    def process_count(cls):
        return 1

    def run(self):
        pass


class SpiderTaskManager:
    def __init__(self) -> None:
        self._taskList = {}
        self._threadList = {}

    def register(self, task):
        if task.key() not in self._taskList:
            self._taskList[task.key()] = task

    def unregister(self, task):
        del self._taskList[task.key()]

    def runAllTask(self):
        for taskKey, task in self._taskList.items():
            logging.info(f"creating task {taskKey}")
            self._threadList[taskKey] = []
            for i in range(task.process_count()):
                logging.info(f'created task {taskKey} {i}')
                subTask = task()
                self._threadList[taskKey].append(subTask)
                subTask.start()