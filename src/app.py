import uuid
from typing import Dict, Optional, Any

from fastapi import FastAPI, UploadFile, File, HTTPException, Query

from document_classifier import DocumentClassifier
from document_ingestor import DocumentIngestor
from llm_utils import get_azure_chat_openai_llm
from metadata_extractor import MetadataExtractor
from models.analyze_response import AnalyzeResponse

app = FastAPI(title="📑 InteliDoc: Intelligence Document API")
# In-memory storage
DOCUMENT_STORE: Dict[str, dict] = {}

# Initialize shared components at app startup
llm = get_azure_chat_openai_llm()
classifier = DocumentClassifier(llm)
extractor = MetadataExtractor(llm)


def _get_field_descriptions(doc_type: str) -> Dict[str, str]:
    """
    Return a dictionary mapping field names to their descriptions for a given document type.

    Args:
        doc_type (str): The type of the document (e.g., 'invoice', 'contract', 'earnings_report').

    Returns:
        Dict[str, str]: A dictionary of field descriptions.
    """
    if doc_type == "invoice":
        return {
            "vendor": "The name of the invoice issuer.",
            "amount": "Total billed amount.",
            "due_date": "Invoice due date.",
            "line_items": "List of billed items with description, quantity, and price."
        }
    elif doc_type == "contract":
        return {
            "parties": "Entities involved in the contract.",
            "effective_date": "Start date of the contract.",
            "termination_date": "End date of the contract, if specified.",
            "key_terms": "Key clauses or points within the agreement."
        }
    elif doc_type == "earnings_report":
        return {
            "reporting_period": "Time period covered by the report.",
            "key_metrics": "Numerical metrics such as revenue, profit, etc.",
            "executive_summary": "A high-level summary of the report."
        }
    return {}


@app.post("/documents/analyze", response_model=AnalyzeResponse)
async def analyze_document(file: UploadFile = File(...)) -> AnalyzeResponse:
    """
    Analyze an uploaded document: ingest, classify, extract metadata, and store results.

    Args:
        file (UploadFile): The uploaded PDF file.

    Returns:
        AnalyzeResponse: The analysis result including document ID, filename, classification, and metadata.

    Raises:
        HTTPException: If any error occurs during processing.
    """
    try:
        contents = await file.read()
        doc_id = str(uuid.uuid4())
        temp_path = f"/tmp/{doc_id}.pdf"

        # Save uploaded PDF temporarily
        with open(temp_path, "wb") as f:
            f.write(contents)

        # Ingest → Classify → Extract
        ingestor = DocumentIngestor(temp_path)
        full_text = ingestor.get_full_text()

        classification = classifier.classify_document(full_text)
        metadata_obj = extractor.extract(classification.type.value, full_text)

        # Store original objects, not flattened values
        DOCUMENT_STORE[doc_id] = {
            "filename": file.filename,
            "classification": classification,
            "metadata": metadata_obj
        }

        return AnalyzeResponse(
            document_id=doc_id,
            filename=file.filename,
            classification=classification,
            metadata=metadata_obj,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents/{doc_id}")
def get_document(doc_id: str) -> Dict[str, Any]:
    """
    Retrieve a document's analysis results by its ID.

    Args:
        doc_id (str): The unique document identifier.

    Returns:
        Dict[str, Any]: The document's filename, classification, metadata, and field descriptions.

    Raises:
        HTTPException: If the document is not found.
    """
    doc = DOCUMENT_STORE.get(doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    classification = doc["classification"]

    return {
        "id": doc_id,
        "filename": doc["filename"],
        "classification": classification,
        "metadata": doc["metadata"],
        "field_descriptions": _get_field_descriptions(classification.type.value)
    }


@app.get("/documents/{doc_id}/actions")
def get_actions(doc_id: str,
                status: Optional[str] = Query(None),
                deadline: Optional[str] = Query(None),
                priority: Optional[str] = Query(None)
                ) -> list[Dict[str, str]]:
    """
    Retrieve possible actions for a document, optionally filtered by status, deadline, or priority.

    Args:
        doc_id (str): The unique document identifier.
        status (Optional[str]): Filter by action status.
        deadline (Optional[str]): Filter by action deadline.
        priority (Optional[str]): Filter by action priority.

    Returns:
        list[Dict[str, str]]: A list of action dictionaries.

    Raises:
        HTTPException: If the document is not found.
    """
    if doc_id not in DOCUMENT_STORE:
        raise HTTPException(status_code=404, detail="Document not found")

    # Stub: simulate extracted actions
    actions = [
        {"action": "follow_up", "status": "pending", "deadline": "2024-07-01", "priority": "high"},
        {"action": "validate_terms", "status": "in_progress", "priority": "medium"},
        {"action": "finalize", "status": "complete", "priority": "low"},
    ]

    def matches(action):
        return (not status or action.get("status") == status) and \
            (not deadline or action.get("deadline") == deadline) and \
            (not priority or action.get("priority") == priority)

    return [a for a in actions if matches(a)]
