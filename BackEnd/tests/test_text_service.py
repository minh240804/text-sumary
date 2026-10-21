import unittest

from app.services.text_service import (
    analyze_text,
    count_words,
    split_paragraphs_with_offsets,
)


class AnalyzeTextTests(unittest.TestCase):
    def test_counts_clean_text(self) -> None:
        result = analyze_text("Xin chào\nViệt Nam")

        self.assertEqual(result.statistics.character_count, 17)
        self.assertEqual(result.statistics.word_count, 4)
        self.assertEqual(result.total_word_count, 4)
        self.assertEqual(result.statistics.line_count, 2)
        self.assertEqual(result.paragraph_count, 1)
        self.assertEqual(result.paragraphs[0].text, "Xin chào\nViệt Nam")
        self.assertFalse(result.has_issues)
        self.assertEqual(result.normalized_text, "Xin chào\nViệt Nam")

    def test_reports_and_normalizes_common_whitespace_issues(self) -> None:
        result = analyze_text("  Xin   chào  \n\n\nViệt Nam")

        issue_codes = {issue.code for issue in result.issues}
        self.assertTrue(result.has_issues)
        self.assertIn("multiple_whitespace", issue_codes)
        self.assertIn("leading_whitespace", issue_codes)
        self.assertIn("trailing_whitespace", issue_codes)
        self.assertIn("multiple_blank_lines", issue_codes)
        self.assertEqual(result.normalized_text, "Xin chào\n\nViệt Nam")

    def test_counts_whitespace_separated_words(self) -> None:
        self.assertEqual(count_words("  một\thai\nba  "), 3)

    def test_splits_paragraphs_and_preserves_source_offsets(self) -> None:
        source = "Đoạn một có ba.\n\nĐoạn hai có bốn từ.\r\n \t\r\nĐoạn ba."

        blocks = split_paragraphs_with_offsets(source)

        self.assertEqual([block.block_id for block in blocks], ["b0001", "b0002", "b0003"])
        self.assertEqual([block.block_index for block in blocks], [0, 1, 2])
        self.assertEqual([block.word_count for block in blocks], [4, 5, 2])
        self.assertEqual(blocks[0].separator_after, "\n\n")
        self.assertEqual(blocks[1].separator_after, "\r\n \t\r\n")
        self.assertEqual(blocks[2].separator_after, "")

        for block in blocks:
            self.assertEqual(
                source[block.source_start : block.source_end],
                block.text,
            )

    def test_analysis_total_matches_sum_of_paragraph_words(self) -> None:
        result = analyze_text("Đoạn thứ nhất.\n\nĐoạn thứ hai có thêm từ.")

        self.assertEqual(result.total_word_count, 9)
        self.assertEqual(
            result.total_word_count,
            sum(paragraph.word_count for paragraph in result.paragraphs),
        )


if __name__ == "__main__":
    unittest.main()
