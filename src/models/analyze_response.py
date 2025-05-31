from typing import Union

from pydantic import BaseModel

from models.document_classification import DocumentClassification
from models.metadata_models.contract import ContractMetadata
from models.metadata_models.earnings_report import EarningsReportMetadata
from models.metadata_models.invoice import InvoiceMetadata


class AnalyzeResponse(BaseModel):
    document_id: str
    filename: str
    classification: DocumentClassification
    metadata: Union[InvoiceMetadata, ContractMetadata, EarningsReportMetadata]
