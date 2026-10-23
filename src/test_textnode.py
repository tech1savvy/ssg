import unittest

from text_textnode_html import text_node_to_html_node, text_to_textnodes
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_text_node_to_html_node(self):
        cases = [
            (TextType.TEXT, "plain text", None, None, "plain text", None),
            (TextType.BOLD, "bold", None, "b", "bold", None),
            (TextType.ITALIC, "italic", None, "i", "italic", None),
            (TextType.CODE, "code", None, "code", "code", None),
            (
                TextType.LINK,
                "link",
                "https://boot.dev",
                "a",
                "link",
                {"href": "https://boot.dev"},
            ),
            (
                TextType.IMAGE,
                "alt text",
                "cat.jpg",
                "img",
                "",
                {"src": "cat.jpg", "alt": "alt text"},
            ),
        ]
        for text_type, text, url, tag, value, props in cases:
            with self.subTest(text_type=text_type):
                html_node = text_node_to_html_node(TextNode(text, text_type, url))
                self.assertEqual(html_node.tag, tag)
                self.assertEqual(html_node.value, value)
                self.assertEqual(html_node.props, props)

    def test_text_node_to_html_node_to_html(self):
        cases = [
            (TextType.TEXT, "plain text", None, "plain text"),
            (TextType.BOLD, "bold", None, "<b>bold</b>"),
            (TextType.ITALIC, "italic", None, "<i>italic</i>"),
            (TextType.CODE, "code", None, "<code>code</code>"),
            (
                TextType.LINK,
                "link",
                "https://boot.dev",
                '<a href="https://boot.dev">link</a>',
            ),
            (
                TextType.IMAGE,
                "alt text",
                "cat.jpg",
                '<img src="cat.jpg" alt="alt text"></img>',
            ),
        ]
        for text_type, text, url, expected in cases:
            with self.subTest(text_type=text_type):
                html_node = text_node_to_html_node(TextNode(text, text_type, url))
                self.assertEqual(html_node.to_html(), expected)

    def test_link_without_url(self):
        html_node = text_node_to_html_node(TextNode("link", TextType.LINK))
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link")
        self.assertEqual(html_node.props, {"href": ""})

    def test_image_without_url(self):
        html_node = text_node_to_html_node(TextNode("alt text", TextType.IMAGE))
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "", "alt": "alt text"})

    def test_text_ignores_url(self):
        html_node = text_node_to_html_node(
            TextNode("plain text", TextType.TEXT, "https://boot.dev")
        )
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "plain text")
        self.assertEqual(html_node.props, None)

    def test_invalid_text_type(self):
        for invalid_type in ["bold", None, 42]:
            with self.subTest(text_type=invalid_type), self.assertRaises(TypeError):
                text_node_to_html_node(TextNode("text", invalid_type))

    def test_empty_text(self):
        html_node = text_node_to_html_node(TextNode("", TextType.TEXT))
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), "")

    def test_special_characters_are_not_escaped(self):
        text = "a < b & c > d"
        html_node = text_node_to_html_node(TextNode(text, TextType.TEXT))
        self.assertEqual(html_node.value, text)

    def test_whitespace_and_unicode_preserved(self):
        text = "  line one\n\tline two — café  "
        html_node = text_node_to_html_node(TextNode(text, TextType.TEXT))
        self.assertEqual(html_node.value, text)

    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("This is a text node", TextType.LINK, "www.boot.dev")
        node2 = TextNode("This is a text node", TextType.LINK, "www.example.com")
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, TextNode("This is a text node", TextType.LINK))

    def test_not_eq_other_type(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertNotEqual(node, "This is a text node")
        self.assertNotEqual(node, None)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "www.boot.dev")
        self.assertEqual(
            node.__repr__(),
            "TextNode(This is a text node, bold, www.boot.dev)",
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
