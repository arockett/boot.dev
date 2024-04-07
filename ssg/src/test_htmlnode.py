import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()

