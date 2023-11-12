from spider.Realtor.RealtorSuggest import RealtorSuggest
from spider.Realtor.RealtorCityData import RealtorCityData
from spider.Realtor.RealtorDetailPage import RealtorDetailPage
from database.crud import upsert_property
from spiderTask import SpiderTask
import time

zipcodes = [
    "90013",
    "11354",
    "08861",
    "07093",
    "07107"
]

class RealtorSpiderTask(SpiderTask):
    def key(self):
        return "realtor_spider_test"

    def description(self):
        return "realtor spider"
    
    def getUrlByZipcode(self, zipcode):
        return f"https://www.realtor.com/realestateandhomes-search/{zipcode}"

    def getByZipcode(self):
        for zipcode in zipcodes:
            url = self.getUrlByZipcode(zipcode)
            model = RealtorCityData().start(url)
            for detailUrl in model.urls:
                time.sleep(2)
                print(upsert_property(RealtorDetailPage().start(detailUrl)))

    def run(self):
        # print(RealtorCityData().start("https://www.realtor.com/realestateandhomes-search/Lafayette_LA/sby-1"))
        # model = RealtorDetailPage().start("https://www.realtor.com/realestateandhomes-detail/507-Flores-Ct_Lafayette_LA_70507_M95730-95159?from=srp-list-card")
        # updateProperty(model)
        self.getByZipcode()