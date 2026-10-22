from textnode import TextNode, TextType
from extract_markdown import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    split_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue

        # Split by delimiter
        sections = node.text.split(delimiter)

        # Closing delimiter not found
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown")

        # Covert to TextNodes
        for i in range(len(sections)):
            # TextType.TEXT
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            # Identify TextType from delimiter
            else:
                split_nodes.append(TextNode(sections[i], text_type))
    return split_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        images = extract_markdown_images(node.text)

        pending_section = node.text
        for image_alt_text, image_url in images:
            sections = pending_section.split(f"![{image_alt_text}]({image_url})", 1)

            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT, None))
            split_nodes.append(TextNode(image_alt_text, TextType.IMAGE, image_url))
            pending_section = sections[1]
        if pending_section != "":
            split_nodes.append(TextNode(pending_section, TextType.TEXT, None))
    return split_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            split_nodes.append(node)
            continue
        links = extract_markdown_links(node.text)

        pending_section = node.text
        for link_text, link_url in links:
            sections = pending_section.split(f"[{link_text}]({link_url})", 1)

            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT, None))

            split_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            pending_section = sections[1]
        if pending_section != "":
            split_nodes.append(TextNode(pending_section, TextType.TEXT, None))
    return split_nodes
