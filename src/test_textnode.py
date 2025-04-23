import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq_with_none_url(self):
        node1 = TextNode("This is a text node", TextType.NORMAL, None)
        node2 = TextNode("This is a text node", TextType.NORMAL)
        self.assertEqual(node1, node2)
        
    def test_not_eq_different_type_and_url(self):
        node3 = TextNode("This is a text node", TextType.NORMAL, "example.com")
        node4 = TextNode("This is a text node", TextType.ITALIC, "wikipedia.org")
        self.assertNotEqual(node3, node4)
        
    def test_not_eq_different_text_type(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node1, node2)

    def test_not_eq_different_text(self):
        node1 = TextNode("Hello", TextType.NORMAL)
        node2 = TextNode("Goodbye", TextType.NORMAL)
        self.assertNotEqual(node1, node2)


if __name__ == "__main__":
    unittest.main()