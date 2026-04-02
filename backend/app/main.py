from fastapi import FastAPI
from app.routers import compare, upload

app = FastAPI()

app.include_router(compare.router, prefix="/api", tags=["Compare"])
app.include_router(upload.router, prefix="/api", tags=["Upload"])

@app.get("/")
def home():
    return {"message": "Backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}