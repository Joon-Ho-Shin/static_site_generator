from textnode import TextNode, TextType
import os
import shutil
from gencontent import generate_page, generate_pages_recursive
import sys

basepath = "/"
if len(sys.argv) > 1:
    basepath = sys.argv[1]

def copy_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    os.mkdir(destination)
    copy_directory_recursive(source, destination)

def copy_directory_recursive(source, destination):
    item_list = os.listdir(source)
    for item in item_list:
        source_path = os.path.join(source, item)
        destination_path = os.path.join(destination, item)

        if os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)
        else:
            os.mkdir(destination_path)
            copy_directory_recursive(source_path, destination_path)
            print(f"Copying {source_path} to {destination_path}")

def main():
    copy_directory("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

main()