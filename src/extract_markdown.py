import re
from textnode import TextType


def extract_markdown_images(text):
    match_images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match_images

def extract_markdown_links(text):
    match_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match_links