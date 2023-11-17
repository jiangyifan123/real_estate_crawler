from spider.Realtor.RealtorSuggest import RealtorSuggest
from spider.Realtor.RealtorCityData import RealtorCityData
from spider.Realtor.RealtorDetailPage import RealtorDetailPage
from spider.RentCast.RentData import RentData
from database.crud import upsert_property, get_all_properties
from spiderTask import SpiderTask
import time

def getUrlByZipcode(zipcode):
    return f"https://www.realtor.com/realestateandhomes-search/{zipcode}"

class RealtorSpiderTask(SpiderTask):
    def __init__(self):
        super(RealtorSpiderTask, self).__init__()
        self.zipcodes = [
            "90013",
            "11354",
            "08861",
            "07093",
            "07107"
        ]

    def key(self):
        return "realtor_spider_test"

    def description(self):
        return "realtor spider"

    def getByZipcode(self):
        for zipcode in self.zipcodes:
            url = getUrlByZipcode(zipcode)
            model = RealtorCityData().start(url)
            for detailUrl in model.urls:
                time.sleep(2)
                detailModel = RealtorDetailPage().start(detailUrl)
                detailModel.rent_zestimate = RentData().start(detailModel.address).rent_estimate
                upsert_property(detailModel)
    
    def getProperty(self):
        for p in get_all_properties():
            if p.rent_zestimate is not None and p.rent_zestimate > 0:
                continue
            rent_zestimate = RentData().start(p.address).rent_estimate
            if rent_zestimate != 0:
                p.rent_zestimate = rent_zestimate
                upsert_property(p)

    def run(self):
        # print(RealtorCityData().start("https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"))
        # model = RealtorDetailPage().start("https://www.realtor.com/realestateandhomes-detail/507-Flores-Ct_Lafayette_LA_70507_M95730-95159?from=srp-list-card")
        # updateProperty(model)
        # self.getByZipcode()
        self.getProperty()