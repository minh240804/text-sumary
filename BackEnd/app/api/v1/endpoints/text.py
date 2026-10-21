from fastapi import APIRouter, Body, HTTPException

from app.schemas.text import MAX_TEXT_LENGTH, TextAnalysisRequest, TextAnalysisResponse
from app.services.text_service import analyze_text

router = APIRouter(prefix="/api/v1/text", tags=["text"])


@router.post("/analyze", response_model=TextAnalysisResponse)
def analyze_text_endpoint(payload: TextAnalysisRequest) -> TextAnalysisResponse:
    return analyze_text(payload.text)


@router.post("/analyze/raw", response_model=TextAnalysisResponse)
def analyze_raw_text_endpoint(
    text: str = Body(
        ...,
        media_type="text/plain",
        description="Dán trực tiếp văn bản nhiều dòng, không cần bọc trong JSON.",
    ),
) -> TextAnalysisResponse:
    """Analyze raw text so clients can paste multiline content directly."""
    if not text:
        raise HTTPException(status_code=422, detail="Văn bản không được để trống.")
    if len(text) > MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=422,
            detail=f"Văn bản không được dài quá {MAX_TEXT_LENGTH} ký tự.",
        )

    return analyze_text(text)
