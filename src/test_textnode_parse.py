import unittest

from textnode import TextNode, TextType
from textnode_parse import *

class TestTextNodeParse(unittest.TestCase):
    def test_text_only(self):
        old_nodes = [TextNode("some text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, old_nodes)

    def test_code_only(self):
        old_nodes = [TextNode("some code", TextType.CODE)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("some code", TextType.CODE)])

    def test_code_as_text(self):
        old_nodes = [TextNode("`some code`", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [TextNode("some code", TextType.CODE)])

    def test_compound_text_code(self):
        old_nodes = [TextNode("text a `some code` text b `more code`", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("text a ", TextType.TEXT),
            TextNode("some code", TextType.CODE),
            TextNode(" text b ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            ])

    def test_compound_text_code_bold(self):
        # You need to split once per TextType to extract
        # (note, nesting of delimiters / styles is ignored in this exercise)
        old_nodes = [TextNode("text a `some code` **text b** `more code`", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("text a ", TextType.TEXT),
            TextNode("some code", TextType.CODE),
            TextNode(" **text b** ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            ])
        with_bold_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(with_bold_nodes, [
            TextNode("text a ", TextType.TEXT),
            TextNode("some code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("text b", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            ])

    def test_imbalanced_raises(self):
        # Missing closing `
        old_nodes = [TextNode("`some code", TextType.TEXT)]
        self.assertRaises(Exception, split_nodes_delimiter, old_nodes, "`", TextType.CODE)

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_no_link(self):
        old_nodes = [
            TextNode(
                "This is text with no link",
                TextType.TEXT
            ),
            TextNode(
                " bold text ",
                TextType.BOLD
            )
        ]
        new_nodes = split_nodes_link(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_no_image(self):
        old_nodes = [
            TextNode(
                "This is text with no image",
                TextType.TEXT
            ),
            TextNode(
                " bold text ",
                TextType.BOLD
            )
        ]
        new_nodes = split_nodes_image(old_nodes)
        self.assertEqual(new_nodes, old_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)
 
if __name__ == "__main__":
    unittest.main()