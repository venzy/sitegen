from typing import Optional

class HTMLNode:
    def __init__(self, tag: Optional[str] = None, value: Optional[str] = None, children: Optional[list["HTMLNode"]] = None, props: Optional[dict[str, str]] = None):
        self.tag: Optional[str] = tag
        self.value: Optional[str] = value
        self.children: Optional[list[HTMLNode]] = children
        self.props: Optional[dict[str, str]] = props
    
    def to_html(self) -> str:
        raise NotImplementedError()
    
    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        return "".join(map(lambda item: f' {item[0]}="{item[1]}"', self.props.items()))
    
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(<{self.tag}>, {self.props_to_html()}, {self.value}, #children: {len(self.children) if self.children is not None else 0})'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return self.tag == other.tag and \
            self.value == other.value and \
            self.props == other.props and \
            self.children == other.children
