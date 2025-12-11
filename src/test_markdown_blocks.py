import unittest
from blocks import BlockType, markdown_to_blocks, block_to_block_type
from textnode import TextNode, TextType


class TestMarkdownToBlocks(unittest.TestCase):
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
        
class TestBlockToBlockType(unittest.TestCase):
    def test_paragraph_single_line(self):
        block = "This is just a paragraph"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        block = "Line one of text. \nLine two of text without any markers"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_paragraph_heading(self):
        block = "### This is a heading"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.HEADING)

    def test_paragraph_code(self):
        block = "```\nThis is a block\nof code\n```"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.CODE)

    def test_paragraph_quote(self):
        block = ">This is a quote"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- This is a list item\n- This is a second list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. This is a list item\n2. This is a second list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.ORDERED_LIST)

    def test_paragraph_with_unordered_list(self):
        markdown = """This is a paragraph.

- list item
- another item
"""
        blocks = markdown_to_blocks(markdown)

        self.assertEqual(len(blocks), 2)

        first_type = block_to_block_type(blocks[0])
        self.assertEqual(first_type, BlockType.PARAGRAPH)

        second_type = block_to_block_type(blocks[1])
        self.assertEqual(second_type, BlockType.UNORDERED_LIST)