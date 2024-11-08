class HTMLNode:
    def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None):
        self.tag: str = tag
        self.value: str = value
        self.children: list[HTMLNode] = children
        self.props: dict[str, str] = props
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join(map(lambda item: f' {item[0]}="{item[1]}"', self.props.items()))
    
    def __repr__(self):
        return f'HTMLNode(<{self.tag}>, {self.props_to_html()}, {self.value}, #children: {len(self.children) if self.children is not None else 0})'