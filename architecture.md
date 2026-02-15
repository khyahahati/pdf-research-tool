1. Deterministic Extraction Layer
    - Table extraction
    - OCR fallback
    - Numeric cleaning
    - Block isolation

2. Semantic Normalization Layer (LLM)
    - Map line item names to standard schema
    - No numeric access

3. Structuring Layer
    - Column header detection
    - Period mapping
    - Missing row insertion

4. Output Layer
    - Structured DataFrame
    - Metadata
    - Excel export
