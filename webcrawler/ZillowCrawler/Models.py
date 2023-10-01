from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from typing import Optional

@dataclass
class PhotoInfo(JSONWizard):
    url: Optional[str] = None


@dataclass
class LatLong(JSONWizard):
    latitude: Optional[float] = None
    longitude: Optional[float] = None


@dataclass
class HomeInfo(JSONWizard):
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
class HdpData(JSONWizard):
    homeInfo: HomeInfo | None


@dataclass
class ZillowModel(JSONWizard):
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


@dataclass
class SearchResultMetaData(JSONWizard):
    regionId: Optional[int] = None
    regionType: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None


@dataclass
class SearchResult(JSONWizard):
    display: str | None
    resultType: str | None
    metaData: Optional[SearchResultMetaData] = None


@dataclass
class SearchResponse(JSONWizard):
    results: Optional[list[SearchResult]] = field(default_factory=list)

@dataclass
class Properties(JSONWizard):
    property_id: str
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

if __name__ == '__main__':
    pass
    # a = ["123", "333"]
    # print(r"'{0}'".format(str(a).replace('[', '{').replace(']', '}').replace("'", '"')))