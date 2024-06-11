import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
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

def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        md_images = extract_markdown_images(old_node.text)
        if len(md_images) == 0:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for image in md_images:
            split_text = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image section not closed")
            before = split_text[0]
            after = split_text[1]

            if len(before) > 0:
                new_nodes.append(TextNode(before, text_type_text))

            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            text = after

        if len(text) > 0:
            new_nodes.append(TextNode(text, text_type_text))
            
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue

        md_links = extract_markdown_links(old_node.text)
        if len(md_links) == 0:
            new_nodes.append(old_node)
            continue

        text = old_node.text
        for link in md_links:
            split_text = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, link section not closed")
            before = split_text[0]
            after = split_text[1]

            if len(before) > 0:
                new_nodes.append(TextNode(before, text_type_text))

            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            text = after

        if len(text) > 0:
            new_nodes.append(TextNode(text, text_type_text))

    return new_nodes


def text_to_textnodes(text: str):
    textnodes = [TextNode(text, text_type_text)]
    textnodes = split_nodes_delimiter(textnodes, "**", text_type_bold)
    textnodes = split_nodes_delimiter(textnodes, "*", text_type_italic)
    textnodes = split_nodes_delimiter(textnodes, "`", text_type_code)
    textnodes = split_nodes_image(textnodes)
    textnodes = split_nodes_link(textnodes)
    return textnodes
