import unittest

from app.services.text_service import analyze_text


class AnalyzeTextTests(unittest.TestCase):
    def test_counts_clean_text(self) -> None:
        result = analyze_text("Xin chào\nViệt Nam")

        self.assertEqual(result.statistics.character_count, 17)
        self.assertEqual(result.statistics.word_count, 4)
        self.assertEqual(result.statistics.line_count, 2)
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


if __name__ == "__main__":
    unittest.main()
