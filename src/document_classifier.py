from dotenv import load_dotenv

from llm_utils import get_azure_chat_openai_llm, with_retries
from models.document_classification import DocumentClassification
from prompts import CLASSIFY_PROMPT_TEMPLATE

load_dotenv()


class DocumentClassifier:
    def __init__(self, llm=None):
        if not llm:
            self.llm = get_azure_chat_openai_llm()
        else:
            self.llm = llm

    def classify_document(self, doc_text: str) -> DocumentClassification:
        def _classify(doc_text):
            prompt = CLASSIFY_PROMPT_TEMPLATE.format(doc_text=doc_text)
            classifier_llm = self.llm.with_structured_output(DocumentClassification)
            return classifier_llm.invoke(prompt)

        return with_retries(_classify, doc_text)

    def classify_documents(self, doc_texts: list[str]) -> list:
        def _classify_batch(doc_texts):
            classifier_llm = self.llm.with_structured_output(DocumentClassification)
            prompts = [CLASSIFY_PROMPT_TEMPLATE.format(doc_text=doc) for doc in doc_texts]
            return list(classifier_llm.batch(prompts))

        return with_retries(_classify_batch, doc_texts)
