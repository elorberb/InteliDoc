## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/elorberb/InteliDoc.git
cd intelidoc
```

### 2. Install Dependencies Using `uv`
First, ensure that `uv` is installed. If not, you can install it using `pip`:

```bash
pip install uv
```
Once `uv` is installed, create a virtual environment and install the required dependencies:

```bash
uv venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
uv pip install -r requirements.txt
```

### 3. Configure Environment Variables
Create a .env file in the root directory and add the following:

```env
AZURE_OPENAI_DEPLOYMENT_NAME=your_azure_deployment_name
OPENAI_API_KEY=your_openai_api_key
OPENAI_API_VERSION=openai_api_version
```

### 4. Run the API
First, add the `src/` directory to your `PYTHONPATH`:
```bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/src  # On Windows use `set PYTHONPATH=%cd%\src`
```

Then, start the FastAPI server using `uvicorn`:
```bash
uvicorn src.app:app --reload
```

Access the API at: http://localhost:8000/docs to test app endpoints in Swagger UI.

## 🛠️ 1. Design Decisions
### 🧱 Modular Architecture
The system is designed with separation of concerns across the following components:

- `DocumentIngestor`
Handles PDF parsing using pdfplumber. Extracts clean, page-by-page text and returns a structured string ready for LLM processing.

- `DocumentClassifier`
Uses Azure-hosted GPT-4o through LangChain with structured output. It classifies documents into one of four types (invoice, contract, earnings_report, unknown).

- `MetadataExtractor`
Based on the classified document type, it selects the correct schema and prompt to extract structured metadata. Uses Pydantic models for type safety and consistency.

### 🧠 LLM Strategy
- **Model:** GPT-4o from Azure OpenAI with support for structured outputs and large context windows.

- **Structured Outputs:** Output is parsed directly into Pydantic models to enforce schema integrity.

- **Retry Logic:** Classification and extraction are wrapped in exponential backoff logic to handle rate limits gracefully.

### 📋 Prompt Engineering
All prompts are centralized in `prompts.py`. Each is designed with identity-setting, detailed task instructions, and handling for edge cases.

- **Classification Prompt:**
Asks the model to choose from `invoice`, `contract`, `earnings_report`, or `unknown`, returning confidence score.

- **Invoice Prompt:**
Extracts metadata like vendor, due date, amount, and line items. Handles currency formatting, taxes, and discounts.

- **Contract Prompt:**
Extracts parties, effective and termination dates, and key clauses.

- **Earnings Report Prompt:**
Extracts reporting period, metrics (revenue, net income, EPS, etc.), and a structured executive summary.


## 🤖 2. AI-Powered Feature Proposals

Below are two flagship capabilities—described in depth—followed by a quick roundup of additional ideas that can be layered on later.

---

### Feature 1 · Conversational Q&A RAG Side-Panel  
*“Ask your document anything and jump straight to the answer.”*

| |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|---|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **What it does** | Adds a chat pane to the viewer. Users type natural-language questions (“What is the net income YoY?” “Who signed on behalf of Acme?”) and receive: 1) a concise answer, 2) a clickable links that scrolls to the exact sentence.                                                                                                                                                                                                                                                                            |
| **Technical approach** | **Ingestion**<br>1. Split each page into semantic chunks (headings, paragraphs, table rows).<br>2. Generate embeddings with `text-embedding-3-small` and store in a vector DB along with page and offset references.<br><br>**Inference**<br>3. Embed the user query and retrieve top-K relevant chunks (using cosine).<br>4. Use GPT-4o to generate a concise answer and return source spans with locations.<br>5. Front-end highlights and scrolls to the relevant text in the viewer. |
| **Business value** | • Helps users instantly find what they need without reading full documents.<br>• Makes the viewer interactive and language-accessible to all roles.<br>• Increases time-on-platform and perceived value.                                                                                                                                                                                                                                                                                                    |

---

### Feature 2 · Cross-Document Metadata Propagation  
*“Use what one document knows to enrich and validate the others.”*

| |                                                                                                                                                                                                                                                                                                                                  |
|---|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **What it does** | Automatically shares and validates key metadata (e.g., `vendor`, `payment_terms`, `contract_id`) across related documents. When missing fields or conflicts are found, the system suggests auto-filling or resolving them based on previously extracted information.                                                             |
| **Technical approach** | 1. Store normalized extracted metadata (e.g., in a Postgres DB).<br>2. On each new document, match it by key fields (e.g., `vendor_name`, `contract_id`).<br>3. Compare known metadata to the new document’s fields.<br>4. Suggest updates. |
| **Business value** | • Reduces human review by filling in metadata gaps automatically.<br>• Prevents errors and inconsistencies across related files.<br>• Makes the Factify knowledge base compound over time—the more you upload, the more powerful it gets.                                                                                        |

---

### 🗂️ Other High-Impact Features (One-Liners)

| Idea | Quick Description |
|------|-------------------|
| **Payables Intelligence & Anomaly Alerts** | Nightly analytics on invoice metadata to flag duplicates, outliers, and cash-flow spikes. |
| **Contract Red-Line Generator** | GPT-4o drafts mark-ups by comparing clauses against a policy library; produces a one-page risk summary. |
| **Currency & Unit Normaliser** | Automatically converts all monetary values and units to corporate standards, storing both raw and normalised figures. |
| **Executive One-Pager Generator** | Generates branded PDF/PowerPoint summaries of earnings reports or contracts for leadership. |
| **Document Health Score** | Rates uploads for completeness (missing signatures, totals) and readability; low scores are routed back to senders. |
| **Semantic Highlights** | Auto-highlights the top-K most informative sentences or rows in the viewer to guide the reader’s attention. |
| **Numeric Validation & Table Audits** | Recomputes totals/subtotals in extracted tables and flags discrepancies or tax miscalculations. |
| **Automated Redaction / Permission Zones** | Detects sensitive content and masks it based on user role; ensures safe sharing with external parties. |


## 🚀 3. Production Considerations

To prepare this system for production use, we considered several operational challenges and designed strategies to handle them effectively.

---

### 1. Rate-limit Errors or Transient Failures

LLM providers like OpenAI enforce rate limits on API usage. If too many requests hit the endpoint in a short time, the API responds with a `429 Too Many Requests` error.

**Solution:**

- Implement **exponential backoff with retries**, already built into the `with_retries()` in the `llm_utils.py` module. This progressively increases the wait time between retries.
- Provision multiple GPT-4o deployments (e.g., `gpt4o-east`, `gpt4o-west`) and cycle through them using a **round-robin mechanism** to balance load and avoid throttling on a single endpoint.

---

### 2. High Latency on Large PDFs

Long documents can take time to parse and process, especially if they approach or exceed token limits, resulting in slow user response times.

**Solution:**

- Convert all FastAPI endpoints to **asynchronous (`async def`) functions** to prevent blocking I/O operations.
- Offload heavy work—such as ingestion, classification, and metadata extraction—to a **background queue**.
- The main API call immediately returns a job ID, and the client polls `GET /status/{job_id}` to check processing progress.
---

### 3. Scanned or Non-Text PDFs

Some PDFs are just images (e.g., scanned contracts or receipts), and text extraction using `pdfplumber` fails or returns empty.

**Solution:**

- Detect empty or near-empty text from `pdfplumber`.
- Route these pages (or the entire document) through an **OCR service** such as Tesseract.
- Merge the OCR-extracted content back into the pipeline before passing it to the LLM.

---

### 4. Very Large PDFs

Processing extremely long documents is expensive and often exceeds LLM context limits.

**Solution:**

- Apply **smart chunking**: split documents by logical headings or every _n_ pages. Run classification once and then process each chunk concurrently.
- Use **Top-K retrieval**: embed all chunks and ask a semantic question like _“Which sections describe financial KPIs?”_. Send only the most relevant chunks to the LLM, reducing cost and context size.

---

### 5. Redundant LLM Calls (Cost Optimization)

To reduce unnecessary LLM calls, we use a two-layer caching strategy:

- **Classification Caching (Semantic)**:  
  We embed each document using a model like `text-embedding-3-small` and compare it against previously classified documents using cosine similarity. If a similar document is found (e.g., ≥ 0.95), we reuse its classification result.

- **Extraction Caching (Exact Match)**:  
  After ingestion, we compute `sha256(clean_text)`. If the same hash exists from a prior run, we reuse the stored metadata instead of re-extracting it.

This approach avoids reprocessing duplicates while ensuring only exact matches are reused for extraction.


### 6. Cost Estimation and Budgeting

LLM API calls can be costly, especially with variable-length documents. Input and output tokens are billed separately by most providers (e.g., OpenAI charges 3× more for output tokens with GPT-4o).

**Solution:**

- Log `input_tokens`, `output_tokens`, and `document_type` for every LLM interaction to build a token usage profile.
- Train a **simple regression model** per document type to predict `output_tokens` based on `input_tokens` (e.g., `output ≈ α + β × input`).
- Use the more accurate cost formula: estimated_cost = (input_tokens × input_price) + (predicted_output_tokens × output_price) where `input_price` and `output_price` are based on the LLM vendor's pricing (e.g., GPT-4o: $0.005/input_token, $0.015/output_token per 1K tokens).
- Refresh the regression model periodically using recent production data to improve cost estimation accuracy.
---