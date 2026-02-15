import os
import tempfile
import threading
from typing import List

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from main import run_pipeline

app = FastAPI(title="Income Statement Extractor")

pipeline_lock = threading.Lock()


def _cleanup(paths: List[str]) -> None:
    for path in paths:
        try:
            if path and os.path.exists(path):
                os.remove(path)
        except OSError:
            pass


@app.get("/")
def index() -> FileResponse:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return FileResponse(os.path.join(base_dir, "static", "index.html"))


@app.post("/extract-income-statement")
async def extract_income_statement(file: UploadFile = File(...)) -> FileResponse:
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file uploaded.")

    filename_lower = file.filename.lower()
    content_type = (file.content_type or "").lower()
    is_pdf = filename_lower.endswith(".pdf") or content_type in {"application/pdf", "application/x-pdf"}

    if not is_pdf:
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    if not pipeline_lock.acquire(blocking=False):
        raise HTTPException(status_code=429, detail="Service is busy. Try again shortly.")

    temp_pdf_path = None
    output_path = None
    response_ready = False

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf_path = temp_pdf.name
            content = await file.read()
            if not content:
                raise HTTPException(status_code=400, detail="Uploaded file is empty.")
            temp_pdf.write(content)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as temp_xlsx:
            output_path = temp_xlsx.name

        result = run_pipeline(temp_pdf_path, output_path=output_path)

        if result is None or not output_path or not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Extraction failed.")

        cleanup_task = BackgroundTask(_cleanup, [temp_pdf_path, output_path])
        response_ready = True
        return FileResponse(
            output_path,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename="income_statement.xlsx",
            background=cleanup_task
        )
    finally:
        pipeline_lock.release()
        if not response_ready:
            _cleanup([temp_pdf_path, output_path])

