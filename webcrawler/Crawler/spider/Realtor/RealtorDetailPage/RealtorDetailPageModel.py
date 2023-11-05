from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard
from datetime import datetime
from enum import Enum

class PropertyType(str, Enum):
    house = "house"
    apartment = "apartment"
    condo = "condo"
    townhouse = "townhouse"
    singleFamily = "singleFamily"
    other = "other"

@dataclass
class RealtorDetailPageModel(JSONWizard):
    property_id: str = "AUTO_GENERATED"
    name: str = "unknown"
    street_address: str = "unknown"
    city: str = "unknown"
    state: str = "unknown"
    zipcode: int = -1
    property_type: PropertyType = PropertyType.other
    num_beds: int = -1
    num_baths: float = -1.0
    sq_ft: int = -1
    sq_ft_lot: int = -1
    purchase_price: int = -1
    estimated_rental_price: int = -1
    image_links: Optional[list[str]] = field(default_factory=list)
    time_on_market: int = -1
    date_first_on_market: datetime = datetime.now()
    year_built: int = -1
    garage: int = -1
    description: str = "unknown"