from spiderTask import SpiderTaskManager
from spider.Zillow.ZillowSpider import ZillowSpiderTask
from spider.Realtor.RealtorSpider import RealtorSpiderTask


if __name__ == '__main__':
    manager = SpiderTaskManager()
    # manager.register(ZillowSpiderTask())
    manager.register(RealtorSpiderTask())
    manager.runAllTask()