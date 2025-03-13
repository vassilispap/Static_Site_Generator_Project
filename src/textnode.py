from enum import Enum 
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, link=None, image_path=None):
        self.text = text
        self.text_type = text_type
        self.url = link
        self.image_path = image_path
    
    def __eq__(TextNode1, TextNode2):
        return TextNode1.text == TextNode2.text and TextNode1.text_type == TextNode2.text_type and TextNode1.url == TextNode2.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url
                                    , "alt": text_node.text})
    return ValueError(f"Unknown text type: {text_node.text_type}")

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
    target_tuple = []
    images = re.findall(r"!\[(.*?)\]", text)
    links = re.findall(r"\]\((.*?)\)", text)
    for image in images:
        target_tuple.append((image, links[images.index(image)]))
    return target_tuple

def extract_markdown_links(text):
    target_tuple = []
    link_texts = re.findall(r"\[(.*?)\]", text)
    links = re.findall(r"\]\((.*?)\)", text)
    for link_text in link_texts:
        target_tuple.append((link_text, links[link_texts.index(link_text)]))
    return target_tuple
