from typing import List

from dotenv import load_dotenv

from llm_utils import get_azure_chat_openai_llm, with_retries
from models.document_classification import DocumentClassification
from prompts import CLASSIFY_PROMPT_TEMPLATE

load_dotenv()


class DocumentClassifier:
    def __init__(self, llm=None):
        """
        Initialize the DocumentClassifier.

        Args:
            llm: An optional language model instance. If not provided, a default LLM is loaded.
        """
        if not llm:
            self.llm = get_azure_chat_openai_llm()
        else:
            self.llm = llm

    def classify_document(self, doc_text: str) -> DocumentClassification:
        """
        Classify a single document's text and return its classification.

        Args:
            doc_text (str): The text content of the document to classify.

        Returns:
            DocumentClassification: The classification result for the document.
        """

        def _classify(doc_text):
            prompt = CLASSIFY_PROMPT_TEMPLATE.format(doc_text=doc_text)
            classifier_llm = self.llm.with_structured_output(DocumentClassification)
            return classifier_llm.invoke(prompt)

        return with_retries(_classify, doc_text)

    def classify_documents(self, doc_texts: list[str]) -> List[DocumentClassification]:
        """
        Classify a batch of documents and return their classifications.

        Args:
            doc_texts (list[str]): A list of document texts to classify.

        Returns:
            list[DocumentClassification]: A list of classification results for each document.
        """

        def _classify_batch(doc_texts):
            classifier_llm = self.llm.with_structured_output(DocumentClassification)
            prompts = [CLASSIFY_PROMPT_TEMPLATE.format(doc_text=doc) for doc in doc_texts]
            return list(classifier_llm.batch(prompts))

        return with_retries(_classify_batch, doc_texts)
