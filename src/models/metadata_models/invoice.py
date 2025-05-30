from typing import Optional, List

from pydantic import BaseModel

from models.metadata_models.base_metadata import BaseMetadata


class InvoiceItem(BaseModel):
    description: str
    qty: Optional[int] = None
    unit_price: Optional[float] = None
    total: Optional[float] = None


class InvoiceMetadata(BaseMetadata):
    vendor: Optional[str]
    amount: Optional[float]
    due_date: Optional[str]
    line_items: List[InvoiceItem]
