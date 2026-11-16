import unittest

from ssg.generate import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_title(self):
        self.assertEqual(extract_title("# My Title"), "My Title")

    def test_title_without_leading_content(self):
        markdown = "# My Title\n\nSome paragraph."
        self.assertEqual(extract_title(markdown), "My Title")

    def test_title_ignores_trailing_content(self):
        markdown = "# First Heading\n\n## Second Heading\n\nParagraph."
        self.assertEqual(extract_title(markdown), "First Heading")

    def test_title_with_punctuation(self):
        self.assertEqual(extract_title("# Hello, World!"), "Hello, World!")

    def test_missing_h1_header(self):
        with self.assertRaises(ValueError):
            extract_title("## Not a title")

    def test_paragraph_before_h1(self):
        markdown = "Some paragraph.\n\n# My Title"
        with self.assertRaises(ValueError):
            extract_title(markdown)

    def test_no_heading(self):
        with self.assertRaises(ValueError):
            extract_title("Just a paragraph")


if __name__ == "__main__":
    unittest.main()
