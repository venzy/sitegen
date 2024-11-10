import unittest

from parse.link_parse import *


class TestLinkParse(unittest.TestCase):
    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(extracted, expected)

    def test_image_no_alt_text(self):
        text = "Surprise... ![](https://i.imgur.com/aKaOqIh.gif)"
        extracted = extract_markdown_images(text)
        expected = [("", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extracted, expected)

    def test_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extracted, expected)

    def test_images_and_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"

        extracted = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(extracted, expected)

        extracted = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        self.assertEqual(extracted, expected)


if __name__ == "__main__":
    unittest.main()