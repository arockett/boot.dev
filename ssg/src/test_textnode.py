import unittest

from textnode import TextNode, split_nodes_delimiter, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_link_eq(self):
        node = TextNode("This is a text node", "link", "https://example.com")
        node2 = TextNode("This is a text node", "link", "https://example.com")
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is another text node", "bold")
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_link_neq(self):
        node = TextNode("This is a text node", "link", "https://example.com")
        node2 = TextNode("This is a text node", "link")
        self.assertNotEqual(node, node2)
        
    def test_bad_eq(self):
        node = TextNode("This is a text node", "bold")
        self.assertEqual(node.__eq__("This is a text node"), NotImplemented)


class TestTextNodeConversion(unittest.TestCase):
    def test_text_node_to_html(self):
        text_node = TextNode("Normal text", "text")
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            "Normal text"
        )
        bold_node = TextNode("Bold text", "bold")
        self.assertEqual(
            text_node_to_html_node(bold_node).to_html(),
            "<b>Bold text</b>"
        )
        italic_node = TextNode("Italic text", "italic")
        self.assertEqual(
            text_node_to_html_node(italic_node).to_html(),
            "<i>Italic text</i>"
        )
        code_node = TextNode("Code text", "code")
        self.assertEqual(
            text_node_to_html_node(code_node).to_html(),
            "<code>Code text</code>"
        )
        link_node = TextNode("Link text", "link", "http://example.com")
        self.assertEqual(
            text_node_to_html_node(link_node).to_html(),
            "<a href=\"http://example.com\">Link text</a>"
        )
        img_node = TextNode("Image alt text", "image", "http://example.com")
        self.assertEqual(
            text_node_to_html_node(img_node).to_html(),
            "<img src=\"http://example.com\" alt=\"Image alt text\"></img>"
        )
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("Bad node", "invalid"))
        
    def test_split_text_nodes(self):
        node = TextNode("This is text with a `code block` word", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "`", "code"),
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ]
        )

    def test_split_multiple_blocks(self):
        node = TextNode("Text **with** multiple **blocks** to split", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "**", "bold"),
            [
                TextNode("Text ", "text"),
                TextNode("with", "bold"),
                TextNode(" multiple ", "text"),
                TextNode("blocks", "bold"),
                TextNode(" to split", "text"),
            ]
        )

    def test_split_with_block_at_end(self):
        node = TextNode("Text with a *block at the end*", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "*", "italic"),
            [
                TextNode("Text with a ", "text"),
                TextNode("block at the end", "italic"),
            ]
        )

    def test_split_with_multiple_types(self):
        node = TextNode("`Text with multiple` types of *blocks*", "text")
        self.assertEqual(
            split_nodes_delimiter([node], "`", "code"),
            [
                TextNode("Text with multiple", "code"),
                TextNode(" types of *blocks*", "text"),
            ]
        )
        self.assertEqual(
            split_nodes_delimiter([node], "*", "italic"),
            [
                TextNode("`Text with multiple` types of ", "text"),
                TextNode("blocks", "italic"),
            ]
        )


if __name__ == "__main__":
    unittest.main()

