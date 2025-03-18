import re
from textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            new_texts = node.text.split(delimiter)
            i = 0
            if len(new_texts) == 1:
                new_nodes.append(node)
            else:
                i = 0
                for new_text in new_texts:
                    if new_text != "":
                        if i%2 == 0:
                            new_nodes.append(TextNode(new_text, TextType.TEXT))
                        else:
                            new_nodes.append(TextNode(new_text, text_type))
                    i += 1
        else:
            new_nodes.append(node)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue
        current_string = ""
        i = 0
        in_image = False
        for char in node.text:
            if not in_image:
                if char == "!":
                    in_image = True                    
                    if current_string != "":
                        new_nodes.append(TextNode(current_string, node.text_type, node.image_path))
                    new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
                    current_string = ""
                    i += 1
                else:
                    current_string += char
            if char == ")":
                if in_image:
                    in_image = False
                    current_string = ""
        if current_string != "":
            new_nodes.append(TextNode(current_string, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        current_string = ""
        i = 0
        in_link = False
        in_image = False
        for char in node.text:
            if char == "!":
                in_image = True
            if not in_link and not in_image:
                if char == "[":
                    in_image = True                    
                    if current_string != "":
                        new_nodes.append(TextNode(current_string, node.text_type))
                    new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
                    current_string = ""
                    i += 1
                else:
                    current_string += char
            if char == ")":
                if in_image:
                    in_image = False
                    in_link = False
                    current_string = ""
        if current_string != "":
            new_nodes.append(TextNode(current_string, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    if len(text.text) == 0:
        return []
    text_nodes = split_nodes_delimiter([text], "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes
    

