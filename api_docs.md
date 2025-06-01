## 📚 API Documentation

The InteliDoc API allows you to upload business documents (PDFs) for classification and metadata extraction. It also
exposes endpoints to retrieve results and simulate document-based action items.

### Swagger URL for Testings:

http://localhost:8000/docs

---

### 📤 POST `/documents/analyze`

**Description**  
Upload a PDF to analyze its content. The document is classified as one of: `invoice`, `contract`, or `earnings_report`,
and structured metadata is extracted accordingly.

**Request**

- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Body**:
    - `file` (required): A PDF file to be analyzed.

**Response**

```json
{
  "document_id": "b2a2b0ac-dc7c-4596-9454-3f50583fcb8e",
  "filename": "invoice2.pdf",
  "classification": {
    "type": "invoice",
    "confidence": 0.96
  },
  "metadata": {
    "vendor": "ACME Corp",
    "amount": "$3,250.00",
    "due_date": "2024-06-15",
    "line_items": [
      {
        "description": "Consulting Services",
        "quantity": 5,
        "unit_price": "$650.00",
        "total": "$3,250.00"
      }
    ]
  }
}
```

**Error Responses**

- `500 Internal Server Error`: If ingestion or LLM processing fails.

---

### 📄 GET `/documents/{doc_id}`

**Description**
Retrieve metadata, classification, and semantic field descriptions for a previously processed document.

**Path Parameters**

- `doc_id` (string): Document UUID returned from `/documents/analyze`.

**Response**

```json
{
  "id": "b2a2b0ac-dc7c-4596-9454-3f50583fcb8e",
  "filename": "invoice2.pdf",
  "classification": {
    "type": "invoice",
    "confidence": 0.96
  },
  "metadata": {
    "vendor": "ACME Corp",
    "amount": "$3,250.00",
    "due_date": "2024-06-15",
    "line_items": [
      ...
    ]
  },
  "field_descriptions": {
    "vendor": "The name of the invoice issuer.",
    "amount": "Total billed amount.",
    "due_date": "Invoice due date.",
    "line_items": "List of billed items with description, quantity, and price."
  }
}

```

**Error Responses**

- `404 Not Found`: Invalid or expired document ID.

---

### 🧾 GET `/documents/{doc_id}/actions`

**Description**
Returns a simulated list of action items related to a document. Can be filtered by status, deadline, or priority.

**Query Parameters (optional)**

- `status`: Filter actions by status (e.g., `pending`, `complete`)

- `deadline`: Filter by deadline date (e.g., `2024-07-01`)

- `priority`: Filter by priority (`high`, `medium`, `low`)

**Example**

```http
GET /documents/b2a2b0ac-dc7c-4596-9454-3f50583fcb8e/actions?status=pending&priority=high
```

**Response**

```json
[
  {
    "action": "follow_up",
    "status": "pending",
    "deadline": "2024-07-01",
    "priority": "high"
  }
]
```

**Error Responses**

- `404 Not Found`: If the document ID is invalid or unknown.

---