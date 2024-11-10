from node.htmlnode import HTMLNode
from typing import Optional

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list[HTMLNode], props: Optional[dict[str, str]] = None):
        super().__init__(tag, None, children, props)
    
    def to_html(self) -> str:
        if self.tag is None or len(self.tag) < 1:
            raise ValueError("ParentNode must have tag")
        if self.children is None or len(self.children) < 1:
            raise ValueError("ParentNode must have children")
        child_html = "".join(list(map(lambda child: child.to_html(), self.children)))
        return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'