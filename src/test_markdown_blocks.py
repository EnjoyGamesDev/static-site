import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type
from markdown_blocks import BlockType
  
class TestMarkDownToBlocks(unittest.TestCase):        
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_heading_paragraph_list(self):
        md = """
# Heading

This is a paragraph.

- Item 1
- Item 2
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Heading",
                "This is a paragraph.",
                "- Item 1\n- Item 2"
            ]
        )

    def test_multiple_blank_lines(self):
        md = """
First block


Second block



Third block
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["First block", "Second block", "Third block"]
        )
        
    def test_inline_formatting(self):
        md = """
This has **bold**, _italic_, and `code`.

Another paragraph.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["This has **bold**, _italic_, and `code`.", "Another paragraph."]
        )

    def test_only_newlines(self):
        md = "\n\n\n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [""])
        
class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "## This is a heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = "```\ndef foo():\n    return 'bar'\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = "> this is\n> a quote block"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = "- item one\n- item two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = "This is just a regular paragraph.\nStill part of the same paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)