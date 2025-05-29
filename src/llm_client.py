# llm_client.py
import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

from models.document_classification import DocumentClassification
from prompts import CLASSIFY_PROMPT_TEMPLATE

load_dotenv()


class LLMClient:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            temperature=0,
        )

    def classify_document(self, doc_text: str) -> DocumentClassification:
        prompt = CLASSIFY_PROMPT_TEMPLATE.format(doc_text=doc_text)
        structured_llm = self.llm.with_structured_output(DocumentClassification)
        result = structured_llm.invoke(prompt)
        return result
