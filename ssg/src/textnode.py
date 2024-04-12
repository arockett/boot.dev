from htmlnode import LeafNode


text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:

    def __init__(self, text: str, text_type: str, url:str|None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, __other: object) -> bool:
        if not isinstance(__other, TextNode):
            return NotImplemented
        return (
            self.text == __other.text and
            self.text_type == __other.text_type and
            self.url == __other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {
            "href": text_node.url
        })
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {
            "src": text_node.url,
            "alt": text_node.text
        })

    raise ValueError(f"Invalid text type: {text_node.text_type}")

def split_nodes_delimiter(
        old_nodes: list[TextNode],
        delimiter: str,
        text_type: str
    ) -> list[TextNode]:

    def split_next(node: TextNode) -> list[TextNode]:
        parts = node.text.split(delimiter, 2)
        if len(parts) == 1:
            return [node]
        if len(parts) != 3:
            raise Exception(f"Missing closing delimiter: {delimiter}")
        nodes = []
        if len(parts[0]) > 0:
            nodes.append(TextNode(parts[0], text_type_text))
        if len(parts[1]) > 0:
            nodes.append(TextNode(parts[1], text_type))
        if len(parts[2]) > 0:
            nodes.append(TextNode(parts[2], text_type_text))
        result = nodes[:-1]
        result.extend(split_next(nodes[-1]))
        return result

    split_nodes = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            split_nodes.extend(split_next(node))
        else:
            split_nodes.append(node)
    return split_nodes

