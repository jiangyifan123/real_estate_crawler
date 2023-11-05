from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard

@dataclass
class Address(JSONWizard):
    streetAddress: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zipcode: Optional[str] = None
    neighborhood: Optional[str] = None
    community: Optional[str] = None
    subdivision: Optional[str] = None

@dataclass
class Schools(JSONWizard):
    name = str | None
    distance: Optional[int] = None
    rating: Optional[int] = None
    level: Optional[str] = None
    grades: Optional[str] = None
    link: Optional[str] = None
    type: Optional[str] = None
    size: Optional[int] = None

@dataclass
class PriceHistory(JSONWizard):
    date: Optional[str] = None
    time: Optional[int] = None
    price: Optional[int] = None
    pricePerSquareFoot: Optional[int] = None
    priceChangeRate: Optional[float] = None
    event: Optional[str] = None
    source: Optional[str] = None

@dataclass
class ResponsivePhotos(JSONWizard):
    url: Optional[str] = None


@dataclass
class ZillowDetailPageModel(JSONWizard):
    zpid: str = ""
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
    next_button: Optional[bool] = None