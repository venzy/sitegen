import unittest

from convert.markdown_conversion import *
from node.leafnode import *

def debug_print(text):
    if False:
        print(text)

class TestMarkdownConversion(unittest.TestCase):
    def test_heading(self):
        for level in range(1, 7):
            markdown = f"{'#' * level} Heading {level}"
            converted = markdown_to_html_node(markdown)
            expected = ParentNode("div", [
                LeafNode(f"h{level}", f"Heading {level}")
            ])
            debug_print(converted.to_html())
            self.assertEqual(converted, expected)

    def test_code_block(self):
        markdown = "```This is a\nmulti-line\ncode block```"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("pre", [
                LeafNode("code", "This is a\nmulti-line\ncode block")
            ])
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)

    def test_quote_block(self):
        markdown = ">This is a\n>multi-line\n>quote block"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            LeafNode("blockquote", "This is a\nmulti-line\nquote block")
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)

    def test_unordered_list(self):
        markdown = "- First\n- Second\n- Third"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ul", [
                LeafNode("li", "First"),
                LeafNode("li", "Second"),
                LeafNode("li", "Third")
            ])
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)

        markdown = "* First\n* Second\n* Third"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ul", [
                LeafNode("li", "First"),
                LeafNode("li", "Second"),
                LeafNode("li", "Third")
            ])
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)

    def test_ordered_list(self):
        markdown = "1. First\n2. Second\n3. Third"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ol", [
                LeafNode("li", "First"),
                LeafNode("li", "Second"),
                LeafNode("li", "Third")
            ])
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)
    
    def test_paragraph(self):
        markdown = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("p", [
                LeafNode(None, "This is "),
                LeafNode("b", "text"),
                LeafNode(None, " with an "),
                LeafNode("i", "italic"),
                LeafNode(None, " word and a "),
                LeafNode("code", "code block"),
                LeafNode(None, " and an "),
                LeafNode("img", "" , {"src": "https://i.imgur.com/fJRm4Vk.jpeg", "alt": "obi wan image"}),
                LeafNode(None, " and a "),
                LeafNode("a", "link", {"href": "https://boot.dev"}),
            ])
        ])
        debug_print("")
        debug_print(expected.to_html())
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)
    
