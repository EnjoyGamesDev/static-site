import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    
    raise Exception("No H1 header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        content = file.read()
    with open(template_path, "r") as file:
        template = file.read() 
    
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    
    final_content = template.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as file:
        file.write(final_content)