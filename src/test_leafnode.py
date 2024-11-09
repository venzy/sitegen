import unittest

from leafnode import LeafNode


def debug_print(node):
    if False:
        print(node)

class TestLeafNode(unittest.TestCase):
    def test_p_value(self):
        node = LeafNode("p", value="What a para")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "What a para")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node.to_html(), "<p>What a para</p>")
        debug_print(node)

    def test_a_href_value(self):
        node = LeafNode("a", "Click me!", props={"href": "https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "Click me!")
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click me!</a>')

    def test_no_value_raises(self):
        node = LeafNode("a", None, props={"href": "https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "https://boot.dev"})
        self.assertRaises(ValueError, node.to_html)

    def test_no_tag_gives_value(self):
        node = LeafNode(None, "Some raw text")
        self.assertIsNone(node.tag)
        self.assertEqual(node.value, "Some raw text")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        self.assertEqual(node.to_html(), "Some raw text")

if __name__ == "__main__":
    unittest.main()