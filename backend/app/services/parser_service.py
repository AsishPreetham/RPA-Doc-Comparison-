from docx import Document
from pathlib import Path


def extract_docx_text(file_path: str) -> str:
    doc = Document(file_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)


def extract_text(file_path: str) -> str:
    path = Path(file_path)
    suffix = path.suffix.lower()

    if suffix == ".docx":
        return extract_docx_text(file_path)

    raise ValueError(f"Unsupported file type: {suffix}")