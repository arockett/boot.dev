import unittest

from textnode import TextNode


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


if __name__ == "__main__":
    unittest.main()

