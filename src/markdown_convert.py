import re

from textnode import TextNode, TextType

delimiters = {
    "**": TextType.BOLD,
    "*": TextType.ITALIC,
    "_": TextType.ITALIC,
    "`": TextType.CODE
}


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes = []

    for node in old_nodes:

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if node.text.count(delimiter) % 2 != 0:
            raise ValueError("Incorrect markdown format")
        
        subnodes = node.text.split(delimiter)

        for i, subnode in enumerate(subnodes):
            if i % 2 == 0:
                new_nodes.append(TextNode(subnode, TextType.TEXT))
            else:
                new_nodes.append(TextNode(subnode, delimiters[delimiter]))


    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_urls(text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_images(node.text)
        remaining = node.text

        for alt, url in matches:
            delim = f"![{alt}]({url})"
            before, after = remaining.split(delim, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(alt, TextType.IMAGE, url))
            remaining = after

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))    

        


    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        matches = extract_markdown_urls(node.text)
        remaining = node.text

        for anchor, url in matches:
            delim = f"[{anchor}]({url})"
            before, after = remaining.split(delim, 1)
            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            remaining = after

        if remaining:
            new_nodes.append(TextNode(remaining, TextType.TEXT))    

    
    return new_nodes



