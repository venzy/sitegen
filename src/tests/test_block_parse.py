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

if __name__ == "__main__":
    unittest.main()