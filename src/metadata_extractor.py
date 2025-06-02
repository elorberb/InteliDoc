from typing import Union

from llm_utils import with_retries, get_azure_chat_openai_llm
from models.metadata_models.contract import ContractMetadata
from models.metadata_models.earnings_report import EarningsReportMetadata
from models.metadata_models.invoice import InvoiceMetadata
from prompts import INVOICE_PROMPT, CONTRACT_PROMPT, EARNINGS_REPORT_PROMPT


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
        }

    def extract(self, doc_type: str, doc_text: str) -> Union[
        InvoiceMetadata, ContractMetadata, EarningsReportMetadata, dict]:
        """
        Extract structured metadata from a document based on its type.

        Args:
            doc_type (str): The type of the document (e.g., 'invoice', 'contract', 'earnings_report').
            doc_text (str): The full text content of the document.

        Returns:
            Any: The extracted metadata object, or an empty dict if extraction fails or type is unsupported.
        """

        def _extract_metadata(doc_type, doc_text):
            schema, prompt_template = self.schemas.get(doc_type, (None, None))
            if not schema:
                return {}
            structured_llm = self.llm.with_structured_output(schema)
            prompt = prompt_template.format(doc_text=doc_text)
            return structured_llm.invoke(prompt)

        try:
            return with_retries(_extract_metadata, doc_type, doc_text)
        except Exception as e:
            print(f"Extraction failed: {e}")
            return {}
