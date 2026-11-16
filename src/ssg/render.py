from ssg.html.leaf import LeafNode
from ssg.html.node import HTMLNode
from ssg.html.parent import ParentNode
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
from ssg.markdown.inline import InlineNode, InlineType, parse_inline


def render_markdown(markdown: str) -> ParentNode:
    children = []
    for block in split_blocks(markdown):
        node = render_block_node(block)
        if node is not None:
            children.append(node)
    return ParentNode("html", children)


def render_inline(text: str) -> list[HTMLNode]:
    return [render_inline_node(node) for node in parse_inline(text)]


def render_block_node(block: str) -> HTMLNode | None:
    block_type = classify_block(block)

    # Heading
    if block_type == BlockType.HEADING:
        level, text = extract_heading(block)
        return ParentNode(f"h{level}", render_inline(text))

    # Code
    if block_type == BlockType.CODE:
        code = extract_code(block)
        return ParentNode("pre", [ParentNode("code", [LeafNode(None, code)])])

    # Paragraph
    if block_type == BlockType.PARAGRAPH:
        return ParentNode("p", render_inline(block))

    # Quote
    if block_type == BlockType.QUOTE:
        quote = extract_quote(block)
        return ParentNode("blockquote", render_inline(quote))

    # Unordered Lists
    if block_type == BlockType.UNORDERED_LIST:
        items = extract_unordered_list_items(block)
        return ParentNode(
            "ul", [ParentNode("li", render_inline(item)) for item in items]
        )

    # Ordered Lists
    if block_type == BlockType.ORDERED_LIST:
        items = extract_ordered_list_items(block)
        return ParentNode(
            "ol", [ParentNode("li", render_inline(item)) for item in items]
        )

    return None


def render_inline_node(inline_node: InlineNode) -> LeafNode:
    if inline_node.inline_type == InlineType.TEXT:
        return LeafNode(tag=None, value=inline_node.text)
    elif inline_node.inline_type == InlineType.BOLD:
        return LeafNode(tag="b", value=inline_node.text)

    elif inline_node.inline_type == InlineType.ITALIC:
        return LeafNode(tag="i", value=inline_node.text)

    elif inline_node.inline_type == InlineType.CODE:
        return LeafNode(tag="code", value=inline_node.text)

    elif inline_node.inline_type == InlineType.LINK:
        url = inline_node.url
        if url is None:
            url = ""
        return LeafNode(tag="a", value=inline_node.text, props={"href": url})

    elif inline_node.inline_type == InlineType.IMAGE:
        url = inline_node.url
        if url is None:
            url = ""
        return LeafNode(
            tag="img", value="", props={"src": url, "alt": inline_node.text}
        )
    else:
        raise TypeError("Invalid InlineType")
