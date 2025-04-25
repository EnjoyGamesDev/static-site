import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextType, TextNode


class TestHTMLNode(unittest.TestCase):
    # HTMLNode tests
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
    
    # LeafNode tests
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

    # ParentNode tests
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_parentnode_multiple_leaf_children(self):
        children = [
            LeafNode("b", "bold"),
            LeafNode(None, " plain "),
            LeafNode("i", "italic"),
        ]
        parent = ParentNode("p", children)
        self.assertEqual(parent.to_html(), "<p><b>bold</b> plain <i>italic</i></p>")
        
    def test_parentnode_with_props(self):
        child_node = LeafNode(None, "text")
        parent_node = ParentNode("div", [child_node], props={"class": "container", "id": "main"})
        self.assertEqual(parent_node.to_html(), '<div class="container" id="main">text</div>')
        
    def test_parentnode_raises_without_tag(self):
        child = LeafNode("span", "oops")
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [child]).to_html()
        self.assertIn("Parent must have a tag", str(context.exception))

    def test_parentnode_raises_without_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("div", []).to_html()
        self.assertIn("Parent must have a children", str(context.exception))
        
    # text_note_to_html_node tests
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