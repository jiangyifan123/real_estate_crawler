import scrapy


class RealtorSpider(scrapy.Spider):
    name = "realtor"
    allowed_domains = ["www.realtor.com"]
    start_urls = ["http://www.realtor.com/"]

    def parse(self, response):
        pass
