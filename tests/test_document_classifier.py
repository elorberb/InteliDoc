import os

import pytest
from document_classifier import DocumentClassifier
from document_ingest import DocumentIngestor

# Map test files to their expected types
expected_types = {
    "invoice1.pdf": "invoice",
    "invoice2.pdf": "invoice",
    "contract.pdf": "contract",
    "earnings.pdf": "report",
    "Home exercise.pdf": "unknown",
}


@pytest.mark.parametrize("filename,expected_type", expected_types.items())
def test_document_classification(filename, expected_type):
    file_path = os.path.join("data", filename)
    ingestor = DocumentIngestor(file_path)
    doc_text = ingestor.get_full_text()

    classifier = DocumentClassifier()
    result = classifier.classify_document(doc_text)

    assert hasattr(result, "type"), f"Result for {filename} missing 'type' attribute"
    assert hasattr(result, "confidence"), f"Result for {filename} missing 'confidence' attribute"
    assert result.type == expected_type, (
        f"Expected type '{expected_type}' for {filename}, got '{result.type}'"
    )
    assert 0.0 <= result.confidence <= 1.0, (
        f"Confidence {result.confidence} for {filename} is out of range [0, 1]"
    )
