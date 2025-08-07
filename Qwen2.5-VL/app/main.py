from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="Qwen2.5-VL OCR API")
app.include_router(router)
