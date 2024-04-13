import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
)

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)


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

    def test_extract_image(self):
        text = "![alt text](./image-link)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "./image-link")]
        )

    def test_extract_multiple_images(self):
        text = "![alt text](./image-link) and ![another](./image)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("alt text", "./image-link"),
                ("another", "./image"),
            ]
        )

    def test_no_images(self):
        text = "This text has no images"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_images_skips_links(self):
        text = "![alt text](./image-link) and [link](./link)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "./image-link")]
        )

    def test_extract_link(self):
        text = "[link text](./link)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link text", "./link")]
        )

    def test_extract_multiple_links(self):
        text = "[link text](./link) and [another](http://)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("link text", "./link"),
                ("another", "http://"),
            ]
        )

    def test_no_links(self):
        text = "This text has no links"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_links_skips_images(self):
        text = "[link text](./link) and ![image](http://)"
        self.assertEqual(
            extract_markdown_links(text),
            [("link text", "./link")]
        )


if __name__ == "__main__":
    unittest.main()

