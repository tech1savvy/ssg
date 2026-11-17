import os

from ssg.markdown.blocks import extract_heading, split_blocks
from ssg.render import render_markdown


def extract_title(markdown) -> str:
    title_block = split_blocks(markdown)[0]
    level, heading = extract_heading(title_block)
    if level != 1:
        raise ValueError("Error: no h1 header")
    return heading


def genrate_page(from_path, template_path, dest_dir, base_path):
    dest_path = os.path.join(
        dest_dir, os.path.basename(from_path).split(".")[0] + ".html"
    )

    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    markdown_file = open(from_path)
    markdown_content = markdown_file.read()
    markdown_file.close()

    template_file = open(template_path)
    template_content = template_file.read()
    template_file.close()

    html_content = render_markdown(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace("{{ Title }}", title)
    template_content = template_content.replace("{{ Content }}", html_content)
    template_content = template_content.replace('href="/', f'href="{base_path}')
    template_content = template_content.replace('src="/', f'src="{base_path}')

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    html_file = open(dest_path, "w")
    html_file.write(template_content)


def genrate_pages_recursive(content_path, template_path, dest_path, base_path):
    dest_dir = os.path.dirname(dest_path)
    if os.path.isfile(content_path):
        genrate_page(content_path, template_path, dest_dir, base_path)
    else:
        for content in os.listdir(content_path):
            nested_content_path = os.path.join(content_path, content)
            nested_dest_path = os.path.join(dest_path, content)
            nested_dest_dir = os.path.dirname(nested_dest_path)

            if os.path.isfile(nested_content_path):
                genrate_page(
                    nested_content_path, template_path, nested_dest_dir, base_path
                )
            else:
                genrate_pages_recursive(
                    nested_content_path, template_path, nested_dest_path, base_path
                )
