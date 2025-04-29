import unittest
from textnode import TextType, TextNode
from inline_markdown import (
    split_nodes_delimiter, 
    extract_markdown_images, 
    extract_markdown_links, 
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes
    )

class TestInlineMarkDown(unittest.TestCase):
    def test_split_code_backticks(self):
        node = TextNode(f"This is `code` example", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" example", TextType.TEXT))
        
    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("An _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("An ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_nodes_delimiter_error(self):
        node = TextNode("Unclosed `code block", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(str(context.exception), "Invalid MarkDown syntax: unmatched delimiter")
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and \
            ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                              ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)
        
    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)
        
    def test_extract_broken_markdown_images(self):
        matches = extract_markdown_images(
            "![This is text with] an https://i.imgur.com/zjjcJKZ.png"
        )
        self.assertListEqual([], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)
    
    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and \
            [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"),
                              ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)
        
    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links(
            "This is text with no link"
        )
        self.assertListEqual([], matches)
    
    def test_extract_broken_markdown_links(self):
        matches = extract_markdown_links(
            "Broken [link](missing closing"
        )
        self.assertListEqual([], matches)
        
    def test_split_images_and_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_no_images(self):
        node = TextNode(
            "This is just text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is just text", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_only_images(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                )
            ],
            new_nodes,
        )
        
    def test_split_single_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")
            ],
            new_nodes,
        )
        
    def test_split_links_and_text(self):
        node = TextNode(
            "This is text with a [Warframe](https://warframe.com) and another [Warframe Wiki](https://wiki.warframe.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("Warframe", TextType.LINK, "https://warframe.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "Warframe Wiki", TextType.LINK, "https://wiki.warframe.com"
                ),
            ],
            new_nodes,
        )
        
    def test_split_no_links(self):
        node = TextNode(
            "This is just text with no link",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is just text with no link", TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_split_only_links(self):
        node = TextNode(
            "[Warframe](https://warframe.com)[Warframe Wiki](https://wiki.warframe.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Warframe", TextType.LINK, "https://warframe.com"),
                TextNode(
                    "Warframe Wiki", TextType.LINK, "https://wiki.warframe.com"
                )
            ],
            new_nodes,
        )
        
    def test_split_single_link(self):
        node = TextNode(
            "[Warframe](https://warframe.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Warframe", TextType.LINK, "https://warframe.com")
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes(self):
        new_nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes_plain_text(self):
        new_nodes = text_to_textnodes("Just text without anything else")
        self.assertListEqual(
            [
                TextNode("Just text without anything else", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes_bold(self):
        new_nodes = text_to_textnodes("This is **bold** text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes_italic(self):
        new_nodes = text_to_textnodes("This is _italic_ text")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes_code(self):
        new_nodes = text_to_textnodes("This is `code` inline")
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" inline", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_textnodes_link(self):
        new_nodes = text_to_textnodes("The [Falcor](https://wiki.warframe.com/w/Falcor) is the best glaive")
        self.assertListEqual(
            [
                TextNode("The ", TextType.TEXT),
                TextNode("Falcor", TextType.LINK, "https://wiki.warframe.com/w/Falcor"),
                TextNode(" is the best glaive", TextType.TEXT),
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes_image(self):
        new_nodes = text_to_textnodes("I'm always in need of ![Forma](https://wiki.warframe.com/w/Forma)")
        self.assertListEqual(
            [
                TextNode("I'm always in need of ", TextType.TEXT),
                TextNode("Forma", TextType.IMAGE, "https://wiki.warframe.com/w/Forma"),
            ],
            new_nodes,
        )