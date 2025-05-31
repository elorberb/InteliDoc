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

    def pretty_print(self):
        print("🧾 Invoice Metadata")
        print(f"  🏢 Vendor: {self.vendor or 'N/A'}")
        print(f"  💵 Amount: {self.amount if self.amount is not None else 'N/A'}")
        print(f"  📅 Due Date: {self.due_date or 'N/A'}")
        print("  📦 Line Items:")
        if self.line_items:
            for i, item in enumerate(self.line_items, 1):
                print(f"    {i}. {item.description or 'No description'}")
                print(f"       ➤ Qty: {item.qty or '?'} × {item.unit_price or '?'} = {item.total or '?'}")
        else:
            print("    No line items found.")
