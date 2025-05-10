import os
import shutil


def copy_content(src, dst):
    # Ensure the destination directory exists
    os.makedirs(dst, exist_ok=True)
    
    contents = os.listdir(src)
    
    for content in contents:
        src_path = os.path.join(src, content)
        dst_path = os.path.join(dst, content)
        
        # If it's a file in the root of `src`, copy it directly
        if os.path.isfile(src_path):
            print("Copying file:", src_path)
            shutil.copy(src_path, dst_path)
        # If it's a directory, recursively copy its contents
        elif os.path.isdir(src_path):
            print("Entering directory:", src_path)
            copy_content(src_path, dst_path)