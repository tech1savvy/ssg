from textnode import TextNode, TextType


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
