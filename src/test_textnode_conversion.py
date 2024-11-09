import unittest

from textnode_conversion import *
from textnode import *
from leafnode import *


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        text_node = TextNode("some text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode(None, "some text")
        self.assertEqual(html_node, expected_html_node)

    def test_bold(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("b", "bold text")
        self.assertEqual(html_node, expected_html_node)

    def test_italic(self):
        text_node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("i", "italic text")
        self.assertEqual(html_node, expected_html_node)

    def test_code(self):
        text_node = TextNode("a == b", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("code", "a == b")
        self.assertEqual(html_node, expected_html_node)

    def test_link(self):
        text_node = TextNode("Click me!", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("a", "Click me!", {"href": "https://boot.dev"})
        self.assertEqual(html_node, expected_html_node)

    def test_image(self):
        text_node = TextNode("an image", TextType.IMAGE, "https://boot.dev/boots.png")
        html_node = text_node_to_html_node(text_node)
        expected_html_node = LeafNode("img", "", {"src": "https://boot.dev/boots.png", "alt": "an image"})
        self.assertEqual(html_node, expected_html_node)
