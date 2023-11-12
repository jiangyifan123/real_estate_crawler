from spiderTask import SpiderTaskManager
from spider.Zillow.ZillowSpider import ZillowSpiderTask
from spider.Realtor.RealtorSpider import RealtorSpiderTask
from spider.RentCast.RentCastSpider import RentCastSpiderTask

if __name__ == '__main__':
    manager = SpiderTaskManager()
    # manager.register(ZillowSpiderTask())
    manager.register(RealtorSpiderTask())
    # manager.register(RentCastSpiderTask())
    manager.runAllTask()