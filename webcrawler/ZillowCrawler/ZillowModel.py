from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from typing import Optional
import os
import unittest


@dataclass
class PhotoInfo(JSONWizard):
    url: str | None


@dataclass
class LatLong(JSONWizard):
    latitude: float | None
    longitude: float | None


@dataclass
class HomeInfo(JSONWizard):
    zpid: int | None
    streetAddress: str | None
    zipcode: str | None
    city: str | None
    state: str | None
    livingArea: int | None
    homeType: str | None
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
    price: str | None
    unformattedPrice: float | None
    detailUrl: str | None
    area: int | None
    latLong: LatLong | None
    imgSrc: Optional[str] = None
    beds: Optional[int] = None
    baths: Optional[int] = None
    zestimate: Optional[float] = None
    hdpData: Optional[HdpData] = None
    carouselPhotos: Optional[list[PhotoInfo]] = field(default_factory=list)


@dataclass
class SearchResultMetaData(JSONWizard):
    regionId: int | None
    regionType: str | None
    city: str | None
    county: str | None
    state: str | None
    country: str | None
    lat: float | None
    lng: float | None


@dataclass
class SearchResult(JSONWizard):
    display: str | None
    resultType: str | None
    metaData: Optional[SearchResultMetaData] = None


@dataclass
class SearchResponse(JSONWizard):
    results: Optional[list[SearchResult]] = field(default_factory=list)


class TestModel(unittest.TestCase):
    def test_ZillowModel(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/ZillowModelSample.json")
        with open(jsFile, "r") as f:
            data = f.read()
            ZillowModel.from_json(data)

    def test_SearchResponse(self):
        jsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), r"samples/SearchResultSample.json")
        with open(jsFile, "r") as f:
            data = f.read()
            SearchResponse.from_json(data)


if __name__ == '__main__':
    unittest.main()