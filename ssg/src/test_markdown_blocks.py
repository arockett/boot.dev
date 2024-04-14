import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_ulist,
    block_type_olist,
)


class TestMarkdownBlocks(unittest.TestCase):
    def test_block_splitting1(self):
        markdown = '''
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
        '''
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is a list item\n* This is another list item"
            ]
        )

    def test_block_splitting2(self):
        markdown = '''
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        '''
        self.assertEqual(
            markdown_to_blocks(markdown),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )

    def test_detect_paragraph_block(self):
        self.assertEqual(
            block_to_block_type("Simple paragraph"),
            block_type_paragraph
        )
        self.assertEqual(
            block_to_block_type("A paragraph\nwith multiple\nlines"),
            block_type_paragraph
        )

    def test_detect_heading_block(self):
        self.assertEqual(
            block_to_block_type("# Header"),
            block_type_heading
        )
        self.assertEqual(
            block_to_block_type("## Header"),
            block_type_heading
        )

    def test_detect_code_block(self):
        self.assertEqual(
            block_to_block_type("```\nThis is some code\n```"),
            block_type_code
        )

    def test_detect_quote_block(self):
        self.assertEqual(
            block_to_block_type(">This is a\n>block quote"),
            block_type_quote
        )

    def test_detect_list_block(self):
        self.assertEqual(
            block_to_block_type("* item one\n* item two\n* item three"),
            block_type_ulist
        )
        self.assertEqual(
            block_to_block_type("- item one\n- item two\n- item three"),
            block_type_ulist
        )

    def test_detect_ordered_list_block(self):
        self.assertEqual(
            block_to_block_type("1. item one\n2. item two\n3. item three"),
            block_type_olist
        )


if __name__ == "__main__":
    unittest.main()

