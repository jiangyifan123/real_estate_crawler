from tasks.spiderTask import SpiderTask, SpiderHandler
from spider.RentCast.RentData import RentData
from spider.RentCast.RentCastSuggest import RentCastSuggest
from database.crud import upsert_property, get_all_property, hashID
from models.models.database.property_info import PropertyInfo
from database.redisHelper import RedisClient


class UpdateRentDataTask(SpiderHandler):
    conn = RedisClient("nimbus_nova", "detailcheck")

    def choosePriorityAddress(self, model: PropertyInfo, address_list: list[str]) -> str:
        if model.city is None:
            return address_list[0]
        for address in address_list:
            if model.city in address and model.address in address:
                return address
        return address_list[0]

    def updateRent(self, p: PropertyInfo) -> bool:
        if p.rent_zestimate is not None and p.rent_zestimate > 0:
            return False
        address_list = RentCastSuggest().start(p.address).address_list
        if len(address_list) == 0:
            return False
        address = self.choosePriorityAddress(p, address_list)
        p.rent_zestimate = RentData().start(address).rent_estimate
        return True

    def isDetailInfoFull(self, p: PropertyInfo) -> bool:
        return self.conn.contains(p.id)

    def updateDetail(self, p: PropertyInfo) -> bool:
        if self.isDetailInfoFull(p):
            return False
        source = p.source
        if source == 'realtor':
            pass
        elif source == 'zillow':
            pass
        return True

    def isValidProperty(self, p: PropertyInfo) -> bool:
        checkList = [
            "address",
            "city",
            "state",
            "zipcode",
        ]
        return False

    def run(self):
        for p in get_all_property():
            isUpdated = False
            checkList = [
                self.updateRent,
                self.updateDetail
            ]

            for f in checkList:
                isUpdated |= f(p)

            if isUpdated:
                upsert_property(p)

            if self.isValidProperty(p):
                pass


class UpdatePropertyTask(SpiderTask):
    _taskList = [
        UpdateRentDataTask,
    ]

    @classmethod
    def key(self):
        return "rent_cast_task_get_rent"

    @classmethod
    def description(self):
        return "update database rent by address"