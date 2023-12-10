from tasks.spiderTask import SpiderTask
from api.main import start_api


class ServerTask(SpiderTask):
    @classmethod
    def key(self):
        return "rent_cast_task_get_rent"

    @classmethod
    def description(self):
        return "update database rent by address"

    def run(self):
        start_api()