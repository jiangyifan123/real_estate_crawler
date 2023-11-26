from utils.RequestTool.CustomRequest import request
from lxml import etree
from urllib.parse import urlparse
from spider.Realtor.RealtorCityData.RealtorCityDataModel import RealtorCityDataModel, RealtorCardDataModel
import json
from utils.Tools import getFirstOne, getJsonValueFromPath

class RealtorCityData:
    def parse(self, url, response):
        if response is None:
            return RealtorCityDataModel()
        URL = urlparse(url)
        html = etree.HTML(response.content)
        next_data = getFirstOne(html.xpath('//*[@id="__NEXT_DATA__"]/text()'), "{}")
        next_data_json = json.loads(next_data)
        property_list = getJsonValueFromPath(next_data_json, "props/pageProps/properties", [])
        model_list = [RealtorCardDataModel(
            url=f"https://www.realtor.com/realestateandhomes-detail/{p.get('permalink', '')}",
            address=p.get("location", {}).get("address", {}).get("line", ""),
            price=p.get("list_price", 0),
            status=p.get("status", ""),
            zipcode=p.get("location", {}).get("address", {}).get("postal_code", ""),
            state=p.get("location", {}).get("address", {}).get("state", ""),
            city=p.get("location", {}).get("address", {}).get("city", ""),
            property_type=p.get("description", {}).get("type", "")
        ) for p in property_list]
        
        next_button = html.xpath('//a[contains(@class, "next-link")]/@href')
        if next_button is not None and len(next_button) > 0:
            next_data = self.start(URL._replace(path=next_button[0]).geturl())
            model_list.extend(next_data.model_list)
        return RealtorCityDataModel(
            model_list=model_list
        )

    def start(self, url):
        response = request("GET", url, cookieKey='realtor', useHttps=True)
        return self.parse(url, response)
    
if __name__ == "__main__":
    url = "https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"