import unittest

from blocktype import BlockType, block_to_block_type


class TestBlockType(unittest.TestCase):
    def test_paragraph(self):
        self.assertEqual(
            block_to_block_type("This is just a paragraph"),
            BlockType.PARAGRAPH,
        )

    def test_heading(self):
        for prefix in ("# ", "## ", "### ", "#### ", "##### ", "###### "):
            with self.subTest(prefix=prefix):
                self.assertEqual(
                    block_to_block_type(f"{prefix}This is a heading"),
                    BlockType.HEADING,
                )

    def test_heading_requires_space(self):
        self.assertEqual(
            block_to_block_type("#hashtag no space"),
            BlockType.PARAGRAPH,
        )

    def test_code(self):
        block = "```\nprint('hello world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_code_missing_fence(self):
        block = "```\nprint('hello world')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote(self):
        block = "> This is a quote\n> on multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_partial(self):
        block = "> This is a quote\nbut this line is not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- This is a list\n- with items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_partial(self):
        block = "- This is a list\nwith an item missing the dash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_single_item(self):
        block = "1. Only one item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_two_items(self):
        block = "1. First item\n2. Second item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_three_items(self):
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_non_sequential(self):
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
