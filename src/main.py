import os
from pathlib import Path
import shutil
from block_markdown import markdown_to_html_node
from textnode import TextNode

public_path = "./public"
static_path = "./static"
content_path = "./content"
template_path = "./template.html"

def main():
    if not os.path.exists(static_path):
        raise Exception(f"{static_path} directory couldn't be found")

    if os.path.exists(public_path):
        print(f"removing {public_path}")
        shutil.rmtree(public_path)

    recursive_copy(static_path,public_path)

    generate_pages_recursive(content_path, template_path, public_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"... searching in {dir_path_content}")

    for filename in os.listdir(dir_path_content):
        source = os.path.join(dir_path_content, filename)
        dest = os.path.join(dest_dir_path, filename)

        if os.path.isfile(source):
            generate_page(source, template_path, dest)
            p = Path(dest)
            p.rename(p.with_suffix(".html"))

        else:
            generate_pages_recursive(source, template_path, dest)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown = read_file(from_path)
    template = read_file(template_path)

    html_node = markdown_to_html_node(markdown)
    content = html_node.to_html()
    title = extract_title(markdown)

    template_with_title = template.replace("{{ Title }}", title)
    webpage = template_with_title.replace("{{ Content }}", content)

    write_file(webpage, dest_path)


def read_file(path: str):
    with open(path, "r") as f:
        return f.read()


def write_file(content: str, path: str):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)

    with open(path, "w") as f:
        f.write(content)


def recursive_copy(source, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    for filename in os.listdir(source):
        source_path = os.path.join(source, filename)
        dest_path = os.path.join(dest, filename)
        if os.path.isfile(source_path):
            print(f"* {source_path} -> {dest_path}")
            shutil.copy(source_path, dest_path)
        else:
            recursive_copy(source_path, dest_path)


def extract_title(markdown: str):
    lines = markdown.split("\n")
    for line in lines:
       if  line.startswith("# "):
           return line.lstrip("# ")
    raise Exception("Markdown does not contain title")

if __name__ == "__main__":
    main()