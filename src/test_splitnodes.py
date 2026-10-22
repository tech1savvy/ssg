import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_code_block_delimitor(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold_delimitor(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_italic_delimitor(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_missing_closing_delimitor(self):
        node = TextNode(
            "This is text with a missing closing `code block delimitor", TextType.TEXT
        )
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_multi_delimitor_text(self):
        node = TextNode("This is text with a **bold** and _italic_ word", TextType.TEXT)
        first_pass = split_nodes_delimiter([node], "_", TextType.ITALIC)
        second_pass = split_nodes_delimiter(first_pass, "**", TextType.BOLD)
        self.assertEqual(
            second_pass,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
