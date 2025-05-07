import unittest

from htmlnode import LeafNode
from textnode import text_node_to_html_node, TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq_with_none_url(self):
        node1 = TextNode("This is a text node", TextType.TEXT, None)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node1, node2)
        
    def test_not_eq_different_type_and_url(self):
        node3 = TextNode("This is a text node", TextType.TEXT, "example.com")
        node4 = TextNode("This is a text node", TextType.ITALIC, "wikipedia.org")
        self.assertNotEqual(node3, node4)
        
    def test_not_eq_different_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("Hello", TextType.TEXT)
        node2 = TextNode("Goodbye", TextType.TEXT)
        self.assertNotEqual(node1, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")
        
    def test_has_url(self):
        node = TextNode("Click me!", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        leaf_node = LeafNode("a", "Click me!", props={"href": "https://example.com"})
        self.assertEqual(html_node, leaf_node)
        
    def test_no_url(self):
        node = TextNode("Missing URL", TextType.LINK, url=None)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "LINK TextType requires a URL")
            
    def test_has_image(self):
        node = TextNode("An image", TextType.IMAGE, url="https:imgur.com/example")
        html_node = text_node_to_html_node(node)
        leaf_node = LeafNode("img", "", props={"src": "https:imgur.com/example", "alt": "An image"})
        self.assertEqual(html_node, leaf_node)
        
    def test_no_image(self):
        node = TextNode("Missing IMAGE", TextType.IMAGE, url=None)
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertEqual(str(context.exception), "IMAGE TextType requires a URL")

if __name__ == "__main__":
    unittest.main()