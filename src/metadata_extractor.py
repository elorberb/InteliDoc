import os

from langchain_openai import AzureChatOpenAI

from models.contract import ContractMetadata
from models.earnings_report import EarningsReportMetadata
from models.invoice import InvoiceMetadata
from prompts import INVOICE_PROMPT, CONTRACT_PROMPT, EARNINGS_REPORT_PROMPT


class MetadataExtractor:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            temperature=0,
        )
        self.schemas = {
            "invoice": (InvoiceMetadata, INVOICE_PROMPT),
            "contract": (ContractMetadata, CONTRACT_PROMPT),
            "earnings_report": (EarningsReportMetadata, EARNINGS_REPORT_PROMPT),
        }

    def extract(self, doc_type: str, doc_text: str):
        schema, prompt_template = self.schemas.get(doc_type, (None, None))
        if not schema:
            return {}
        structured_llm = self.llm.with_structured_output(schema)
        prompt = prompt_template.format(doc_text=doc_text[:6000])
        try:
            return structured_llm.invoke(prompt)
        except Exception as e:
            print(f"Extraction failed: {e}")
            return {}


if __name__ == '__main__':
    from document_ingestor import DocumentIngestor
    from document_classifier import DocumentClassifier
    from metadata_extractor import MetadataExtractor

    file_path = "data/Contract.pdf"
    ingestor = DocumentIngestor(file_path)
    doc_text = ingestor.get_full_text()

    classifier = DocumentClassifier()
    doc_type = classifier.classify_document(doc_text).type.value

    extractor = MetadataExtractor()
    metadata = extractor.extract(doc_type, doc_text)

    print("Doc Type:", doc_type)
    print("Extracted Metadata:")
    print(metadata)
