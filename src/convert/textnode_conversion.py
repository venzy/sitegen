from node.textnode import TextNode, TextType
from node.leafnode import LeafNode

def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            if text_node.url is None:
                raise ValueError("Text node with TextType.LINK is expected to have a URL")
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            if text_node.url is None:
                raise ValueError("Text node with TextType.IMAGE is expected to have a URL")
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case TextType.CHECKBOX:
            props = {"type": "checkbox"}
            if text_node.text == "[x]":
                props["checked"] = "checked"
            return LeafNode("input", "", props)
        case _:
            raise ValueError(f'Unrecognised TextType: "{text_node.text_type}"')
