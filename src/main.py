from textnode import TextNode, TextType
from htmlnode import HTMLNODE

def main():
    dummy_TextNode = TextNode("This is some anchor text", TextType.NORMAL, "https://www.boot.dev")
    print(dummy_TextNode)

    
main()