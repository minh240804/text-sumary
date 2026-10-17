from fastapi import FastAPI

from app.api.v1.api import api_router

app = FastAPI(
    title="Dự án FastAPI của tôi",
    description="API ví dụ khởi tạo ban đầu",
    version="1.0.0",
)

app.include_router(api_router)
