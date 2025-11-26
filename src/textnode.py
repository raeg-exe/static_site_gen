from enum import Enum
from src.htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


SIMPLE_TAGS = {
    TextType.TEXT: None,
    TextType.BOLD: "b",
    TextType.ITALIC: "i",
    TextType.CODE: "code",
}

def text_node_to_html_node(text_node):
    if text_node is None:
        raise Exception("TextNode has no value")

    if text_node.text_type in SIMPLE_TAGS:
        tag = SIMPLE_TAGS[text_node.text_type]
        return LeafNode(tag=tag, value=text_node.text)

    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    
    raise Exception("Invalid TextType")