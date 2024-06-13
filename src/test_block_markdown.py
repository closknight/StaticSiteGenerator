import unittest

from block_markdown import (
    block_to_block_type,
    markdown_to_blocks,
    block_type_heading,
    block_type_paragraph,
    block_type_ordered_list,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    markdown_to_html_node
    )

markdown_mixed = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""

md_heading1 ="""\
# hello
"""

md_heading7 ="""\
####### hello\
"""

md_code_good ="""\
```
print("hello world")
```\
"""

md_code_bad ="""\
```
print("hello world")
````\
"""

md_quote_good = """\
>the
>end\
"""

md_quote_bad = """\
>the
what
>end\
"""

md_ul_good ="""\
* fdskjf
* fdjsl
* fdjsklf\
"""

md_ul_bad ="""\
* dsklf
fkdlsf
* fdjklsfjs\
"""

md_ol_good = """\
1. one
2. two
3. three\
"""

md_ol_bad = """\
1. one
5. five
7. seven\
"""


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        blocks = markdown_to_blocks(markdown_mixed)

        self.assertEqual(
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
            blocks
        )

    def test_block_to_block_type(self):
        self.assertEqual(block_to_block_type(md_heading1), block_type_heading)
        self.assertEqual(block_to_block_type(md_heading7), block_type_paragraph)

        self.assertEqual(block_to_block_type(md_code_good), block_type_code)
        self.assertEqual(block_to_block_type(md_code_bad), block_type_paragraph)

        self.assertEqual(block_to_block_type(md_quote_good), block_type_quote)
        self.assertEqual(block_to_block_type(md_quote_bad), block_type_paragraph)

        self.assertEqual(block_to_block_type(md_ul_good), block_type_unordered_list)
        self.assertEqual(block_to_block_type(md_ul_bad), block_type_paragraph)

        self.assertEqual(block_to_block_type(md_ol_good), block_type_ordered_list)
        self.assertEqual(block_to_block_type(md_ol_bad), block_type_paragraph)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == "__main__":
    unittest.main()
