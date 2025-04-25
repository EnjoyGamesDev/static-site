from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        
        result = ""
        for key, value in self.props.items():
            result += f'{key}="{value}" '
        return result.strip()
    
    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        return f"HTMLNODE({self.tag}, {self.value}, {self.children}, {self.props})"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, children=None, props=props)
        
    def to_html(self):
        # Check if value is not empty, if tag is None then return the raw value
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag is None:
            return self.value
        
        # Convert the properties to html
        props_str = self.props_to_html()
        
        # Return the full HTML string
        if props_str:
            return f"<{self.tag} {props_str}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)
        
    def to_html(self):
        # Check if tag and children are not empty
        if not self.tag:
            raise ValueError("Parent must have a tag")
        if not self.children:
            raise ValueError("Parent must have a children")
        
        # Recursively render the children
        children_html = "".join(child.to_html() for child in self.children)
        
        # Get all HTML attributes from props
        props_str = self.props_to_html()
        
        if props_str:
            return f"<{self.tag} {props_str}>{children_html}</{self.tag}>"
        else:
            return f"<{self.tag}>{children_html}</{self.tag}>"
        
def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case (TextType.TEXT):
            return LeafNode(tag=None, value=text_node.text)
        case (TextType.BOLD):
            return LeafNode(tag="b", value=text_node.text)
        case (TextType.ITALIC):
            return LeafNode(tag="i", value=text_node.text)
        case (TextType.CODE):
            return LeafNode(tag="code", value=text_node.text)
        case (TextType.LINK):
            if not text_node.url:
                raise Exception("LINK TextType requires a URL")
            return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case (TextType.IMAGE):
            if not text_node.url:
                raise Exception("IMAGE TextType requires a URL")
            return LeafNode(
                tag="img",
                value="",
                props={"src": text_node.url, "alt": text_node.text}
            )