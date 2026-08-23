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

def extract_markdown_images(text: str) -> list[str]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_urls(text: str) -> list[str]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    