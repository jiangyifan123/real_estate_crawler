from spiderTask import SpiderTaskManager
from spider.Zillow.ZillowSpider import ZillowSpiderTask
from spider.Realtor.RealtorSpider import RealtorSpiderTask
from spider.RentCast.RentCastSpider import RentCastSpiderTask
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)

if __name__ == '__main__':
    logging.info("Starting Crawler...")
    manager = SpiderTaskManager()
    logging.info("Registering Tasks...")
    #获取zillow房源数据
    # manager.register(ZillowSpiderTask)
    #获取realtor房源数据
    # manager.register(RealtorSpiderTask)
    #更新数据库无rent的房源数据
    manager.register(RentCastSpiderTask)
    #每天更新数据库已有房源数据状态
    logging.info("Tasks Registered!")

    logging.info("Running Tasks...")
    manager.runAllTask()