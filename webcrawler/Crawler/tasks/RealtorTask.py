from tasks.spiderTask import SpiderTask, SpiderHandler
from spider.Realtor.RealtorSuggest import RealtorSuggest
from spider.Realtor.RealtorCityData import RealtorCityData
from spider.Realtor.RealtorDetailPage import RealtorDetailPage
from spider.RentCast.RentData import RentData
from database.crud import upsert_property, check_property


def getUrlByZipcode(zipcode):
    return f"https://www.realtor.com/realestateandhomes-search/{zipcode}"


def getCityUrl(city):
    return f"https://www.realtor.com/realestateandhomes-search/{city}/sby-1"


class RealtorSpiderTaskByZipcode(SpiderHandler):
    zipcodes = [
        "90013",
        "11354",
        "08861",
        "07093",
        "07107"
    ]

    def getByZipcode(self):
        for zipcode in self.zipcodes:
            url = getUrlByZipcode(zipcode)
            model_list = RealtorCityData().start(url).model_list
            for model in model_list:
                if check_property(model):
                    continue
                detailModel = RealtorDetailPage().start(model.url)
                upsert_property(detailModel)

    def run(self):
        self.getByZipcode()


class RealtorSpiderTaskByCity(SpiderHandler):
    cities = [
        "Lafayette_LA",
    ]

    def run(self):
        for city in self.cities:
            url = getCityUrl(city)
            model_list = RealtorCityData().start(url).model_list
            for model in model_list:
                if check_property(model):
                    continue
                detailModel = RealtorDetailPage().start(model.url)
                upsert_property(detailModel)


class RealtorSpiderTask(SpiderTask):
    _taskList = [
        RealtorSpiderTaskByZipcode,
        RealtorSpiderTaskByCity
    ]

    @classmethod
    def key(self):
        return "realtor_spider"

    @classmethod
    def description(self):
        return "realtor spider"
