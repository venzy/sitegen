from textnode import *

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