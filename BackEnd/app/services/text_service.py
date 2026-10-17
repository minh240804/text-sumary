import re

from app.schemas.text import TextAnalysisResponse, TextIssue, TextStatistics

MULTIPLE_HORIZONTAL_WHITESPACE = re.compile(r"[ \t]{2,}")
LEADING_WHITESPACE = re.compile(r"(?m)^[ \t]+")
TRAILING_WHITESPACE = re.compile(r"(?m)[ \t]+$")
MULTIPLE_BLANK_LINES = re.compile(r"\n[ \t]*\n(?:[ \t]*\n)+")
WORD = re.compile(r"\S+")


def analyze_text(text: str) -> TextAnalysisResponse:
    issues = _find_issues(text)

    return TextAnalysisResponse(
        statistics=TextStatistics(
            character_count=len(text),
            character_count_without_whitespace=sum(
                not character.isspace() for character in text
            ),
            word_count=len(WORD.findall(text)),
            line_count=text.count("\n") + 1,
            space_count=text.count(" "),
        ),
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
