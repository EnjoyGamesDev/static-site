import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()