from pydantic import BaseModel, Field

MAX_TEXT_LENGTH = 100_000


class TextAnalysisRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=MAX_TEXT_LENGTH,
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


class ParagraphBlock(BaseModel):
    block_id: str
    block_index: int = Field(ge=0)
    source_start: int = Field(ge=0)
    source_end: int = Field(ge=0)
    text: str
    separator_after: str
    word_count: int = Field(ge=0)


class TextAnalysisResponse(BaseModel):
    statistics: TextStatistics
    total_word_count: int = Field(ge=0)
    paragraph_count: int = Field(ge=0)
    paragraphs: list[ParagraphBlock]
    has_issues: bool
    issues: list[TextIssue]
    normalized_text: str
