import unittest
from blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type
)
from markdown_to_html_node import (
    markdown_to_html_node,
    extract_title,
    generate_page
)
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
        self.assertEqual(result, BlockType.ULIST)

    def test_ordered_list(self):
        block = "1. This is a list item\n2. This is a second list item"
        result = block_to_block_type(block)
        self.assertEqual(result, BlockType.OLIST)

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
        self.assertEqual(second_type, BlockType.ULIST)

# markdown_to_html_node tests

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )

    def test_heading_1(self):
        md = "# This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading</h1></div>",
        )

    def test_heading_3(self):
        md = "### This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h3>This is a heading</h3></div>",
        )

    def test_heading_6(self):
        md = "###### This is a heading"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h6>This is a heading</h6></div>",
        )

    def test_olist(self):
        md = """
1. first item
2. second item
3. third item
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>first item</li><li>second item</li><li>third item</li></ol></div>"
        )

    def test_ulist(self):
        md = """
- first
- second
- third
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>first</li><li>second</li><li>third</li></ul></div>"
        )

    def test_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote></div>"
        )

    def test_heading_with_olist(self):
        md = """
# Heading

1. first
2. second
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><ol><li>first</li><li>second</li></ol></div>"
        )

# test extract title

class TestExtractTitle(unittest.TestCase):
    def test_extract_title_simple(self):
        markdown = "# Hello"
        self.assertEqual(extract_title(markdown), "Hello")

    def test_extract_title_later_line(self):
        markdown = "Intro text\n# Tolkien Fan Club\nMore text"
        self.assertEqual(extract_title(markdown), "Tolkien Fan Club")

    def test_extract_title_with_spaces(self):
        markdown = "#   Tolkien Fan Club   "
        self.assertEqual(extract_title(markdown), "Tolkien Fan Club")

    def test_extract_title_no_h1_raises(self):
        markdown = "## Not an h1\nJust text"
        with self.assertRaises(Exception):
            extract_title(markdown)