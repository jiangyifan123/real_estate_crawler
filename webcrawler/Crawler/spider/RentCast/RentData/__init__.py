from utils.RequestTool.CustomRequest import request
import urllib.parse

class RentData:
    def getUrl(self, address):
        url = "https://us-central1-rentcast-4da28.cloudfunctions.net/getRentData"
        params = {
            "address": address,
            "params": "{}",
            "getPropertyData": "true"
        }
        return f"{url}?{urllib.parse.urlencode(params)}"

    def parse(self, response):
        print(response.json())
        return {}

    def start(self, address):
        url = self.getUrl(address)
        response = request("GET", url)
        return self.parse(response)