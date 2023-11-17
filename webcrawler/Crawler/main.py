from spiderTask import SpiderTaskManager
# from spider.Zillow.ZillowSpider import ZillowSpiderTask
from spider.Realtor.RealtorSpider import RealtorSpiderTask
# from spider.RentCast.RentCastSpider import RentCastSpiderTask
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
    # manager.register(ZillowSpiderTask())
    manager.register(RealtorSpiderTask())
    # manager.register(RentCastSpiderTask())
    logging.info("Tasks Registered!")

    logging.info("Running Tasks...")
    manager.runAllTask()