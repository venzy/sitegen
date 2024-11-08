from htmlnode import HTMLNode
from typing import Optional

class LeafNode(HTMLNode):
    def __init__(self, tag: Optional[str], value: str, props: Optional[dict[str, str]] = None):
        super().__init__(tag, value, None, props)
    
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'