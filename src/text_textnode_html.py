from leafnode import LeafNode
from splitnodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def text_to_textnodes(text: str):
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text, TextType.TEXT, None)], "**", TextType.BOLD
                    ),
                    "_",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=text_node.text)

    elif text_node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=text_node.text)

    elif text_node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=text_node.text)

    elif text_node.text_type == TextType.LINK:
        url = text_node.url
        if url is None:
            url = ""
        return LeafNode(tag="a", value=text_node.text, props={"href": url})

    elif text_node.text_type == TextType.IMAGE:
        url = text_node.url
        if url is None:
            url = ""
        return LeafNode(tag="img", value="", props={"src": url, "alt": text_node.text})
    else:
        raise TypeError("Invalid TextType")
