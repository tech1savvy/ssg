import os

from ssg.markdown.blocks import extract_heading, split_blocks
from ssg.render import render_markdown


def extract_title(markdown) -> str:
    title_block = split_blocks(markdown)[0]
    level, heading = extract_heading(title_block)
    if level != 1:
        raise ValueError("Error: no h1 header")
    return heading


def genrate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown_content = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path)
    template_content = template_file.read()
    template_file.close()

    html_content = render_markdown(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content.replace("{{ Title }}", title)
    template_content.replace("{{ Content }}", html_content)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    html_file = open(dest_path, "w")
    html_file.write(html_content)
