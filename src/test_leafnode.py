import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_no_value(self):
        node = LeafNode("h1", None)
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag(self):
        raw = "this is a string"
        node = LeafNode(None, raw)
        self.assertEqual(raw, node.to_html())

    def test_to_html(self):
        p_node = LeafNode("p", "This is a paragraph of text.")
        p_html = "<p>This is a paragraph of text.</p>"
        self.assertEqual(p_node.to_html(), p_html)

        a_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        a_html = "<a href=\"https://www.google.com\">Click me!</a>"
        self.assertEqual(a_node.to_html(), a_html)


    