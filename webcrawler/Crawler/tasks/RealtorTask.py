from tasks.spiderTask import SpiderTask
from spider.Realtor.RealtorSuggest import RealtorSuggest
from spider.Realtor.RealtorCityData import RealtorCityData
from spider.Realtor.RealtorDetailPage import RealtorDetailPage
from spider.RentCast.RentData import RentData
from database.crud import upsert_property, check_property


def getUrlByZipcode(zipcode):
    return f"https://www.realtor.com/realestateandhomes-search/{zipcode}"


def getCityUrl(city):
    return f"https://www.realtor.com/realestateandhomes-search/{city}/sby-1"


class RealtorSpiderTaskByZipcode(SpiderTask):
    def __init__(self):
        super().__init__()
        self.zipcodes = [
            "90013",
            "11354",
            "08861",
            "07093",
            "07107"
        ]

    @classmethod
    def key(self):
        return "realtor_spider_test"

    @classmethod
    def description(self):
        return "realtor spider search property"

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


class RealtorSpiderTaskByCity(SpiderTask):
    def __init__(self):
        super().__init__()
        self.cities = [
            "Lafayette_LA",
        ]

    @classmethod
    def key(self):
        return "realtor_spider_test"

    @classmethod
    def description(self):
        return "realtor spider search property by city"

    def run(self):
        for city in self.cities:
            url = getCityUrl(city)
            model_list = RealtorCityData().start(url).model_list
            for model in model_list:
                if check_property(model):
                    continue
                detailModel = RealtorDetailPage().start(model.url)
                upsert_property(detailModel)