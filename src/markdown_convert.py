import re
from enum import Enum

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UL ='unordered_list'
    OL = 'ordered_list'


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

def text_to_textnodes(text: str) -> list[TextNode]:

    node = [TextNode(text, TextType.TEXT)]

    new_nodes = split_nodes_link(split_nodes_image(node))

    for k, v in delimiters.items():
        new_nodes = split_nodes_delimiter(new_nodes, k, v)

    return new_nodes

def markdown_to_blocks(markdown: str) -> list[str]:

    return [x.strip() for x in markdown.split('\n\n') if x != '']

def block_to_blocktype(md_block: str) -> BlockType:

    # early exit
    if len(md_block) == 0:
        return BlockType.PARAGRAPH

    if re.match(r'#{1,6} .*$', md_block):
        return BlockType.HEADING
    
    if re.match(r'```\n[\s\S]*?```$', md_block):
        return BlockType.CODE

    lines = md_block.split('\n')
    
    if all(line.startswith('>') for line in lines):
        return BlockType.QUOTE
    
    if all(line.startswith('- ') for line in lines):
        return BlockType.UL

            
    if all(re.match(fr'^{i+1}\. ', line) for i, line in enumerate(lines)):
        return BlockType.OL
        
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)


def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_blocktype(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OL:
        return olist_to_html_node(block)
    if block_type == BlockType.UL:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> ParentNode:
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        parts = item.split(". ", 1)
        text = parts[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)