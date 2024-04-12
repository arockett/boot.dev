import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)

from inline_markdown import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    def test_split_text_nodes(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ]
        )

    def test_split_multiple_blocks(self):
        node = TextNode("Text **with** multiple **blocks** to split", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "**", text_type_bold),
            [
                TextNode("Text ", text_type_text),
                TextNode("with", text_type_bold),
                TextNode(" multiple ", text_type_text),
                TextNode("blocks", text_type_bold),
                TextNode(" to split", text_type_text),
            ]
        )

    def test_split_with_block_at_end(self):
        node = TextNode("Text with a *block at the end*", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("Text with a ", text_type_text),
                TextNode("block at the end", text_type_italic),
            ]
        )

    def test_split_with_multiple_types(self):
        node = TextNode("`Text with multiple` types of *blocks*", text_type_text)
        self.assertEqual(
            split_nodes_delimiter([node], "`", text_type_code),
            [
                TextNode("Text with multiple", text_type_code),
                TextNode(" types of *blocks*", text_type_text),
            ]
        )
        self.assertEqual(
            split_nodes_delimiter([node], "*", text_type_italic),
            [
                TextNode("`Text with multiple` types of ", text_type_text),
                TextNode("blocks", text_type_italic),
            ]
        )


if __name__ == "__main__":
    unittest.main()

