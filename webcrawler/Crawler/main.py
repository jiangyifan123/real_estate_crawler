from spiderTask import SpiderTaskManager
from spider.Zillow.ZillowSpider import ZillowSpiderTaskByZipcode, ZillowSpiderTaskByCity
from spider.Realtor.RealtorSpider import RealtorSpiderTaskByZipcode, RealtorSpiderTaskByCity
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
    ZillowSpiderTaskByZipcode,  # 获取zillow房源数据 by zipcode
    ZillowSpiderTaskByCity,  # 获取zillow房源 by city
    RealtorSpiderTaskByZipcode,  # 获取realtor房源数据
    RealtorSpiderTaskByCity,  # 根据city获取realtor数据
    RentCastSpiderTask,  # 更新数据库无rent的房源数据
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