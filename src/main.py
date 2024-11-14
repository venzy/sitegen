import os
import shutil

from convert.markdown_conversion import markdown_to_html_node
from parse.block_parse import extract_title

def main():
    copy_tree("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")

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

def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using template {template_path}")

    markdown = ""
    with open(from_path) as source_file:
        markdown = source_file.read()
    
    template = ""
    with open(template_path) as source_file:
        template = source_file.read()
    
    content_html = markdown_to_html_node(markdown).to_html()

    title = extract_title(markdown)

    output_html = template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    with open(dest_path, 'w') as dest_file:
        dest_file.write(output_html)

main()