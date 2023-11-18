from spiderTask import SpiderTask
from spider.RentCast.RentData import RentData
from database.crud import upsert_property, get_all_property, hashID
from models.models.database.property_info import PropertyInfo

class RentCastSpiderTask(SpiderTask):
    @classmethod
    def key(self):
        return "rent_cast_task_get_rent"

    @classmethod
    def description(self):
        return "update database rent by address"

    def updateRent(self):
        for p in get_all_property():
            if p.rent_zestimate is not None and p.rent_zestimate > 0:
                continue
            rent_zestimate = RentData().start(p.address).rent_estimate
            if rent_zestimate != 0:
                model = PropertyInfo(
                    property_id=hashID(p),
                    rent_zestimate=rent_zestimate
                )
                upsert_property(model)

    def run(self):
        self.updateRent()