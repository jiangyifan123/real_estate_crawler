from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard
from models.models.database.property_info import PropertyInfo as RealtorCardDataModel

@dataclass
class RealtorCityDataModel(JSONWizard):
    model_list: Optional[list[RealtorCardDataModel]] = field(default_factory=list)