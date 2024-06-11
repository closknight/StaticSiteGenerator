import unittest

from htmlnode import LeafNode, ParentNode

class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
        "p",
        [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), html)


    def test_nested_to_html(self):
        node = ParentNode(
        "div",
        [
            ParentNode("p", [LeafNode("b", "Bold text")]),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )
        html = "<div><p><b>Bold text</b></p>Normal text<i>italic text</i>Normal text</div>"
        self.assertEqual(node.to_html(), html)

if __name__ == "__main__":
    unittest.main()