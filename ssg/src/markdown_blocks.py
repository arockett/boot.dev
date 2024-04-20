import re

from htmlnode import LeafNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ulist = "unordered_list"
block_type_olist = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = [b.strip() for b in markdown.split("\n\n")]
    return [b for b in blocks if len(b) > 0]

def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children: list[ParentNode] = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    root = ParentNode(tag="div", children=children)
    return root

def block_to_html_node(block: str) -> ParentNode:
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return paragraph_to_html_node(block)
    if block_type == block_type_heading:
        return heading_to_html_node(block)
    if block_type == block_type_code:
        return code_to_html_node(block)
    if block_type == block_type_olist:
        return olist_to_html_node(block)
    if block_type == block_type_ulist:
        return ulist_to_html_node(block)
    if block_type == block_type_quote:
        return quote_to_html_node(block)
    raise ValueError("Invalid block type")

def block_to_block_type(block: str) -> str:
    lines = block.split("\n")
    if re.match(r"#{1,6} .+", block) is not None:
        return block_type_heading
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return block_type_code
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_ulist
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return block_type_paragraph
            i += 1
        return block_type_olist
    return block_type_paragraph

def text_to_children(text: str) -> list[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(n) for n in text_nodes]

def paragraph_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode(tag="p", children=children)

def heading_to_html_node(block: str) -> ParentNode:
    level, text = block.split(" ", maxsplit=1)
    children = text_to_children(text)
    return ParentNode(tag=f"h{len(level)}", children=children)

def code_to_html_node(block: str) -> ParentNode:
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode(tag="code", children=children)
    return ParentNode(tag="pre", children=[code])

def quote_to_html_node(block: str) -> ParentNode:
    lines = block.split("\n")
    quote_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        quote_lines.append(line.lstrip(">").strip())
    quote = " ".join(quote_lines)
    children = text_to_children(quote)
    return ParentNode(tag="blockquote", children=children)

def ulist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ul", children=html_items)

def olist_to_html_node(block: str) -> ParentNode:
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode(tag="li", children=children))
    return ParentNode(tag="ol", children=html_items)
