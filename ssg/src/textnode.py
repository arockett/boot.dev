
class TextNode:

    def __init__(self, text, text_type, url=None) -> None:
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

