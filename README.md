
# Income Statement Extractor (Minimal UI + API)

This repo exposes the existing extraction pipeline through a minimal FastAPI endpoint and a single-page HTML UI.

## What it does

- Upload a PDF annual report
- Run the existing extraction pipeline (`run_pipeline`)
- Download the generated Excel file

## Local setup

1. Set required environment variable:

	- `GEMINI_API_KEY` (only needed if LLM normalization is enabled)

2. Install Python dependencies:

	```bash
	pip install -r requirements.txt
	```

	The pipeline also depends on OCR and PDF tooling, which must be installed for your OS:

	- Tesseract OCR (required for OCR fallback)
	- Poppler (required for `pdf2image`)

3. Run the API:

	```bash
	uvicorn app:app --reload
	```

4. Open the UI in your browser:

	- http://localhost:8000

## API

- `POST /extract-income-statement`
  - Form-data field: `file` (PDF)
  - Returns: `income_statement.xlsx`

## Deployment (free-tier)

You can deploy on Render or Railway as a single FastAPI service. The HTML is served by the same app.

Example (Render):

1. Create a new Web Service and connect this repo.
2. Set the build command:

	```bash
	pip install -r requirements.txt
	```

	This repo includes a requirements file for installation.

3. Set the start command:

	```bash
	uvicorn app:app --host 0.0.0.0 --port $PORT
	```

4. Add environment variable:

	- `GEMINI_API_KEY`

## Known limitations (free-tier hosting)

- File size limits (varies by host, often 10-50 MB)
- Cold starts (first request can be slow)
- OCR latency (large PDFs can take time)
- OCR dependencies must be installed in the deployment environment

## Files added for the minimal interface

- [app.py](app.py)
- [static/index.html](static/index.html)
