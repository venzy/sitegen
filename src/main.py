import os
import shutil

from node.textnode import TextNode

def main():
    copy_tree("static", "public")

def copy_tree(source_dir: str, dest_dir: str):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)
    if not os.path.exists(dest_dir):
        raise Exception(f"Could not create destination directory {dest_dir}")
    
    if not os.path.exists(source_dir):
        raise Exception(f"Could not find source directory {source_dir}")
    
    for path in os.listdir(source_dir):
        source_path = os.path.join(source_dir, path)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_dir)
        else:
            # Assume it's a directory
            copy_tree(source_path, os.path.join(dest_dir, path))


main()