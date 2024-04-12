from textnode import (
    TextNode,
    text_type_text,
)


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

