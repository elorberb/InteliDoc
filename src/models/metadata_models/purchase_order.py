from typing import List, Optional
from pydantic import BaseModel
from models.metadata_models.base_metadata import BaseMetadata


class PurchaseOrderLineItem(BaseModel):
    item_number: Optional[str]
    description: Optional[str]
    quantity: Optional[float] = None
    unit_price: Optional[float] = None
    total_price: Optional[float] = None
    uom: Optional[str] = None


class PurchaseOrderMetadata(BaseMetadata):
    po_number: Optional[str] = None
    po_date: Optional[str] = None
    buyer_name: Optional[str] = None
    vendor_name: Optional[str] = None
    currency: Optional[str] = None
    payment_terms: Optional[str] = None
    line_items: List[PurchaseOrderLineItem] = []
    subtotal: Optional[float] = None
    tax_amount: Optional[float] = None
    shipping_fee: Optional[float] = None
    grand_total: Optional[float] = None

    def pretty_print(self):
        print("📦 Purchase Order Metadata")
        print(f"  🔢 PO Number: {self.po_number or 'N/A'}")
        print(f"  📅 PO Date: {self.po_date or 'N/A'}")
        print(f"  🛒 Buyer: {self.buyer_name or 'N/A'}")
        print(f"  🏭 Vendor: {self.vendor_name or 'N/A'}")
        print(f"  💱 Currency: {self.currency or 'N/A'}")
        print(f"  💳 Payment Terms: {self.payment_terms or 'N/A'}")
        print("  📦 Line Items:")
        for i, item in enumerate(self.line_items, 1):
            print(f"    {i}. {item.description or 'N/A'} - {item.quantity or '?'} {item.uom or ''} @ {item.unit_price or '?'} = {item.total_price or '?'}")
        print(f"  Subtotal: {self.subtotal if self.subtotal is not None else 'N/A'}")
        print(f"  Tax Amount: {self.tax_amount if self.tax_amount is not None else 'N/A'}")
        print(f"  Shipping Fee: {self.shipping_fee if self.shipping_fee is not None else 'N/A'}")
        print(f"  Grand Total: {self.grand_total if self.grand_total is not None else 'N/A'}")
