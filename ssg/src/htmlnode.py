
class HTMLNode:

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplemented

    def props_to_html(self) -> str:
        if self.props is None:
            return ""
        prop_strings = [f" {k}=\"{v}\"" for k,v in self.props.items()]
        return "".join(prop_strings)

    def __repr__(self) -> str:
        parts = [
            f"HTMLNode({self.tag}",
            self.value,
            self.children,
            f"{self.props})",
        ]
        return ", ".join(parts)

class LeafNode(HTMLNode):

    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("All leaf nodes require a value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

