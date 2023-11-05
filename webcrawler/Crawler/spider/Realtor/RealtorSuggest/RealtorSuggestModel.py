from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard

class RealtorSuggestModel(JSONWizard):
    test: str = ""