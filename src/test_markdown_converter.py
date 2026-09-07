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

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_urls(self):
        node = TextNode(
            "This is text with a [link](example.com) and another [second link](example.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "example.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "example.com"),
            ],
            new_nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
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
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
        #TODO learn the dedent lib
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
                [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                ],
            )

    def test_block_to_blocktype_paragraph(self):
        cases = [
            ("", BlockType.PARAGRAPH), # empty string should be paragraph
            ("   ", BlockType.PARAGRAPH),
            ("just some text", BlockType.PARAGRAPH),
            ("line one\nline two", BlockType.PARAGRAPH),
            ("this - has a dash", BlockType.PARAGRAPH),
        ]

        for block, expected in cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_blocktype(block), expected)

    def test_block_to_blocktype_header(self):
        cases = [
            ("# Heading", BlockType.HEADING),
            ("###### Six hashes", BlockType.HEADING),
            ("# ", BlockType.HEADING),                    # trailing space, empty title still matches
            ("####### Seven hashes", BlockType.PARAGRAPH),
            ("#No space", BlockType.PARAGRAPH),
            (" # Leading space", BlockType.PARAGRAPH),
            ("# Heading\nwith a second line", BlockType.PARAGRAPH),
        ]

        for block, expected in cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_blocktype(block), expected)

    def test_block_to_blocktype_code(self):
        cases = [
            ("```\ncode here\n```", BlockType.CODE),
            ("```\n\n```", BlockType.CODE),
            ("```python\nprint()\n```", BlockType.PARAGRAPH),
            ("```code```", BlockType.PARAGRAPH),
            ("```\ncode\n```\ntrailing", BlockType.PARAGRAPH),
            ("```\nunclosed", BlockType.PARAGRAPH),
        ]
    
        for block, expected in cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_blocktype(block), expected)

    def test_block_to_blocktype_quote(self):
            cases = [
                ("> quote", BlockType.QUOTE),
                ("> line one\n> line two", BlockType.QUOTE),
                (">no space", BlockType.QUOTE), # space not required
                (">", BlockType.QUOTE),
                ("> line one\nline two", BlockType.PARAGRAPH),
                ("> line one\n\n> line two", BlockType.PARAGRAPH),
            ]
        
            for block, expected in cases:
                with self.subTest(block=block):
                    self.assertEqual(block_to_blocktype(block), expected)

    def test_block_to_blocktype_ul(self):
        cases = [
            ("- item", BlockType.UL),
            ("- one\n- two\n- three", BlockType.UL),
            ("-no space", BlockType.PARAGRAPH),
            ("* star bullet", BlockType.PARAGRAPH),
            ("- one\n- two\nthree", BlockType.PARAGRAPH),
            ("- one\n  - nested", BlockType.PARAGRAPH),
        ]
    
        for block, expected in cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_blocktype(block), expected)

    def test_block_to_blocktype_ol(self):
        cases = [
            ("1. item", BlockType.OL),
            ("1. one\n2. two\n3. three", BlockType.OL),
            ("1. one\n3. three", BlockType.PARAGRAPH),    # must increment by one
            ("2. two\n3. three", BlockType.PARAGRAPH),    # must start at 1
            ("0. zero\n1. one", BlockType.PARAGRAPH),
            ("1.no space", BlockType.PARAGRAPH),
            ("1) one\n2) two", BlockType.PARAGRAPH),
            ("1. one\n2. two\nthree", BlockType.PARAGRAPH),
        ]
    
        for block, expected in cases:
            with self.subTest(block=block):
                self.assertEqual(block_to_blocktype(block), expected)


        


if __name__ == "__main__":
    unittest.main()