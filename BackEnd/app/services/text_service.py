import re

from app.schemas.text import (
    ParagraphBlock,
    TextAnalysisResponse,
    TextIssue,
    TextStatistics,
)

MULTIPLE_HORIZONTAL_WHITESPACE = re.compile(r"[ \t]{2,}")
LEADING_WHITESPACE = re.compile(r"(?m)^[ \t]+")
TRAILING_WHITESPACE = re.compile(r"(?m)[ \t]+$")
MULTIPLE_BLANK_LINES = re.compile(r"\n[ \t]*\n(?:[ \t]*\n)+")
PARAGRAPH_SEPARATOR = re.compile(r"(?:\r?\n[ \t]*){2,}")


def count_words(text: str) -> int:
    """Count whitespace-separated units in text."""
    return len(text.split())


def split_paragraphs_with_offsets(source_text: str) -> list[ParagraphBlock]:
    """Split paragraphs and retain their exact ranges in the source text."""
    blocks: list[ParagraphBlock] = []
    cursor = 0

    for match in PARAGRAPH_SEPARATOR.finditer(source_text):
        paragraph = source_text[cursor : match.start()]

        if paragraph.strip():
            blocks.append(
                ParagraphBlock(
                    block_id=f"b{len(blocks) + 1:04d}",
                    block_index=len(blocks),
                    source_start=cursor,
                    source_end=match.start(),
                    text=paragraph,
                    separator_after=match.group(),
                    word_count=count_words(paragraph),
                )
            )

        cursor = match.end()

    paragraph = source_text[cursor:]
    if paragraph.strip():
        blocks.append(
            ParagraphBlock(
                block_id=f"b{len(blocks) + 1:04d}",
                block_index=len(blocks),
                source_start=cursor,
                source_end=len(source_text),
                text=paragraph,
                separator_after="",
                word_count=count_words(paragraph),
            )
        )

    return blocks


def analyze_text(text: str) -> TextAnalysisResponse:
    issues = _find_issues(text)
    paragraphs = split_paragraphs_with_offsets(text)
    total_word_count = count_words(text)

    return TextAnalysisResponse(
        statistics=TextStatistics(
            character_count=len(text),
            character_count_without_whitespace=sum(
                not character.isspace() for character in text
            ),
            word_count=total_word_count,
            line_count=text.count("\n") + 1,
            space_count=text.count(" "),
        ),
        total_word_count=total_word_count,
        paragraph_count=len(paragraphs),
        paragraphs=paragraphs,
        has_issues=bool(issues),
        issues=issues,
        normalized_text=_normalize_text(text),
    )


def _find_issues(text: str) -> list[TextIssue]:
    checks = (
        (
            "multiple_whitespace",
            "Văn bản có nhiều khoảng trắng liên tiếp.",
            MULTIPLE_HORIZONTAL_WHITESPACE,
        ),
        (
            "leading_whitespace",
            "Một hoặc nhiều dòng bắt đầu bằng khoảng trắng.",
            LEADING_WHITESPACE,
        ),
        (
            "trailing_whitespace",
            "Một hoặc nhiều dòng kết thúc bằng khoảng trắng.",
            TRAILING_WHITESPACE,
        ),
        (
            "multiple_blank_lines",
            "Văn bản có nhiều dòng trống liên tiếp.",
            MULTIPLE_BLANK_LINES,
        ),
    )

    issues = []
    for code, message, pattern in checks:
        occurrences = len(pattern.findall(text))
        if occurrences:
            issues.append(
                TextIssue(
                    code=code,
                    message=message,
                    occurrences=occurrences,
                )
            )

    return issues


def _normalize_text(text: str) -> str:
    normalized_lines = [
        re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")
    ]
    normalized_text = "\n".join(normalized_lines)
    normalized_text = re.sub(r"\n{3,}", "\n\n", normalized_text)
    return normalized_text.strip()
