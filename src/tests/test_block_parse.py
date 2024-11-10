import unittest

from parse.block_parse import *


class TestBlockParse(unittest.TestCase):
    def test_empty(self):
        text = ""
        extracted = markdown_to_blocks(text)
        expected = []
        self.assertEqual(extracted, expected)

    def test_empty_multiple_lines(self):
        text = "\n\n\n\n"
        extracted = markdown_to_blocks(text)
        expected = []
        self.assertEqual(extracted, expected)

    def test_one_line(self):
        text = "some text"
        extracted = markdown_to_blocks(text)
        expected = ["some text"]
        self.assertEqual(extracted, expected)

    def test_two_lines(self):
        text = "some text\nmore text"
        extracted = markdown_to_blocks(text)
        expected = ["some text\nmore text"]
        self.assertEqual(extracted, expected)

    def test_two_blocks(self):
        text = "some text\nmore text\n\nnew block"
        extracted = markdown_to_blocks(text)
        expected = ["some text\nmore text", "new block"]
        self.assertEqual(extracted, expected)

    def test_two_blocks_trailing_newline(self):
        text = "some text\nmore text\n\nnew block\n"
        extracted = markdown_to_blocks(text)
        expected = ["some text\nmore text", "new block"]
        self.assertEqual(extracted, expected)

    def test_two_blocks_extra_newlines(self):
        text = "some text\nmore text\n\n\n\n\nnew block\n"
        extracted = markdown_to_blocks(text)
        expected = ["some text\nmore text", "new block"]
        self.assertEqual(extracted, expected)

    def test_block_type_paragraph(self):
        text = "some text"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_block_type_heading(self):
        text = "# Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")
        text = "## Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")
        text = "### Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")
        text = "#### Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")
        text = "##### Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")
        text = "###### Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "heading")
        # More than 6 '#' - "paragraph"
        text = "####### Heading"
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_block_type_code(self):
        text = '```print("Hello, world!")```'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "code")

    def test_block_type_code_multiline(self):
        text = '```print("Hello, world!")\nsys.exit()```'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "code")

    def test_block_type_quote(self):
        text = '>The raven'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "quote")

    def test_block_type_quote_multiline(self):
        text = '>The raven\n>- Some guy'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "quote")

    def test_block_type_quote_multiline_fallback_to_paragraph(self):
        text = '>The raven\n>- Some guy\nNot a quote'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_block_type_unordered_dash(self):
        text = '- first'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered_list")

    def test_block_type_unordered_dash_multiline(self):
        text = '- first\n- second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered_list")

    def test_block_type_unordered_dash_multiline_typo(self):
        # no space after dash in second line
        text = '- first\n-second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_block_type_unordered_asterisk(self):
        text = '* first'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered_list")

    def test_block_type_unordered_asterisk_multiline(self):
        text = '* first\n* second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "unordered_list")

    def test_block_type_unordered_asterisk_multiline_typo(self):
        # no space after asterisk in first line
        text = '*first\n* second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_block_type_ordered(self):
        text = '1. first'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "ordered_list")

    def test_block_type_ordered_multiline(self):
        text = '1. first\n2. second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "ordered_list")

    def test_block_type_ordered_multiline_typo(self):
        # no space after period in first line
        text = '1.first\n2. second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_block_type_ordered_multiline_repeat(self):
        # repeated number (apparently valid in real markdown?)
        text = '1. first\n1. second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")

    def test_block_type_ordered_multiline_skip(self):
        # repeated number (apparently valid in real markdown?)
        text = '1. first\n3. second'
        block_type = block_to_block_type(text)
        self.assertEqual(block_type, "paragraph")


if __name__ == "__main__":
    unittest.main()