import unittest

from ssg.html.parent import ParentNode
from ssg.markdown.inline import InlineNode, InlineType
from ssg.render import (
    render_block_node,
    render_inline,
    render_inline_node,
    render_markdown,
)


class TestRenderInlineNode(unittest.TestCase):
    def test_render_inline_node(self):
        cases = [
            (InlineType.TEXT, "plain text", None, None, "plain text", None),
            (InlineType.BOLD, "bold", None, "b", "bold", None),
            (InlineType.ITALIC, "italic", None, "i", "italic", None),
            (InlineType.CODE, "code", None, "code", "code", None),
            (
                InlineType.LINK,
                "link",
                "https://boot.dev",
                "a",
                "link",
                {"href": "https://boot.dev"},
            ),
            (
                InlineType.IMAGE,
                "alt text",
                "cat.jpg",
                "img",
                "",
                {"src": "cat.jpg", "alt": "alt text"},
            ),
        ]
        for inline_type, text, url, tag, value, props in cases:
            with self.subTest(inline_type=inline_type):
                html_node = render_inline_node(InlineNode(text, inline_type, url))
                self.assertEqual(html_node.tag, tag)
                self.assertEqual(html_node.value, value)
                self.assertEqual(html_node.props, props)

    def test_render_inline_node_to_html(self):
        cases = [
            (InlineType.TEXT, "plain text", None, "plain text"),
            (InlineType.BOLD, "bold", None, "<b>bold</b>"),
            (InlineType.ITALIC, "italic", None, "<i>italic</i>"),
            (InlineType.CODE, "code", None, "<code>code</code>"),
            (
                InlineType.LINK,
                "link",
                "https://boot.dev",
                '<a href="https://boot.dev">link</a>',
            ),
            (
                InlineType.IMAGE,
                "alt text",
                "cat.jpg",
                '<img src="cat.jpg" alt="alt text"></img>',
            ),
        ]
        for inline_type, text, url, expected in cases:
            with self.subTest(inline_type=inline_type):
                html_node = render_inline_node(InlineNode(text, inline_type, url))
                self.assertEqual(html_node.to_html(), expected)

    def test_link_without_url(self):
        html_node = render_inline_node(InlineNode("link", InlineType.LINK))
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "link")
        self.assertEqual(html_node.props, {"href": ""})

    def test_image_without_url(self):
        html_node = render_inline_node(InlineNode("alt text", InlineType.IMAGE))
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "", "alt": "alt text"})

    def test_text_ignores_url(self):
        html_node = render_inline_node(
            InlineNode("plain text", InlineType.TEXT, "https://boot.dev")
        )
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "plain text")
        self.assertEqual(html_node.props, None)

    def test_invalid_inline_type(self):
        for invalid_type in ["bold", None, 42]:
            with self.subTest(inline_type=invalid_type), self.assertRaises(TypeError):
                render_inline_node(InlineNode("text", invalid_type))

    def test_empty_text(self):
        html_node = render_inline_node(InlineNode("", InlineType.TEXT))
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.to_html(), "")

    def test_special_characters_are_not_escaped(self):
        text = "a < b & c > d"
        html_node = render_inline_node(InlineNode(text, InlineType.TEXT))
        self.assertEqual(html_node.value, text)

    def test_whitespace_and_unicode_preserved(self):
        text = "  line one\n\tline two — café  "
        html_node = render_inline_node(InlineNode(text, InlineType.TEXT))
        self.assertEqual(html_node.value, text)


class TestRenderInline(unittest.TestCase):
    def test_inline_spans_become_html_nodes(self):
        nodes = render_inline("This is **bold** text")
        self.assertEqual(
            "".join(node.to_html() for node in nodes), "This is <b>bold</b> text"
        )

    def test_plain_text(self):
        nodes = render_inline("Just words")
        self.assertEqual("".join(node.to_html() for node in nodes), "Just words")


class TestRenderBlockNode(unittest.TestCase):
    def test_heading(self):
        node = render_block_node("## Hello")
        self.assertEqual(node.to_html(), "<h2>Hello</h2>")

    def test_code(self):
        node = render_block_node("```\nvalue = 1\n```")
        self.assertEqual(node.to_html(), "<pre><code>value = 1</code></pre>")

    def test_paragraph(self):
        node = render_block_node("Just a paragraph")
        self.assertEqual(node.to_html(), "<p>Just a paragraph</p>")

    def test_paragraph_with_inline_formatting(self):
        node = render_block_node("This is **bold** text")
        self.assertEqual(node.to_html(), "<p>This is <b>bold</b> text</p>")

    def test_quote(self):
        node = render_block_node("> hello\n> world")
        self.assertEqual(node.to_html(), "<blockquote>hello\nworld</blockquote>")

    def test_unordered_list(self):
        node = render_block_node("- one\n- two")
        self.assertEqual(node.to_html(), "<ul><li>one</li><li>two</li></ul>")

    def test_unordered_list_with_inline_formatting(self):
        node = render_block_node("- Disney _didn't ruin it_\n- **bold**")
        self.assertEqual(
            node.to_html(),
            "<ul><li>Disney <i>didn't ruin it</i></li><li><b>bold</b></li></ul>",
        )

    def test_ordered_list(self):
        node = render_block_node("1. one\n2. two")
        print(node)
        self.assertEqual(node.to_html(), "<ol><li>one</li><li>two</li></ol>")

    def test_ordered_list_with_inline_formatting(self):
        node = render_block_node("1. _first_\n2. [link](/x)")
        self.assertEqual(
            node.to_html(),
            '<ol><li><i>first</i></li><li><a href="/x">link</a></li></ol>',
        )


class TestRenderMarkdown(unittest.TestCase):
    def test_returns_root_div(self):
        node = render_markdown("# Hello")
        self.assertIsInstance(node, ParentNode)
        self.assertEqual(node.tag, "div")

    def test_empty_markdown(self):
        node = render_markdown("")
        self.assertEqual(node.to_html(), "<div></div>")

    def test_heading_with_level(self):
        node = render_markdown("## Hello")
        self.assertEqual(node.to_html(), "<div><h2>Hello</h2></div>")

    def test_heading_with_inline_formatting(self):
        node = render_markdown("### Hi **there**")
        self.assertEqual(node.to_html(), "<div><h3>Hi <b>there</b></h3></div>")

    def test_code_block(self):
        node = render_markdown("```\nprint('hello world')\n```")
        self.assertEqual(
            node.to_html(),
            "<div><pre><code>print('hello world')</code></pre></div>",
        )

    def test_heading_and_code(self):
        markdown = "# Title\n\n```\nvalue = 1\n```"
        node = render_markdown(markdown)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><pre><code>value = 1</code></pre></div>",
        )

    def test_paragraph(self):
        node = render_markdown("This is **bold** text")
        self.assertEqual(node.to_html(), "<div><p>This is <b>bold</b> text</p></div>")

    def test_large_document(self):
        markdown = (
            "# Title\n\n"
            "Intro with **bold**, _italic_, and `code`.\n\n"
            "> quoted **text**\n"
            "> second line\n\n"
            "- _first_\n"
            "- second\n\n"
            "1. one\n"
            "2. two\n\n"
            "```\n"
            'print("hi")\n'
            "```"
        )
        node = render_markdown(markdown)
        self.assertEqual(
            node.to_html(),
            "<div>"
            "<h1>Title</h1>"
            "<p>Intro with <b>bold</b>, <i>italic</i>, and <code>code</code>.</p>"
            "<blockquote>quoted <b>text</b>\nsecond line</blockquote>"
            "<ul><li><i>first</i></li><li>second</li></ul>"
            "<ol><li>one</li><li>two</li></ol>"
            '<pre><code>print("hi")</code></pre>'
            "</div>",
        )


if __name__ == "__main__":
    unittest.main()
