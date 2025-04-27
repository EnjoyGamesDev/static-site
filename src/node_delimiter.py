from textnode import TextType, TextNode
from typing import List


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    
    # If it's not plain text, keep it as-is
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        parts = node.text.split(delimiter)
        
        if len(parts) % 2 == 0:
            raise Exception("Invalid MarkDown syntax: unmatched delimiter")
        
        # Build a small list of nodes for this one node
        split_nodes = []
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(part, TextType.TEXT))
            else:
                split_nodes.append(TextNode(part, text_type))
                
        new_nodes.extend(split_nodes) # Add all nodes at once
        
    return new_nodes