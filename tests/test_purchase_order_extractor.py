from pathlib import Path
import sys

sys.path.append('src')

from fpdf import FPDF

from core.document_ingestor import DocumentIngestor
from core.metadata_extractor import MetadataExtractor
from models.metadata_models.purchase_order import (
    PurchaseOrderMetadata,
    PurchaseOrderLineItem,
)


class DummyLLM:
    """Simple LLM stub that returns fixed purchase order metadata."""

    def with_structured_output(self, schema):
        class _Invoker:
            def invoke(self, prompt):
                return PurchaseOrderMetadata(
                    po_number="PO123",
                    po_date="2024-06-01",
                    buyer_name="ABC Corp",
                    vendor_name="XYZ Supplies",
                    currency="USD",
                    payment_terms="Net 30",
                    line_items=[
                        PurchaseOrderLineItem(
                            item_number="1",
                            description="Widget",
                            quantity=5.0,
                            unit_price=10.0,
                            total_price=50.0,
                            uom="pcs",
                        )
                    ],
                    subtotal=50.0,
                    tax_amount=5.0,
                    shipping_fee=2.0,
                    grand_total=57.0,
                )

        return _Invoker()


def _create_sample_po_pdf(path: Path) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, "Purchase Order", ln=1)
    pdf.cell(0, 10, "PO Number: PO123", ln=1)
    pdf.cell(0, 10, "PO Date: 2024-06-01", ln=1)
    pdf.cell(0, 10, "Buyer: ABC Corp", ln=1)
    pdf.cell(0, 10, "Vendor: XYZ Supplies", ln=1)
    pdf.cell(0, 10, "Currency: USD", ln=1)
    pdf.cell(0, 10, "Payment Terms: Net 30", ln=1)
    pdf.cell(0, 10, "Item Description Qty UOM Unit Price Total", ln=1)
    pdf.cell(0, 10, "1 Widget 5 pcs 10.00 50.00", ln=1)
    pdf.cell(0, 10, "Subtotal: 50.00", ln=1)
    pdf.cell(0, 10, "Tax: 5.00", ln=1)
    pdf.cell(0, 10, "Shipping: 2.00", ln=1)
    pdf.cell(0, 10, "Grand Total: 57.00", ln=1)
    output = path / "sample_po.pdf"
    pdf.output(str(output))
    return output


def test_purchase_order_extraction(tmp_path):
    pdf_path = _create_sample_po_pdf(tmp_path)
    ingestor = DocumentIngestor(str(pdf_path))
    text = ingestor.get_full_text()
    extractor = MetadataExtractor(llm=DummyLLM())
    metadata = extractor.extract("purchase_order", text)

    assert metadata.po_number == "PO123"
    assert metadata.buyer_name == "ABC Corp"
    assert metadata.vendor_name == "XYZ Supplies"
    assert metadata.currency == "USD"
    assert metadata.payment_terms == "Net 30"
    assert metadata.grand_total == 57.00
    assert len(metadata.line_items) == 1
