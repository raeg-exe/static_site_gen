import re
from textnode import TextType, TextNode


def extract_markdown_images(text):
    match_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match_images

def extract_markdown_links(text):
    match_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match_links


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        extracted_images = extract_markdown_images(original_text)
        
        if len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue

        for image in extracted_images:
            alt, link = image
            sections = original_text.split(f"![{alt}]({link})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, link))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        extracted_links = extract_markdown_links(original_text)
        
        if len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue

        for link in extracted_links:
            alt, url = link
            sections = original_text.split(f"[{alt}]({url})", 1)

            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.LINK, url))
            original_text = sections[1]

        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes