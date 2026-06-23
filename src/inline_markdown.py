from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    
    modified_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            sections = node.text.split(delimiter)
            if len(sections) % 2 == 0:
                raise Exception("Invalid markdown syntax")
            for i in range(len(sections)):
                if sections[i] == "":
                    continue
                if i % 2 == 0:
                    modified_list.append(TextNode(sections[i], TextType.TEXT))
                else:
                    modified_list.append(TextNode(sections[i], text_type))
        else:
            modified_list.append(node)
        
    return modified_list

def extract_markdown_images(text):
    matched_links = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matched_links

def extract_markdown_links(text):
    matched_links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matched_links

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    modified_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_images(node.text)
            if not links:
                modified_list.append(node)
                continue
            original_text = node.text
            for link in links:    
                alt = link[0]
                url = link[1]
                sections = original_text.split(f"![{alt}]({url})", 1)
                if len(sections)  != 2:
                    raise Exception("Invalid markdown syntax")
                if sections[0] != "":
                    modified_list.append(TextNode(sections[0], TextType.TEXT))
                modified_list.append(TextNode(alt, TextType.IMAGE, url))
                original_text = sections[1]
            if original_text != "":
                modified_list.append(TextNode(original_text, TextType.TEXT))
        else:
            modified_list.append(node)
    return modified_list

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]: 
    modified_list = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            if not links:
                modified_list.append(node)
                continue
            original_text = node.text
            for link in links:    
                alt = link[0]
                url = link[1]
                sections = original_text.split(f"[{alt}]({url})", 1)
                if len(sections)  != 2:
                    raise Exception("Invalid markdown syntax")
                if sections[0] != "":
                    modified_list.append(TextNode(sections[0], TextType.TEXT))
                modified_list.append(TextNode(alt, TextType.LINK, url))
                original_text = sections[1]
            if original_text != "":
                modified_list.append(TextNode(original_text, TextType.TEXT))
        else:
            modified_list.append(node)
    return modified_list

def text_to_textnodes(text):
    TextNodeList = []
    text_to_TextNode = TextNode(text, TextType.TEXT)
    TextNodeList.append(text_to_TextNode)
    TextNodeList = split_nodes_delimiter(TextNodeList, "**", TextType.BOLD)
    TextNodeList = split_nodes_delimiter(TextNodeList, "_", TextType.ITALIC)
    TextNodeList = split_nodes_delimiter(TextNodeList, "`", TextType.CODE)
    TextNodeList = split_nodes_image(TextNodeList)
    TextNodeList = split_nodes_link(TextNodeList)

    return TextNodeList
    

    