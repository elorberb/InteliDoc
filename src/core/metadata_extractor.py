from typing import Union

from llm.prompts import (
    INVOICE_PROMPT,
    CONTRACT_PROMPT,
    EARNINGS_REPORT_PROMPT,
    PURCHASE_ORDER_PROMPT,
)
from llm.utils import get_azure_chat_openai_llm, retry_on_rate_limit
from models.metadata_models.contract import ContractMetadata
from models.metadata_models.earnings_report import EarningsReportMetadata
from models.metadata_models.invoice import InvoiceMetadata
from models.metadata_models.purchase_order import PurchaseOrderMetadata


class MetadataExtractor:
    def __init__(self, llm=None):
        """
        Initialize the MetadataExtractor with an optional language model.

        Args:
            llm (Optional[Any]): An optional language model instance. If not provided, a default LLM is loaded.
        """
        if not llm:
            self.llm = get_azure_chat_openai_llm()
        else:
            self.llm = llm
        self.schemas = {
            "invoice": (InvoiceMetadata, INVOICE_PROMPT),
            "contract": (ContractMetadata, CONTRACT_PROMPT),
            "earnings_report": (EarningsReportMetadata, EARNINGS_REPORT_PROMPT),
            "purchase_order": (PurchaseOrderMetadata, PURCHASE_ORDER_PROMPT),
        }

    @retry_on_rate_limit()
    def extract(
            self, doc_type: str, doc_text: str
    ) -> Union[
        InvoiceMetadata,
        ContractMetadata,
        EarningsReportMetadata,
        PurchaseOrderMetadata,
        dict,
    ]:
        """
        Extract structured metadata from a document based on its type.

        Args:
            doc_type (str): The type of the document (e.g., 'invoice', 'contract', 'earnings_report').
            doc_text (str): The full text content of the document.

        Returns:
            Any: The extracted metadata object, or an empty dict if extraction fails or type is unsupported.
        """

        schema, prompt_template = self.schemas.get(doc_type, (None, None))
        if not schema:
            return {}
        structured_llm = self.llm.with_structured_output(schema)
        prompt = prompt_template.format(doc_text=doc_text)
        return structured_llm.invoke(prompt)
