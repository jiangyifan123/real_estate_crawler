from spiderTask import SpiderTask
from spider.RentCast.RentData import RentData

class RentCastSpiderTask(SpiderTask):
    def key(self):
        return "rent_cast_task_get_rent"
    
    def description(self):
        return "get rent by address"

    def run(self):
        print(RentData().start("5200 Keller Springs Rd APT 526"))