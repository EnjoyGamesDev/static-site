import os, shutil

from copy_to_static import copy_content
from get_content import generate_page, generate_pages_recursive

def main():
    # First, delete the contents of the public directory
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    
    # Start the copying process
    copy_content("static", "public")
    
    # Generate the index page
    generate_pages_recursive("content", "template.html", "public")

main()