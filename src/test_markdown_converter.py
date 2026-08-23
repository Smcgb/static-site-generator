import unittest

from markdown_convert import *
from textnode import TextType


class TestMarkdownConverter(unittest.TestCase):

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("bold", TextType.BOLD),
                            TextNode(" word", TextType.TEXT),
                        ])

    def test_italic(self):
        node = TextNode("This is text with a *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("italic", TextType.ITALIC),
                            TextNode(" word", TextType.TEXT),
                        ])

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes,
                         [
                            TextNode("This is text with a ", TextType.TEXT),
                            TextNode("code block", TextType.CODE),
                            TextNode(" word", TextType.TEXT),
                        ])


    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_url(self):
            matches = extract_markdown_urls(
            "This is text with an [link](example.com)"
            )
            self.assertListEqual([("link", "example.com")], matches)   