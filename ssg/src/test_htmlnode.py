import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_html(self):
        node = HTMLNode(props={"link": "http://example.com", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(),
            " link=\"http://example.com\" target=\"_blank\""
        )

    def test_empty_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_html(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph</p>"
        )

    def test_html_with_props(self):
        node = LeafNode("a", "Link", {"href": "http://example.com"})
        self.assertEqual(
            node.to_html(),
            "<a href=\"http://example.com\">Link</a>"
        )

    def test_no_tag(self):
        node = LeafNode(None, value="Just some text")
        self.assertEqual(
            node.to_html(),
            "Just some text"
        )

    def test_no_value(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None)
            node.to_html()


if __name__ == "__main__":
    unittest.main()

