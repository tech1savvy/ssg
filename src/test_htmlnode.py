import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            tag="a",
            value="Boot.dev",
            props={"href": "https://www.boot.dev", "target": "_blank"},
        )
        props_str = node.props_to_html()
        self.assertEqual(props_str, ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "Hello, world!", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
