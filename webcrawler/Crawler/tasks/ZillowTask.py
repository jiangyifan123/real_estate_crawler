from tasks.spiderTask import SpiderTask, SpiderHandler
from spider.Zillow.ZillowSuggest import ZillowSuggest, ZillowSuggestModel
from spider.Zillow.ZillowDetailPage import ZillowDetailPageModel, ZillowDetailPage
from spider.Zillow.ZillowSearchPage import ZillowSearchPageModel, ZillowSearchPage, SearchType
from database.crud import upsert_property, get_all_property, check_property


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
        modelList = getAllResultByCity(cityName).zillowList
    elif regionType == "zipcode":
        modelList = getAllDataByZipcode(display).zillowList
    elif regionType == "Address":
        pass
    return modelList

class ZillowSpiderTaskByZipcode(SpiderHandler):
    zipcodes = [
        98121,
    ]

    def run(self):
        for zipcode in self.zipcodes:
            for model in getEstateByFuzzySearch(zipcode):
                if check_property(model):
                    continue
                pass


class ZillowSpiderTaskByCity(SpiderHandler):
    cities = [
        "seattle-wa-98121",
    ]

    def run(self):
        for city in self.cities:
            for model in getEstateByFuzzySearch(city):
                if check_property(model):
                    continue
                pass


class ZillowSpiderTask(SpiderTask):
    _taskList = [
        ZillowSpiderTaskByZipcode,
        ZillowSpiderTaskByCity
    ]

    @classmethod
    def key(self):
        return "zillow_spider"

    @classmethod
    def description(self):
        return "zillow spider"