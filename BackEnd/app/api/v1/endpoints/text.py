from fastapi import APIRouter

from app.schemas.text import TextAnalysisRequest, TextAnalysisResponse
from app.services.text_service import analyze_text

router = APIRouter(prefix="/api/v1/text", tags=["text"])


@router.post("/analyze", response_model=TextAnalysisResponse)
def analyze_text_endpoint(payload: TextAnalysisRequest) -> TextAnalysisResponse:
    return analyze_text(payload.text)
