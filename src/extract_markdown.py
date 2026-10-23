import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_blocks(text: str) -> list[str]:
    blocks = []
    unfiltered_blocks = text.split("\n\n")
    for block in unfiltered_blocks:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks
