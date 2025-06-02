import os

from langchain_openai import AzureChatOpenAI

from llm_utils import with_retries, get_azure_chat_openai_llm
from models.metadata_models.contract import ContractMetadata
from models.metadata_models.earnings_report import EarningsReportMetadata
from models.metadata_models.invoice import InvoiceMetadata
from prompts import INVOICE_PROMPT, CONTRACT_PROMPT, EARNINGS_REPORT_PROMPT


class MetadataExtractor:
    def __init__(self, llm=None):
        if not llm:
            self.llm = get_azure_chat_openai_llm()
        else:
            self.llm = llm
        self.schemas = {
            "invoice": (InvoiceMetadata, INVOICE_PROMPT),
            "contract": (ContractMetadata, CONTRACT_PROMPT),
            "earnings_report": (EarningsReportMetadata, EARNINGS_REPORT_PROMPT),
        }

    def extract(self, doc_type: str, doc_text: str):
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


if __name__ == '__main__':
    from document_ingestor import DocumentIngestor
    from document_classifier import DocumentClassifier
    from metadata_extractor import MetadataExtractor

    file_path = "data/scanned_pdfs/scanned_contract1.pdf"
    ingestor = DocumentIngestor(file_path)
    doc_text = ingestor.get_full_text()

    classifier = DocumentClassifier()
    doc_type = classifier.classify_document(doc_text).type.value

    extractor = MetadataExtractor()
    metadata = extractor.extract(doc_type, doc_text)

    print("Extracted Metadata:")
    metadata.pretty_print()
