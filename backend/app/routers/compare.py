from fastapi import APIRouter

router = APIRouter()


@router.post("/compare")
def compare_documents():
    return {
        "comparison_id": "123",
        "message": "Compare API working",
        "result": [],
    }
