from utils.RequestTool.CustomRequest import request
from lxml import etree
from urllib.parse import urlparse
from spider.Realtor.RealtorCityData.RealtorCityDataModel import RealtorCityDataModel

class RealtorCityData:
    def parse(self, url, response):
        if response is None:
            return RealtorCityDataModel()
        URL = urlparse(url)
        html = etree.HTML(response.content)
        urls = html.xpath('//a[contains(@class, "LinkComponent_anchor__0C2xC")]/@href')
        next_button = html.xpath('//a[contains(@class, "next-link")]/@href')
        if next_button is not None and len(next_button) > 0:
            next_data = self.start(URL._replace(path=next_button[0]).geturl())
            urls.extend(next_data.urls)
        return RealtorCityDataModel(**{
            "urls": list(set(urls))
        })

    def start(self, url):
        response = request("GET", url)
        return self.parse(url, response)
    
if __name__ == "__main__":
    url = "https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"