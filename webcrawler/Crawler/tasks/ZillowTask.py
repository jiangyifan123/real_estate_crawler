from tasks.spiderTask import SpiderTask, SpiderHandler
from spider.Zillow.ZillowSuggest import ZillowSuggest, ZillowSuggestModel
from spider.Zillow.ZillowDetailPage import ZillowDetailPageModel, ZillowDetailPage
from spider.Zillow.ZillowSearchPage import ZillowSearchPageModel, ZillowSearchPage, SearchType
from database.crud import upsert_property, get_all_property, check_property_update
from models.models.database.property_info import PropertyInfo

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
    return modelList


def transferToPropertyInfo(model) -> PropertyInfo:
    return PropertyInfo(
        address=model.address,
        city=model.addressCity,
        state=model.addressState,
        zipcode=model.addressZipcode,
        property_type=model.hdpData.homeInfo.homeType,
        num_beds=model.beds,
        num_baths=model.baths,
        sq_ft=model.area,
        sq_ft_lot=model.area,
        purchase_price=int(model.hdpData.homeInfo.price),
        image_links=[p.url for p in model.carouselPhotos],
        source='zillow',
        zestimate=model.zestimate,
        detailurl=model.detailUrl,
        unit=model.hdpData.homeInfo.unit,
        latitude=model.latLong.latitude,
        longitude=model.latLong.longitude,
        status_type=model.statusType,
        rent_zestimate=model.hdpData.homeInfo.rentZestimate
    )


class ZillowSpiderTaskByZipcode(SpiderHandler):
    zipcodes = [
        "90013",
        "11354",
        "08861",
        "07093",
        "07107"
    ]

    def run(self):
        for zipcode in self.zipcodes:
            for model in getEstateByFuzzySearch(zipcode):
                propertyObj = transferToPropertyInfo(model)
                if not check_property_update(propertyObj):
                    continue
                upsert_property(propertyObj, 'zillow_zipcode')


class ZillowSpiderTaskByCity(SpiderHandler):
    cities = [
        "seattle-wa-98121",
        "Lafayette_LA",
        "Lafayette_CA",
    ]

    def run(self):
        for city in self.cities:
            for model in getEstateByFuzzySearch(city):
                propertyObj = transferToPropertyInfo(model)
                if not check_property_update(propertyObj):
                    continue
                upsert_property(propertyObj, 'zillow_city')


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