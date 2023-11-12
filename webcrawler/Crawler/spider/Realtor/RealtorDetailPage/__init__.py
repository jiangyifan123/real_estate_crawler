from utils.RequestTool.CustomRequest import request
from lxml import etree
from spider.Realtor.RealtorDetailPage.RealtorDetailPageModel import RealtorDetailPageModel
import json
from utils.Tools import getFirstOne, getJsonValueFromPath

class RealtorDetailPage:
    def parse(self, url, response) -> RealtorDetailPageModel:
        if response is None:
            return RealtorDetailPageModel()
        html = etree.HTML(response.content)
        street_address = getFirstOne(html.xpath('//*[@id="__next"]/div/div[1]/div[6]/div[4]/div[1]/div[2]/div[4]/div[1]/div[2]/div/h1/text()'), "")
        nextData = getFirstOne(html.xpath('//*[@id="__NEXT_DATA__"]/text()'), "{}")
        days_on_market = getFirstOne(html.xpath('//*[@id="__next"]/div/div[1]/div[6]/div[4]/div[1]/div[2]/div[4]/div[1]/div[4]/ul/li[2]/div/div[2]/text()'), "-1").split(" ")[0]
        nextJson = json.loads(nextData)
        detailProperty = nextJson.get("props", {}).get("pageProps", {}).get("initialReduxState", {}).get("propertyDetails", {})
        address = getJsonValueFromPath(detailProperty, 'location/address', {})
        description = getJsonValueFromPath(detailProperty, "description", {})
        photos = getJsonValueFromPath(detailProperty, 'photos', [])
        photos = [p["href"] for p in photos]
        schools = getJsonValueFromPath(detailProperty, "nearby_schools", {})
        return RealtorDetailPageModel(
            address=street_address,
            city=address.get("city", ""),
            state=address.get("state", ""),
            zipcode=address.get("postal_code", ""),
            property_type=description.get("type", ""),
            num_beds=description.get("beds", -1),
            num_baths=description.get("baths", -1),
            sq_ft=description.get("sqft", -1),
            sq_ft_lot=description.get("lot_sqft", -1),
            purchase_price=detailProperty.get("list_price", -1),
            num_days_on_market=int(days_on_market),
            year_built=description.get("year_built", -1),
            num_garage=description.get("garage", -1),
            description=description.get("text", ""),
            image_links=photos,
            schools=json.dumps(schools),
            hoa=getJsonValueFromPath(detailProperty, "hoa/fee", 0),
            source="realtor",
            zestimate=0,
            detailurl=url,
            unit=description.get("units", ""),
            latitude=getJsonValueFromPath(address, "coordinate/lat", 0),
            longitude=getJsonValueFromPath(address, "coordinate/lon", 0),
            status_type=description.get("type", ""),
            status_text="",
            rent_zestimate=0
        )

    def start(self, url) -> RealtorDetailPageModel:
        response = request("GET", url, cookieKey='realtor')
        return self.parse(url, response)

if __name__ == "__main__":
    testUrl = "https://www.realtor.com/realestateandhomes-detail/507-Flores-Ct_Lafayette_LA_70507_M95730-95159?from=srp-list-card"