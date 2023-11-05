import scrapy
from scrapy.crawler import CrawlerProcess

class ZillowSpider(scrapy.Spider):
    name = "zillow"
    allowed_domains = ["www.zillow.com"]
    start_urls = ["https://www.baidu.com"]

    def parse(self, response):
        pass