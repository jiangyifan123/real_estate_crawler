from utils.RequestTool.CustomRequest import request
from spider.RentCast.RentData.RentDataModel import RentDataModel
import urllib.parse
from spider.RentCast.RentCastSuggest.RentCastSuggestModel import RentCastSuggestModel

class RentCastSuggest:
    def getUrl(self, address) -> str:
        url = "https://geocode.arcgis.com/arcgis/rest/services/World/GeocodeServer/suggest"
        params = {
            "text": address,
            "category": "Address",
            "f": "json"
        }
        return f"{url}?{urllib.parse.urlencode(params)}"

    def parse(self, response) -> RentCastSuggestModel:
        if response is None:
            return RentCastSuggestModel()
        model = RentCastSuggestModel()
        suggestJson = response.json()
        model.address_list.extend([i['text'] for i in suggestJson.get("suggestions", {})])
        return model

    def start(self, address) -> RentCastSuggestModel:
        url = self.getUrl(address)
        response = request("GET", url, tryCount=1)
        return self.parse(response)