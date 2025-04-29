from textnode import TextType, TextNode
from typing import List
import re


def split_nodes_delimiter(old_nodes: List[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []
    
    # If it's not plain text, keep it as-is
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        parts = old_node.text.split(delimiter)
        
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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    
    # If there are no images or links respectively, just return a list with the original TextNode in it
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        images = extract_markdown_images(old_node.text)
        
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        
        for image_alt, image_link in images:
            parts = current_text.split(f"![{image_alt}]({image_link})", 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
        
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            
            if len(parts) > 1:
                current_text = parts[1]
            
    return new_nodes
        

def split_nodes_link(old_nodes):
    new_nodes = []
    
    # If there are no images or links respectively, just return a list with the original TextNode in it
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        links = extract_markdown_links(old_node.text)
        
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        
        current_text = old_node.text
        
        for link_text, url in links:
            parts = current_text.split(f"[{link_text}]({url})", 1)
            
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
        
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            
            if len(parts) > 1:
                current_text = parts[1]
            
    return new_nodes