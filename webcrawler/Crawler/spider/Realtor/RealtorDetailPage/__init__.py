from utils.RequestTool.CustomRequest import request
from lxml import etree
from spider.Realtor.RealtorDetailPage.RealtorDetailPageModel import RealtorDetailPageModel
import json

def getFirstOne(value, default):
    return next(iter(value), default)

class RealtorDetailPage:
    def parse(self, url, response):
        if response is None:
            return RealtorDetailPageModel()
        html = etree.HTML(response.content)
        street_address = getFirstOne(html.xpath('//*[@id="__next"]/div/div[1]/div[6]/div[4]/div[1]/div[2]/div[4]/div[1]/div[2]/div/h1/text()'), "")
        nextData = getFirstOne(html.xpath('//*[@id="__NEXT_DATA__"]/text()'), "{}")
        nextJson = json.loads(nextData)
        detailProperty = nextJson.get("props", {}).get("pageProps", {}).get("initialReduxState", {}).get("propertyDetails", {})
        address = detailProperty.get("location", {}).get("address", {})
        description = detailProperty.get("description", {})
        days_on_market = getFirstOne(html.xpath('//*[@id="__next"]/div/div[1]/div[6]/div[4]/div[1]/div[2]/div[4]/div[1]/div[4]/ul/li[2]/div/div[2]/text()'), "-1").split(" ")[0]
        photos = [p["href"] for p in detailProperty.get("photos", [])]
        return RealtorDetailPageModel(
            street_address=street_address,
            city=address.get("city", ""),
            state=address.get("state", ""),
            zipcode=address.get("postal_code", ""),
            property_type=description.get("type", ""),
            num_beds=description.get("beds", -1),
            num_baths=description.get("baths", -1),
            sq_ft=description.get("sqft", -1),
            sq_ft_lot=description.get("lot_sqft", -1),
            purchase_price=detailProperty.get("list_price", -1),
            estimated_rental_price=-1,
            image_links=photos,
            time_on_market=int(days_on_market),
            date_first_on_market="2023-10-29T23:58:35.656704",
            year_built=description.get("year_built", -1),
            garage=description.get("garage", -1),
            description=description.get("text", "")
        )

    def start(self, url):
        headers = {
            'Cookie': '__bot=false; __ssn=c7ed5a67-504f-4f26-a186-b261b7b0ac09; __ssnstarttime=1699075802; __vst=2590da8a-4a50-456a-8022-f1d33213d9c4; split=n; split_tcv=111'
        }
        response = request("GET", url, headers=headers)
        return self.parse(url, response)

if __name__ == "__main__":
    testUrl = "https://www.realtor.com/realestateandhomes-detail/507-Flores-Ct_Lafayette_LA_70507_M95730-95159?from=srp-list-card"