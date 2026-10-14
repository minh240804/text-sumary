from fastapi import FastAPI

app = FastAPI(
    title="Dự án FastAPI của tôi",
    description="API ví dụ khởi tạo ban đầu",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Xin chào! FastAPI đã hoạt động thành công."}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "query_string": q}