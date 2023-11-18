from spider.Realtor.RealtorSuggest import RealtorSuggest
from spider.Realtor.RealtorCityData import RealtorCityData
from spider.Realtor.RealtorDetailPage import RealtorDetailPage
from spider.RentCast.RentData import RentData
from database.crud import upsert_property, get_all_property
from spiderTask import SpiderTask
import time

def getUrlByZipcode(zipcode):
    return f"https://www.realtor.com/realestateandhomes-search/{zipcode}"

def getCityUrl(city):
    return f"https://www.realtor.com/realestateandhomes-search/{city}/sby-1"

class RealtorSpiderTask(SpiderTask):
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
            model = RealtorCityData().start(url)
            for detailUrl in model.urls:
                detailModel = RealtorDetailPage().start(detailUrl)
                detailModel.rent_zestimate = RentData().start(detailModel.address).rent_estimate
                upsert_property(detailModel)

    def run(self):
        # print(RealtorCityData().start("https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"))
        self.getByZipcode()


class RealtorSpiderTask_update_by_city(SpiderTask):
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

    def getByCity(self):
        for city in self.cities:
            url = getCityUrl(city)
            model = RealtorCityData().start(url)
            for detailUrl in model.urls:
                detailModel = RealtorDetailPage().start(detailUrl)
                detailModel.rent_zestimate = RentData().start(detailModel.address).rent_estimate
                upsert_property(detailModel)

    def run(self):
        # print(RealtorCityData().start("https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"))
        self.getByCity()


class RealtorSpiderTask_Update_Property(SpiderTask):
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
        return "realtor spider update property"

    def getByZipcode(self):
        for zipcode in self.zipcodes:
            url = getUrlByZipcode(zipcode)
            model = RealtorCityData().start(url)
            for detailUrl in model.urls:
                detailModel = RealtorDetailPage().start(detailUrl)
                detailModel.rent_zestimate = RentData().start(detailModel.address).rent_estimate
                upsert_property(detailModel)

    def run(self):
        # print(RealtorCityData().start("https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"))
        self.getByZipcode()