from pydantic import BaseModel
from typing import List, Optional, Dict

class UploadResponse(BaseModel):
    columns: List[str]
    count: int
    last_filename: Optional[str]

class PaginatedRows(BaseModel):
    total: int
    offset: int
    limit: int
    rows: List[Dict]

class SeriesItem(BaseModel):
    label: str
    value: float

class ProductionBySource(BaseModel):
    year: int
    items: List[SeriesItem]

class CalcRequest(BaseModel):
    kwh_total: float
    country: Optional[str] = None
    year: Optional[int] = None