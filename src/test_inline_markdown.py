import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)

from textnode import (
    TextNode,
    text_type_text,
    text_type_code,
    text_type_italic,
    text_type_bold
)

class TestInlineMarkdown(unittest.TestCase):
    def test_inline_code(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        correct = [
            TextNode("This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word", text_type_text),
        ]

        self.assertEqual(new_nodes, correct)

    def test_inline_bold(self):
        node = TextNode("This is text with a **bold block** word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)

        correct = [
            TextNode("This is text with a ", text_type_text),
            TextNode("bold block", text_type_bold),
            TextNode(" word", text_type_text),
        ]

        self.assertEqual(new_nodes, correct)

    def test_inline_italics(self):
        node = TextNode("This is text with a *italic block* word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "*", text_type_italic)

        correct = [
            TextNode("This is text with a ", text_type_text),
            TextNode("italic block", text_type_italic),
            TextNode(" word", text_type_text),
        ]

        self.assertEqual(new_nodes, correct)

    def test_inline_code_multiple(self):
        node = TextNode("`this` This is text with a `code block` word and `another code block`", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)

        correct = [
            TextNode("this", text_type_code),
            TextNode(" This is text with a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" word and ", text_type_text),
            TextNode("another code block", text_type_code)
        ]
        self.assertEqual(new_nodes, correct)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev)"
        )
        self.assertListEqual(
            [
                ("link", "https://boot.dev"),
                ("another link", "https://blog.boot.dev"),
            ],
            matches,
        )

