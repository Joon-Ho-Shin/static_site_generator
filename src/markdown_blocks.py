from enum import Enum
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, text_node_to_html_node, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unordered_list"
    ORDERED = "ordered_list"

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    filtered_list = []
    for block in block_list:
        if block.strip() != "":
            filtered_list.append(block.strip())

    return filtered_list

def block_to_block_type(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    
    line_list = markdown.split("\n")
    if line_list[0].startswith("```") and line_list[-1].startswith("```") and len(line_list) > 1:
        return BlockType.CODE
    
    if markdown.startswith(">"):
        for line in line_list:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
            
    if markdown.startswith("- "):
        for line in line_list:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED
    
    if markdown.startswith("1. "):
        index = 1
        for line in line_list:
            if not line.startswith(f"{index}. "):   
                return BlockType.PARAGRAPH
            index += 1
        return BlockType.ORDERED
    
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown) -> HTMLNode:
    block_list = markdown_to_blocks(markdown)
    children_list = []
    for block in block_list:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            paragraph_text = block.replace("\n", " ")
            inline_children = text_to_children(paragraph_text)
            html = ParentNode("p", inline_children)
            children_list.append(html)
        elif block_type == BlockType.HEADING:
            level = count_leading_hashes(block)
            tag = f"h{level}"
            heading_text = block[level + 1:]
            inline_children = text_to_children(heading_text)
            html = ParentNode(tag, inline_children)
            children_list.append(html)
        elif block_type == BlockType.QUOTE:
            quote_lines = block.split("\n")
            cleaned_lines = []

            for line in quote_lines:
                line_without_marker = line[1:]
                cleaned = line_without_marker.strip()
                cleaned_lines.append(cleaned)

            quote_text = " ".join(cleaned_lines)
            inline_children = text_to_children(quote_text)
            html = ParentNode("blockquote", inline_children)
            children_list.append(html)
        elif block_type == BlockType.UNORDERED:
            list_lines = block.split("\n")
            list_item_nodes = []

            for line in list_lines:
                line_without_dash = line[2:].strip()
                inline_children = text_to_children(line_without_dash)
                li = ParentNode("li", inline_children)
                list_item_nodes.append(li)

            html = ParentNode("ul", list_item_nodes)
            children_list.append(html)

        elif block_type == BlockType.ORDERED:
            list_lines = block.split("\n")
            list_item_nodes = []

            for line in list_lines:
                parts = line.split(". ", 1)
                item_text = parts[1].strip()
                inline_children = text_to_children(item_text)
                li = ParentNode("li", inline_children)
                list_item_nodes.append(li)

            html = ParentNode("ol", list_item_nodes)
            children_list.append(html)           

        elif block_type == BlockType.CODE:
            if not block.startswith("```") or not block.endswith("```"):
                raise ValueError("invalid code block")
            text = block[4:-3]
            raw_text_node = TextNode(text, TextType.TEXT)
            child = text_node_to_html_node(raw_text_node)
            code_node = ParentNode("code", [child])
            pre_node = ParentNode("pre", [code_node])
            children_list.append(pre_node)  

    return ParentNode("div", children_list)


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []

    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        html_nodes.append(html_node)

    return html_nodes

def count_leading_hashes(text):
    count = 0

    for char in text:
        if char == "#":
            count += 1
        else:
            break

    return count