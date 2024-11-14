import os
import shutil

from convert.markdown_conversion import markdown_to_html_node
from parse.block_parse import extract_title

def main():
    copy_tree("static", "public")
    generate_pages_recursive("content", "template.html", "public")

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

def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    if not os.path.exists(dir_path_content):
        raise Exception(f"Could not find source directory {dir_path_content}")

    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)

    for path in os.listdir(dir_path_content):
        source_path = os.path.join(dir_path_content, path)
        dest_path = os.path.join(dest_dir_path, path)
        if os.path.isfile(source_path):
            (dest_file, _) = os.path.splitext(dest_path)
            dest_file += ".html"
            generate_page(source_path, template_path, dest_file)
        else:
            # Assume it's a directory
            generate_pages_recursive(source_path, template_path, dest_path)

main()