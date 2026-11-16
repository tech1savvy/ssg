from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def classify_block(block: str) -> BlockType:
    # Heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType("heading")

    # Code
    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType("code")

    lines = block.split("\n")

    # Quote
    if lines[0].startswith(">"):
        isQuoteBlock = True
        for line in lines:
            if not line.startswith(">"):
                isQuoteBlock = False
        if isQuoteBlock:
            return BlockType("quote")

    # Unordered List
    if lines[0].startswith("- "):
        isUnorderedList = True
        for line in lines:
            if not line.startswith("- "):
                isUnorderedList = False
        if isUnorderedList:
            return BlockType("unordered_list")

    # Ordered List
    count = 2
    if lines[0].startswith("1. "):
        isOrderedList = True
        for i in range(1, len(lines)):
            if not lines[i].startswith(f"{count}. "):
                isOrderedList = False
            count += 1
        if isOrderedList:
            return BlockType("ordered_list")

    return BlockType("paragraph")


def split_blocks(text: str) -> list[str]:
    blocks = []
    unfiltered_blocks = text.split("\n\n")
    for block in unfiltered_blocks:
        if block == "":
            continue
        blocks.append(block.strip())
    return blocks


def extract_heading(block: str) -> tuple[int, str]:
    parts = block.split(maxsplit=1)
    level = parts[0].count("#")
    text = parts[1] if len(parts) > 1 else ""
    return level, text


def extract_code(block: str) -> str:
    return block.removeprefix("```\n").removesuffix("\n```")


def extract_quote(block: str) -> str:
    lines = block.split("\n")
    cleaned_lines = [line.lstrip("> ") for line in lines]
    return "\n".join(cleaned_lines)


def extract_unordered_list_items(block: str) -> list[str]:
    lines = block.split("\n")
    cleaned_lines = [line.lstrip("- ") for line in lines]
    return cleaned_lines


def extract_ordered_list_items(block: str) -> list[str]:
    lines = block.split("\n")
    cleaned_lines = [line.split(". ")[1] for line in lines]
    return cleaned_lines
