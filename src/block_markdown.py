import re

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered list"
block_type_ordered_list = "ordered list"

def markdown_to_blocks(markdown: str):
    blocks = []
    for block in markdown.split("\n\n"):
        if block != "":
            blocks.append(block.strip())

    return blocks

def block_to_block_type(block: str):
    if (block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")):
        return block_type_heading
    
    lines = block.split("\n")
    
    if len(lines) > 1 and lines[0] == "```" and lines[-1] == "```":
        return block_type_code
    
    if block.startswith(">"):
        for line in block.split("\n"):
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    
    if block.startswith("* "):
        for line in block.split("\n"):
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    
    if block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    
    if block.startswith("1. "):
        i = 1
        for line in block.split("\n"):
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    
    return block_type_paragraph