import unittest
from markdown_functions import text_to_textnodes
from textnode import(TextNode, TextType)

class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes_plain_text(self):
        text = "This is a string with plain text"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is a string with plain text", TextType.TEXT),
            ],
            new_node
        )

    def test_text_to_textnodes_bold(self):
        text = "This is a string with **bold** text"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is a string with ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
            new_node
        )

    def test_text_to_textnodes_italic(self):
        text = "This is a string with _italic_ text"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is a string with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text",TextType.TEXT),
            ],
            new_node
        )

    def test_text_to_textnodes_code(self):
        text = "This is a string with `code` text"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is a string with ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text",TextType.TEXT),
            ],
            new_node
        )

    def test_text_to_textnodes_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ",TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_node
        )

    def test_text_to_textnodes_link(self):
        text = "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ",TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://www.youtube.com")
            ],
            new_node
        )

    def test_text_to_textnodes_italic_link(self):
        text = "This is text with a _italic_ and a [link](https://www.youtube.com)"
        new_node = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" and a ",TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.youtube.com")
            ],
            new_node
        )