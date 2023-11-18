from spiderTask import SpiderTask
from spider.RentCast.RentData import RentData
from spider.RentCast.RentCastSuggest import RentCastSuggest
from database.crud import upsert_property, get_all_property, hashID
from models.models.database.property_info import PropertyInfo

class RentCastSpiderTask(SpiderTask):
    @classmethod
    def key(self):
        return "rent_cast_task_get_rent"

    @classmethod
    def description(self):
        return "update database rent by address"

    def choosePriorityAddress(self, model: PropertyInfo, address_list: list[str]) -> str:
        for address in address_list:
            if model.city in address and model.address in address:
                return address
        return address_list[0]

    def updateRent(self):
        for p in get_all_property():
            if p.rent_zestimate is not None and p.rent_zestimate > 0:
                continue
            address_list = RentCastSuggest().start(p.address).address_list
            if len(address_list) == 0:
                continue
            address = self.choosePriorityAddress(p, address_list)
            rent_zestimate = RentData().start(address).rent_estimate
            if rent_zestimate != 0:
                model = PropertyInfo(
                    property_id=hashID(p),
                    rent_zestimate=rent_zestimate
                )
                upsert_property(model)

    def run(self):
        self.updateRent()