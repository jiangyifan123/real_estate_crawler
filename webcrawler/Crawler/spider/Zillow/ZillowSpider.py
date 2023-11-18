from spider.Zillow.ZillowSuggest import ZillowSuggest, ZillowSuggestModel
from spider.Zillow.ZillowDetailPage import ZillowDetailPageModel, ZillowDetailPage
from spider.Zillow.ZillowSearchPage import ZillowSearchPageModel, ZillowSearchPage, SearchType
from spiderTask import SpiderTask


def getSuggestions(searchText: str) -> ZillowSuggestModel.SearchResponse:
    return ZillowSuggest().start(searchText)

def getZillowDetailPage(url) -> ZillowDetailPageModel:
    return ZillowDetailPage().start(url)

def getAllDataByZipcode(zipcode) -> ZillowSearchPageModel:
    return ZillowSearchPage().start(searchType=SearchType.ZIPCODE, searchText=zipcode)

def getAllResultByCity(city) -> ZillowSearchPageModel:
    return ZillowSearchPage().start(searchType=SearchType.CITY, searchText=city)

# zillo fuzzy search
def getEstateByFuzzySearch(searchText):
    suggestions = getSuggestions(searchText)
    if len(suggestions.results) == 0:
        return []

    regionType = suggestions.results[0].metaData.regionType
    display = suggestions.results[0].display
    modelList = []
    if regionType in ["city", "neighborhood"]:    
        cityName = ''.join(display.strip('').replace(' ', '-').lower().split(','))
        modelList = getAllResultByCity(cityName)
    elif regionType == "zipcode":
        modelList = getAllDataByZipcode(display)
    elif regionType == "Address":
        pass
    return modelList


class ZillowSpiderTask(SpiderTask):
    @classmethod
    def key(self):
        return "zillow_spider_test"

    @classmethod
    def description(self):
        return "zillow spider"

    def run(self):
        # url = "https://www.zillow.com/homedetails/79-E-Agate-Ave-UNIT-401-Las-Vegas-NV-89123/55110557_zpid/"
        # print(getZillowDetailPage(url))
        # print(getSuggestions('New York'))
        print(getEstateByFuzzySearch('98121'))