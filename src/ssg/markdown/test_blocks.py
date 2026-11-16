import unittest

from ssg.markdown.blocks import (
    BlockType,
    classify_block,
    extract_code,
    extract_heading,
    extract_ordered_list_items,
    extract_quote,
    extract_unordered_list_items,
    split_blocks,
)


class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(
            classify_block("This is just a paragraph"),
            BlockType.PARAGRAPH,
        )

    def test_heading(self):
        for prefix in ("# ", "## ", "### ", "#### ", "##### ", "###### "):
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    classify_block(f"{prefix}This is a heading"),
                    BlockType.HEADING,
                )

    def test_heading_requires_space(self):
        self.assertEqual(
            classify_block("#hashtag no space"),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        block = "```\nprint('hello world')\n```"
        self.assertEqual(classify_block(block), BlockType.CODE)

    def test_code_missing_fence(self):
        block = "```\nprint('hello world')"
        self.assertEqual(classify_block(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> This is a quote\n> on multiple lines"
        self.assertEqual(classify_block(block), BlockType.QUOTE)

    def test_quote_partial(self):
        block = "> This is a quote\nbut this line is not"
        self.assertEqual(classify_block(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- This is a list\n- with items"
        self.assertEqual(classify_block(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_partial(self):
        block = "- This is a list\nwith an item missing the dash"
        self.assertEqual(classify_block(block), BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        block = "1. Only one item"
        self.assertEqual(classify_block(block), BlockType.ORDERED_LIST)

    def test_ordered_list_two_items(self):
        block = "1. First item\n2. Second item"
        self.assertEqual(classify_block(block), BlockType.ORDERED_LIST)

    def test_ordered_list_three_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(classify_block(block), BlockType.ORDERED_LIST)

    def test_ordered_list_non_sequential(self):
        block = "1. First item\n3. Third item"
        self.assertEqual(classify_block(block), BlockType.PARAGRAPH)


class TestSplitBlocks(unittest.TestCase):
    def test_split_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = split_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_split_blocks_multiple_newlines(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line



- This is a list
- with items
"""
        blocks = split_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestExtractHeading(unittest.TestCase):
    def test_heading_levels(self):
        for level in range(1, 7):
            with self.subTest(level=level):
                block = f"{'#' * level} Chapter {level}"
                self.assertEqual(extract_heading(block), (level, f"Chapter {level}"))

    def test_multi_word_text(self):
        self.assertEqual(
            extract_heading("## Getting Started Today"), (2, "Getting Started Today")
        )


class TestExtractCode(unittest.TestCase):
    def test_single_line(self):
        block = "```\nprint('hello world')\n```"
        self.assertEqual(extract_code(block), "print('hello world')")

    def test_multiple_lines(self):
        block = "```\ndef main():\n    return 42\n```"
        self.assertEqual(extract_code(block), "def main():\n    return 42")


class TestExtractQuote(unittest.TestCase):
    def test_single_line(self):
        self.assertEqual(extract_quote("> To be or not to be"), "To be or not to be")

    def test_multiple_lines(self):
        block = "> This is a quote\n> on multiple lines"
        self.assertEqual(extract_quote(block), "This is a quote\non multiple lines")

    def test_marker_without_trailing_space(self):
        self.assertEqual(extract_quote(">no space here"), "no space here")


class TestExtractUnorderedListItems(unittest.TestCase):
    def test_items(self):
        block = "- First item\n- Second item\n- Third item"
        self.assertEqual(
            extract_unordered_list_items(block),
            ["First item", "Second item", "Third item"],
        )

    def test_single_item(self):
        self.assertEqual(extract_unordered_list_items("- Only item"), ["Only item"])


class TestExtractOrderedListItems(unittest.TestCase):
    def test_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(
            extract_ordered_list_items(block),
            ["First item", "Second item", "Third item"],
        )

    def test_single_item(self):
        self.assertEqual(extract_ordered_list_items("1. Only one"), ["Only one"])


if __name__ == "__main__":
    unittest.main()
