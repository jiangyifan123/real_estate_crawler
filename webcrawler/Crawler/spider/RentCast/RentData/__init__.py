from utils.RequestTool.CustomRequest import request
import urllib.parse
from spider.RentCast.RentData.RentDataModel import RentDataModel
from utils.Tools import getJsonValueFromPath

class RentData:
    def getUrl(self, address) -> str:
        url = "https://us-central1-rentcast-4da28.cloudfunctions.net/getRentData"
        params = {
            "address": address,
            "params": "{}",
            "getPropertyData": "true"
        }
        return f"{url}?{urllib.parse.urlencode(params)}"

    def parse(self, response) -> RentDataModel:
        if response is None:
            return RentDataModel()
        jsonData = response.json()
        property = getJsonValueFromPath(jsonData, 'data/property', {})
        description = property.get("description", {})
        location = property.get("location", [])
        latitude = 0
        longitude = 0
        if len(location) == 2:
            latitude, longitude = location
        rent_estimate = property.get("rentEstimate", {}).get("value", 0)
        return RentDataModel(
            address = property.get("address", {}).get("street", ""),
            bathrooms = description.get("bathrooms", 0),
            bedrooms = description.get("bedrooms", 0),
            livingAreaSize = description.get("livingAreaSize", 0),
            lotSize = description.get("lotSize", 0),
            propertyType = description.get("propertyType", ""),
            yearBuilt = description.get("yearBuilt", 0),
            latitude = latitude,
            longitude = longitude,
            rent_estimate = rent_estimate
        )

    def start(self, address) -> RentDataModel:
        url = self.getUrl(address)
        response = request("GET", url, tryCount=3)
        return self.parse(response)