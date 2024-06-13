from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

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
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list
    
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list
    
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_ordered_list
    
    return block_type_paragraph

def text_to_html(text: str):
    textnodes = text_to_textnodes(text)
    children = list(map(text_node_to_html_node, textnodes))
    return children

def heading_block_to_html(block: str):
    i = 0
    for ch in block:
        if ch != "#" or i > 6:
            break
        i += 1
    if i > 6:
        raise Exception("Heading level greater than 6")
    children = text_to_html(block[i + 1:])
    return ParentNode(f"h{i}", children)

def p_block_to_html(block: str):
    lines = block.split("\n")
    text = " ".join(lines)
    children = text_to_html(text)
    return ParentNode("p", children)

def quote_block_to_html(block: str):
    lines = block.split("\n")
    striped_lines = list(map(lambda line: line.lstrip("> "), lines))
    text = " ".join(striped_lines)
    children = text_to_html(text)
    return ParentNode("blockquote", children)

def code_block_to_html(block: str):
    block = block[3: -4]
    children = text_to_html(block)
    code_block = ParentNode("code", children)
    return ParentNode("pre", [code_block])

def ul_block_to_html(block: str):
    def process_li(line: str):
        line = line.lstrip("*- ")
        li_children = text_to_html(line)
        return ParentNode("li", li_children)
     
    lines = block.split("\n")
    list_items = list(map(process_li, lines))
    return ParentNode("ul", list_items)

def ol_block_to_html(block: str):
    def process_li(line: str):
        index = line.find(". ")
        li_children = text_to_html(line[index + 2:])
        return ParentNode("li", li_children)

    lines = block.split("\n")
    list_items = list(map(process_li, lines))
    return ParentNode("ol", list_items)

def markdown_to_html_node(markdown: str):
    children = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == block_type_paragraph:
            children.append(p_block_to_html(block))
        elif block_type == block_type_heading:
            children.append(heading_block_to_html(block))
        elif block_type == block_type_quote:
            children.append(quote_block_to_html(block))
        elif block_type == block_type_code:
            children.append(code_block_to_html(block))
        elif block_type == block_type_unordered_list:
            children.append(ul_block_to_html(block))
        elif block_type == block_type_ordered_list:
            children.append(ol_block_to_html(block))
        else:
            raise ValueError(f"{block_type} block type does not exist")

    return ParentNode("div", children)


