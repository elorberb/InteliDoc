CLASSIFY_PROMPT_TEMPLATE = """
You are a document classifier for business documents. The possible document types are: "invoice", "contract", or "earnings report".

You will be provided with the text from one of the following business documents:
- invoice.pdf: A typical business invoice (there are 2 such files)
- contract.pdf: A legal contract with multiple clauses
- earnings.pdf: A quarterly business report with tables and charts

Given the following document text, classify it and respond only with a valid JSON object matching this schema:
{{
  "type": "...",         // one of: "invoice", "contract", "report", "unknown"
  "confidence": ...      // number between 0 and 1
}}

Document text:
\"\"\"
{doc_text}
\"\"\"
"""
