from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard
from datetime import datetime
from enum import Enum
import hashlib

@dataclass
class PropertyModel(JSONWizard):
    property_id: str | None = ""
    address: str | None = ""
    city: str | None = ""
    state: str | None = ""
    zipcode: int | None = 0
    property_type: str | None = ""
    num_beds: int | None = 0
    num_baths: float | None = 0.0
    sq_ft: int | None = 0
    sq_ft_lot: int | None = 0
    purchase_price: int | None = 0
    num_days_on_market: int | None = 0
    year_built: int | None = 0
    num_garage: int | None = 0
    description: str | None = ""
    image_links: Optional[list[str]] = field(default_factory=list)
    schools: str | None = ""
    hoa: int | None = 0
    source: str | None = ""
    zestimate: int | None = 0
    detailurl: str | None = ""
    unit: int | str | None = 0
    latitude: float | None = 0.0
    longitude: float | None = 0.0
    status_type: str | None = ""
    status_text: str | None = ""
    rent_zestimate: int | None = 0

    def __post_init__(self):
        self.property_id = hashlib.sha256((self.address + self.city + self.state + str(self.zipcode) + self.property_type).encode('utf-8')).hexdigest()