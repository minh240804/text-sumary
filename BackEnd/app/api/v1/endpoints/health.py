from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/", response_model=HealthResponse)
def read_root() -> HealthResponse:
    return HealthResponse(
        message="Xin chào! FastAPI đã hoạt động thành công."
    )
