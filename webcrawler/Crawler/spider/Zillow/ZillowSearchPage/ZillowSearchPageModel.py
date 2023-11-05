from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard


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
    zpid: str = ""
    statusType: str = ""
    address: str = ""
    addressStreet: str = ""
    addressCity: str = ""
    addressState: str = ""
    addressZipcode: str = ""
    countryCurrency: str = ""
    detailUrl: str = ""
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


@dataclass
class ZillowSearchPageModel(JSONWizard):
    zillowList: Optional[list[ZillowModel]] = field(default_factory=list)