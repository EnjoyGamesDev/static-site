import os, shutil, sys

from copy_to_static import copy_content
from get_content import generate_pages_recursive

def main():
    
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    
    # First, delete the contents of the public directory
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    
    # Start the copying process
    copy_content("static", "docs")
    
    # Generate the index page
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()