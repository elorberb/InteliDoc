CLASSIFY_PROMPT_TEMPLATE = """You are a document classifier for business documents. The possible document types are: 
"invoice", "contract", or "earnings_report".

You will be provided with the text from one of the following business documents:
- invoice: A typical business invoice (there are 2 such files)
- contract: A legal contract with multiple clauses
- earnings_report: A quarterly business report with tables and charts

Given the following document text, classify it and respond only with a valid JSON object matching this schema:
{{
  "type": "...",         // one of: "invoice", "contract", "earnings_report", "unknown"
  "confidence": ...      // number between 0 and 1
}}

Document text:
\"\"\"
{doc_text}
\"\"\"
"""

INVOICE_PROMPT = """
You are a invoice document understanding assistant. Extract the following metadata from the invoice text below:
- vendor
- amount
- due date
- line items: each with description, quantity, unit price, and total

Return ONLY a JSON matching the expected schema.
Document:
\"\"\"{doc_text}\"\"\"
"""

CONTRACT_PROMPT = """
You are a contract document understanding assistant. Extract the following metadata from this contract:
- parties (as a list of names)
- effective_date
- termination_date (if exists)
- key_terms (as a list of phrases)

Return ONLY valid JSON matching the schema.
Document:
\"\"\"{doc_text}\"\"\"
"""

EARNINGS_REPORT_PROMPT = """
You are a earnings report document understanding assistant. Extract the following from the business report:
- reporting period
- key metrics (as a dict of name: value)
- executive summary (short paragraph)

Return JSON matching the expected schema.
Document:
\"\"\"{doc_text}\"\"\"
"""
