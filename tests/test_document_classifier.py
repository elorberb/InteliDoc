import os
import random

import sys
import pytest
from sklearn.metrics import accuracy_score, precision_score, recall_score

sys.path.append('src')

from core.document_classifier import DocumentClassifier
from core.document_ingestor import DocumentIngestor

# Map test files to their expected types
expected_types = {
    "invoice1.pdf": "invoice",
    "invoice2.pdf": "invoice",
    "contract.pdf": "contract",
    "earnings.pdf": "earnings_report",
    "Home exercise.pdf": "unknown",
}


def prepare_docs():
    doc_texts = []
    doc_labels = []
    for filename, label in expected_types.items():
        file_path = os.path.join("data", "factify", filename)
        ingestor = DocumentIngestor(file_path)
        doc_texts.append(ingestor.get_full_text())
        doc_labels.append(label)
    return doc_texts, doc_labels


@pytest.mark.parametrize("n_runs", [50])
def test_classifier_batch_metrics(n_runs):
    doc_texts, doc_labels = prepare_docs()
    classifier = DocumentClassifier()

    # Randomly sample documents for the batch
    indices = [random.randint(0, len(doc_texts) - 1) for _ in range(n_runs)]
    batch_texts = [doc_texts[i] for i in indices]
    y_true = [doc_labels[i] for i in indices]

    print(f"Classifying a batch of {n_runs} documents...")
    results = classifier.classify_documents(batch_texts)
    y_pred = [res.type.value for res in results]

    classes = list(set(expected_types.values()))
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, labels=classes, average=None, zero_division=0)
    recall = recall_score(y_true, y_pred, labels=classes, average=None, zero_division=0)

    print(f"\nAccuracy: {accuracy:.2f}")
    for cls, p, r in zip(classes, precision, recall):
        print(f"Class '{cls}': Precision={p:.2f}, Recall={r:.2f}")

    assert accuracy > 0.9, "Classifier accuracy is too low"


@pytest.mark.parametrize("target_class", list(set(expected_types.values())))
@pytest.mark.parametrize("n_runs", [50])
def test_metrics_per_class(target_class, n_runs):
    # Prepare only documents of the target class
    doc_files = [f for f, label in expected_types.items() if label == target_class]
    if not doc_files:
        pytest.skip(f"No documents for class {target_class}")

    doc_texts = []
    for filename in doc_files:
        file_path = os.path.join("data", "factify", filename)
        ingestor = DocumentIngestor(file_path)
        doc_texts.append(ingestor.get_full_text())

    classifier = DocumentClassifier()

    # Sample with replacement if not enough docs
    batch_texts = [random.choice(doc_texts) for _ in range(n_runs)]
    y_true = [target_class] * n_runs

    results = classifier.classify_documents(batch_texts)
    y_pred = [res.type.value for res in results]

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, labels=[target_class], average="macro", zero_division=0)
    recall = recall_score(y_true, y_pred, labels=[target_class], average="macro", zero_division=0)

    print(f"\nClass '{target_class}': Accuracy={accuracy:.2f}, Precision={precision:.2f}, Recall={recall:.2f}")

    assert accuracy > 0.9, f"Accuracy for class {target_class} is too low"


@pytest.mark.parametrize("filename,expected_type", expected_types.items())
def test_document_classification_simple_case(filename, expected_type):
    file_path = os.path.join("data", "factify", filename)
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
