from textnode import TextNode, TextType
import os, shutil


def main():    
    copy_content("static", "public")

def copy_content(src, dst):
    
    # First, delete the contents of the public directory
    if os.path.exists("public"):
        shutil.rmtree("public")
        
    os.mkdir("public")
    
    # Ensure the destination directory exists
    os.makedirs(dst, exist_ok=True)
    
    contents = os.listdir(src)
    
    # Iterate over each content
    for content in contents:
        src_path = os.path.join(src, content)
        dst_path = os.path.join(dst, content)
        
        # Copy the file to the destination
        if os.path.isfile(src_path):
            print("Copying file to:", src_path)
            shutil.copy(src_path, dst_path)
        # If it's a directory, create the same directory at the destination
        elif os.path.isdir(src_path):
            print("Entering directory:", src_path)
            os.makedirs(dst_path, exist_ok=True)
            copy_content(src_path, dst_path)


    
main()