from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil

from app.services.parser_service import extract_text

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_documents(
    document_a: UploadFile = File(...),
    document_b: UploadFile = File(...)
):
    try:
        file_a_path = UPLOAD_DIR / document_a.filename
        file_b_path = UPLOAD_DIR / document_b.filename

        with file_a_path.open("wb") as buffer:
            shutil.copyfileobj(document_a.file, buffer)

        with file_b_path.open("wb") as buffer:
            shutil.copyfileobj(document_b.file, buffer)

        text_a = extract_text(str(file_a_path))
        text_b = extract_text(str(file_b_path))

        return {
            "message": "Files uploaded and parsed successfully",
            "document_a": document_a.filename,
            "document_b": document_b.filename,
            "document_a_preview": text_a[:1000],
            "document_b_preview": text_b[:1000],
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))