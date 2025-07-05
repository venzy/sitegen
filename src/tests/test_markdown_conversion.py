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
    
    def test_heading_fancy(self):
        markdown = "### The *Struggle* of Good vs. Evil"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("h3", [
                LeafNode(None, "The "),
                LeafNode("i", "Struggle"),
                LeafNode(None, " of Good vs. Evil")
            ])
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

    def test_code_block_whitespace(self):
        markdown = "```\nThis is a\n  multi-line\n   code block\n```"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("pre", [
                LeafNode("code", "This is a\n  multi-line\n   code block")
            ])
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)

    def test_quote_block(self):
        markdown = "> This is a\n> multi-line\n> quote block"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            LeafNode("blockquote", "This is a<br/>multi-line<br/>quote block")
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)

    def test_quote_block_blank_in_middle(self):
        markdown = "> \"I am in fact a Hobbit in all but size.\"\n>\n> -- J.R.R. Tolkien"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            LeafNode("blockquote", "\"I am in fact a Hobbit in all but size.\"<br/><br/>-- J.R.R. Tolkien")
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

        markdown = "- First *italic text*\n- Second **bold text**\n- Third"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "First "),
                    LeafNode("i", "italic text")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Second "),
                    LeafNode("b", "bold text")
                ]),
                LeafNode("li", "Third")
            ])
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)

        markdown = "* First - *italic text*\n* Second - **bold text**\n* Third -"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode(None, "First - "),
                    LeafNode("i", "italic text")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Second - "),
                    LeafNode("b", "bold text")
                ]),
                LeafNode("li", "Third -")
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

        markdown = "1. First *italic text*\n2. Second **bold text**\n3. Third"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ol", [
                ParentNode("li", [
                    LeafNode(None, "First "),
                    LeafNode("i", "italic text")
                ]),
                ParentNode("li", [
                    LeafNode(None, "Second "),
                    LeafNode("b", "bold text")
                ]),
                LeafNode("li", "Third")
            ])
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)
    
    def test_paragraph(self):
        markdown = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
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
    
    def test_link_in_list(self):
        #markdown = "- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)\n- [Why Tom Bombadil Was a Mistake](/blog/tom)\n- [The Unparalleled Majesty of \"The Lord of the Rings\"](/blog/majesty)"
        markdown = "- [Why Glorfindel is More Impressive than Legolas](/blog/glorfindel)"
        converted = markdown_to_html_node(markdown)
        expected = ParentNode("div", [
            ParentNode("ul", [
                ParentNode("li", [
                    LeafNode("a", "Why Glorfindel is More Impressive than Legolas", {"href": "/blog/glorfindel"}),
                ]),
            ]),
        ])
        debug_print(converted.to_html())
        self.assertEqual(converted, expected)
