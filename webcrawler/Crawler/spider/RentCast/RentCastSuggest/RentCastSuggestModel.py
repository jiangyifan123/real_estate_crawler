from dataclasses import dataclass, field
from dataclass_wizard import JSONWizard
from typing import Optional

@dataclass
class RentCastSuggestModel(JSONWizard):
    address_list: Optional[list[str]] = field(default_factory=list)