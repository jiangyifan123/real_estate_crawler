from dataclasses import dataclass, field
from typing import Optional
from dataclass_wizard import JSONWizard

@dataclass
class SearchResultMetaData(JSONWizard):
    regionId: Optional[int] = None
    regionType: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None

@dataclass
class SearchResult(JSONWizard):
    display: str | None
    resultType: str | None
    metaData: Optional[SearchResultMetaData] = None

@dataclass
class SearchResponse(JSONWizard):
    results: Optional[list[SearchResult]] = field(default_factory=list)