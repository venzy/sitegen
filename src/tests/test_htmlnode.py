import unittest

from node.htmlnode import HTMLNode


def debug_print(node):
    if False:
        print(node)

class TestHTMLNode(unittest.TestCase):
    def test_init_a(self):
        node = HTMLNode("a")
        self.assertEqual(node.tag, "a")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        debug_print(node)

    def test_init_a_href(self):
        node = HTMLNode("a", props={"href": "https://boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertEqual(node.props, {"href": "https://boot.dev"})
        debug_print(node)

    def test_init_p_value(self):
        node = HTMLNode("p", value="What a para")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "What a para")
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)
        debug_print(node)

    def test_init_ul(self):
        children = [HTMLNode("li", "First"), HTMLNode("li", "Second")]
        node = HTMLNode("ul", children=children)
        self.assertEqual(node.tag, "ul")
        self.assertIsNone(node.value)
        self.assertEqual(node.children, children)
        self.assertIsNone(node.props)
        debug_print(node)
    
    def test_props_to_html_single(self):
        node = HTMLNode("a", props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')
        debug_print(node)

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="_blank"')
        debug_print(node)


if __name__ == "__main__":
    unittest.main()