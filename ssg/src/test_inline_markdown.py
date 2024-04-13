import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
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
        self.assertEqual(
            split_nodes_delimiter(
                split_nodes_delimiter([node], "*", text_type_italic),
                "`",
                text_type_code,
            ),
            [
                TextNode("Text with multiple", text_type_code),
                TextNode(" types of ", text_type_text),
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

    def test_split_image_node(self):
        node = TextNode(
            "This has one ![image](./image)",
            text_type_text
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("This has one ", text_type_text),
                TextNode("image", text_type_image, "./image")
            ]
        )

    def test_split_image_nodes(self):
        node = TextNode(
            "![image one](./image) and ![image two](./image2)?",
            text_type_text
        )
        self.assertEqual(
            split_nodes_image([node]),
            [
                TextNode("image one", text_type_image, "./image"),
                TextNode(" and ", text_type_text),
                TextNode("image two", text_type_image, "./image2"),
                TextNode("?", text_type_text)
            ]
        )

    def test_split_no_image_node(self):
        node = TextNode("no images here", text_type_text)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_split_link_node(self):
        node = TextNode(
            "This has one [link](./link)",
            text_type_text
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("This has one ", text_type_text),
                TextNode("link", text_type_link, "./link")
            ]
        )

    def test_split_link_nodes(self):
        node = TextNode(
            "[link one](./link) and [link two](./link2)?",
            text_type_text
        )
        self.assertEqual(
            split_nodes_link([node]),
            [
                TextNode("link one", text_type_link, "./link"),
                TextNode(" and ", text_type_text),
                TextNode("link two", text_type_link, "./link2"),
                TextNode("?", text_type_text)
            ]
        )

    def test_split_no_link_node(self):
        node = TextNode("no links here", text_type_text)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_text_to_textnodes(self):
        self.assertEqual(
            text_to_textnodes(
                "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
            ),
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ]
        )


if __name__ == "__main__":
    unittest.main()

