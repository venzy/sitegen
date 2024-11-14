import re

image_re = re.compile(r"\!\[(.*?)\]\((.*?)\)")
def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    images: list[tuple[str, str]] = image_re.findall(text)
    return images

link_re = re.compile(r"(?<!!)\[(.*?)\]\((.*?)\)")
def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = link_re.findall(text)
    return links