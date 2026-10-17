from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=10_000,
        description="Văn bản cần thống kê và kiểm tra.",
    )


class TextIssue(BaseModel):
    code: str
    message: str
    occurrences: int = Field(ge=1)


class TextStatistics(BaseModel):
    character_count: int = Field(ge=0)
    character_count_without_whitespace: int = Field(ge=0)
    word_count: int = Field(ge=0)
    line_count: int = Field(ge=1)
    space_count: int = Field(ge=0)


class TextAnalysisResponse(BaseModel):
    statistics: TextStatistics
    has_issues: bool
    issues: list[TextIssue]
    normalized_text: str
