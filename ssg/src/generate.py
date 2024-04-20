import os
import shutil
from pathlib import Path

from markdown_blocks import markdown_to_html_node


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path):
            print(f" * {from_path} -> {dest_path}")
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        path_content = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(path_content):
            if path_content.endswith(".md"):
                dest_path = Path(dest_path).with_suffix(".html")
                generate_page(path_content, template_path, dest_path)
        else:
            generate_pages_recursive(path_content, template_path, dest_path)

def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")

    with open(from_path, 'r') as f:
        md = f.read()
    title = extract_title(md)
    content = markdown_to_html_node(md).to_html()

    with open(template_path, 'r') as f:
        page_html = f.read()
    page_html = page_html.replace("{{ Title }}", title)
    page_html = page_html.replace("{{ Content }}", content)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(page_html)

def extract_title(markdown: str) -> str:
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise RuntimeError("Markdown missing title")
