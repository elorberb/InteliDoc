import os
import time

import openai
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

from document_ingest import DocumentIngestor
from models.document_classification import DocumentClassification
from prompts import CLASSIFY_PROMPT_TEMPLATE

load_dotenv()


class DocumentClassifier:
    def __init__(self):
        self.llm = AzureChatOpenAI(
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            api_version=os.getenv("OPENAI_API_VERSION"),
            temperature=0,
        )

    @staticmethod
    def _with_retries(func, *args, max_retries=5, base_delay=5, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except openai.RateLimitError:
                wait_time = base_delay * (2 ** attempt)
                print(f"Rate limit hit. Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(wait_time)
        raise RuntimeError("Exceeded maximum retries due to rate limiting.")

    def classify_document(self, doc_text: str) -> DocumentClassification:
        def _classify(doc_text):
            prompt = CLASSIFY_PROMPT_TEMPLATE.format(doc_text=doc_text)
            classifier_llm = self.llm.with_structured_output(DocumentClassification)
            return classifier_llm.invoke(prompt)

        return self._with_retries(_classify, doc_text)

    def classify_documents(self, doc_texts: list[str]) -> list:
        def _classify_batch(doc_texts):
            classifier_llm = self.llm.with_structured_output(DocumentClassification)
            prompts = [CLASSIFY_PROMPT_TEMPLATE.format(doc_text=doc) for doc in doc_texts]
            return list(classifier_llm.batch(prompts))

        return self._with_retries(_classify_batch, doc_texts)


if __name__ == "__main__":
    ingestor = DocumentIngestor("data/Contract.pdf")
    doc_text = ingestor.get_full_text()

    doc_classifier = DocumentClassifier()
    classification = doc_classifier.classify_document(doc_text)
    print("Classification Result:")
    print(classification)
