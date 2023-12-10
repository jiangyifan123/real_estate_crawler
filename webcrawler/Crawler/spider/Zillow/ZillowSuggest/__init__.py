from utils.RequestTool.CustomRequest import request
import urllib.parse
from spider.Zillow.ZillowSuggest.ZillowSuggestModel import SearchResponse

class ZillowSuggest:
    def getUrl(self, searchText):
        params = {
            "q": searchText,
            "resultTypes": "allRegion,allAddress",
            "abKey": "acb00326-9a70-42e6-a1f7-eda19d1bcd71",
            "clientId": "static-search-page"
        }
        url = f"https://www.zillowstatic.com/autocomplete/v3/suggestions?{urllib.parse.urlencode(params)}"
        return url

    def parse(self, response):
        if response is None:
            return SearchResponse()
        return SearchResponse.from_json(response.content)

    def start(self, searchText):
        url = self.getUrl(searchText)
        response = request("GET", url, useHttps=True, useProxy=True)
        return self.parse(response)