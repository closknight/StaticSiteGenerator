import re

from textnode import (
    TextNode,
    text_type_text
)

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: str):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            split_nodes = []
            line = node.text.split(delimiter)
            is_text = True
            #Test for  in begining & end 
            for part in line:
                if part != "":
                    split_nodes.append(TextNode(part, text_type_text if is_text else text_type))
                is_text = not is_text
            if is_text:
                raise Exception("Delimeter is not closed")
            new_nodes.extend(split_nodes)

        else:
            new_nodes.append(node)

    return new_nodes

def extract_markdown_images(text: str):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text:str):
    return re.findall(r"\[(.*?)\]\((.*?)\)",text)

def split_nodes_image(old_nodes):
    new_nodes = []
    pass

def split_nodes_link(old_nodes):
    pass