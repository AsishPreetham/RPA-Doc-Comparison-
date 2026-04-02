from fastapi import FastAPI, UploadFile, File, HTTPException
from pathlib import Path
import shutil
from uuid import uuid4

from text_extractor import extract_text
from field_extractor import extract_fields
from comparator import compare_structured_fields
from app.services.bigquery_service import (
    insert_comparison_result,
    get_comparison_results,
)

app = FastAPI()

UPLOAD_FOLDER = Path("uploads")
UPLOAD_FOLDER.mkdir(exist_ok=True)


@app.get("/")
def home():
    return {"message": "Backend is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/comparison-results")
def comparison_results():
    try:
        results = get_comparison_results()
        return {
            "message": "Comparison results fetched successfully",
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-documents")
def upload_documents(
    prior_auth_file: UploadFile = File(...),
    insurance_file: UploadFile = File(...)
):
    try:
        prior_auth_name = f"{uuid4()}_{prior_auth_file.filename}"
        insurance_name = f"{uuid4()}_{insurance_file.filename}"

        prior_auth_path = UPLOAD_FOLDER / prior_auth_name
        insurance_path = UPLOAD_FOLDER / insurance_name

        with open(prior_auth_path, "wb") as buffer:
            shutil.copyfileobj(prior_auth_file.file, buffer)

        with open(insurance_path, "wb") as buffer:
            shutil.copyfileobj(insurance_file.file, buffer)

        prior_auth_text = extract_text(str(prior_auth_path))
        insurance_text = extract_text(str(insurance_path))

        prior_auth_fields = extract_fields(prior_auth_text)
        insurance_fields = extract_fields(insurance_text)

        comparison_result = compare_structured_fields(
            prior_auth_fields,
            insurance_fields
        )

        bigquery_row = insert_comparison_result(
            prior_auth_file=prior_auth_name,
            insurance_file=insurance_name,
            comparison_result=comparison_result,
            prior_auth_fields=prior_auth_fields,
            insurance_fields=insurance_fields
        )

        return {
            "message": "Files uploaded, parsed, compared, and saved to BigQuery successfully",
            "prior_auth_file": prior_auth_name,
            "insurance_file": insurance_name,
            "prior_auth_preview": prior_auth_text[:1000],
            "insurance_preview": insurance_text[:1000],
            "prior_auth_fields": prior_auth_fields,
            "insurance_fields": insurance_fields,
            "comparison_result": comparison_result,
            "bigquery_row": bigquery_row
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))