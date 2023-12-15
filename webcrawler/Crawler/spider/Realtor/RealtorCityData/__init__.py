from utils.RequestTool.CustomRequest import request
from lxml import etree
from urllib.parse import urlparse
from spider.Realtor.RealtorCityData.RealtorCityDataModel import RealtorCityDataModel, RealtorCardDataModel
import json
from utils.Tools import getFirstOne, getJsonValueFromPath
import time

class RealtorCityData:
    def parse(self, url, response):
        if response is None:
            return RealtorCityDataModel()
        URL = urlparse(url)
        html = etree.HTML(response.content)
        next_data = getFirstOne(html.xpath('//*[@id="__NEXT_DATA__"]/text()'), "{}")
        next_data_json = json.loads(next_data)
        property_list = getJsonValueFromPath(next_data_json, "props/pageProps/properties", [])
        model_list = []
        for p in property_list:
            try:
                photos = p.get("photos", [])
                if photos is None:
                    photos = []
                model_list.append(RealtorCardDataModel(
                    detailurl=f"https://www.realtor.com/realestateandhomes-detail/{p.get('permalink', '')}",
                    address=getJsonValueFromPath(p, "location/address/line", ""),
                    purchase_price=p.get("list_price", 0),
                    status_type=p.get("status", ""),
                    zipcode=getJsonValueFromPath(p, "location/address/postal_code", ""),
                    state=getJsonValueFromPath(p, "location/address/state", ""),
                    city=getJsonValueFromPath(p, "location/address/city", ""),
                    property_type=getJsonValueFromPath(p, "description/type", 0),
                    num_beds=int(float(getJsonValueFromPath(p, "description/beds", 0))),
                    num_baths=int(float(getJsonValueFromPath(p, "description/baths_consolidated", 0))),
                    sq_ft=getJsonValueFromPath(p, "description/sqft", 0),
                    sq_ft_lot=getJsonValueFromPath(p, "description/lot_sqft", 0),
                    # num_days_on_market=0,
                    # year_built=0,
                    # num_garage=0,
                    # description="",
                    image_links=[v["href"] for v in photos],
                    # schools="{}",
                    # hoa=0,
                    source='realtor',
                    # zestimate=0,
                    # unit="",
                    latitude=getJsonValueFromPath(p, "location/address/coordinate/lat", 0),
                    longitude=getJsonValueFromPath(p, "location/address/coordinate/lon", 0),
                    # status_text="",
                    # rent_zestimate=0,
                ))
            except Exception as e:
                print(e)
        
        next_button = html.xpath('//a[contains(@class, "next-link")]/@href')
        if next_button is not None and len(next_button) > 0:
            next_data = self.start(URL._replace(path=next_button[0]).geturl())
            model_list.extend(next_data.model_list)
        return RealtorCityDataModel(
            model_list=model_list
        )

    def start(self, url):
        time.sleep(1)
        response = request("GET", url, cookieKey='realtor', useHttps=True)
        return self.parse(url, response)
    
if __name__ == "__main__":
    url = "https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"