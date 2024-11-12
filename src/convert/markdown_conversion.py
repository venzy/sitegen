import re
from convert.textnode_conversion import text_node_to_html_node
from node.htmlnode import HTMLNode
from node.leafnode import LeafNode
from node.parentnode import ParentNode
from parse.block_parse import markdown_to_blocks, block_to_block_type
from parse.textnode_parse import text_to_textnodes

def markdown_to_html_node(markdown: str) -> HTMLNode:
    result_node: HTMLNode = ParentNode("div", [])
    assert(result_node.children is not None)

    blocks: list[str] = markdown_to_blocks(markdown)

    for block in blocks:
        match block_to_block_type(block):
            case "heading":
                result_node.children.append(heading_to_html_node(block))
            case "code":
                # This is a ```code block``` as opposed to `inline code`
                result_node.children.append(code_to_html_node(block))
            case "quote":
                result_node.children.append(quote_to_html_node(block))
            case "unordered_list":
                result_node.children.append(unordered_list_to_html_node(block))
            case "ordered_list":
                result_node.children.append(ordered_list_to_html_node(block))
            case "paragraph":
                result_node.children.append(paragraph_to_html_node(block))

    return result_node

def heading_to_html_node(block: str) -> LeafNode:
    level = 0
    for c in block:
        if c == '#':
            level += 1
        else:
            break
    
    return LeafNode(f'h{level}', block[level + 1:])

def code_to_html_node(block: str) -> ParentNode:
    return ParentNode("pre", [LeafNode("code", block.lstrip("```").rstrip("```"))])

def quote_to_html_node(block: str) -> LeafNode:
    lines = [line.lstrip('>') for line in block.splitlines()]
    return LeafNode("blockquote", "\n".join(lines))

def unordered_list_to_html_node(block: str) -> ParentNode:
    items = [re.sub(r'^[-*] ', '', line) for line in block.splitlines()]
    return ParentNode("ul", [LeafNode("li", item) for item in items])

def ordered_list_to_html_node(block: str) -> ParentNode:
    items = [re.sub(r'^\d+\. ', '', line) for line in block.splitlines()]
    return ParentNode("ol", [LeafNode("li", item) for item in items])

def paragraph_to_html_node(block: str) -> ParentNode:
    textnodes = text_to_textnodes(block)
    return ParentNode("p", [text_node_to_html_node(node) for node in textnodes])