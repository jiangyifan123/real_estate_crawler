from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard


@dataclass
class RealtorCityDataModel(JSONWizard):
    urls: Optional[list[str]] = field(default_factory=list)