import os
from markdown_blocks import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    
    for line in lines:
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    
    raise Exception("No H1 header found")

def generate_page(from_path, template_path, dest_path, basepath="/"):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r") as file:
        content = file.read()
    with open(template_path, "r") as file:
        template = file.read() 
    
    html_content = markdown_to_html_node(content).to_html()
    title = extract_title(content)
    
    final_content = (
    template
    .replace("{{ Title }}", title)
    .replace("{{ Content }}", html_content)
    .replace('href="/', f'href="{basepath}')
    .replace('src="/', f'src="{basepath}')
)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    with open(dest_path, "w") as file:
        file.write(final_content)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath="/"):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        
        # Recuse if it's a directory
        if os.path.isdir(entry_path):
            new_dest_dir = os.path.join(dest_dir_path, entry)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(entry_path, template_path, new_dest_dir, basepath)
                
        elif os.path.isfile(entry_path) and entry_path.endswith(".md"):
            output_filename = os.path.join(dest_dir_path, os.path.basename(entry_path).replace(".md", ".html"))
            print(f"Generating HTML file: {output_filename} from {entry_path}")
            generate_page(entry_path, template_path, output_filename, basepath)