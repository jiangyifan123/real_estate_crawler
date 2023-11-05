from utils.RequestTool.CustomRequest import request
from bs4 import BeautifulSoup
import json
from spider.Zillow.ZillowSearchPage.ZillowSearchPageModel import ZillowSearchPageModel, ZillowModel
from enum import Enum
from urllib.parse import urlparse

isDebuging = False


class SearchType(Enum):
    CITY = "city"
    ZIPCODE = "zipcode"


class ZillowSearchPage:

    def getUrlByZipcode(self, zipcode: str) -> str:
        return f"https://www.zillow.com/homes/{zipcode}/"

    def getUrlByCity(self, city: str) -> str:
        return f"https://www.zillow.com/{city}/"

    def parse(self, url, response):
        if response is None:
            return ZillowSearchPageModel()
        soup = BeautifulSoup(response.content, 'lxml')
        scripts = soup.find_all("script", {"id": "__NEXT_DATA__"})
        if len(scripts) == 0:
            print("parse error")
            return ZillowSearchPageModel()

        modelList = []
        URL = urlparse(url)
        try:
            nextPageButton = soup.find("a", {"title": "Next page"})
            nextPage = isDebuging is False and nextPageButton is not None and nextPageButton.get("aria-disabled", "true") == "false"
            dataJsonString = scripts[0].text
            data = json.loads(dataJsonString)
            resultList = data["props"]["pageProps"]["searchPageState"]["cat1"]["searchResults"]["listResults"]
            for result in resultList:
                model = ZillowModel.from_json(json.dumps(result))
                modelList.append(model)
            if nextPage:
                path = nextPageButton.get("href", None)
                if path is not None:
                    nextPageZillowList = self.startUrl(URL._replace(path=path).geturl())
                    modelList.extend(nextPageZillowList.zillowList)
            return ZillowSearchPageModel(modelList)
        except Exception as e:
            print(e)
        return ZillowSearchPageModel(modelList)

    def startUrl(self, url):
        response = request("GET", url, cookieKey='zillow')
        return self.parse(url, response)

    def start(self, searchType: SearchType, searchText: str):
        if searchType == SearchType.CITY:
            url = self.getUrlByCity(searchText)
            response = request("GET", url, cookieKey='zillow')
            return self.parse(url, response)
        elif searchType == SearchType.ZIPCODE:
            url = self.getUrlByZipcode(searchText)
            response = request("GET", url, cookieKey='zillow')
            return self.parse(url, response)
        raise Exception("Unknown search type")