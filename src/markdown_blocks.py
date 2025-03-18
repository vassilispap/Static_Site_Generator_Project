from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    blocks = []
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if len(block) == 0:
            continue
        block = block.strip()
        if block != "\n":
            new_blocks.append(block)    
    return new_blocks 

def block_to_block_type(block):
    valid_heading_start = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    for start in valid_heading_start:
        if block.startswith(start):
            return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith("> "):
        return BlockType.QUOTE

    lines = block.split("\n")

    in_unordered_list = True
    for line in lines:
        if not line.startswith("- "):
            in_unordered_list = False
    if in_unordered_list:
        return BlockType.UNORDERED_LIST

    in_ordered_list = True
    number = 1
    for line in lines:
        
        match = re.match(r'^(\d+)\.\s(.*)$', line)
        if match:
            if int(match.group(1)) != number:
                in_ordered_list = False
                break
            number +=1
        else:
            in_ordered_list = False
            break

    if in_ordered_list:
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)