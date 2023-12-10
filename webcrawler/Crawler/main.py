from spiderTask import SpiderTaskManager
from spider.Zillow.ZillowSpider import ZillowSpiderTask
from spider.Realtor.RealtorSpider import RealtorSpiderTask, RealtorSpiderTask_update_by_city, RealtorSpiderTask_Update_Property
from spider.RentCast.RentCastSpider import RentCastSpiderTask
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)

taskList = [
    ZillowSpiderTask,  # 获取zillow房源数据
    RealtorSpiderTask,  # 获取realtor房源数据
    RentCastSpiderTask,  # 更新数据库无rent的房源数据
    RealtorSpiderTask_update_by_city, # 根据city获取realtor数据
    #每天更新数据库已有房源数据状态
]

if __name__ == '__main__':
    logging.info("Starting Crawler...")
    manager = SpiderTaskManager()
    logging.info("Registering Tasks...")
    for task in taskList:
        manager.register(task)
    logging.info("Tasks Registered!")

    logging.info("Running Tasks...")
    manager.runAllTask()