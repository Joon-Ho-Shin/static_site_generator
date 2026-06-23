import os
from markdown_blocks import markdown_to_html_node
from pathlib import Path

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[1:].strip()
    raise Exception("There is no h1 header")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    markdown_file = open(from_path, "r")
    markdown_contents = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path, "r")
    template_contents = template_file.read()
    template_file.close()

    content = markdown_to_html_node(markdown_contents).to_html()
    title = extract_title(markdown_contents)

    result = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", content)

    
    directory = os.path.dirname(dest_path)
    os.makedirs(directory, exist_ok=True)

    output_file = open(dest_path, "w")
    output_file.write(result)
    output_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for name in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, name)
        if os.path.isfile(full_path):
            print(f"Found a file: {full_path}")
            destination_path =  os.path.join(dest_dir_path, name)
            html_path = Path(destination_path).with_suffix(".html")
            generate_page(full_path, template_path, html_path)
        else:
            print(f"Found a directory: {full_path}")
            destination_path = os.path.join(dest_dir_path, name)
            generate_pages_recursive(full_path, template_path, destination_path)