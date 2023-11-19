from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard

@dataclass
class RealtorCardDataModel(JSONWizard):
    url: str = ""
    address: str = ""
    price: int = 0
    status: str = ""
    zipcode: str = ""
    state: str = ""
    city: str = ""
    property_type: str = ""


@dataclass
class RealtorCityDataModel(JSONWizard):
    model_list: Optional[list[RealtorCardDataModel]] = field(default_factory=list)