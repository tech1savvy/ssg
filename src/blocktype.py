from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
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
