import unittest

from ssg.markdown.inline import (
    InlineNode,
    InlineType,
    extract_images,
    extract_links,
    parse_inline,
    split_by_delimiter,
    split_by_image,
    split_by_link,
)


class TestInlineNode(unittest.TestCase):
    def test_eq(self):
        node = InlineNode("This is a text node", InlineType.BOLD)
        node2 = InlineNode("This is a text node", InlineType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = InlineNode("This is a text node", InlineType.BOLD)
        node2 = InlineNode("This is another text node", InlineType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_inline_type(self):
        node = InlineNode("This is a text node", InlineType.ITALIC)
        node2 = InlineNode("This is a text node", InlineType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = InlineNode("This is a text node", InlineType.LINK, "www.boot.dev")
        node2 = InlineNode("This is a text node", InlineType.LINK, "www.example.com")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, InlineNode("This is a text node", InlineType.LINK))

    def test_not_eq_other_type(self):
        node = InlineNode("This is a text node", InlineType.TEXT)
        self.assertNotEqual(node, "This is a text node")
        self.assertNotEqual(node, None)

    def test_repr(self):
        node = InlineNode("This is a text node", InlineType.BOLD, "www.boot.dev")
        self.assertEqual(
            node.__repr__(),
            "InlineNode(This is a text node, bold, www.boot.dev)",
        )


class TestSplitNodes(unittest.TestCase):
    def test_code_block_delimitor(self):
        node = InlineNode("This is text with a `code block` word", InlineType.TEXT)
        new_nodes = split_by_delimiter([node], "`", InlineType.CODE)
        self.assertEqual(
            new_nodes,
            [
                InlineNode("This is text with a ", InlineType.TEXT),
                InlineNode("code block", InlineType.CODE),
                InlineNode(" word", InlineType.TEXT),
            ],
        )

    def test_bold_delimitor(self):
        node = InlineNode("This is text with a **bold** word", InlineType.TEXT)
        new_nodes = split_by_delimiter([node], "**", InlineType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                InlineNode("This is text with a ", InlineType.TEXT),
                InlineNode("bold", InlineType.BOLD),
                InlineNode(" word", InlineType.TEXT),
            ],
        )

    def test_italic_delimitor(self):
        node = InlineNode("This is text with an _italic_ word", InlineType.TEXT)
        new_nodes = split_by_delimiter([node], "_", InlineType.ITALIC)
        self.assertEqual(
            new_nodes,
            [
                InlineNode("This is text with an ", InlineType.TEXT),
                InlineNode("italic", InlineType.ITALIC),
                InlineNode(" word", InlineType.TEXT),
            ],
        )

    def test_missing_closing_delimitor(self):
        node = InlineNode(
            "This is text with a missing closing `code block delimitor", InlineType.TEXT
        )
        with self.assertRaises(ValueError):
            split_by_delimiter([node], "`", InlineType.CODE)

    def test_multi_delimitor_text(self):
        node = InlineNode(
            "This is text with a **bold** and _italic_ word", InlineType.TEXT
        )
        first_pass = split_by_delimiter([node], "_", InlineType.ITALIC)
        second_pass = split_by_delimiter(first_pass, "**", InlineType.BOLD)
        self.assertEqual(
            second_pass,
            [
                InlineNode("This is text with a ", InlineType.TEXT),
                InlineNode("bold", InlineType.BOLD),
                InlineNode(" and ", InlineType.TEXT),
                InlineNode("italic", InlineType.ITALIC),
                InlineNode(" word", InlineType.TEXT),
            ],
        )

    def test_split_image(self):
        node = InlineNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            InlineType.TEXT,
        )
        new_nodes = split_by_image([node])
        self.assertListEqual(
            [
                InlineNode("This is text with an ", InlineType.TEXT),
                InlineNode(
                    "image", InlineType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = InlineNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            InlineType.TEXT,
        )
        new_nodes = split_by_image([node])
        self.assertListEqual(
            new_nodes,
            [
                InlineNode("This is text with an ", InlineType.TEXT),
                InlineNode(
                    "image", InlineType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"
                ),
                InlineNode(" and another ", InlineType.TEXT),
                InlineNode(
                    "second image", InlineType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
        )

    def test_split_image_single(self):
        node = InlineNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            InlineType.TEXT,
        )
        new_nodes = split_by_image([node])
        self.assertListEqual(
            [
                InlineNode(
                    "image", InlineType.IMAGE, "https://www.example.COM/IMAGE.PNG"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = InlineNode(
            "This is text with an [link](https://www.boot.dev/) and another [second link](https://regexr.com)",
            InlineType.TEXT,
        )
        new_nodes = split_by_link([node])
        self.assertListEqual(
            new_nodes,
            [
                InlineNode("This is text with an ", InlineType.TEXT),
                InlineNode("link", InlineType.LINK, "https://www.boot.dev/"),
                InlineNode(" and another ", InlineType.TEXT),
                InlineNode("second link", InlineType.LINK, "https://regexr.com"),
            ],
        )


class TestExtractInline(unittest.TestCase):
    def test_extract_images(self):
        matches = extract_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_links(self):
        matches = extract_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )


class TestParseInline(unittest.TestCase):
    def test_parse_inline(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            parse_inline(text),
            [
                InlineNode("This is ", InlineType.TEXT),
                InlineNode("text", InlineType.BOLD),
                InlineNode(" with an ", InlineType.TEXT),
                InlineNode("italic", InlineType.ITALIC),
                InlineNode(" word and a ", InlineType.TEXT),
                InlineNode("code block", InlineType.CODE),
                InlineNode(" and an ", InlineType.TEXT),
                InlineNode(
                    "obi wan image",
                    InlineType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                InlineNode(" and a ", InlineType.TEXT),
                InlineNode("link", InlineType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
