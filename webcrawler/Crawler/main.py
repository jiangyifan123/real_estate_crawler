from tasks.spiderTask import SpiderTaskManager
from tasks.RealtorTask import RealtorSpiderTask
from tasks.ZillowTask import ZillowSpiderTask
from tasks.UpdatePropertyTask import UpdatePropertyTask
import logging
from dotenv import load_dotenv
from api.main import start_api

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] {%(filename)s:%(funcName)s:%(lineno)d} %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("logs.log"), logging.StreamHandler()],
)

taskList = [
    ZillowSpiderTask,  # 获取zillow房源数据
    RealtorSpiderTask,  # 获取realtor房源数据
    UpdatePropertyTask,  # 更新raw房源表数据并且验证好的数据到验证表
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
    logging.info("running server api")
    start_api()