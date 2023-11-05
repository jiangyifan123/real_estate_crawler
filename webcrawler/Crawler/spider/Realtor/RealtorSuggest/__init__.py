from utils.RequestTool.CustomRequest import request
import urllib.parse
from spider.Realtor.RealtorSuggest.RealtorSuggestModel import RealtorSuggestModel

class RealtorSuggest:
    def getUrl(self, searchText):
        params = {
            "input": searchText,
            "client_id": "for-sale",
            "limit": 10
        }
        url = f"https://parser-external.geo.moveaws.com/suggest?{urllib.parse.urlencode(params)}"
        return url

    def parse(self, response):
        print(response.json())
        return RealtorSuggestModel()

    def start(self, searchText):
        url = self.getUrl(searchText)
        response = request("GET", url)
        return self.parse(response)