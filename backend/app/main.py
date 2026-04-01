from fastapi import FastAPI
from app.routers import compare, upload

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Backend running"}


@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(compare.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
