from dataclasses import dataclass, field
from typing import Optional
from SqlUtls import CustomJSONWizard
import hashlib

@dataclass
class PhotoInfo(CustomJSONWizard):
    url: Optional[str] = None


@dataclass
class LatLong(CustomJSONWizard):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class HomeInfo(CustomJSONWizard):
    zpid: int | None
    streetAddress: Optional[str] = None
    zipcode: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    livingArea: Optional[int] = None
    homeType: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    price: Optional[float] = None
    bathrooms: Optional[int] = None
    bedrooms: Optional[int] = None
    homeStatus: Optional[str] = None
    priceForHDP: Optional[float] = None
    currency: Optional[str] = None
    country: Optional[str] = None
    unit: Optional[str] = None
    datePriceChanged: Optional[float] = None
    priceChange: Optional[float] = None
    taxAssessedValue: Optional[float] = None
    zestimate: Optional[float] = None
    rentZestimate: Optional[float] = None


@dataclass
class HdpData(CustomJSONWizard):
    homeInfo: HomeInfo | None


@dataclass
class ZillowModel(CustomJSONWizard):
    zpid: str | None
    statusType: str | None
    address: str | None
    addressStreet: str | None
    addressCity: str | None
    addressState: str | None
    addressZipcode: str | None
    countryCurrency: str | None
    detailUrl: str | None
    price: Optional[str] = None
    unformattedPrice: Optional[float] = None
    area: Optional[int] = None
    latLong: Optional[LatLong] = None
    imgSrc: Optional[str] = None
    beds: Optional[int] = None
    baths: Optional[int] = None
    zestimate: Optional[float] = None
    hdpData: Optional[HdpData] = None
    carouselPhotos: Optional[list[PhotoInfo]] = field(default_factory=list)
    statusText: Optional[str] = None

    def __post_init__(self):
        self.registerModelFactory(Properties, self.__toProperties)

    def __toProperties(self):
        homeInfo = self.hdpData.homeInfo
        return Properties(
            property_id = self.zpid,
            address = homeInfo.streetAddress,
            city = homeInfo.city,
            state = homeInfo.state,
            zipcode = homeInfo.zipcode,
            property_type = homeInfo.homeType,
            num_beds = homeInfo.bedrooms,
            num_baths = homeInfo.bathrooms,
            sq_ft = homeInfo.livingArea,
            sq_ft_lot = homeInfo.livingArea,
            purchase_price = int(homeInfo.price) if homeInfo.price is not None else homeInfo.price,
            num_days_on_market = None,
            year_built = None,
            num_garage = None,
            description = None,
            image_links = [p.url for p in self.carouselPhotos] if self.carouselPhotos is not None else [],
            schools = None,
            hoa = None,
            source = "zillow",
            zestimate = int(homeInfo.zestimate) if homeInfo.zestimate is not None else homeInfo.zestimate,
            detailurl = self.detailUrl,
            unit = homeInfo.unit,
            latitude = homeInfo.latitude,
            longitude = homeInfo.longitude,
            status_type = self.statusType,
            status_text = self.statusText,
        )


@dataclass
class SearchResultMetaData(CustomJSONWizard):
    regionId: Optional[int] = None
    regionType: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


@dataclass
class SearchResult(CustomJSONWizard):
    display: str | None
    resultType: str | None
    metaData: Optional[SearchResultMetaData] = None


@dataclass
class SearchResponse(CustomJSONWizard):
    results: Optional[list[SearchResult]] = field(default_factory=list)

@dataclass
class resoFacts(CustomJSONWizard):
    garageParkingCapacity: Optional[int] = None

@dataclass
class Properties(CustomJSONWizard):
    property_id: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    property_type: Optional[str] = None
    num_beds: Optional[int] = None
    num_baths: Optional[int] = None
    sq_ft: Optional[int] = None
    sq_ft_lot: Optional[int] = None
    purchase_price: Optional[int] = None
    num_days_on_market: Optional[int] = None
    year_built: Optional[int] = None
    num_garage: Optional[int] = None
    description: Optional[str] = None
    image_links: Optional[list[str]] = field(default_factory=list)
    schools: Optional[str] = None
    hoa: Optional[int] = None
    source: Optional[str] = None
    zestimate: Optional[int] = None 
    detailurl: Optional[str] = None
    unit: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    id: Optional[int] = None
    status_type: Optional[str] = None
    status_text: Optional[int] = None
    zestimate: Optional[int] = None
    rent_zestimate: Optional[int] = None

    @classmethod
    def tableName(self):
        return 'raw.properties'

    @classmethod
    def canHandle(self, k, enterFrom):
        if str(k) == 'id' and enterFrom == self.EnterFrom.WRITE:
            return False
        return super().canHandle(k, enterFrom)
    
    def handleValues(self, k, v):
        if k == 'property_id':
            s = self.address + self.city + self.state + self.zipcode + self.property_type
            return "'{}'".format(hashlib.sha256(s.encode('utf-8')).hexdigest())
        return super().handleValues(k, v)


@dataclass
class Address(CustomJSONWizard):
    streetAddress: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    neighborhood: Optional[str] = None
    community: Optional[str] = None
    subdivision: Optional[str] = None

@dataclass
class Schools(CustomJSONWizard):
    name = str | None
    distance: Optional[int] = None
    rating: Optional[int] = None
    level: Optional[str] = None
    grades: Optional[str] = None
    link: Optional[str] = None
    type: Optional[str] = None
    size: Optional[int] = None

@dataclass
class PriceHistory(CustomJSONWizard):
    date: Optional[str] = None
    time: Optional[int] = None
    price: Optional[int] = None
    pricePerSquareFoot: Optional[int] = None
    priceChangeRate: Optional[float] = None
    event: Optional[str] = None
    source: Optional[str] = None

@dataclass
class ResponsivePhotos(CustomJSONWizard):
    url: Optional[str] = None

@dataclass
class ZillowDetailPage(CustomJSONWizard):
    zpid: str | None
    city: Optional[str] = None
    state: Optional[str] = None
    homeStatus: Optional[str] = None
    address: Optional[Address] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    price: Optional[int] = None
    streetAddress: Optional[str] = None
    zipcode: Optional[str] = None
    regionString: Optional[str] = None
    homeType: Optional[str] = None
    yearBuilt: Optional[int] = None
    livingArea: Optional[int] = None
    zestimate: Optional[int] = None
    rentZestimate: Optional[int] = None
    schools: Optional[list[Schools]] = field(default_factory=list)
    priceHistory: Optional[list[PriceHistory]] = field(default_factory=list)
    description: Optional[str] = None
    daysOnZillow: Optional[int] = None
    responsivePhotos: Optional[list[ResponsivePhotos]] = field(default_factory=list)
    lotSize: Optional[int] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    hdpUrl: Optional[str] = None
    monthlyHoaFee: Optional[int] = None
    num_garage: Optional[int] = None
    status_text: Optional[str] = None

    def __post_init__(self, *args, **kargs):
        self.registerModelFactory(Properties, self.__toProperties)

    def __toProperties(self):
        return Properties(
            address = self.streetAddress,
            city = self.city,
            state = self.state,
            zipcode = self.zipcode,
            property_type = self.homeType,
            num_beds = self.bedrooms,
            num_baths = self.bathrooms,
            sq_ft = self.livingArea,
            sq_ft_lot = self.lotSize,
            purchase_price = self.price,
            num_days_on_market = self.daysOnZillow,
            year_built = self.yearBuilt,
            description = self.description,
            image_links = [p.url for p in self.responsivePhotos] if self.responsivePhotos  is not None else [],
            schools = self.schools,
            hoa = self.monthlyHoaFee,
            source = "zillow",
            zestimate = self.zestimate, 
            detailurl = "https://www.zillow.com" + self.hdpUrl,
            unit = None,
            latitude = self.latitude,
            longitude = self.longitude,
            status_type = self.homeType,
            status_text = self.status_text,
            rent_zestimate = self.rentZestimate,
            num_garage = self.num_garage,
        )


if __name__ == '__main__':
    pass