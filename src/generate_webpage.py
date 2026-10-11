import os
import re

from markdown_convert import markdown_to_html_node


def extract_title(markdown: str) -> str:

    heading = re.search(r"^# .*", markdown, re.MULTILINE)
    if heading is None:
        raise ValueError("Markdown document has no valid H1 header")

    return heading.group()[1:].strip()


def generate_page(source: str, template: str, destination: str) -> None:

    print(f"Generating page from {source} to {destination} using {template}")

    with open(source) as f:
        md = f.read()
    with open(template) as f:
        html_template = f.read()

    content = markdown_to_html_node(md)
    title = extract_title(md)
    content_html = content.to_html()

    page = html_template.replace("{{ Title }}", title).replace("{{ Content }}", content_html)

    os.makedirs(os.path.dirname(destination), exist_ok=True)
    with open(destination, "w") as f:
        f.write(page)