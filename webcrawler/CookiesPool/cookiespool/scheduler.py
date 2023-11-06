import time
from multiprocessing import Process

from cookiespool.api.main import start_api
from cookiespool.config import *
from cookiespool.generator import *
from cookiespool.tester import *


class Scheduler(object):
    @staticmethod
    def valid_cookie(cycle=CYCLE):
        while True:
            print('Cookies检测进程开始运行')
            try:
                for website, cls in TESTER_MAP.items():
                    tester = eval(cls + '(website="' + website + '")')
                    tester.run()
                    print('Cookies检测完成')
                    del tester
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)
    
    @staticmethod
    def generate_cookie(cycle=CYCLE):
        while True:
            print('Cookies生成进程开始运行')
            try:
                for website, cls in GENERATOR_MAP.items():
                    generator = eval(cls + '(website="' + website + '")')
                    generator.run()
                    print('Cookies生成完成')
                    generator.close()
                    time.sleep(cycle)
            except Exception as e:
                print(e.args)
    
    def run(self):        
        if GENERATOR_PROCESS:
            print("set up cookie process")
            generate_process = Process(target=Scheduler.generate_cookie)
            generate_process.start()
        
        if VALID_PROCESS:
            print('set up valid process')
            valid_process = Process(target=Scheduler.valid_cookie)
            valid_process.start()
        
        if API_PROCESS:
            print('API接口开始运行')
            start_api()