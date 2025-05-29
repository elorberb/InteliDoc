from enum import Enum

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    invoice = "invoice"
    contract = "contract"
    report = "report"
    unknown = "unknown"


class DocumentClassification(BaseModel):
    type: DocumentType = Field(
        ...,
        description="Document type: invoice, contract, report, or unknown"
    )
    confidence: float = Field(..., description="Confidence score between 0 and 1")
