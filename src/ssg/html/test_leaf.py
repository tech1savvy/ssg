import unittest

from ssg.html.leaf import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_tag_types(self):
        cases = [
            ("p", "Hello, world!", "<p>Hello, world!</p>"),
            ("b", "bold", "<b>bold</b>"),
            ("i", "italic", "<i>italic</i>"),
            ("em", "emphasized", "<em>emphasized</em>"),
            ("strong", "important", "<strong>important</strong>"),
            ("code", "print('hello')", "<code>print('hello')</code>"),
            ("pre", "preformatted text", "<pre>preformatted text</pre>"),
            ("h1", "My heading", "<h1>My heading</h1>"),
            ("h2", "My subheading", "<h2>My subheading</h2>"),
            ("div", "block", "<div>block</div>"),
            ("span", "inline", "<span>inline</span>"),
            ("li", "list item", "<li>list item</li>"),
        ]
        for tag, value, expected in cases:
            with self.subTest(tag=tag):
                node = LeafNode(tag, value)
                self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_void_elements(self):
        cases = [
            ("br", "<br></br>"),
            ("hr", "<hr></hr>"),
        ]
        for tag, expected in cases:
            with self.subTest(tag=tag):
                node = LeafNode(tag, "")
                self.assertEqual(node.to_html(), expected)

    def test_leaf_to_html_none_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_empty_value(self):
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_to_html_none_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_no_props(self):
        node = LeafNode("p", "Hello, world!", props={})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", props={"src": "cat.jpg", "alt": "A cat"})
        self.assertEqual(node.to_html(), '<img src="cat.jpg" alt="A cat"></img>')

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Boot.dev", props={"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Boot.dev</a>')

    def test_leaf_to_html_multiple_props(self):
        node = LeafNode(
            "a",
            "Boot.dev",
            props={"href": "https://www.boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev" target="_blank">Boot.dev</a>',
        )

    def test_repr(self):
        node = LeafNode("p", "Hello, world!", props={"class": "primary"})
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, Hello, world!, {'class': 'primary'})",
        )


if __name__ == "__main__":
    unittest.main()
