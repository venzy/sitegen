from node.textnode import *
from parse.link_parse import *

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node is None:
            pass
        elif old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            token_count = 0
            for token in old_node.text.split(delimiter):
                if token != "":
                    if token_count % 2 == 1:
                        new_nodes.append(TextNode(token, text_type))
                    else:
                        new_nodes.append(TextNode(token, TextType.TEXT))
                token_count += 1

            if token_count != 1 and token_count % 2 == 0:
                raise Exception(f'No closing "{delimiter}" delimeter found')

    return new_nodes

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node is None:
            pass
        elif old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            images = extract_markdown_images(old_node.text)
            if len(images) == 0:
                new_nodes.append(old_node)
            else:
                remainder = old_node.text
                for (alt_text, url) in images:
                    (prefix, _, suffix) = remainder.partition(f'![{alt_text}]({url})')
                    if prefix == remainder:
                        raise Exception("We expect to find the image!")
                    if prefix != "":
                        new_nodes.append(TextNode(prefix, TextType.TEXT))
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                    remainder = suffix
                if remainder != "":
                    new_nodes.append(TextNode(remainder, TextType.TEXT))
    
    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node is None:
            pass
        elif old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            links = extract_markdown_links(old_node.text)
            if len(links) == 0:
                new_nodes.append(old_node)
            else:
                remainder = old_node.text
                for (title, url) in links:
                    (prefix, _, suffix) = remainder.partition(f'[{title}]({url})')
                    if prefix == remainder:
                        raise Exception("We expect to find the link!")
                    if prefix != "":
                        new_nodes.append(TextNode(prefix, TextType.TEXT))
                    new_nodes.append(TextNode(title, TextType.LINK, url))
                    remainder = suffix
                if remainder != "":
                    new_nodes.append(TextNode(remainder, TextType.TEXT))
    
    return new_nodes

def split_nodes_task(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node is None:
            pass
        elif old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            remainder = old_node.text
            while remainder != "":
                (prefix, value, suffix) = remainder.partition("[ ]")
                if prefix == remainder:
                    (prefix, value, suffix) = remainder.partition("[x]")
                if prefix == remainder:
                    break
                else:
                    if prefix != "":
                        new_nodes.append(TextNode(prefix, TextType.TEXT))
                    new_nodes.append(TextNode(value, TextType.CHECKBOX))
                    remainder = suffix
            if remainder != "":
                new_nodes.append(TextNode(remainder, TextType.TEXT))
    
    return new_nodes

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes: list[TextNode] = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_task(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes