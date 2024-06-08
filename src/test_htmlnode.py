import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("h1", "This is a title", None, None)
        self.assertEqual("HTMLNode(h1, This is a title, None, None)", repr(node))

    def test_to_html(self):
        node = HTMLNode("h1", "This is a title")
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a",props={"href": "https://www.google.com", "target": "_blank"})
        correct = " href=\"https://www.google.com\" target=\"_blank\""
        self.assertEqual(node.props_to_html(), correct)
