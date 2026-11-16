import re
from enum import Enum


class InlineType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class InlineNode:
    def __init__(
        self, text: str, inline_type: InlineType, url: str | None = None
    ) -> None:
        self.text = text
        self.inline_type = inline_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, InlineNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.inline_type == other.inline_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"InlineNode({self.text}, {self.inline_type.value}, {self.url})"


def extract_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_by_delimiter(
    old_nodes: list[InlineNode], delimiter: str, inline_type: InlineType
) -> list[InlineNode]:
    split_nodes = []

    for node in old_nodes:
        if node.inline_type != InlineType.TEXT:
            split_nodes.append(node)
            continue

        # Split by delimiter
        sections = node.text.split(delimiter)

        # Closing delimiter not found
        if len(sections) % 2 == 0:
            raise ValueError("Invalid Markdown")

        # Covert to InlineNodes
        for i in range(len(sections)):
            # InlineType.TEXT
            if i % 2 == 0:
                split_nodes.append(InlineNode(sections[i], InlineType.TEXT))
            # Identify InlineType from delimiter
            else:
                split_nodes.append(InlineNode(sections[i], inline_type))
    return split_nodes


def split_by_image(old_nodes: list[InlineNode]) -> list[InlineNode]:
    split_nodes = []
    for node in old_nodes:
        if node.inline_type != InlineType.TEXT:
            split_nodes.append(node)
            continue
        images = extract_images(node.text)

        pending_section = node.text
        for image_alt_text, image_url in images:
            sections = pending_section.split(f"![{image_alt_text}]({image_url})", 1)

            if sections[0] != "":
                split_nodes.append(InlineNode(sections[0], InlineType.TEXT, None))
            split_nodes.append(InlineNode(image_alt_text, InlineType.IMAGE, image_url))
            pending_section = sections[1]
        if pending_section != "":
            split_nodes.append(InlineNode(pending_section, InlineType.TEXT, None))
    return split_nodes


def split_by_link(old_nodes: list[InlineNode]) -> list[InlineNode]:
    split_nodes = []
    for node in old_nodes:
        if node.inline_type != InlineType.TEXT:
            split_nodes.append(node)
            continue
        links = extract_links(node.text)

        pending_section = node.text
        for link_text, link_url in links:
            sections = pending_section.split(f"[{link_text}]({link_url})", 1)

            if sections[0] != "":
                split_nodes.append(InlineNode(sections[0], InlineType.TEXT, None))

            split_nodes.append(InlineNode(link_text, InlineType.LINK, link_url))
            pending_section = sections[1]
        if pending_section != "":
            split_nodes.append(InlineNode(pending_section, InlineType.TEXT, None))
    return split_nodes


def parse_inline(text: str):
    return split_by_link(
        split_by_image(
            split_by_delimiter(
                split_by_delimiter(
                    split_by_delimiter(
                        [InlineNode(text, InlineType.TEXT, None)], "**", InlineType.BOLD
                    ),
                    "_",
                    InlineType.ITALIC,
                ),
                "`",
                InlineType.CODE,
            )
        )
    )
