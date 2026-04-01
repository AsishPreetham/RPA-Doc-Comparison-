from fastapi import APIRouter, UploadFile, File

router = APIRouter()


@router.post("/upload")
def upload_documents(
    document_a: UploadFile = File(...),
    document_b: UploadFile = File(...),
):
    return {
        "document_a": document_a.filename,
        "document_b": document_b.filename,
    }
