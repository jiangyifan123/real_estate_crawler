from dataclasses import dataclass
from dataclass_wizard import JSONWizard


@dataclass
class RentDataModel(JSONWizard):
    address: str | None = ""
    bathrooms: int | None = 0
    bedrooms: int | None = 0
    livingAreaSize: int | None = 0
    lotSize: int | None = 0
    propertyType: str | None = ""
    yearBuilt: int | None = 0
    latitude: float | None = 0
    longitude: float | None = 0
    rent_estimate: int | None = 0