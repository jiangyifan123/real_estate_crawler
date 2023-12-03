from spider.Realtor.RealtorSuggest import RealtorSuggest
from spider.Realtor.RealtorCityData import RealtorCityData
from spider.Realtor.RealtorDetailPage import RealtorDetailPage
from spider.RentCast.RentData import RentData
from database.crud import upsert_property, check_property
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
            model_list = RealtorCityData().start(url).model_list
            for model in model_list:
                if check_property(model):
                    continue
                detailModel = RealtorDetailPage().start(model.url)
                if detailModel.address is not None and len(detailModel.address) != 0:
                    detailModel.rent_zestimate = RentData().start(model.address).rent_estimate
                    upsert_property(detailModel)

    def run(self):
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
            model_list = RealtorCityData().start(url).model_list
            for model in model_list:
                if check_property(model):
                    continue
                detailModel = RealtorDetailPage().start(model.url)
                detailModel.rent_zestimate = RentData().start(model.address).rent_estimate
                upsert_property(detailModel)

    def run(self):
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

    def checkProperty(self):
        for zipcode in self.zipcodes:
            url = getUrlByZipcode(zipcode)
            model = RealtorCityData().start(url)

    def run(self):
        self.checkProperty()