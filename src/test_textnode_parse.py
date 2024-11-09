import unittest

from textnode import TextNode, TextType
from textnode_parse import split_nodes_delimiter

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


if __name__ == "__main__":
    unittest.main()