from scrapy.cmdline import execute

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# print(sys.path)
execute("scrapy crawl realtor".split(' '))