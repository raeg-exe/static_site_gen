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
import os


def paragraph_to_html_node(block):
    lines = block.split('\n')
    lines = [line.strip() for line in lines]
    paragraph = ' '.join(lines)
    children = text_to_children(paragraph)
    return ParentNode(tag="p", children=children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    text = block[level +1:]
    tag = f"h{level}"
    children = text_to_children(text)
    return ParentNode(tag, children)

def code_to_html_node(block):
    text = block[4: -3]
    node = TextNode(text, TextType.TEXT)
    html_node = text_node_to_html_node(node)
    code_node = ParentNode("code", [html_node])
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def quote_to_html_node(block):
    clean_lines = []
    lines = block.split('\n')
    for line in lines:
        clean_lines.append(line.lstrip('>').strip())
    clean_lines = ' '.join(clean_lines)
    children = text_to_children(clean_lines)
    return ParentNode("blockquote", children)

def olist_to_html_node(block):
    html_items = []
    lines = block.split('\n')
    for line in lines:
        text = line[3:]
        children = text_to_children(text)
        ol_node = ParentNode("li", children)
        html_items.append(ol_node)
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    html_items = []
    lines = block.split('\n')
    for line in lines:
        text = line.lstrip("- ")
        children = text_to_children(text)
        li_node = ParentNode("li", children)
        html_items.append(li_node)
    return ParentNode("ul", html_items)
    

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


def extract_title(markdown):
    strings = markdown.split('\n')
    for string in strings:
        if string.startswith('# '):
            title = string.lstrip('# ')
            title = title.strip()
            return title
    else:
        raise Exception("No h1 heading to extract...")

def generate_page(from_path, template_path, dst_path):
    print(f"Generating page from {from_path} to {dst_path} using {template_path}...")

    with open(from_path, "r") as md_file:
        markdown = md_file.read()
    with open(template_path, "r") as file:
        template = file.read()

    content_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", content_html)

    destination = os.path.dirname(dst_path)
    if destination:
        os.makedirs(destination, exist_ok=True)

    with open(dst_path, "w") as f:
        f.write(full_html)
