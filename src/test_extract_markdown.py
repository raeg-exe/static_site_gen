import unittest
from textnode import TextNode, TextType
from markdown_functions import (
    extract_markdown_images, 
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link
)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multi(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image](https://imgur.com/gallery/ahri-fox-girl-hDMA0Q3#/t/fox_girl)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"), ("image", "https://imgur.com/gallery/ahri-fox-girl-hDMA0Q3#/t/fox_girl")], matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multi(self):
        matches = extract_markdown_links(
            "This is text with links to [link](https://www.boot.dev) and [link](https://www.youtube.com)"
        )
        self.assertListEqual([("link", "https://www.boot.dev"), ("link", "https://www.youtube.com")], matches)

    def test_extract_markdown_images_links_I(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_links_II(self):
        matches = extract_markdown_links(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)


    def test_split_images(self):
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

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and another [second link](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com"
                ),
            ],
            new_nodes,
        )

    def test_split_images_link(self):
        node = TextNode(
            "This is text with a [link](https://www.boot.dev) and an ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT
        )
        nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
            ],
            new_nodes,
        )