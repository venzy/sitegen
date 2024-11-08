import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_leaf(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")
        print(node)

    def test_nested_parents(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode("ul", [
                    ParentNode("li", [
                        LeafNode(None, "Normal text")
                    ]),
                    ParentNode("li", [
                        LeafNode("i", "italic text")
                    ]),
                    ParentNode("li", [
                        LeafNode(None, "Normal text")
                    ])
                ])
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><ul><li>Normal text</li><li><i>italic text</i></li><li>Normal text</li></ul></p>")
        print(node)
    
    def test_no_tag_raises(self):
        node = ParentNode("", [LeafNode(None, "Normal text")])
        self.assertRaises(ValueError, node.to_html)

    def test_none_tag_raises(self):
        node = ParentNode(None, [LeafNode(None, "Normal text")])
        self.assertRaises(ValueError, node.to_html)

    def test_no_children_raises(self):
        node = ParentNode("p", [])
        self.assertRaises(ValueError, node.to_html)

    def test_none_children_raises(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)


if __name__ == "__main__":
    unittest.main()