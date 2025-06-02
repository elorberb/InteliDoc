CLASSIFY_PROMPT_TEMPLATE = """You are a document classifier for business documents. The possible document types are: 
"invoice", "contract", or "earnings_report".

You will be provided with the text from one of the following business documents:
- invoice: A typical business invoice (there are 2 such files)
- contract: A legal contract with multiple clauses
- earnings_report: A business report with tables and charts

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
You are an invoice document understanding assistant. Extract the following metadata from the invoice text below:
- vendor (the company or entity that issued the invoice)
- amount (total amount due)
- due date
- line items: each with description, quantity, unit price, and total

IMPORTANT GUIDELINES:
1. LANGUAGE CONSISTENCY: The extracted metadata (including all keys and values) must be in the same language as the invoice text. Do not translate or change the language.
2. NUMBER FORMATTING: Pay careful attention to decimal vs. thousand separators:
   - In some regions: $1,234.56 (comma = thousands, period = decimals)
   - In other regions: $1.234,56 (period = thousands, comma = decimals)
   Determine the convention from context.

3. DATE FORMATS: Consider all possible formats (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD).

4. TAX AND DISCOUNTS: Include any tax (VAT/GST) or discounts in the total amount.

5. CURRENCY: Note the currency symbol used and maintain consistency.

Return ONLY a JSON matching the expected schema, using the same language as the document.
Document:
\"\"\"{doc_text}\"\"\"
"""

CONTRACT_PROMPT = """
You are a contract document understanding assistant. Extract the following metadata from this contract:
- parties (as a list of organization/company names involved in the agreement)
- effective_date (when the contract begins)
- termination_date (when the contract ends, if specified)
- key_terms (as a list of important clauses or conditions)
- contract_value (total monetary value of the contract, if specified)

IMPORTANT GUIDELINES:
1. PARTIES: Include full legal names of all signing parties (companies/organizations).
   - Distinguish between the primary parties (e.g., "Provider" and "Client")
   - Include subsidiaries or parent companies if mentioned in relation to the agreement

2. DATES: Consider all possible date formats (MM/DD/YYYY, DD/MM/YYYY, YYYY-MM-DD).
   - For effective dates, look for terms like "effective date," "commencement date," "execution date"
   - For termination, look for "expiration," "term ends," "valid until," or calculations like "shall remain in effect for X years"

3. KEY TERMS: Focus on extracting:
   - Payment terms and schedules
   - Confidentiality/NDA clauses
   - Intellectual property provisions
   - Termination conditions
   - Limitation of liability
   - Indemnification clauses
   - Governing law/jurisdiction

4. CONTRACT VALUE: If monetary value is mentioned, note the currency and total amount.
   - This may appear in sections about compensation, payment, or consideration

Return ONLY valid JSON matching the schema.
Document:
\"\"\"{doc_text}\"\"\"
"""

EARNINGS_REPORT_PROMPT = """
You are an earnings report document understanding assistant. Extract the following from the business report:
- reporting_period (clearly identify the time frame covered by the report, e.g., "Q1 2024" or "FY 2023")
- key_metrics (as a dict of name: value)
- executive_summary (concise yet comprehensive paragraph highlighting key performance indicators, significant developments, and business outlook)

IMPORTANT GUIDELINES:
1. NUMBER FORMATTING: Pay careful attention to financial metrics notation:
   - Millions may be abbreviated as "M" or "m" (e.g., $10M means $10 million)
   - Billions may be abbreviated as "B" or "b" (e.g., $2B means $2 billion)
   - Some reports use parentheses for negative values: ($5M) means -$5 million
   - Year-over-year changes may be indicated with +/- percentages

2. REPORTING PERIOD: Identify whether this is a quarterly (Q1/Q2/Q3/Q4) or annual/fiscal year (FY) report.

3. CURRENCY: Note if different metrics use different currencies (USD, EUR, etc.)

4. KEY METRICS: Extract ALL significant financial metrics mentioned in the report, which may include but are not limited to:
   - Revenue/Sales
   - Net Income/Profit
   - Earnings Per Share (EPS)
   - EBITDA
   - Operating Margin
   - Free Cash Flow
   - Return on Investment/Equity (ROI/ROE)
   - Debt-to-Equity Ratio
   - Year-over-Year (YoY) growth figures
   - Industry-specific KPIs (e.g., ARR, MRR, DAU/MAU for tech companies)
   - IMPORTANT: The keys in the key_metrics dictionary MUST be consistent, use only lowercase letters and underscores (snake_case), e.g., "net_income", "operating_margin", "free_cash_flow".

5. EXECUTIVE SUMMARY: Include only factual information from the document covering:
   - Overall financial performance compared to previous periods
   - Major business developments or strategic initiatives
   - Challenges or risks mentioned
   - Forward-looking statements and guidance
   - CEO/management comments on performance
   - Do not include speculative analysis or information not present in the document

Return ONLY a JSON matching the expected schema. All key_metrics keys must be in snake_case (lowercase with underscores).
Document:
\"\"\"{doc_text}\"\"\"
"""
