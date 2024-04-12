import unittest

from textnode import (
    TextNode,
    text_node_to_html_node,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node, node2)

    def test_link_eq(self):
        node = TextNode("This is a text node", text_type_link, "https://example.com")
        node2 = TextNode("This is a text node", text_type_link, "https://example.com")
        self.assertEqual(node, node2)

    def test_text_neq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is another text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_type_neq(self):
        node = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_italic)
        self.assertNotEqual(node, node2)

    def test_link_neq(self):
        node = TextNode("This is a text node", text_type_link, "https://example.com")
        node2 = TextNode("This is a text node", text_type_link)
        self.assertNotEqual(node, node2)
        
    def test_bad_eq(self):
        node = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node.__eq__("This is a text node"), NotImplemented)


class TestTextNodeConversion(unittest.TestCase):
    def test_text_node_to_html(self):
        text_node = TextNode("Normal text", text_type_text)
        self.assertEqual(
            text_node_to_html_node(text_node).to_html(),
            "Normal text"
        )
        bold_node = TextNode("Bold text", text_type_bold)
        self.assertEqual(
            text_node_to_html_node(bold_node).to_html(),
            "<b>Bold text</b>"
        )
        italic_node = TextNode("Italic text", text_type_italic)
        self.assertEqual(
            text_node_to_html_node(italic_node).to_html(),
            "<i>Italic text</i>"
        )
        code_node = TextNode("Code text", text_type_code)
        self.assertEqual(
            text_node_to_html_node(code_node).to_html(),
            "<code>Code text</code>"
        )
        link_node = TextNode("Link text", text_type_link, "http://example.com")
        self.assertEqual(
            text_node_to_html_node(link_node).to_html(),
            "<a href=\"http://example.com\">Link text</a>"
        )
        img_node = TextNode("Image alt text", text_type_image, "http://example.com")
        self.assertEqual(
            text_node_to_html_node(img_node).to_html(),
            "<img src=\"http://example.com\" alt=\"Image alt text\"></img>"
        )
        with self.assertRaises(ValueError):
            text_node_to_html_node(TextNode("Bad node", "invalid"))


if __name__ == "__main__":
    unittest.main()

