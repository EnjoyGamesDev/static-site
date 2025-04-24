import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(
            tag="a",
            value="Google",
            props={"href": "https://google.com", "target": "_blank"}
        )
        result = node.props_to_html()
        self.assertIn('href="https://google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertEqual(len(result.split()), 2)
        
        node2 = HTMLNode(
            tag="a",
            value="Google",
            props={"href": "https://google.com", "target": "_blank"}
        )
        
        self.assertEqual(node, node2)
        
    def test_props_to_html_single_attribute(self):
        node = HTMLNode(
            tag="img",
            value=None,
            props={"src": "image.png"}
        )
        result = node.props_to_html()
        self.assertEqual(result, 'src="image.png"')
        
    def test_props_to_html_no_attributes(self):
        node = HTMLNode(
            tag="p",
            value="No props",
            props=None
        )
        result = node.props_to_html()
        self.assertEqual(result, "")
        
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_leaf_to_html_text_only(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")
        
    def test_leaf_to_html_with_props(self):
        node = LeafNode("a", "Link", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Link</a>')

    def test_leaf_to_html_raises_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

if __name__ == "__main__":
    unittest.main()