from utils.RequestTool.CustomRequest import request
from bs4 import BeautifulSoup
import json
from spider.Zillow.ZillowDetailPage.ZillowDetailPageModel import ZillowDetailPageModel


class ZillowDetailPage:
    def parse(self, url, response):
        model = ZillowDetailPageModel()
        if response is None:
            return model
        soup = BeautifulSoup(response.content, 'lxml')
        scripts = soup.find_all("script", {"id": "__NEXT_DATA__"})
        if len(scripts) == 0:
            print("parse error")
            return model

        try:
            dataJsonString = scripts[0].text
            data = json.loads(dataJsonString)
            detailData = json.loads(data["props"]["pageProps"]["gdpClientCache"])
            values = detailData.values()
            if len(values) < 1:
                return model
            property = list(values)[0]["property"]
            model = ZillowDetailPageModel.from_json(json.dumps(property))
            model.num_garage = property.get("resoFacts", {}).get("garageParkingCapacity",None)
            model.status_text = property.get("attributionInfo", {}).get("trueStatus", None)
            return model
        except Exception as e:
            print(e)
        finally:
            return model

    def start(self, url):
        response = request("GET", url, cookieKey='zillow', useHttps=True, useProxy=True)
        return self.parse(url, response)

if __name__ == "__main__":
    testUrl = "https://www.realtor.com/realestateandhomes-detail/507-Flores-Ct_Lafayette_LA_70507_M95730-95159?from=srp-list-card"