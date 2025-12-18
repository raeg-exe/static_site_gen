from blocks import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type
)
from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode
)
from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node
)
from markdown_functions import text_to_textnodes


def paragraph_to_html_node(block):
    block = block.split('\n')
    block = ' '.join(block)
    children = text_to_children(block)
    return ParentNode(tag="p", children=children)

def heading_to_html_node(block):
    pass

def code_to_html_node(block):
    pass

def quote_to_html_node(block):
    pass

def olist_to_html_node(block):
    pass

def ulist_to_html_node(block):
    pass

def text_to_children(text):
    html_nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes


def markdown_to_html_node(markdown):
    html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == BlockType.PARAGRAPH:
            html_node = paragraph_to_html_node(block)
            html_nodes.append(html_node)
        
        elif block_type == BlockType.HEADING:
            html_node = heading_to_html_node(block)
            html_nodes.append(html_node)

        elif block_type == BlockType.CODE:
            html_node = code_to_html_node(block)
            html_nodes.append(html_node)

        elif block_type == BlockType.QUOTE:
            html_node = quote_to_html_node(block)
            html_nodes.append(html_node)

        elif block_type == BlockType.OLIST:
            html_node = olist_to_html_node(block)
            html_nodes.append(html_node)

        elif block_type == BlockType.ULIST:
            html_node = ulist_to_html_node(block)
            html_nodes.append(html_node)

        else:
            raise Exception("Invalid Markdown...")

    return ParentNode(tag="div", children=html_nodes)